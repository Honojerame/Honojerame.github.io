# Verification methodology

## What counts as evidence

The project uses two complementary techniques: architectural differential checking and protocol-level assertions. It does not infer correctness from successful compilation or from a demonstration waveform.

| Layer | Implementation | Failure it can expose |
| --- | --- | --- |
| Architectural reference | Independent sequential RV32 interpreter, Python matrix products, lane-memory models | Wrong values, missing/extra retirement, bad masking, incorrect sign extension |
| Transaction scoreboard | Testbench request pools and NoC source/sequence identities | Duplication, corruption, phantom replies, misroutes, missing completion |
| Handshake assertions | Payload stability, index/last consistency, legal request identities | Changes during backpressure, output count errors, illegal transaction reuse |
| Bounded simulation | Per-test clock limits and finite workloads | Deadlock or failure to drain under supplied stimulus |
| Structural tools | Verilator lint; Yosys hierarchy and `check -assert` | Latches, broken connections, unsupported structure, multiple drivers |
| Measurements | RTL counters and observed injection/ejection timestamps | Incorrect performance accounting and ungrounded throughput claims |

## Independence and limitations

The CPU model interprets instructions sequentially and knows nothing about the pipeline or arbitration. Matrix expected values are computed from the mathematical sum, not a cycle-by-cycle copy of the PE implementation. Scratchpad service expectations count distinct words per bank. Coalescer expectations count unique 32-byte sector addresses. NoC identity/payload scoreboards are independent of the router's internal grants.

The models and RTL were developed together and can still share conceptual mistakes. The suite has not been run against the official RISC-V architectural compliance framework, a commercial verification IP, or a silicon reference. No formal proof, UVM environment, constrained-random coverage closure, gate-level simulation, CDC analysis, or power analysis is claimed.

## Reproducibility

Python generators use explicit seeds. SystemVerilog drivers seed `$urandom` before use. Bit-exact data results should remain invariant across compliant simulators; the precise pseudo-random stall sequence and resulting cycle counts can differ by simulator/version. Published cycle measurements refer to the documented Icarus version and workload.

Inputs and outputs remain available in `build/` after the run. JSON summaries are regenerated only by actual simulation. Test counts aggregate different units: a CPU test is a program/core-count combination; a systolic test is a tile configuration; a memory test is a warp operation; a NoC test is a complete traffic experiment. The collection total is a convenience, not a standardized coverage metric.

## Structural lint policy

All remaining warnings are fatal after four explicit waivers: `WIDTH`, `UNUSEDSIGNAL`, `UNUSEDPARAM`, and `UNSIGNED`. The designs use 32-bit host configuration/index fields and constant coordinate/generate parameters; these produce expected width, unused-field, and constant unsigned comparison diagnostics. The waivers are broad and therefore a known limitation: lint does not establish width correctness. Boundary arithmetic is exercised by directed functional tests. Latch and multiple-driver checks are not waived.

## Measurement boundaries

- **CPU cycles** include startup, dependency stalls, memory waits, redirects, and terminal-trap drain. Retired counts exclude terminal trap events.
- **Systolic compute cycles** exclude host preload and result drain. Useful utilization divides valid MACs by `N² × compute_cycles`.
- **Coalescer latency** counts ACTIVE-state clocks; it excludes the input handshake edge and output backpressure.
- **Scratchpad service cycles** count distinct-word service rounds, excluding output backpressure.
- **NoC latency** starts when the network accepts a packet, excluding waiting time at its source. Throughput includes workload injection and drain, so it is a finite-workload metric rather than a steady-state saturation measurement.
- **Generic synthesis cells** include generic logic and flip-flops after memory lowering. They are not LUTs, standard-cell area, physical delay, or energy.

These boundaries are part of the result, not footnotes to be discarded when quoting a number.
