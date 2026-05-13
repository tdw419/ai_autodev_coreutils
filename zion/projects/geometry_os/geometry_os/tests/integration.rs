
use geometry_os::asm;
use geometry_os::vm::Vm;
use geometry_os::render::Framebuffer;

#[test]
fn test_counter_program() {
    // Count 0-9 into framebuffer. R0 is hardwired to 0, so use R1+.
    let source = r#"
        LDI R1, 0       ; counter (R0 is always 0)
        LDI R2, 10      ; limit
        LDI R4, 0       ; framebuffer offset

    loop:
        CMP R1, R2
        JEQ done
        POKE R1, R4     ; write counter to framebuffer[offset]
        LDI R3, 1
        ADD R1, R3      ; counter++
        ADD R4, R3      ; offset++
        JMP loop

    done:
        HALT
    "#;

    let bytecode = asm::assemble(source).expect("Assembly failed");
    let mut vm = Vm::new(32, 32);
    vm.load(&bytecode);
    vm.run();

    for i in 0..10 {
        assert_eq!(vm.fb.get_linear(i), i as u32, "Pixel {} should be {}", i, i);
    }
    assert!(!vm.running);
}

#[test]
fn test_fibonacci() {
    // Fibonacci: store first 12 numbers in framebuffer. R0=0 always.
    let source = r#"
        ; R1 = fib(n-2), R2 = fib(n-1)
        LDI R1, 0
        LDI R2, 1
        LDI R4, 0       ; fb offset
        LDI R5, 12      ; count limit

        ; Store fib(0) and fib(1)
        POKE R1, R4
        LDI R6, 1
        ADD R4, R6
        POKE R2, R4
        ADD R4, R6

    loop:
        CMP R4, R5
        JEQ done

        ; R3 = R1 + R2 (next fib)
        LDI R3, 0
        ADD R3, R1
        ADD R3, R2

        ; Store R3
        POKE R3, R4

        ; Shift: R1 = R2, R2 = R3
        LDI R7, 0
        ADD R7, R2      ; R7 = R2 (save)
        LDI R1, 0
        ADD R1, R7      ; R1 = old R2
        LDI R2, 0
        ADD R2, R3      ; R2 = R3 (new value)

        LDI R6, 1
        ADD R4, R6
        JMP loop

    done:
        HALT
    "#;

    let bytecode = asm::assemble(source).expect("Assembly failed");
    let mut vm = Vm::new(32, 32);
    vm.load(&bytecode);
    vm.run();

    let expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89];
    for (i, &exp) in expected.iter().enumerate() {
        assert_eq!(vm.fb.get_linear(i), exp, "fib({}) should be {}", i, exp);
    }
}

#[test]
fn test_mirror_pixel() {
    use geometry_os::pixel;

    let mut fb = Framebuffer::new(32, 32);
    fb.set(5, 5, pixel::rgb(0xFF, 0, 0));
    fb.set(10, 10, pixel::mirror(5, 5));

    let resolved = fb.resolve(10, 10);
    assert_eq!(resolved, pixel::rgb(0xFF, 0, 0));
}

#[test]
fn test_temporal_pixel() {
    use geometry_os::pixel;

    let mut fb = Framebuffer::new(32, 32);
    fb.set(5, 5, pixel::temporal(200, 50));

    assert_eq!(fb.resolve(5, 5), pixel::rgb(200, 200, 200));
    fb.tick();
    assert_eq!(fb.resolve(5, 5), pixel::rgb(50, 50, 50));
    fb.tick();
    assert_eq!(fb.resolve(5, 5), pixel::rgb(200, 200, 200));
}

#[test]
fn test_portal_pixel() {
    use geometry_os::pixel;

    let mut fb = Framebuffer::new(256, 256);
    fb.set_linear(100, pixel::rgb(0xAA, 0xBB, 0xCC));
    fb.set(5, 5, pixel::portal(100));

    assert_eq!(fb.resolve(5, 5), pixel::rgb(0xAA, 0xBB, 0xCC));
}

#[test]
fn test_r0_is_zero() {
    // Verify R0 is always zero (hardwired)
    let mut vm = Vm::new(16, 16);
    // LDI R0, 42; HALT
    vm.load(&[0x02, 0x00, 0x00, 0x2A, 0x01]);
    vm.run();
    assert_eq!(vm.regs[0], 0, "R0 should always be 0");
}

