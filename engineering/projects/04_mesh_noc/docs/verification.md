# Mesh verification

## Stimulus matrix

| Axis | Values |
| --- | --- |
| Topology / FIFO depth | 2×2/depth 2; 2×2/depth 4; 3×2/depth 4; 3×3/depth 4 |
| Destination pattern | Uniform random; complementary node; hotspot node 0; next node modulo node count |
| Source offer probability | 15%, 60%, 100% when able to offer |
| Sink readiness | Random 70%, or 20% for the 100% offer case; forced ready every eighth cycle |
| Workload size | 120 packets per source |
| Packet data | Source ID, source-local sequence, randomized 24-bit payload |

There are 4 parameter configurations × 4 destination patterns × 3 offer settings = **48 experiments**, totaling **33,120 delivered packets**.

## Scoreboard and assertions

At accepted injection, the bench saves the full 64-bit flit and injection cycle under `(source,sequence)`. At accepted ejection, it checks destination coordinates, legal identity, previous injection, no previous ejection, and bit-exact payload equality. Each identity must appear exactly once before the test can finish.

The bench checks that every stalled ejection retains valid and data. It enforces a clock timeout and a finite drain requirement. The Python driver independently checks packet-log count, uniqueness, and the sum of per-packet latencies against the simulation summary.

A miswire between opposite router directions produces a misroute, corruption, or failure to drain. A FIFO overflow or duplicate pop changes identity/payload counts. A grant changing during a blocked ejection triggers the stable-output assertion. Hotspot traffic concentrates contention at one destination and stresses backpressure propagation.

## What is not established

No formal deadlock or fairness proof is included. The suite does not report code coverage or exhaustively exercise FIFO pointer states independently of network traffic. Router-internal links rely on the same RTL contracts; only endpoint stalled-data stability is explicitly monitored. Reset is tested at startup, not during network occupancy. Malformed destinations are outside the traffic contract.

For a next step, add a standalone FIFO property harness with bounded formal assertions for occupancy, conservation, and ordering, followed by per-router grant-exclusion and internal-link stability assertions. A performance extension should use controlled sink readiness, warm-up, steady-state sampling, multiple seeds, and confidence intervals before describing a saturation curve.
