#!/usr/bin/env python3
"""
A from-scratch DNS resolver.
Constructs raw UDP packets, queries nameservers, parses binary responses.
No DNS libraries -- just struct, socket, and the RFC 1035 wire format.

Usage:
    python dns_resolver.py example.com
    python dns_resolver.py example.com MX
    python dns_resolver.py example.com AAAA 1.1.1.1
"""

import socket
import struct
import sys
import random
import time

# DNS record type constants
QTYPE_A     = 1
QTYPE_NS    = 2
QTYPE_CNAME = 5
QTYPE_MX    = 15
QTYPE_TXT   = 16
QTYPE_AAAA  = 28

TYPE_NAMES = {
    1: "A", 2: "NS", 5: "CNAME", 15: "MX", 16: "TXT", 28: "AAAA",
}
TYPE_LOOKUP = {v: k for k, v in TYPE_NAMES.items()}

RCODE_NAMES = {
    0: "NOERROR", 1: "FORMERR", 2: "SERVFAIL", 3: "NXDOMAIN",
    4: "NOTIMP", 5: "REFUSED",
}


def encode_name(name):
    """Encode a domain name into DNS wire format: len-prefixed labels."""
    parts = []
    for label in name.rstrip(".").split("."):
        raw = label.encode("ascii")
        parts.append(struct.pack("B", len(raw)) + raw)
    parts.append(b"\x00")  # root label
    return b"".join(parts)


def build_query(domain, qtype=QTYPE_A):
    """Build a complete DNS query packet from scratch."""
    # Header: ID (2) + Flags (2) + QDCOUNT (2) + ANCOUNT (2) + NSCOUNT (2) + ARCOUNT (2)
    txn_id = random.randint(0, 65535)
    # Flags: recursion desired, standard query
    flags = 0x0100  # RD=1
    header = struct.pack("!HHHHHH", txn_id, flags, 1, 0, 0, 0)
    # Question section
    question = encode_name(domain) + struct.pack("!HH", qtype, 1)  # QCLASS=IN
    return txn_id, header + question


def decode_name(data, offset):
    """
    Decode a DNS name from the response, handling pointer compression.
    Pointers are 2 bytes starting with 0xC0, pointing to an earlier offset.
    Returns (name_string, new_offset).
    """
    labels = []
    jumped = False
    original_offset = offset
    max_jumps = 20  # prevent infinite loops

    jumps = 0
    while True:
        if offset >= len(data):
            break
        length = data[offset]

        # Pointer: top 2 bits are 11
        if (length & 0xC0) == 0xC0:
            if not jumped:
                original_offset = offset + 2
            pointer = struct.unpack("!H", data[offset:offset + 2])[0] & 0x3FFF
            offset = pointer
            jumped = True
            jumps += 1
            if jumps > max_jumps:
                break
            continue

        # Zero-length label = end of name
        if length == 0:
            offset += 1
            break

        offset += 1
        labels.append(data[offset:offset + length].decode("ascii", errors="replace"))
        offset += length

    return ".".join(labels), (original_offset if jumped else offset)


def parse_rdata(qtype, data, offset, rdlength):
    """Parse the RDATA field based on record type."""
    raw = data[offset:offset + rdlength]
    end = offset + rdlength

    if qtype == QTYPE_A and rdlength == 4:
        return ".".join(str(b) for b in raw)
    elif qtype == QTYPE_AAAA and rdlength == 16:
        groups = []
        for i in range(0, 16, 2):
            groups.append(format(struct.unpack("!H", raw[i:i+2])[0], "x"))
        # Compress runs of zeros
        return ":".join(groups)
    elif qtype == QTYPE_CNAME or qtype == QTYPE_NS:
        name, _ = decode_name(data, offset)
        return name
    elif qtype == QTYPE_MX:
        preference = struct.unpack("!H", data[offset:offset + 2])[0]
        exchange, _ = decode_name(data, offset + 2)
        return f"{preference} {exchange}"
    elif qtype == QTYPE_TXT:
        texts = []
        pos = offset
        while pos < end:
            tlen = data[pos]
            pos += 1
            texts.append(data[pos:pos + tlen].decode("utf-8", errors="replace"))
            pos += tlen
        return " ".join(texts)
    else:
        return raw.hex()


