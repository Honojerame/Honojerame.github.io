# Measured RTL results

Generated from the checked-in JSON by `make report`. Run `make test`, `make lint`, and `make synth` first to produce new evidence. The reference simulation tool is Icarus Verilog 12.0; exact randomized cycle counts can vary with simulator versions.

| Suite | Cases / operations | Compared evidence |
| --- | --- | --- |
| RV32 cluster | 32 | 25,668 retirement events + complete final RAM |
| INT8 systolic | 48 | 1,344 matrix elements |
| Warp memory | 948 | 18,096 lane values |
| Mesh NoC | 48 | 33,120 packets |


**Total: 1,076 cases/operations.** These counts are different test units, not a coverage percentage.

## CPU: contention is visible

The table shows seed 0 with memory ready on every clock. Every hart executes a private-data version of the same mixed instruction stream. These are full program completion clocks, including pipeline startup, redirects, and terminal trap drain; this is not an application speedup benchmark.

| Cores | Hart | Cycles | Retired | Memory wait clocks | Load-use bubbles | Redirects |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 430 | 323 | 0 | 42 | 30 |
| 4 | 0 | 508 | 323 | 78 | 42 | 30 |
| 4 | 1 | 509 | 324 | 80 | 42 | 29 |
| 4 | 2 | 510 | 324 | 81 | 42 | 29 |
| 4 | 3 | 511 | 324 | 82 | 42 | 29 |


## Systolic: useful work versus fill/drain

Full active tiles with K=16. Select the first matching measured case for each physical size. Preload and result-drain time are excluded from compute utilization.

| Array | K | Useful MACs | Compute clocks | Compute utilization |
| --- | --- | --- | --- | --- |
| 2×2 | 16 | 64 | 18 | 88.89% |
| 4×4 | 16 | 256 | 22 | 72.73% |
| 8×8 | 16 | 1024 | 30 | 53.33% |


The larger physical array spends a larger fraction of this short reduction filling and draining. This is an inference from the schedule and measurements, not a claim that larger arrays are always slower.

## Global loads: same warp, different transaction count

| Active lanes | Stride (words) | Offset (words) | Sector requests | ACTIVE clocks |
| --- | --- | --- | --- | --- |
| 32 | 0 | 0 | 1 | 15 |
| 32 | 1 | 0 | 4 | 26 |
| 32 | 1 | 1 | 5 | 21 |
| 32 | 1 | 7 | 5 | 26 |
| 32 | 8 | 0 | 32 | 71 |
| 32 | 32 | 0 | 32 | 68 |


The response model observed **17 concurrent outstanding requests** and **1,957 out-of-order response pairs**. A pair counts an older outstanding request bypassed by a younger response; several pairs can arise from one response.

## Scratchpad: distinct words determine conflict cost

| Lanes | Banks | Stride (words) | Service clocks |
| --- | --- | --- | --- |
| 32 | 8 | 0 | 1 |
| 32 | 8 | 1 | 4 |
| 32 | 8 | 2 | 8 |
| 32 | 8 | 4 | 16 |
| 32 | 8 | 8 | 32 |
| 32 | 8 | 16 | 16 |
| 32 | 8 | 32 | 8 |


Repeated addresses broadcast within a service round. Stride wraps modulo 256 words in this experiment, so some large strides repeat addresses; the table must not be interpreted as an unbounded address stream.

## Mesh: contention and endpoint service

Selected depth-4 experiments at 60% source offer probability and 70% random sink readiness, with forced sink progress every eighth clock. Mean/max latency begins at accepted injection. Delivery rate includes finite-workload drain.

| Mesh | Pattern | Packets | Total clocks | Mean latency | Max latency | Packets / node / clock |
| --- | --- | --- | --- | --- | --- | --- |
| 2×2 | Uniform | 480 | 218 | 5.558 | 21 | 0.550459 |
| 2×2 | Hotspot | 480 | 655 | 30.717 | 87 | 0.183206 |
| 3×2 | Uniform | 720 | 216 | 6.449 | 25 | 0.555556 |
| 3×2 | Hotspot | 720 | 971 | 47.987 | 177 | 0.123584 |
| 3×3 | Uniform | 1080 | 243 | 8.448 | 44 | 0.493827 |
| 3×3 | Hotspot | 1080 | 1440 | 67.872 | 504 | 0.083333 |


Hotspot delivery is limited by the destination and its backpressure. These are seeded finite runs without confidence intervals; they do not establish a saturation throughput curve.

## Structural checks

Verilator lint passed for 5 top levels with the documented waivers. Yosys `synth -noabc` and `check -assert` completed for all five default top-level configurations.

| Top | Generic cells | Wire bits |
| --- | --- | --- |
| rv32_cluster | 35644 | 46197 |
| systolic_tile | 24847 | 38817 |
| warp_coalescer | 20400 | 65309 |
| banked_scratchpad | 89994 | 236702 |
| mesh_noc | 78240 | 201364 |


Generic counts include lowered storage and are not technology-mapped area, FPGA LUTs, timing, or power. They should not be compared directly between unrelated architectures as a quality ranking. Full synthesis transcripts are in `results/synth_*.log.gz`.

## Source identity

[source-manifest.json](../results/source-manifest.json) records SHA-256 hashes of RTL, testbenches, and Python tools present when this report was generated. A manifest is provenance, not a substitute for rerunning verification after edits.

See [verification methodology](verification-methodology.md) and each project verification guide for assumptions and untested cases.
