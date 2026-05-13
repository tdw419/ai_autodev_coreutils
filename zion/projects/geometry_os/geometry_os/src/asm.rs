// asm.rs -- The Substrate Assembler
//
// Translates human-readable mnemonics into VM bytecode.
// Two-pass: first pass collects labels, second pass emits bytes.
//
// Syntax:
//   LDI R0, 42         -- load immediate 16-bit into register
//   ADD R0, R1         -- R0 = R0 + R1
//   JMP label          -- jump to label address
//   FILL 10, 20, 50, 50, 0xFF0000  -- draw filled rectangle
//   label:             -- define a label at this address
//   ; comment          -- ignored

/// Assembler error.
#[derive(Debug)]
pub enum AsmError {
    UnknownOpcode(String),
    UnknownRegister(String),
    BadOperand { line: usize, msg: String },
    UndefinedLabel(String),
    DuplicateLabel(String),
    TruncatedLine(usize),
}

impl std::fmt::Display for AsmError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AsmError::UnknownOpcode(op) => write!(f, "Unknown opcode: {}", op),
            AsmError::UnknownRegister(r) => write!(f, "Unknown register: {}", r),
            AsmError::BadOperand { line, msg } => write!(f, "Line {}: {}", line, msg),
            AsmError::UndefinedLabel(l) => write!(f, "Undefined label: {}", l),
            AsmError::DuplicateLabel(l) => write!(f, "Duplicate label: {}", l),
            AsmError::TruncatedLine(n) => write!(f, "Truncated line {}", n),
        }
    }
}

/// Register name -> index.
fn parse_reg(s: &str) -> Result<u8, AsmError> {
    let cleaned = s.trim().trim_end_matches(',').to_uppercase();
    if cleaned.starts_with('R') {
        let num: u8 = cleaned[1..]
            .parse()
            .map_err(|_| AsmError::UnknownRegister(cleaned.clone()))?;
        if num < 32 {
            return Ok(num);
        }
    }
    Err(AsmError::UnknownRegister(cleaned))
}

/// Parse a numeric literal (decimal or 0x hex).
fn parse_num(s: &str) -> Result<u32, AsmError> {
    let s = s.trim().trim_end_matches(',');
    if s.starts_with("0x") || s.starts_with("0X") {
        u32::from_str_radix(&s[2..], 16).map_err(|_| AsmError::BadOperand {
            line: 0,
            msg: format!("Bad hex literal: {}", s),
        })
    } else {
        s.parse().map_err(|_| AsmError::BadOperand {
            line: 0,
            msg: format!("Bad number: {}", s),
        })
    }
}

/// Instruction info: opcode byte + operand format.
struct InstInfo {
    opcode: u8,
    // Format: "rr" = two registers, "ri" = reg + imm16, "i" = imm16, "n" = none, "raw" = variable
    fmt: &'static str,
}

