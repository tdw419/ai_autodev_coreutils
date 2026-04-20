# Geometry OS Roadmap

GPU-native operating system where pixels are instructions, the GPU texture is memory,
and programs write programs. Implemented in Rust (~19,400 lines) with 347 tests passing
on real hardware (NVIDIA RTX 5090, 32GB VRAM).


**Progress:** 8/14 phases complete, 0 in progress

**Deliverables:** 33/59 complete

## Scope Summary

| Phase | Status | Deliverables | LOC Target | Tests |
|-------|--------|-------------|-----------|-------|
| phase-0 Bootstrap | COMPLETE | 2/2 | 500 | 10 |
| phase-1 Pixel VM Core | COMPLETE | 4/4 | 4,000 | 80 |
| phase-2 Spatial Memory | COMPLETE | 3/3 | 5,500 | 120 |
| phase-3 Compilation Pipeline | COMPLETE | 4/4 | 9,000 | 180 |
| phase-4 IPC and I/O | COMPLETE | 7/7 | 13,000 | 260 |
| phase-5 Self-Improvement | COMPLETE | 4/4 | 16,000 | 300 |
| phase-6 Visualization | COMPLETE | 4/4 | 18,000 | 330 |
| phase-7 Infrastructure | COMPLETE | 5/5 | 19,400 | 347 |
| phase-8 Bare-Metal RV64 | PLANNED | 0/4 | 26,000 | 420 |
| phase-9 AI-Native Opcodes | PLANNED | 0/8 | 23,000 | 400 |
| phase-10 Persistent Spatial Filesystem | FUTURE | 0/4 | 25,000 | 450 |
| phase-11 Networking as Spatial I/O | FUTURE | 0/3 | 26,000 | 480 |
| phase-12 Self-Hosting | FUTURE | 0/3 | 28,000 | 520 |
| phase-13 Multi-Agent Orchestration | FUTURE | 0/4 | 32,000 | 600 |

## Dependencies

| From | To | Type | Reason |
|------|----|------|--------|
| phase-6 | phase-7 | hard | Visualization required for canvas UI |
| phase-7 | phase-8 | hard | Need working wgpu-based system as reference implementation |
| phase-7 | phase-9 | soft | Can be developed in parallel with Phase 8 but benefits from stable base |
| phase-5 | phase-9 | informs | Self-improvement patterns inform AI-native opcode design |
| phase-7 | phase-10 | hard | Need stable memory allocation and CPU stub for persistence |
| phase-2 | phase-10 | hard | Hilbert curve mapping is the foundation of spatial file addressing |
| phase-4 | phase-11 | hard | CPU stub pattern is the I/O mechanism |
| phase-3 | phase-12 | hard | Need working GeoLang compiler and transpiler |
| phase-10 | phase-12 | soft | Filesystem helpful for managing compiler output on the texture |
| phase-4 | phase-13 | hard | IPC and CPU stub are the communication backbone |
| phase-5 | phase-13 | hard | Evolution engine and fitness functions are the core mechanism |
| phase-9 | phase-13 | soft | AI-native oppcodes would improve agent-generated code quality |
| phase-12 | phase-13 | soft | Self-hosting means agents can modify the compiler itself |

## [x] phase-0: Bootstrap (COMPLETE)

**Goal:** Rust project skeleton with wgpu initialization and a 4096x4096 texture.

The foundation. Rust binary that initializes wgpu, creates the 4096x4096 RGBA8
texture (64MB), and proves the GPU pipeline works end-to-end.


### Deliverables

- [x] **wgpu initialization** -- Create GPU device, queue, and 4096x4096 RGBA8 texture
  - [x] Texture created and accessible via compute shader
    _Validation: cargo test --lib texture_init_
- [x] **Cargo project structure** -- Multi-binary Cargo.toml with daemon, repl, debug targets
  - [x] cargo build succeeds for all targets

## [x] phase-1: Pixel VM Core (COMPLETE)

**Goal:** Fetch-decode-execute loop that reads opcodes from pixel values in the texture.

The VM reads RGBA pixels as (opcode, stratum, p1, p2) and executes them.
8 concurrent VMs, each with 128 registers, 64-level call stack, program counter.
Software VM (software_vm.rs) mirrors the shader exactly for cross-validation.