#[test]
fn test_hamming_pixel() {
    use geometry_os::pixel;
    let mut fb = Framebuffer::new(32, 32);
    
    let original_data = 0x7ABCD; // 19 bits
    let hamming_px = pixel::hamming(original_data);
    
    // Corrupt one bit (bit 10) in the encoded 24-bit RGB area
    let corrupted = hamming_px ^ (1 << 10);
    fb.set(0, 0, corrupted);
    
    // Resolve should repair it back to original 19-bit data
    let resolved = fb.resolve(0, 0);
    assert_eq!(resolved, original_data);
}

#[test]
fn test_memory_layers() {
    let mut vm = Vm::new(32, 32);

    let source = r#"
        LDI R1, 0       ; Layer 0
        LDI R2, 1       ; Layer 1
        LDI R3, 10      ; Offset
        LDI R4, 0xAAAA  ; Value for Layer 0
        LDI R5, 0xBBBB  ; Value for Layer 1

        LAYER R1        ; Select Layer 0
        POKE R4, R3     ; fb[10] = 0xAAAA in Layer 0

        LAYER R2        ; Select Layer 1
        POKE R5, R3     ; fb[10] = 0xBBBB in Layer 1

        LAYER R1        ; Select Layer 0
        PEEK R6, R3     ; R6 = fb[10] from Layer 0

        LAYER R2        ; Select Layer 1
        PEEK R7, R3     ; R7 = fb[10] from Layer 1

        HALT
    "#;

    let bytes = asm::assemble(source).unwrap();
    vm.load(&bytes);
    vm.run();

    assert_eq!(vm.regs[6], 0xAAAA);
    assert_eq!(vm.regs[7], 0xBBBB);
}

#[test]
fn test_cppm_and_dna() {
    let mut vm = Vm::new(32, 32);
    vm.set_dna(0x9105003C);

    // Loop a few times to build up CPPM, then query it and DNA
    let source = r#"
        LDI R1, 0
        LDI R2, 5
    loop:
        LDI R3, 1
        ADD R1, R3
        CMP R1, R2
        JNE loop

        YIELD       ; Recalculate CPPM
        CPPM R4     ; Store CPPM in R4
        DNA R5      ; Store DNA in R5
        HALT
    "#;

    let bytes = asm::assemble(source).unwrap();
    vm.load(&bytes);
    vm.run();

    assert!(vm.regs[4] > 0, "CPPM should be > 0");
    assert_eq!(vm.regs[5], 0x9105003C, "DNA should match BIOS pixel");
}

#[test]
fn test_logic_gate_and() {
    use geometry_os::pixel;
    use geometry_os::logic::{LogicGate, GateType};

    let mut fb = Framebuffer::new(32, 32);

    // Place two data pixels: pixel at (5,5) with bit 3 set, pixel at (7,5) with bit 3 set
    let data_a = pixel::rgb(0xFF, 0, 0); // bit 3 = 1 (bit 3 of R channel)
    let data_b = pixel::rgb(0xFF, 0, 0); // bit 3 = 1
    fb.set(5, 5, data_a);
    fb.set(7, 5, data_b);

    // Place an AND gate at (6,5) that reads from (-1,0) and (+1,0), checks bit 19
    // (bit 3 of R channel, which is at bits 16-23 of the pixel word)
    // Tag for LogicGate is 0x7B (alpha channel tag)
    let gate_px = LogicGate::encode(0x7B, GateType::And, (-1, 0), (1, 0), 19);
    fb.set(6, 5, gate_px);

    // Verify the gate decodes correctly
    let gate = LogicGate::decode(gate_px);
    assert_eq!(gate.gate_type, GateType::And);
    assert_eq!(gate.input_a_offset, (-1, 0));
    assert_eq!(gate.input_b_offset, (1, 0));
    assert_eq!(gate.output_bit, 19);

    // Verify execution: AND of bit 19 in both inputs should be true
    let a_val = fb.resolve(5, 5);
    let b_val = fb.resolve(7, 5);
    let result = gate.execute(a_val, b_val);
    assert!(result, "AND of two set bits should be true");

    // Now test with one input having bit 19 clear
    fb.set(7, 5, pixel::rgb(0, 0, 0)); // bit 19 = 0
    let b_val2 = fb.resolve(7, 5);
    let result2 = gate.execute(a_val, b_val2);
    assert!(!result2, "AND with one clear bit should be false");
}