fn lookup_opcode(mnemonic: &str) -> Option<InstInfo> {
    let m = mnemonic.to_uppercase();
    Some(match m.as_str() {
        "NOP" => InstInfo { opcode: 0x00, fmt: "n" },
        "HALT" => InstInfo { opcode: 0x01, fmt: "n" },
        "LDI" => InstInfo { opcode: 0x02, fmt: "ri" },
        "LDR" => InstInfo { opcode: 0x03, fmt: "rr" },
        "STR" => InstInfo { opcode: 0x04, fmt: "rr" },
        "ADD" => InstInfo { opcode: 0x05, fmt: "rr" },
        "SUB" => InstInfo { opcode: 0x06, fmt: "rr" },
        "MUL" => InstInfo { opcode: 0x07, fmt: "rr" },
        "AND" => InstInfo { opcode: 0x08, fmt: "rr" },
        "OR" => InstInfo { opcode: 0x09, fmt: "rr" },
        "XOR" => InstInfo { opcode: 0x0A, fmt: "rr" },
        "SHR" => InstInfo { opcode: 0x0B, fmt: "rr" },
        "SHL" => InstInfo { opcode: 0x0C, fmt: "rr" },
        "JMP" => InstInfo { opcode: 0x0D, fmt: "i" },
        "JEQ" => InstInfo { opcode: 0x0E, fmt: "i" },
        "JNE" => InstInfo { opcode: 0x0F, fmt: "i" },
        "PUSH" => InstInfo { opcode: 0x10, fmt: "r" },
        "POP" => InstInfo { opcode: 0x11, fmt: "r" },
        "PEEK" => InstInfo { opcode: 0x12, fmt: "rr" },
        "POKE" => InstInfo { opcode: 0x13, fmt: "rr" },
        "CALL" => InstInfo { opcode: 0x14, fmt: "i" },
        "RET" => InstInfo { opcode: 0x15, fmt: "n" },
        "CMP" => InstInfo { opcode: 0x16, fmt: "rr" },
        "FILL" => InstInfo { opcode: 0x17, fmt: "raw" }, // x,y,w,h,color (5 bytes)
        "RECT" => InstInfo { opcode: 0x18, fmt: "rrrrr" },
        "YIELD" => InstInfo { opcode: 0x19, fmt: "n" },
        "SEED" => InstInfo { opcode: 0x1A, fmt: "r" },
        "CPPM" => InstInfo { opcode: 0x1B, fmt: "r" },
        "DNA" => InstInfo { opcode: 0x1C, fmt: "r" },
        "LAYER" => InstInfo { opcode: 0x1D, fmt: "r" },
        "EXPAND" => InstInfo { opcode: 0x1E, fmt: "n" },
        _ => return None,
        })
        }
/// Calculate the byte size of an instruction line (for pass 1).
fn inst_size(parts: &[&str]) -> usize {
    if parts.is_empty() {
        return 0;
    }
    let mnemonic = parts[0];
    let info = match lookup_opcode(mnemonic) {
        Some(i) => i,
        None => return 0, // label or directive
    };
    match info.fmt {
        "n" => 1,
        "r" => 2,
        "rr" => 3,
        "ri" => 4,     // opcode + reg + imm16
        "i" => 3,      // opcode + imm16
        "rri" => 5,    // opcode + reg + reg + imm16
        "raw" => {
            // FILL/RECT: opcode + x + y + w + h + color(3 bytes) = 8 bytes
            8
        }
        _ => 1,
    }
}

