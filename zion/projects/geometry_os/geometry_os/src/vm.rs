// vm.rs -- The Substrate VM
//
// A minimal bytecode VM that executes pixels. The framebuffer IS memory.
// Opcodes are 1 byte, followed by operand bytes. Programs start at address 0x1000.
//
// Memory layout:
//   0x0000 - 0x0FFF: Zero page (BIOS, stack, system)
//   0x1000 - 0xFFFF: Program space
//   0x10000+:         Framebuffer (256x256 = 65536 pixels)

use crate::render::Framebuffer;

/// VM register file. 32 general-purpose 32-bit registers.
pub const NUM_REGS: usize = 32;

/// Program counter start address.
pub const PROGRAM_START: u32 = 0x1000;

/// Stack pointer initial value (grows down from 0x0F00).
pub const STACK_START: u32 = 0x0F00;

/// Opcodes for the Substrate VM.
/// Keeping it minimal -- expand as needed.
#[repr(u8)]
pub enum Op {
    Nop   = 0x00,
    Halt  = 0x01,
    Ldi   = 0x02, // LDI Rd, imm16
    Ldr   = 0x03, // LDR Rd, [Rs]
    Str   = 0x04, // STR Rd, [Rs]
    Add   = 0x05, // ADD Rd, Rs
    Sub   = 0x06, // SUB Rd, Rs
    Mul   = 0x07, // MUL Rd, Rs
    And   = 0x08, // AND Rd, Rs
    Or    = 0x09, // OR  Rd, Rs
    Xor   = 0x0A, // XOR Rd, Rs
    Shr   = 0x0B, // SHR Rd, Rs
    Shl   = 0x0C, // SHL Rd, Rs
    Jmp   = 0x0D, // JMP addr16
    Jeq   = 0x0E, // JEQ addr16 (jump if Rd == Rs)
    Jne   = 0x0F, // JNE addr16
    Push  = 0x10, // PUSH Rd
    Pop   = 0x11, // POP  Rd
    Peek  = 0x12, // PEEK Rd, Rs (read pixel at framebuffer[Rs])
    Poke  = 0x13, // POKE Rd, Rs (write Rd to framebuffer at Rs)
    Call  = 0x14, // CALL addr16
    Ret   = 0x15, // RET
    Cmp   = 0x16, // CMP Rd, Rs (sets flags, doesn't store)
    Fill  = 0x17, // FILL x, y, w, h, color (draw rect)
    Rect  = 0x18, // RECT outline
    Yield = 0x19, // YIELD (end of frame, advance framebuffer tick)
    Seed  = 0x1A, // SEED Rd (load entropy into Rd)
    Cppm  = 0x1B, // CPPM Rd (query current pressure)
    Dna   = 0x1C, // DNA Rd (query BIOS DNA pixel)
    Layer = 0x1D, // LAYER Rs (switch active memory layer 0-3)
    Expand = 0x1E, // EXPAND -- collapse/expand: reset PC and SP, restart execution
}

pub struct Vm {
    pub ram: Vec<u8>,
    pub regs: [u32; NUM_REGS],
    pub pc: u32,
    pub sp: u32,
    pub fb: Framebuffer,
    pub running: bool,
    pub flag_zero: bool,
    pub flag_carry: bool,
    pub cycles: u64,
    pub max_cycles: u64,
    
    // CPM (Cycles Per Minute) tracking
    pub cpm_limit: u64,
    pub current_cpm: f64,
    pub last_frame_cycles: u64,
    pub pressure_decay: f64,
    pub dna: u32,
}

impl Vm {
    pub fn new(fb_width: usize, fb_height: usize) -> Self {
        let mut vm = Vm {
            ram: vec![0u8; 0x20000], // 128KB address space
            regs: [0u32; NUM_REGS],
            pc: PROGRAM_START,
            sp: STACK_START,
            fb: Framebuffer::new(fb_width, fb_height),
            running: false,
            flag_zero: false,
            flag_carry: false,
            cycles: 0,
            max_cycles: 100_000,
            cpm_limit: 1_000_000_000, // 1 Billion CPM default
            current_cpm: 0.0,
            last_frame_cycles: 0,
            pressure_decay: 0.9, // 10% decay per frame
            dna: 0,
        };
        // r0 is always zero
        vm.regs[0] = 0;
        vm
    }

