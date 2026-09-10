# 01 · Four-core RV32I pipeline cluster

A five-stage integer pipeline replicated behind a locked, round-robin shared-memory arbiter. The project concentrates on architectural correctness under dependency hazards, redirects, and variable memory latency.

**Run:** `make cpu` from the collection root. **Evidence:** [CPU results](../../results/cpu.json). **Deep dives:** [architecture](docs/architecture.md), [verification](docs/verification.md).

## Implemented

- IF/ID/EX/MEM/WB pipeline and 32 integer registers per hart, with hard-wired x0.
- RV32I integer ALU, immediate operations, shifts, signed/unsigned comparisons, branches, jumps, upper immediates, byte/halfword/word loads and stores.
- EX/MEM and MEM/WB forwarding, WB-to-decode bypass, load-use interlock, branch flush.
- Synchronous terminal traps for illegal instructions, misalignment, ECALL, and EBREAK.
- Parameterized hart replication and stable round-robin shared-memory arbitration.
- Architectural retirement trace and per-core performance counters.

## Start reading

1. `rtl/rv32_core.sv`: combinational execute/decode, then the sequential pipeline update. Pay particular attention to the `blocked` path.
2. `rtl/rv32_cluster.sv`: grant selection, lock ownership, per-hart ready qualification.
3. `tb/tb_cluster.sv`: shared-memory completion model and retirement trace.
4. `../../tools/test_cpu.py`: assembler helpers, independent interpreter, seeded programs, and comparison.

The checked suite runs 16 programs at both one and four cores. Each hart owns a private 256-byte data region in the shared RAM, letting arithmetic and load/store results be checked independently while all harts still contend for the same memory port.

This is a pipelined integer architecture study, not a complete privileged RISC-V platform. There are no caches, coherence protocol, atomic instructions, multiplication extension, CSR bank, interrupts, debug module, or operating-system boot flow. The initial a0 hart ID is a documented project convention, not an ISA reset requirement.