/// Assemble source code into bytecode.
/// Returns a vector of bytes ready to load at 0x1000.
pub fn assemble(source: &str) -> Result<Vec<u8>, AsmError> {
    let lines: Vec<&str> = source.lines().collect();

    // Pass 1: collect labels and calculate addresses.
    let mut labels = std::collections::HashMap::new();
    let mut addr: usize = 0;

    // Strip comments and whitespace, collect cleaned lines.
    let cleaned: Vec<(usize, String)> = lines
        .iter()
        .enumerate()
        .map(|(i, line)| {
            let no_comment = line.split(';').next().unwrap_or("").trim();
            (i + 1, no_comment.to_string())
        })
        .filter(|(_, line)| !line.is_empty())
        .collect();

    for (_line_num, line) in &cleaned {
        if line.ends_with(':') {
            // Label definition
            let name = line.trim_end_matches(':').trim().to_string();
            if labels.contains_key(&name) {
                return Err(AsmError::DuplicateLabel(name));
            }
            labels.insert(name, addr);
        } else {
            let parts: Vec<&str> = line.split_whitespace().collect();
            if !parts.is_empty() {
                addr += inst_size(&parts);
            }
        }
    }

    // Pass 2: emit bytes.
    let mut bytecode = Vec::new();

    for (line_num, line) in &cleaned {
        if line.ends_with(':') {
            continue; // labels already processed
        }

        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.is_empty() {
            continue;
        }

        let mnemonic = parts[0].to_uppercase();
        let info = lookup_opcode(&mnemonic)
            .ok_or_else(|| AsmError::UnknownOpcode(mnemonic.clone()))?;

        bytecode.push(info.opcode);

        match info.fmt {
            "n" => {} // no operands
            "r" => {
                // single register
                let reg = parse_reg(parts.get(1).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                bytecode.push(reg);
            }
            "rr" => {
                let rd = parse_reg(parts.get(1).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                let rs = parse_reg(parts.get(2).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                bytecode.push(rd);
                bytecode.push(rs);
            }
            "ri" => {
                // register + immediate/label
                let rd = parse_reg(parts.get(1).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                let imm_str = parts.get(2).ok_or(AsmError::TruncatedLine(*line_num))?;
                let imm = resolve_imm(imm_str, &labels)?;
                bytecode.push(rd);
                bytecode.push((imm >> 8) as u8);
                bytecode.push((imm & 0xFF) as u8);
            }
            "i" => {
                // immediate/label only
                let imm_str = parts.get(1).ok_or(AsmError::TruncatedLine(*line_num))?;
                let imm = resolve_imm(imm_str, &labels)?;
                // For JMP/CALL, add 0x1000 base
                let target = if imm < 0x1000 { imm + 0x1000 } else { imm };
                bytecode.push((target >> 8) as u8);
                bytecode.push((target & 0xFF) as u8);
            }
            "rri" => {
                // two registers + immediate/label
                let rd = parse_reg(parts.get(1).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                let rs = parse_reg(parts.get(2).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                let imm_str = parts.get(3).ok_or(AsmError::TruncatedLine(*line_num))?;
                let imm = resolve_imm(imm_str, &labels)?;
                let target = if imm < 0x1000 { imm + 0x1000 } else { imm };
                bytecode.push(rd);
                bytecode.push(rs);
                bytecode.push((target >> 8) as u8);
                bytecode.push((target & 0xFF) as u8);
            }
            "raw" => {
                // FILL x,y,w,h,color or RECT x,y,w,h,color
                // Expect 5 operands: x y w h color
                for i in 1..=4 {
                    let v = parse_num(parts.get(i).ok_or(AsmError::TruncatedLine(*line_num))?)?;
                    bytecode.push(v as u8);
                }
                // Color: 3 bytes (R, G, B)
                let color_str = parts.get(5).ok_or(AsmError::TruncatedLine(*line_num))?;
                let color = parse_num(color_str)?;
                bytecode.push(((color >> 16) & 0xFF) as u8);
                bytecode.push(((color >> 8) & 0xFF) as u8);
                bytecode.push((color & 0xFF) as u8);
            }
            _ => {}
        }
    }

    Ok(bytecode)
}

/// Resolve an immediate value -- could be a number or a label.
fn resolve_imm(s: &str, labels: &std::collections::HashMap<String, usize>) -> Result<u32, AsmError> {
    let s = s.trim().trim_end_matches(',');
    if s.starts_with("0x") || s.starts_with("0X") || s.chars().all(|c| c.is_ascii_digit()) {
        parse_num(s)
    } else {
        // Try as a label
        labels
            .get(s)
            .map(|&addr| addr as u32)
            .ok_or_else(|| AsmError::UndefinedLabel(s.to_string()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_halt() {
        let code = "HALT";
        let bytes = assemble(code).unwrap();
        assert_eq!(bytes, vec![0x01]);
    }

    #[test]
    fn test_ldi() {
        let code = "LDI R0, 42";
        let bytes = assemble(code).unwrap();
        assert_eq!(bytes, vec![0x02, 0x00, 0x00, 0x2A]);
    }

    #[test]
    fn test_add() {
        let code = "LDI R0, 10\nLDI R1, 20\nADD R0, R1\nHALT";
        let bytes = assemble(code).unwrap();
        assert_eq!(bytes[0], 0x02); // LDI
        assert_eq!(bytes[4], 0x02); // LDI
        assert_eq!(bytes[8], 0x05); // ADD
        assert_eq!(bytes[9], 0x00); // R0
        assert_eq!(bytes[10], 0x01); // R1
        assert_eq!(bytes[11], 0x01); // HALT
    }

    #[test]
    fn test_label_jump() {
        let code = "  JMP skip\n  NOP\nskip:\n  HALT";
        let bytes = assemble(code).unwrap();
        // JMP = 3 bytes, NOP = 1 byte, HALT at offset 4
        // "skip" resolves to address 4 (offset from start of bytecode)
        // JMP adds 0x1000 base, so target = 0x1004
        assert_eq!(bytes[0], 0x0D); // JMP
        assert_eq!(bytes[1], 0x10); // hi byte of 0x1004
        assert_eq!(bytes[2], 0x04); // lo byte of 0x1004
        assert_eq!(bytes[3], 0x00); // NOP
        assert_eq!(bytes[4], 0x01); // HALT
    }

    #[test]
    fn test_fill() {
        let code = "FILL 10, 20, 50, 50, 0xFF0000";
        let bytes = assemble(code).unwrap();
        assert_eq!(bytes[0], 0x17); // FILL opcode
        assert_eq!(bytes[1], 10);   // x
        assert_eq!(bytes[2], 20);   // y
        assert_eq!(bytes[3], 50);   // w
        assert_eq!(bytes[4], 50);   // h
        assert_eq!(bytes[5], 0xFF); // R
        assert_eq!(bytes[6], 0x00); // G
        assert_eq!(bytes[7], 0x00); // B
    }

    #[test]
    fn test_comments() {
        let code = "; This is a comment\nLDI R0, 100 ; load 100\nHALT";
        let bytes = assemble(code).unwrap();
        assert_eq!(bytes[0], 0x02); // LDI
        assert_eq!(bytes[3], 100);  // imm
        assert_eq!(bytes[4], 0x01); // HALT
    }

    #[test]
    fn test_duplicate_label() {
        let code = "start:\nNOP\nstart:\nHALT";
        assert!(assemble(code).is_err());
    }

    #[test]
    fn test_undefined_label() {
        let code = "JMP nowhere";
        assert!(assemble(code).is_err());
    }

    #[test]
    fn test_push_pop() {
        let code = "LDI R5, 42\nPUSH R5\nPOP R6\nHALT";
        let bytes = assemble(code).unwrap();
        assert_eq!(bytes[4], 0x10); // PUSH
        assert_eq!(bytes[5], 0x05); // R5
        assert_eq!(bytes[6], 0x11); // POP
        assert_eq!(bytes[7], 0x06); // R6
    }

    #[test]
    fn test_comparison() {
        // JEQ now takes only a label (no registers, uses flag from CMP)
        let code =
            "LDI R0, 5\nLDI R1, 5\nCMP R0, R1\nJEQ match\nHALT\nmatch:\nLDI R2, 1\nHALT";
        let bytes = assemble(code).unwrap();
        // Layout:
        //   LDI R0,5  = 4 bytes (0-3)
        //   LDI R1,5  = 4 bytes (4-7)
        //   CMP R0,R1 = 3 bytes (8-10)
        //   JEQ match = 3 bytes (11-13): opcode + addr16
        //   HALT      = 1 byte  (14)
        //   match: LDI R2,1 = 4 bytes (15-18)
        //   HALT = 1 byte (19)
        // match label = offset 15, + 0x1000 = 0x100F
        assert_eq!(bytes[8], 0x16); // CMP
        assert_eq!(bytes[11], 0x0E); // JEQ
        assert_eq!(bytes[12], 0x10); // hi byte of 0x100F
        assert_eq!(bytes[13], 0x0F); // lo byte
    }
}
