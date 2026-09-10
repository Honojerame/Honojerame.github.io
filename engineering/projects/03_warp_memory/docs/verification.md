# Warp-memory verification

## Global-load path

For each input, Python independently computes the unique sectors, active-lane count, alignment outcome, and expected lane words. The test memory function is `0x9e3779b9 XOR ((byte_address >> 2) * 0x01010101)` modulo 2³². Each accepted sector request returns eight words from that function.

The SystemVerilog memory model retains requests in a tag-indexed pool, delays them 4–23 clocks, and selects among eligible replies in a randomized rotated order. It checks for tag reuse and counts observed outstanding occupancy and out-of-order response pairs. The latter counts every older outstanding request bypassed by a response, so it is not the number of reordered responses.

| Coverage axis | Stimulus |
| --- | --- |
| Lane width | 8 and 32 |
| Regular layouts | Strides 0,1,2,4,8,16,32 words; offsets 0,1,7 words |
| Irregular layouts | 60 seeded random warps per lane width |
| Masks | Full, random, empty |
| Error | Misaligned active address; no request may issue |
| Concurrency | Multiple sector requests in flight and replies out of issue order |
| Backpressure | Random request readiness and completed-warp readiness |
| Protocol | Stable request and output data while stalled; one output per input tag |

The response check compares all lanes, including inactive zeros. Tag identity, sector count, active count, and error status must also match. A timeout catches a context that cannot complete under the supplied memory behavior.

## Scratchpad path

Each parameter run first initializes every storage word using the public store interface. Tests then perform regular loads, duplicate stores followed by broadcasts, invalid/empty requests, and 100 mixed randomized loads/stores. The Python memory model applies the documented highest-lane store rule and counts distinct words per bank independently.

The suite tests 8/32 lanes against 4/8/16 physical banks. Every returned lane value and every service-cycle count must match. Random output stalls exercise retained completions.

Together the paths check **948 operations and 18,096 lane values**. The machine-readable report includes measured sector counts, service cycles, peak observed outstanding requests, and response reordering evidence.

## Remaining verification work

Not included: reset during active traffic, invalid/duplicate-tag recovery, exhausted multi-warp context tables, store coalescing on the global path, byte-granular atomics, memory consistency, caches, ECC, TLB faults, or actual DRAM timing. Response producers obey the required stable-payload contract, but the default model normally sees ready high for valid tags; this is not a stress test of sustained backpressure on the sector-response channel.

The scratchpad parameter contract requires WORDS divisible by BANKS. Arbitrary unsupported parameter combinations are not guarded by a synthesizable parameter-validation circuit; integration must enforce the documented constraints.