### Deliverables

- [x] **Compute shader VM (glyph_vm_scheduler.wgsl)** -- GPU compute shader that fetches, decodes, and executes pixel opcodes
  - [x] All basic opcodes execute correctly on GPU
    _Validation: 347 tests pass, 0 failures_
- [x] **Software VM mirror (software_vm.rs)** -- CPU-side VM that produces identical results to the shader
  - [x] Cross-validated: same inputs produce same outputs on CPU and GPU
- [x] **Opcode set (35+ opcodes)** -- NOP, LDI, MOV, LOAD, STORE, ADD, SUB, MUL, DIV, JMP, BNE, CALL, RET, HALT, ENTRY, CHAR, BLIT, SEND, RECV, SPAWN, YIELD, WAIT_EVENT, XOR, NOT, MOD, LDB, STB, RECTF, LINE, TEXT_STR, CIRCLEF, and more
  - [x] Each opcode has dedicated tests
- [x] **8 concurrent VMs** -- Parallel execution with per-VM register file, PC, call stack
  - [x] All 8 VMs can execute simultaneously

### Technical Notes

The pixel encoding: R=opcode (0-255), G=stratum (layer/mode/condition),
B=parameter 1, A=parameter 2. Each VM gets a spatial region of the texture.


## [x] phase-2: Spatial Memory (COMPLETE)

**Goal:** Hilbert curve mapping and spatial memory allocation with bounds checking.

Memory management via 2D spatial coordinates mapped to 1D via Hilbert curve.
Each VM gets an isolated region bounded by base_addr/bound_addr.
Out-of-bounds access triggers VM_FAULT.


### Deliverables

- [x] **Hilbert curve mapping** -- 2D texture coords <-> 1D physical addresses via Hilbert curve
  - [x] Spatial locality preserved in physical cache layout
- [x] **Spatial memory allocation** -- VM isolation via base_addr/bound_addr bounds checking
  - [x] Out-of-bounds access triggers VM_FAULT
- [x] **Visual memory debugging** -- Used vs free regions visible as different colors on texture

## [x] phase-3: Compilation Pipeline (COMPLETE)

**Goal:** Text assembly and C-like language to pixel bytecode compilation.

Three-tier compilation: .gasm text assembly -> pixel bytecode,
GeoLang compiler (C-like -> pixel opcodes directly, 2079 lines, 25 tests),
and C-to-.glyph transpiler supporting arithmetic, control flow, structs, pointers, arrays.


### Deliverables

- [x] **Assembler (.gasm -> pixel bytecode)** -- Two-pass assembler with labels, DATA directives, disassembler
  - [x] Labels resolve correctly, DATA sections load into texture
- [x] **GeoLang compiler** -- C-like language compiled directly to pixel opcodes (2079 lines, 25 tests)
  - [x] Arithmetic, control flow, functions compile and execute
- [x] **C-to-.glyph transpiler** -- Transpiles C: arithmetic, control flow, structs, pointers, arrays -> pixel bytecode
- [x] **GASP animation compiler** -- Tween/animation system with keyframe labels (src/gasp_compiler.rs)

## [x] phase-4: IPC and I/O (COMPLETE)

**Goal:** Inter-VM communication and the CPU stub pattern for external I/O.

SPAWN/YIELD for VM forking with memory isolation. SEND/RECV message queues
for inter-VM communication. 3-layer IPC: GPU VM -> device proxy .glyph shim -> CPU stub Rust thread.
CPU stub with 9 command types including file I/O, SQL queries, and LLM calls.


### Deliverables

- [x] **SPAWN/YIELD VM forking** -- Create child VMs with isolated memory regions
  - [x] Child VM executes independently, memory isolated from parent
- [x] **SEND/RECV message queues** -- Inter-VM message passing via mailbox system
- [x] **Event queue (WAIT_EVENT)** -- External event injection for keyboard, mouse, inter-VM messages
- [x] **CPU stub with 9 command types** -- READ_BLOCK, WRITE_BLOCK, OPEN, CLOSE, IOCTL, CMD_SQL_QUERY, CMD_MODEL_CALL, CMD_STATUS_READ, CMD_STATUS_WRITE
- [x] **SqliteExecutor** -- rusqlite-backed SQL query execution via CPU stub
- [x] **ModelExecutor** -- HTTP LLM client via CPU stub -- VM can call LLMs
- [x] **FileExecutor** -- File I/O via CPU stub

