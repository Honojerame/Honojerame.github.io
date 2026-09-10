# 04 · Buffered mesh network-on-chip

A configurable two-dimensional mesh of five-port routers using deterministic X-before-Y routing, input FIFOs, per-output round-robin arbitration, and stable grants under backpressure.

**Run:** `make noc`. **Evidence:** [noc.json](../../results/noc.json). **Deep dives:** [architecture](docs/architecture.md), [verification](docs/verification.md).

| Module | Responsibility |
| --- | --- |
| `rtl/rv_fifo.sv` | Parameterized synchronous input queue |
| `rtl/xy_router.sv` | Destination decode, five input queues, per-output arbitration |
| `rtl/mesh_noc.sv` | Neighbor wiring and mesh boundary termination |
| `tb/tb_mesh.sv` | Traffic injection, bounded sink stalls, packet identity/payload scoreboard |
| `../../tools/test_noc.py` | 48 traffic experiments and independent log consistency checks |

The reference run checks **33,120 packets** across 2×2, 3×2, and 3×3 meshes, including uniform, complement, hotspot, and ring-destination traffic. The experiments measure accepted-packet latency and finite-workload delivery rate.

This is a single-flit packet network. Virtual channels, wormhole packet reservation, credit flow control, adaptive routing, clock-domain crossings, fault routing, and coherence messages are not implemented.
