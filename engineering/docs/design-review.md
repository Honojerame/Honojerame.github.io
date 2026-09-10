# Architecture review walkthrough

Use these questions to inspect the source and explain the engineering. Each walkthrough connects a claim to code and a reproducible experiment. These are study prompts, not claims of personal employment experience.

## 1. Walk an instruction through the cluster

Start with a store followed by a load and dependent ALU instruction in `tools/test_cpu.py`. Trace IF, ID, EX, MEM, and WB in `rv32_core.sv`. Explain why forwarding does not remove every load-use stall. Then hold shared memory ready low: show why the grant cannot change, why WB must retire at most once, and why a held EX operand must retain a WB forwarding result.

Read the terminal-trap test. Why is a younger store placed after it? Which stage detects the trap? Which older instructions can still retire? What state would be needed to replace terminal halt with a privileged trap handler?

**Tradeoff to defend:** a single blocking memory interface gives simple serialization and visible contention, but adding cores cannot create memory bandwidth. A cache or multiple outstanding requests would change the correctness argument, not just a parameter.

## 2. Derive the systolic schedule

For N=4, K=16, identify when `A[3,15]` and `B[15,3]` reach the bottom-right PE. Derive 22 RUN cycles and 256 useful MACs. Explain why the peak is 16 MACs per compute clock but measured utilization is 256/(16×22), and why neither number includes preload or output transfer.

Change to a 3×3 active tile in the physical 4×4 array. Which operands become zero? What happens to utilization if the controller retains the same fill/drain schedule? Inspect negative INT8 multiplication and the sign extension into the accumulator.

**Tradeoff to defend:** output-stationary accumulation reduces movement of partial sums; single-bank loading leaves substantial scheduling and bandwidth opportunities unimplemented.

## 3. Explain a warp access pattern

Compare 32 contiguous words starting at byte 0 with the same words starting at byte 4. Count sectors before running the RTL. Then compare stride 8 words with a broadcast. Explain why the same number of lanes can require one, four, five, or 32 sector requests.

Return the third issued sector before the first. Which tag belongs to each lane? Why must a response refer to a previously accepted request? Why does an input with no active lanes still need a completion?

For the scratchpad, distinguish multiple lanes reading the same word from multiple distinct words mapping to the same bank. Explain the deterministic same-address store rule and why it is a project contract rather than a claim about CUDA data races.

**Tradeoff to defend:** one resident warp with many sectors in flight isolates response assembly, but does not model scheduling among many warps or a real cache hierarchy.

## 4. Follow a contended packet

Choose two input FIFO heads targeting the same router output. Walk the rotating grant, then stall the sink. Explain why a locked grant is necessary for stable output data and why round robin alone does not provide a finite end-to-end latency bound if the sink can stall indefinitely.

Compare uniform and hotspot traffic. Identify the concentration of ejections at node 0. Explain why increasing FIFO depth can absorb bursts but cannot increase that endpoint's sustained service rate. Locate head-of-line blocking in the input-buffered structure.

**Tradeoff to defend:** deterministic X-before-Y routing on a non-wrapping mesh has a simple channel-dependency argument, but this suite measures finite-workload progress rather than formally proving deadlock freedom.

## Extensions with acceptance criteria

| Extension | Required design work | Evidence required before claiming it |
| --- | --- | --- |
| CPU private caches | Tags, misses, coherence or documented non-coherent programming model | Aliasing, eviction, shared-data visibility, contention tests |
| Double-buffered accelerator | Bank ownership, concurrent load/compute, completion ordering | Back-to-back tiles, bank hazards, measured end-to-end overlap |
| Multi-warp memory | Context IDs, resource allocation, response isolation | Interleaved completions and fairness under bounded stalls |
| Multi-flit NoC packets | Route reservation, tail release, buffer management | Interleaved packet stress, no premature grant release |
| FPGA demonstration | Board memory/clock/reset adapters, constraints | Timing report, resource utilization, hardware result capture |
| Formal invariants | Abstract assumptions and bounded/unbounded proof setup | Checked proof logs, failed-property counterexamples, documented assumptions |
