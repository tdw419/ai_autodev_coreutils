#!/usr/bin/env python3
"""
Health check: Is the Geometry OS desktop binary running and responsive?
Outputs structured key=value for Oracle preflight to consume.

Exit 0 = desktop alive and responsive
Exit 1 = desktop not running or unresponsive
"""
import socket, sys, os, subprocess, time

SOCKET_PATH = "/tmp/geo_cmd.sock"
GEO_BIN = os.path.expanduser("~/zion/projects/geometry_os/geometry_os/target/release/geometry_os")
RESTART_COOLDOWN = 60  # seconds between restart attempts
RESTART_MARKER = "/tmp/geo_last_restart"


def geo_cmd(cmd, timeout=3):
    """Send a command to the Geometry OS socket. Returns response string or None."""
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(SOCKET_PATH)
        s.sendall((cmd + "\n").encode())
        s.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            try:
                chunk = s.recv(65536)
                if not chunk:
                    break
                data += chunk
            except socket.timeout:
                break
        s.close()
        return data.decode().strip()
    except (ConnectionRefusedError, FileNotFoundError, socket.timeout, OSError):
        return None


def try_restart():
    """Try to restart the Geometry OS binary if it's not running."""
    # Check cooldown
    if os.path.exists(RESTART_MARKER):
        try:
            with open(RESTART_MARKER) as f:
                last = float(f.read().strip())
            if time.time() - last < RESTART_COOLDOWN:
                print("DESKTOP_RESTART: cooldown (skipping)")
                return False
        except:
            pass

    if not os.path.exists(GEO_BIN):
        print("DESKTOP_RESTART: binary not found")
        return False

    # Kill any existing process
    subprocess.run(["pkill", "-f", "target/release/geometry_os"],
                   capture_output=True, timeout=5)
    time.sleep(0.5)

    # Start fresh
    log_file = open("/tmp/geo_os_restart.log", "a")
    proc = subprocess.Popen(
        [GEO_BIN],
        cwd=os.path.expanduser("~/zion/projects/geometry_os/geometry_os"),
        stdout=log_file, stderr=log_file,
        stdin=subprocess.DEVNULL,
    )

    # Record restart time
    with open(RESTART_MARKER, "w") as f:
        f.write(str(time.time()))

    print(f"DESKTOP_RESTART: started pid={proc.pid}")

    # Wait for socket to become available
    for _ in range(30):
        time.sleep(0.5)
        if os.path.exists(SOCKET_PATH):
            result = geo_cmd("status")
            if result:
                print("DESKTOP_RESTART: socket responsive")
                return True

    print("DESKTOP_RESTART: failed (socket not responsive after 15s)")
    return False


def main():
    # First check: is the socket there?
    if not os.path.exists(SOCKET_PATH):
        print("DESKTOP_ALIVE: false")
        print("DESKTOP_REASON: socket not found")
        try_restart()
        return

    # Second check: is it responsive?
    result = geo_cmd("status")
    if not result:
        print("DESKTOP_ALIVE: false")
        print("DESKTOP_REASON: socket exists but not responsive")
        try_restart()
        return

    # Parse status output
    print("DESKTOP_ALIVE: true")
    for line in result.split("\n"):
        line = line.strip()
        if line:
            print(f"DESKTOP_{line}")


if __name__ == "__main__":
    main()
