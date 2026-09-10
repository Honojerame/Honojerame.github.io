# Systolic verification

Python computes each expected result directly from the matrix sum. The reference does not model systolic timing or reuse PE code. The SystemVerilog bench separately checks output ordering, last signaling, count, and payload stability during stalls.

| Axis | Exercised values |
| --- | --- |
| Physical N | 2, 4, 8 |
| Reduction K | 1, 2, 7, 16 |
| Active shape | Full and reduced rows/columns |
| Data | Seeded random signed bytes; all -128; 127 × -128 |
| Preload timing | Random 0–2 clock gaps |
| Output timing | Approximately 1/4 readiness probability |
| Invalid command | K=0 rejected before each valid tile |
| Schedule | Observed RUN clocks equal `K+2N-2` |
| Useful work | Counter equals `rows*cols*K` |

The reference run contains **48 configurations and 1,344 compared output elements**. Results and counters are retained in [systolic.json](../../../results/systolic.json).

The signed-extreme tests catch accidental unsigned multiplication. K=1 stresses fill/drain boundaries. Tail masking catches invalid rows/columns leaking nonzero values. Random result backpressure checks that serialization cannot skip or change a held accumulator value.

Coverage gaps: the suite does not exercise reset mid-tile, overflow at very large K, repeated valid tiles without reset, every invalid descriptor form, or a hardware memory macro implementation. Preload data is fully initialized. Double buffering and overlapping DMA are extension work and are not measured.

To extend this project, implement a second operand bank with explicit load/compute ownership. Acceptance requires back-to-back tiles with distinct signed data, stalled results, concurrent preload, and an end-to-end timing comparison that includes both data transfer directions.