### Technical Notes

The CPU stub pattern is what makes agent-driven execution possible:
the VM can call an LLM, query a database, or read a file without any
of those concepts existing in the GPU shader.


## [x] phase-5: Self-Improvement (COMPLETE)

**Goal:** Evolution engine with fitness-guided mutations and governance gates.

The VM can evolve its own programs. Evolution engine (src/evolution.rs, 1045 lines)
performs mutation -> execute -> score -> keep/discard cycles. Fitness function
(src/fitness.rs) uses composite scoring: speed, correctness, memory, spatial locality.
Governance gate (src/governance.rs, 558 lines) enforces Seven Laws before any mutation.


### Deliverables

- [x] **Evolution engine (evolution.rs)** -- Mutation -> execute -> score -> keep/discard loop
  - [x] GEO-68: fitness-component-guided mutations beat random by 57% on real GPU
- [x] **Fitness function (fitness.rs)** -- Composite scoring: speed, correctness, memory, spatial locality
- [x] **Mutation engine (mutation.rs)** -- Pixel-level variations with selection pressure
- [x] **Governance gate (governance.rs)** -- Seven Laws check before any mutation executes (558 lines)

## [x] phase-6: Visualization (COMPLETE)

**Goal:** Windowed runtime with VM HUD overlay, filmstrip projector, and font atlas.

Real-time visualization of the 4096x4096 texture at 30fps. VM HUD overlay shows
register values, PC, execution state. Filmstrip projector captures multi-frame
execution for time-based debugging. 8x8 bitmap font atlas at 0x00F00000.


### Deliverables

- [x] **Windowed runtime** -- 4096x4096 texture display at 30fps via wgpu
- [x] **VM HUD overlay** -- Register values, PC, execution state rendered spatially
- [x] **Filmstrip projector (filmstrip.rs)** -- Multi-frame execution capture for time-based debugging
- [x] **Font atlas** -- 8x8 bitmap font at 0x00F00000, CHAR opcode renders glyphs

## [x] phase-7: Infrastructure (COMPLETE)

**Goal:** DRM backend, pixel compiler/linker, multiple binary targets, and canvas-based UI.

DRM backend for AMDGPU with DMA-BUF sharing. Pixel compiler/linker with stdlib.
Multiple binaries: daemon, pmp-eval, pmp-repl, pmp-trace, frame_debug.
Canvas-based UI: 32x32 text surface, assembler, terminal mode (geo> CLI),
256x256 framebuffer. Old sprints A-E completed here.


### Deliverables

- [x] **DRM backend** -- AMDGPU command buffers, DMA-BUF sharing for zero-copy
- [x] **Pixel compiler/linker with stdlib** -- Standard library: memset, memcpy, math routines loaded as pixel programs
- [x] **Multi-binary targets** -- daemon, pmp-eval, pmp-repl, pmp-trace, frame_debug
- [x] **Canvas text surface + assembler** -- 32x32 grid, type assembly, F8 to assemble, F5 to run
  - [x] All Sprint A-E visual and interactive programs work
- [x] **Terminal mode (geo> CLI)** -- REPL with help, list/ls, load, run, edit, regs, peek, poke, reset, clear, quit

## [ ] phase-8: Bare-Metal RV64 (PLANNED)

**Goal:** Boot a minimal RV64 Linux kernel on the GPU, bypassing wgpu entirely.

The current system runs through wgpu, which has limitations: no native u64 support
in WGSL (requiring vec2<u32> emulation), buffer size constraints, and an abstraction
layer between the shader and the hardware. Phase 8 goes direct to metal.

Port the VM to SPIR-V with native u64 support. AMDGPU direct command submission
via DRM ioctl. DMA-BUF framebuffer sharing for zero-copy visualization. RV64I base
instruction set with Sv39 MMU.


### Deliverables

