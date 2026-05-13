// logic.rs -- Spatial logic gates on the pixel grid
//
// A logic gate pixel performs a bitwise operation on its neighbors.
// For example: pixel[x,y].LSB = pixel[x-1,y].LSB AND pixel[x+1,y].LSB

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GateType {
    And = 0,
    Or = 1,
    Xor = 2,
    Not = 3,
    Nand = 4,
    Nor = 5,
}

pub struct LogicGate {
    pub gate_type: GateType,
    pub input_a_offset: (i8, i8),
    pub input_b_offset: (i8, i8),
    pub output_bit: u8, // which bit to read the result to
}

impl LogicGate {
    /// Decode a logic gate from a 32-bit pixel.
    /// Layout: [24:31] Tag | [21:23] GateType | [17:20] A_dx | [13:16] A_dy | [9:12] B_dx | [5:8] B_dy | [0:4] Bit
    pub fn decode(pixel: u32) -> Self {
        let gt = ((pixel >> 21) & 0x7) as u8;
        let gate_type = match gt {
            0 => GateType::And,
            1 => GateType::Or,
            2 => GateType::Xor,
            3 => GateType::Not,
            4 => GateType::Nand,
            5 => GateType::Nor,
            _ => GateType::And,
        };

        // Offsets are 4-bit signed: -8 to 7
        let a_dx = (((pixel >> 17) & 0xF) as i8) - 8;
        let a_dy = (((pixel >> 13) & 0xF) as i8) - 8;
        let b_dx = (((pixel >> 9) & 0xF) as i8) - 8;
        let b_dy = (((pixel >> 5) & 0xF) as i8) - 8;
        let bit = (pixel & 0x1F) as u8;

        LogicGate {
            gate_type,
            input_a_offset: (a_dx, a_dy),
            input_b_offset: (b_dx, b_dy),
            output_bit: bit,
        }
    }

    /// Encode a logic gate into a 32-bit pixel.
    pub fn encode(tag: u8, gt: GateType, a: (i8, i8), b: (i8, i8), bit: u8) -> u32 {
        let mut p = (tag as u32) << 24;
        p |= (gt as u32 & 0x7) << 21;
        p |= (((a.0 + 8) as u32) & 0xF) << 17;
        p |= (((a.1 + 8) as u32) & 0xF) << 13;
        p |= (((b.0 + 8) as u32) & 0xF) << 9;
        p |= (((b.1 + 8) as u32) & 0xF) << 5;
        p |= bit as u32 & 0x1F;
        p
    }

    /// Execute the gate logic.
    pub fn execute(&self, a_val: u32, b_val: u32) -> bool {
        let a = (a_val >> self.output_bit) & 1 == 1;
        let b = (b_val >> self.output_bit) & 1 == 1;
        
        match self.gate_type {
            GateType::And => a && b,
            GateType::Or => a || b,
            GateType::Xor => a ^ b,
            GateType::Not => !a,
            GateType::Nand => !(a && b),
            GateType::Nor => !(a || b),
        }
    }
}
