# 02 · Output-stationary INT8 systolic tile

A parameterized N×N array of signed INT8 multiply-accumulate processing elements, with skewed operand injection, local forwarding, tail masking, and a backpressured INT32 output stream.

**Run:** `make systolic`. **Evidence:** [systolic.json](../../results/systolic.json). **Deep dives:** [architecture](docs/architecture.md), [verification](docs/verification.md).

The RTL computes `C[r,c] = Σ A[r,k] × B[k,c]` for one tile. Accumulators remain in their PEs while A moves right and B moves down. The implementation makes fill/drain cost measurable rather than reporting only peak multiplication capacity.

| Implemented component | Source |
| --- | --- |
| Signed PE, forwarding registers, 32-bit accumulation | `rtl/mac_pe.sv` |
| Operand memories, descriptor validation, skew schedule, output serialization | `rtl/systolic_tile.sv` |
| Configuration driver, invalid descriptor test, random output stalls | `tb/tb_systolic.sv` |
| Independent matrix oracle and parameter sweep | `../../tools/test_systolic.py` |

The test suite covers physical array sizes 2, 4, and 8; K=1,2,7,16; signed extrema; random operands; and partially active tiles. A full 4×4 tile with K=16 performs 256 useful MACs over 22 compute clocks. This excludes preload and result transfer.

This is a compute-tile study, not a complete neural-network accelerator. DMA, AXI, double buffering, quantization scaling, activation functions, sparsity, floating point, and a compiler/runtime are not implemented.