- [ ] **SPIR-V RV64 kernel** -- Port the VM to SPIR-V with native u64 registers
  - [ ] SPIR-V shader compiles and dispatches on AMD hardware
    _Validation: Native GPU dispatch without wgpu_
  - [ ] Native u64 registers work (no vec2<u32> emulation)
  _~2000 LOC_
- [ ] **AMDGPU direct command submission** -- PM4 packets, GVM management via DRM ioctl
  - [ ] Submit compute dispatches directly to AMDGPU
    _Validation: DRM ioctl calls succeed, shader executes_
  _~1500 LOC_
- [ ] **RV64I base instruction set** -- Implement RV64I with Sv39 page table walks in the shader
  - [ ] rv64ui-p-* compliance tests pass
    _Validation: RISC-V compliance test suite_
  _~3000 LOC_
- [ ] **Boot minimal RV64 Linux** -- The 'screen is the hard drive' concept fully realized
  - [ ] Linux kernel boots on the GPU VM
    _Validation: Kernel boot messages visible on framebuffer_

### Technical Notes

Steps:
1. Create SPIR-V RV64 kernel (systems/infinite_map_rs/src/shaders/riscv64_vm.glsl)
2. Implement native u64 registers and Sv39 page table walks in the shader
3. Complete AMDGPU command buffer submission (PM4 packets, GVM management)
4. Boot minimal RV64 Linux on the native GPU executor
5. Verify with rv64ui-p-* compliance tests


### Risks

- AMDGPU ioctl interface is poorly documented -- may need kernel module development
- SPIR-V compute shaders have different capabilities than WGSL -- feature discovery needed
- RV64I emulation performance on GPU compute units is unknown

## [ ] phase-9: AI-Native Opcodes (PLANNED)

**Goal:** Opcodes designed for probabilistic, AI-generated code execution.

The current opcode set is deterministic: ADD always adds, JMP always jumps.
But LLM-generated code is probabilistic. Phase 9 introduces opcodes for
uncertainty-aware execution, attention mechanisms, and self-modification.


### Deliverables

- [ ] **BRANCH_PROB (220)** -- Branch based on probability threshold
  - [ ] Branches correctly with given probability value
- [ ] **CONFIDENCE_MARK (221)** -- Associate confidence score with a code block
- [ ] **ALTERNATE_PATH (222)** -- Define fallback paths for low-confidence execution
- [ ] **ATTENTION_FOCUS (223)** -- Mark spatial regions as active, skip inactive regions
- [ ] **GLYPH_MUTATE (224)** -- Transform a glyph at a coordinate (self-modification)
- [ ] **SPATIAL_SPAWN (225)** -- Create new glyph clusters at target coordinates
- [ ] **SEMANTIC_MERGE (226)** -- Unify redundant glyph clusters (spatial refactoring)
- [ ] **LOAD_EMBEDDING (227)** -- Load vector embeddings into specialized registers
  - [ ] Embedding loaded and accessible by other opcodes

### Technical Notes

When an AI generates .glyph code, it doesn't know with certainty that every opcode
is correct. Probabilistic execution lets the VM handle uncertainty gracefully.
Attention focus lets it skip clearly wrong regions. Self-modification opcodes
let it fix its own output.


### Risks

- Probabilistic opcodes make debugging harder -- need excellent visualization
- Unclear how to test non-deterministic opcodes -- may need statistical testing

## [?] phase-10: Persistent Spatial Filesystem (FUTURE)

**Goal:** Files as spatial regions of the texture, not traditional block devices.

Each file occupies a contiguous spatial region of the texture. Directory structure
is a spatial hierarchy (parent regions contain child regions). Metadata stored as
pixel headers. CPU stub's existing file I/O handles persistence to disk. Hilbert
curve ensures spatial locality for related files.


### Deliverables

- [ ] **Spatial file allocator** -- Allocate/free spatial regions for file storage in the texture
  - [ ] Files can be created, read, written, and deleted
  - [ ] Spatial locality maintained for related files
- [ ] **Directory hierarchy** -- Parent regions contain child regions with metadata headers
  - [ ] Nested directory traversal works
- [ ] **Persistence bridge** -- CPU stub syncs spatial regions to/from disk
  - [ ] Files survive VM restart
