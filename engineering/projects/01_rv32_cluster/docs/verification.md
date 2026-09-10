# RV32 verification plan and evidence

## Oracle

`tools/test_cpu.py` builds instructions directly and executes an independent sequential interpreter. It compares every observed event as `(PC, instruction, destination, architectural value, terminal cause)` for each hart. Non-writing trace values are deliberately ignored because they have no architectural meaning. It also compares every final byte of the 4 KiB shared RAM.

| Stimulus / check | Implemented evidence |
| --- | --- |
| 1-core and 4-core execution | Same 16 seeded programs at each size |
| Arithmetic and logical dependencies | Directed chains plus 180 randomized operations per program |
| Sign extension and arithmetic right shift | Negative INT8 load, halfword forms, negative arithmetic shifts |
| Store byte lanes and load sizes | Byte, halfword, word, signed and unsigned loads; final RAM comparison |
| Load-use hazard | A load immediately followed by a consumer |
| Branches and jumps | Random condition forms, counted backward loop, JAL and JALR |
| x0 | Explicit attempted write and reference-model x0 behavior |
| Memory stalls | Ready every cycle in one case; approximately 1/4 or 1/8 ready probability in others |
| Precise stopping | ECALL, EBREAK, illegal instruction, misaligned load/store/jump; younger sentinel store must not execute |
| Arbiter lock | Shared request payload and valid must remain stable under backpressure |
| Progress | Every hart must halt before the simulation clock limit |

The reference run compared **25,668 trace events** across **32 simulations**. This includes terminal events. Seeds and per-hart counters are in [cpu.json](../../../results/cpu.json).

## Failures this suite is designed to catch

A wrong signed shift creates a value mismatch at the exact retirement. A missing load interlock corrupts the dependent destination. Repeated WB retirement changes the trace length. A younger store escaping a terminal trap changes final memory. A grant switching while blocked triggers the shared-interface stability assertion. A lost completion prevents the finite program from draining.

## Coverage gaps

No instruction-encoding or code-coverage percentage is reported. Random generation is not a replacement for an exhaustive legal/illegal encoding matrix. No official architectural compliance suite, interrupt test, reset-during-transaction test, cache-coherence test, or shared-memory litmus test is included. Instruction fetch is idealized and data addresses are constrained to the test RAM. CPU performance cases execute mixed integer programs with private data regions; they are not SPEC, CoreMark, or a parallel application speedup benchmark.

## Useful next experiment

Add a shared-memory producer/consumer program only after specifying its synchronization mechanism. Without atomics or a privileged runtime, a four-core cluster should not be advertised as a general-purpose multicore operating-system platform. A smaller first step is to instrument separate arbiter-wait and memory-service counters and compare them under a fixed-latency memory model.