def parse_response(data):
    """Parse a complete DNS response packet."""
    # Header
    txn_id, flags, qdcount, ancount, nscount, arcount = struct.unpack(
        "!HHHHHH", data[:12]
    )
    rcode = flags & 0x000F
    authoritative = bool(flags & 0x0400)
    truncated = bool(flags & 0x0200)
    recursion_available = bool(flags & 0x0080)

    result = {
        "id": txn_id,
        "rcode": RCODE_NAMES.get(rcode, f"UNKNOWN({rcode})"),
        "authoritative": authoritative,
        "truncated": truncated,
        "recursion_available": recursion_available,
        "questions": [],
        "answers": [],
        "authorities": [],
        "additional": [],
    }

    offset = 12

    # Parse questions
    for _ in range(qdcount):
        name, offset = decode_name(data, offset)
        qtype, qclass = struct.unpack("!HH", data[offset:offset + 4])
        offset += 4
        result["questions"].append({
            "name": name, "type": TYPE_NAMES.get(qtype, str(qtype))
        })

    # Parse resource records (answers, authorities, additional)
    for section_name, count in [
        ("answers", ancount), ("authorities", nscount), ("additional", arcount)
    ]:
        for _ in range(count):
            name, offset = decode_name(data, offset)
            rtype, rclass, ttl, rdlength = struct.unpack(
                "!HHIH", data[offset:offset + 10]
            )
            offset += 10
            rdata = parse_rdata(rtype, data, offset, rdlength)
            offset += rdlength
            result[section_name].append({
                "name": name,
                "type": TYPE_NAMES.get(rtype, str(rtype)),
                "ttl": ttl,
                "data": rdata,
            })

    return result


def resolve(domain, qtype=QTYPE_A, server="8.8.8.8", port=53, timeout=5):
    """Resolve a DNS query from scratch."""
    txn_id, packet = build_query(domain, qtype)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    start = time.time()

    try:
        sock.sendto(packet, (server, port))
        response, _ = sock.recvfrom(4096)
    finally:
        sock.close()

    elapsed = (time.time() - start) * 1000

    # Verify transaction ID matches
    resp_id = struct.unpack("!H", response[:2])[0]
    if resp_id != txn_id:
        raise ValueError(f"Transaction ID mismatch: sent {txn_id}, got {resp_id}")

    parsed = parse_response(response)
    parsed["elapsed_ms"] = elapsed
    parsed["server"] = server
    return parsed


def print_result(result):
    """Pretty-print a DNS response."""
    print(f";; ->>HEADER<<- opcode: QUERY, status: {result['rcode']}, id: {result['id']}")
    flags = []
    if result["authoritative"]:
        flags.append("aa")
    if result["truncated"]:
        flags.append("tc")
    if result["recursion_available"]:
        flags.append("ra")
    print(f";; flags: {' '.join(flags)}; QUERY: {len(result['questions'])}, "
          f"ANSWER: {len(result['answers'])}, "
          f"AUTHORITY: {len(result['authorities'])}, "
          f"ADDITIONAL: {len(result['additional'])}")
    print()

    if result["questions"]:
        print(";; QUESTION SECTION:")
        for q in result["questions"]:
            print(f";; {q['name']:30s} IN  {q['type']}")
        print()

    for section_name in ["answers", "authorities", "additional"]:
        records = result[section_name]
        if records:
            label = section_name.upper().rstrip("S") + " SECTION"
            print(f";; {label}:")
            for r in records:
                print(f"{r['name']:30s} {r['ttl']:>7d}  IN  {r['type']:>6s}  {r['data']}")
            print()

    print(f";; Query time: {result['elapsed_ms']:.1f} ms")
    print(f";; Server: {result['server']}#53")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <domain> [A|AAAA|MX|NS|TXT|CNAME] [server]")
        print(f"Examples:")
        print(f"  {sys.argv[0]} example.com")
        print(f"  {sys.argv[0]} example.com MX")
        print(f"  {sys.argv[0]} example.com AAAA 1.1.1.1")
        sys.exit(1)

    domain = sys.argv[1]
    qtype_str = sys.argv[2].upper() if len(sys.argv) > 2 else "A"
    server = sys.argv[3] if len(sys.argv) > 3 else "8.8.8.8"

    qtype = TYPE_LOOKUP.get(qtype_str)
    if qtype is None:
        print(f"Unknown record type: {qtype_str}")
        print(f"Supported: {', '.join(TYPE_LOOKUP.keys())}")
        sys.exit(1)

    print(f";; Resolving {domain} {qtype_str} via {server}\n")
    result = resolve(domain, qtype, server)
    print_result(result)


if __name__ == "__main__":
    main()