- [ ] **Visual file browser** -- See your files on the texture -- opening a file is navigating to a spatial region

### Risks

- Fragmentation of spatial regions over time -- need spatial defragmentation
- File size limited by available texture space (64MB total)

## [?] phase-11: Networking as Spatial I/O (FUTURE)

**Goal:** Network communication through the CPU stub pattern.

New CPU stub commands: CMD_NET_SEND (10), CMD_NET_RECV (11), CMD_NET_DNS (12).
Network addresses represented as spatial coordinates. Agent loops can query
external services, fetch data, communicate with other instances. The VM doesn't
know about TCP/IP -- it writes a message and reads the response.


### Deliverables

- [ ] **Network CPU stub commands** -- CMD_NET_SEND, CMD_NET_RECV, CMD_NET_DNS in the stub executor
  - [ ] VM can send/receive messages to/from network endpoints
- [ ] **Spatial address mapping** -- Network endpoints mapped to spatial coordinates
- [ ] **DNS resolution** -- VM can resolve hostnames via CPU stub

## [?] phase-12: Self-Hosting (FUTURE)

**Goal:** The GeoLang compiler, compiled to .glyph, running on the GPU VM.

The ultimate proof of the architecture. If the compiler can run on the VM it
targets, the system has achieved self-hosting. Same milestone GCC and Rust
achieved for traditional platforms.


### Deliverables

- [ ] **Compiler self-compilation** -- Verify GeoLang compiler can compile itself (self-compilation)
  - [ ] Compiler output matches reference build
- [ ] **Compiler transpiled to .glyph** -- Transpile the compiler's own C output to .glyph bytecode
- [ ] **Compiler loaded into GPU texture** -- The compiled compiler runs on the GPU VM
  - [ ] VM can assemble programs using the on-GPU compiler

### Technical Notes

Steps:
1. Verify the GeoLang compiler can compile itself (self-compilation)
2. Transpile the compiler's own C output to .glyph bytecode
3. Load the compiled compiler into the GPU texture
4. The VM assembles its own programs -- the system builds itself


### Risks

- Compiler may be too large for a single VM's memory region
- Performance of compiler on GPU VM may be impractically slow
- Bootstrapping may require multiple passes

## [?] phase-13: Multi-Agent Orchestration (FUTURE)

**Goal:** Multiple agent loops running concurrently on different VMs, coordinated via IPC.

Specialized agents on separate VMs: researcher (queries LLM for ideas),
coder (generates .glyph), tester (runs programs and scores fitness), reviewer (governance gate).
GPU-parallel evolution: population of mutants evaluated simultaneously across 8 VMs.


### Deliverables

- [ ] **Agent role definitions** -- Researcher, Coder, Tester, Reviewer -- each on its own VM
  - [ ] Each agent role executes its specialized task independently
- [ ] **Inter-agent IPC protocol** -- SEND/RECV message queue protocol for agent coordination
  - [ ] Agents can delegate tasks and share results via IPC
- [ ] **GPU-parallel evolution** -- Population of mutants evaluated simultaneously across 8 VMs
  - [ ] 8 VMs evaluate different mutants in parallel
- [ ] **Agent-driven self-improvement loop** -- The multi-agent system runs autonomously, improving the codebase
  - [ ] System produces measurably improved programs without human intervention

### Risks

- Agent coordination complexity -- deadlock and starvation possible
- Resource contention across 8 VMs for GPU time
- Governance enforcement across multiple agents is non-trivial

## Global Risks

- wgpu API changes between versions may break shader compatibility
- GPU compute shader precision varies across vendors -- NVIDIA-only for now
- 64MB texture limit constrains program complexity and filesystem size
- Self-hosting bootstrap problem: compiler needs itself to build itself
- Regulatory/ethical concerns around autonomous self-improving GPU programs

## Conventions

- All opcodes tested on both software_vm.rs and GPU shader
- Rust code formatted with rustfmt, linted with clippy
- 347 tests must remain green -- no regressions allowed
- New opcodes require: implementation, tests, documentation, assembler support
- CPU stub executors are independently testable
- Spatial locality principle: related data goes in adjacent texture regions
- The 'screen is the hard drive' -- framebuffer regions map to persistent data
