# 03 · Warp memory: coalescing and bank replay

Two independently testable structures study the memory behavior behind SIMT workloads: a tagged global-load coalescer and an explicitly banked shared scratchpad.

**Run:** `make memory`. **Evidence:** [memory.json](../../results/memory.json). **Deep dives:** [architecture](docs/architecture.md), [verification](docs/verification.md).

| Structure | Implemented behavior |
| --- | --- |
| Global-load coalescer | Groups active word addresses by 32-byte sector; issues tagged sector requests; permits multiple sectors in flight; gathers out-of-order replies into lane order |
| Banked scratchpad | Serves one distinct word per bank per clock; broadcasts duplicate loads; replays bank conflicts; deterministic same-word stores; one physical write port per bank |

The experiment compares contiguous, offset, strided, broadcast, and random access patterns. The same number of active lanes can require radically different transaction counts. Memory performance is therefore a property of address layout and service resources, not just the arithmetic width of a compute unit.

Start with `rtl/warp_coalescer.sv` and `rtl/banked_scratchpad.sv`, then inspect their separate benches. `../../tools/test_memory.py` predicts unique sectors, expected lane values, and distinct-word service rounds independently from the RTL.

The collection contains **948 memory operations** at 8 and 32 lanes, including scratchpads with 4, 8, and 16 banks. No CUDA binary execution, NVIDIA microarchitecture replication, cache hierarchy, TLB, DRAM controller, or multi-warp scheduler is claimed.