    /// Load a bytecode program into RAM at PROGRAM_START.
    pub fn load(&mut self, bytecode: &[u8]) {
        let start = PROGRAM_START as usize;
        let end = start + bytecode.len();
        if end <= self.ram.len() {
            self.ram[start..end].copy_from_slice(bytecode);
        }
        self.pc = PROGRAM_START;
    }

    /// Set the BIOS DNA pixel.
    pub fn set_dna(&mut self, pixel: u32) {
        self.dna = pixel;
    }

    /// Read a byte from RAM.
    fn read8(&self, addr: u32) -> u8 {
        self.ram.get(addr as usize).copied().unwrap_or(0)
    }

    /// Write a byte to RAM.
    fn write8(&mut self, addr: u32, val: u8) {
        if (addr as usize) < self.ram.len() {
            self.ram[addr as usize] = val;
        }
    }

    /// Read 16-bit big-endian from RAM.
    fn read16(&self, addr: u32) -> u16 {
        let hi = self.read8(addr) as u16;
        let lo = self.read8(addr + 1) as u16;
        (hi << 8) | lo
    }

    /// Read 32-bit from RAM (4 bytes, little-endian for register values).
    fn read32(&self, addr: u32) -> u32 {
        let b0 = self.read8(addr) as u32;
        let b1 = self.read8(addr + 1) as u32;
        let b2 = self.read8(addr + 2) as u32;
        let b3 = self.read8(addr + 3) as u32;
        b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)
    }

    /// Write 32-bit to RAM.
    fn write32(&mut self, addr: u32, val: u32) {
        self.write8(addr, (val & 0xFF) as u8);
        self.write8(addr + 1, ((val >> 8) & 0xFF) as u8);
        self.write8(addr + 2, ((val >> 16) & 0xFF) as u8);
        self.write8(addr + 3, ((val >> 24) & 0xFF) as u8);
    }

    /// Parse register index from next byte (1-31, clamped).
    fn read_reg(&mut self) -> usize {
        let r = (self.read8(self.pc) as usize).min(31).max(0);
        self.pc += 1;
        if r == 0 { return 0; } // r0 hardwired to 0
        r
    }

    /// Execute one instruction. Returns false if halted.
    pub fn step(&mut self) -> bool {
        if !self.running || self.cycles >= self.max_cycles {
            self.running = false;
            return false;
        }

        let op = self.read8(self.pc);
        self.pc += 1;
        self.cycles += 1;

        match op {
            0x00 => { /* NOP */ }
            0x01 => { /* HALT */
                self.running = false;
                return false;
            }
            0x02 => { /* LDI Rd, imm16 */
                let rd = self.read_reg();
                let imm = self.read16(self.pc) as u32;
                self.pc += 2;
                self.regs[rd] = imm;
            }
            0x03 => { /* LDR Rd, [Rs] */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let addr = self.regs[rs];
                self.regs[rd] = self.read32(addr);
            }
            0x04 => { /* STR Rd, [Rs] */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let addr = self.regs[rs];
                self.write32(addr, self.regs[rd]);
            }
            0x05 => { /* ADD Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let (result, carry) = self.regs[rd].overflowing_add(self.regs[rs]);
                self.regs[rd] = result;
                self.flag_zero = result == 0;
                self.flag_carry = carry;
            }
            0x06 => { /* SUB Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let (result, carry) = self.regs[rd].overflowing_sub(self.regs[rs]);
                self.regs[rd] = result;
                self.flag_zero = result == 0;
                self.flag_carry = carry;
            }
            0x07 => { /* MUL Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                self.regs[rd] = self.regs[rd].wrapping_mul(self.regs[rs]);
                self.flag_zero = self.regs[rd] == 0;
            }
            0x08 => { /* AND Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                self.regs[rd] &= self.regs[rs];
                self.flag_zero = self.regs[rd] == 0;
            }
            0x09 => { /* OR Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                self.regs[rd] |= self.regs[rs];
                self.flag_zero = self.regs[rd] == 0;
            }
            0x0A => { /* XOR Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                self.regs[rd] ^= self.regs[rs];
                self.flag_zero = self.regs[rd] == 0;
            }
            0x0B => { /* SHR Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let shift = self.regs[rs] & 31;
                self.regs[rd] >>= shift;
                self.flag_zero = self.regs[rd] == 0;
            }
            0x0C => { /* SHL Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let shift = self.regs[rs] & 31;
                self.regs[rd] <<= shift;
                self.flag_zero = self.regs[rd] == 0;
            }
            0x0D => { /* JMP addr16 */
                let addr = self.read16(self.pc) as u32;
                self.pc = addr;
            }
            0x0E => { /* JEQ addr16 */
                let addr = self.read16(self.pc) as u32;
                self.pc += 2;
                if self.flag_zero {
                    self.pc = addr;
                }
            }
            0x0F => { /* JNE addr16 */
                let addr = self.read16(self.pc) as u32;
                self.pc += 2;
                if !self.flag_zero {
                    self.pc = addr;
                }
            }
            0x10 => { /* PUSH Rd */
                let rd = self.read_reg();
                self.sp -= 4;
                self.write32(self.sp, self.regs[rd]);
            }
            0x11 => { /* POP Rd */
                let rd = self.read_reg();
                self.regs[rd] = self.read32(self.sp);
                self.sp += 4;
            }
            0x12 => { /* PEEK Rd, Rs -- read pixel from framebuffer */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let offset = self.regs[rs] as usize;
                self.regs[rd] = self.fb.get_linear(offset);
            }
            0x13 => { /* POKE Rd, Rs -- write pixel to framebuffer */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let offset = self.regs[rs] as usize;
                self.fb.set_linear(offset, self.regs[rd]);
            }
            0x14 => { /* CALL addr16 */
                let addr = self.read16(self.pc) as u32;
                self.pc += 2;
                self.sp -= 4;
                self.write32(self.sp, self.pc);
                self.pc = addr;
            }
            0x15 => { /* RET */
                self.pc = self.read32(self.sp);
                self.sp += 4;
            }
            0x16 => { /* CMP Rd, Rs */
                let rd = self.read_reg();
                let rs = self.read_reg();
                let (result, carry) = self.regs[rd].overflowing_sub(self.regs[rs]);
                self.flag_zero = result == 0;
                self.flag_carry = carry;
            }
            0x17 => { /* FILL x, y, w, h, color -- solid rectangle */
                let x = self.read_reg();
                let y = self.read_reg();
                let w = self.read_reg();
                let h = self.read_reg();
                let color = self.read_reg();
                let color_val = self.regs[color];
                for dy in 0..self.regs[h] as usize {
                    for dx in 0..self.regs[w] as usize {
                        let px = self.regs[x] as usize + dx;
                        let py = self.regs[y] as usize + dy;
                        self.fb.set(px, py, color_val);
                    }
                }
            }
            0x18 => { /* RECT x, y, w, h, color -- outline rectangle */
                let x = self.read_reg();
                let y = self.read_reg();
                let w = self.read_reg();
                let h = self.read_reg();
                let color = self.read_reg();
                let color_val = self.regs[color];
                let xv = self.regs[x] as usize;
                let yv = self.regs[y] as usize;
                let wv = self.regs[w] as usize;
                let hv = self.regs[h] as usize;
                // Top and bottom
                for dx in 0..wv {
                    self.fb.set(xv + dx, yv, color_val);
                    self.fb.set(xv + dx, yv + hv - 1, color_val);
                }
                // Left and right
                for dy in 0..hv {
                    self.fb.set(xv, yv + dy, color_val);
                    self.fb.set(xv + wv - 1, yv + dy, color_val);
                }
            }
            0x19 => { /* YIELD -- end of frame */
                // Calculate CPM (Cycles Per Minute)
                // Composite metric: (Cycles + Register Pressure bonus) * Frames Per Minute
                let frame_cycles = self.cycles - self.last_frame_cycles;
                self.last_frame_cycles = self.cycles;

                // Estimate register pressure: non-zero registers / total registers
                let active_regs = self.regs.iter().filter(|&&r| r != 0).count() as f64;
                let reg_pressure = active_regs / NUM_REGS as f64;

                // CPM formula: (Cycles + Weighted Register Pressure) * 3600
                // This reflects both instruction throughput and state density.
                let instantaneous_cpm = (frame_cycles as f64 + (reg_pressure * 100.0)) * 3600.0;

                // Exponential moving average for smoothing (0.9 decay)
                self.current_cpm = (self.current_cpm * self.pressure_decay)
                    + (instantaneous_cpm * (1.0 - self.pressure_decay));
                                    
                self.fb.tick();
            }
            0x1A => { /* SEED Rd -- load entropy from TRNG substrate */
                let rd = self.read_reg();
                // Harvest entropy from the currently active layer
                let layer_idx = self.fb.active_layer;
                let pixels = &self.fb.layers[layer_idx];
                self.regs[rd] = crate::entropy::seed_from_framebuffer(pixels);
            }
            0x1B => { /* CPPM Rd -- query current pressure */
                let rd = self.read_reg();
                self.regs[rd] = self.current_cpm as u32;
            }
            0x1C => {
                /* DNA Rd -- query BIOS DNA pixel */
                let rd = self.read_reg();
                self.regs[rd] = self.dna;
            }
            0x1D => {
                /* LAYER Rs -- switch active layer */
                let rs = self.read_reg();
                self.fb.active_layer = (self.regs[rs] as usize).min(3);
            }
            0x1E => {
                /* EXPAND -- collapse/expand cycle:
                   Reset PC and SP, keep registers and DNA intact.
                   If CPM is within budget, the program re-executes from 0x1000.
                   If CPM exceeds the limit, halt to prevent runaway expands. */
                if (self.current_cpm as u64) >= self.cpm_limit {
                    self.running = false;
                } else {
                    self.pc = PROGRAM_START;
                    self.sp = STACK_START;
                }
            }
            _ => { /* Unknown opcode = NOP */ }
        }

        // r0 is always zero
        self.regs[0] = 0;
        true
    }

    /// Run until halt or max cycles.
    pub fn run(&mut self) -> u64 {
        self.running = true;
        while self.step() {}
        self.cycles
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_vm() -> Vm {
        Vm::new(256, 256)
    }

    #[test]
    fn test_nop_halt() {
        let mut vm = make_vm();
        vm.load(&[0x00, 0x00, 0x01]); // NOP, NOP, HALT
        vm.run();
        assert_eq!(vm.cycles, 3);
    }

    #[test]
    fn test_ldi() {
        let mut vm = make_vm();
        vm.load(&[0x02, 1, 0x00, 0x2A, 0x01]); // LDI r1, 42; HALT
        vm.run();
        assert_eq!(vm.regs[1], 42);
    }

    #[test]
    fn test_add() {
        let mut vm = make_vm();
        // LDI r1, 10; LDI r2, 20; ADD r1, r2; HALT
        vm.load(&[
            0x02, 1, 0x00, 0x0A, // LDI r1, 10
            0x02, 2, 0x00, 0x14, // LDI r2, 20
            0x05, 1, 2,          // ADD r1, r2
            0x01,                // HALT
        ]);
        vm.run();
        assert_eq!(vm.regs[1], 30);
    }

    #[test]
    fn test_sub_flags() {
        let mut vm = make_vm();
        // LDI r1, 10; LDI r2, 10; SUB r1, r2; HALT
        vm.load(&[
            0x02, 1, 0x00, 0x0A,
            0x02, 2, 0x00, 0x0A,
            0x06, 1, 2,
            0x01,
        ]);
        vm.run();
        assert_eq!(vm.regs[1], 0);
        assert!(vm.flag_zero);
    }

    #[test]
    fn test_peek_poke() {
        let mut vm = make_vm();
        // LDI r1, 0x00123456; LDI r2, 0; POKE r1, r2; PEEK r3, r2; HALT
        vm.load(&[
            0x02, 1, 0x56, 0x34, // LDI r1, 0x5634 (imm16 only)
            0x02, 2, 0x00, 0x00, // LDI r2, 0
            0x13, 1, 2,          // POKE r1, r2
            0x12, 3, 2,          // PEEK r3, r2
            0x01,
        ]);
        vm.run();
        assert_eq!(vm.regs[3], 0x5634);
    }

    #[test]
    fn test_push_pop() {
        let mut vm = make_vm();
        // LDI r1, 99; PUSH r1; LDI r1, 0; POP r2; HALT
        vm.load(&[
            0x02, 1, 0x00, 0x63, // LDI r1, 99
            0x10, 1,              // PUSH r1
            0x02, 1, 0x00, 0x00, // LDI r1, 0
            0x11, 2,              // POP r2
            0x01,
        ]);
        vm.run();
        assert_eq!(vm.regs[1], 0);
        assert_eq!(vm.regs[2], 99);
    }

    #[test]
    fn test_jump() {
        let mut vm = make_vm();
        // JMP 0x1004; HALT at 0x1004
        vm.load(&[
            0x0D, 0x10, 0x04, // JMP to 0x1004
            0x01,             // HALT at offset 3 -> addr 0x1003... wait
        ]);
        // offset 0 = 0x1000 (JMP), 0x1001, 0x1002 (addr bytes), 0x1003 (HALT)
        // JMP wants to skip to HALT. But HALT is at 0x1003 right after the JMP bytes.
        // Let's just JMP forward past a NOP.
        vm.load(&[
            0x0D, 0x10, 0x05, // JMP to 0x1005
            0xFF,             // garbage at 0x1003
            0x01,             // HALT at 0x1004... nope
        ]);
        // Actually: offset 0->0x1000(JMP), 1->0x1001(hi), 2->0x1002(lo)
        //           offset 3->0x1003(FF), offset 4->0x1004(01=HALT)
        // So JMP 0x1004 should land on HALT
        vm.load(&[
            0x0D, 0x10, 0x04, // JMP to 0x1004
            0xFF,             // garbage at 0x1003
            0x01,             // HALT at 0x1004
        ]);
        vm.run();
        assert!(vm.cycles < 5);
    }

    #[test]
    fn test_fill() {
        let mut vm = make_vm();
        // LDI r1, 10; LDI r2, 10; LDI r3, 5; LDI r4, 5; LDI r5, 0xFF; FILL r1-r5; HALT
        vm.load(&[
            0x02, 1, 0x00, 0x0A, // r1 = 10 (x)
            0x02, 2, 0x00, 0x0A, // r2 = 10 (y)
            0x02, 3, 0x00, 0x05, // r3 = 5 (w)
            0x02, 4, 0x00, 0x05, // r4 = 5 (h)
            0x02, 5, 0x00, 0xFF, // r5 = 0xFF (color)
            0x17, 1, 2, 3, 4, 5, // FILL
            0x01,                // HALT
        ]);
        vm.run();
        // Check center pixel
        assert_eq!(vm.fb.get(12, 12), 0xFF);
        // Check outside
        assert_eq!(vm.fb.get(8, 8), 0);
    }

    #[test]
    fn test_expand_under_budget() {
        // EXPAND with low CPM should reset PC and continue execution.
        // Program: LDI r1, 42; EXPAND; LDI r2, 7; HALT
        // After EXPAND, PC resets to 0x1000, re-executes LDI r1,42 and EXPAND again.
        // But max_cycles prevents infinite loop.
        let mut vm = make_vm();
        vm.max_cycles = 100;
        vm.load(&[
            0x02, 1, 0x00, 0x2A, // LDI r1, 42
            0x1E,                // EXPAND
            0x02, 2, 0x00, 0x07, // LDI r2, 7
            0x01,                // HALT
        ]);
        vm.run();
        // Should have looped (EXPAND resets PC) and hit max_cycles.
        // r1 = 42 still, r2 may or may not be set depending on when max_cycles hit.
        assert_eq!(vm.regs[1], 42);
        assert!(!vm.running);
    }

    #[test]
    fn test_expand_over_budget_halts() {
        // EXPAND with CPM over limit should halt immediately.
        let mut vm = make_vm();
        vm.current_cpm = 2_000_000_000.0; // way over default 1B limit
        vm.load(&[
            0x02, 1, 0x00, 0x2A, // LDI r1, 42
            0x1E,                // EXPAND -- should halt here
            0x02, 2, 0x00, 0x07, // LDI r2, 7 (should not execute)
            0x01,                // HALT
        ]);
        vm.run();
        assert!(!vm.running);
        assert_eq!(vm.regs[2], 0); // r2 never set
    }
}
