# Reproduce, inspect, change

## Environment

Reference run: Ubuntu 24.04 user-space tools, Icarus Verilog 12.0, Verilator 5.020, Yosys 0.33, and Python 3. The simulation uses Icarus; Verilator is an independent structural lint tool. Yosys performs synthesis with technology mapping to generic gates and flip-flops, with ABC disabled.

The reference environment did not permit system package installation, so official Ubuntu packages were SHA-256 verified and extracted into a task-local tool directory. The repository does not depend on that directory or ship those binaries. The normal Ubuntu installation in the root README is sufficient.

## Commands

| Command | What it actually executes | Output |
| --- | --- | --- |
| `make cpu` | RV32 RTL at 1 and 4 harts; compare every retirement and final RAM | `results/cpu.json` |
| `make systolic` | PE arrays at N=2,4,8; compare every result element | `results/systolic.json` |
| `make memory` | Sector-return and scratchpad transaction tests | `results/memory.json` |
| `make noc` | 48 seeded mesh traffic runs with packet scoreboards | `results/noc.json` |
| `make lint` | Verilator on all five top modules | `results/lint.json` |
| `make synth` | Yosys synthesis, `check -assert`, generic statistics | `results/synth.json` and gzip-compressed transcripts |
| `make report` | Read measured JSON and regenerate report; no simulation | `docs/results.md` |
| `make clean` | Delete temporary build products | Keeps source and checked-in results |

Run the commands from the collection root, the directory containing `Makefile`. The build has no non-standard Python imports. `make -j4 test` can run the four independent suites concurrently; avoid running two copies of the same suite because they share build filenames.

## Tool overrides

Environment variables `IVERILOG`, `VVP`, `VERILATOR`, `YOSYS`, and the make variable `PYTHON` select tools. Commands are split using Python `shlex`, so an override can include tool options:

```sh
IVERILOG='/opt/iverilog/bin/iverilog -B/opt/iverilog/lib/ivl' \
VVP=/opt/iverilog/bin/vvp make test
```

For a relocatable Verilator package, set its documented `VERILATOR_ROOT` to the package's `share/verilator` directory. A locally extracted Yosys may also need its shared-library directory in `LD_LIBRARY_PATH`.

## Inspect a failed case

All input vectors and simulator outputs remain in `build/`. CPU filenames contain core count and seed. The coalescer and scratchpad drivers retain entire operation streams. NoC logs contain source, source-local sequence, destination, and accepted-injection-to-ejection latency.

An assertion failure prints enough context to locate the case. For example, a CPU mismatch includes core count, seed, hart, retirement index, observed tuple, and expected tuple. Compare the `.trace` with the generated `.hex`; `tools/test_cpu.py` contains the independent instruction interpreter.

Rerun a simulator directly by copying its invocation from the raised error. The Python wrapper includes the full command on failure. Change `+SEED=` to vary simulator-side stalls, or change the stimulus generator seed to vary architectural data. These are different axes of verification.

## Waveforms

```sh
WAVES=1 make cpu
WAVES=1 make systolic
WAVES=1 make memory
WAVES=1 make noc
```

The testbenches emit `build/cluster.vcd`, `build/tb_systolic.vcd`, `build/tb_coalescer.vcd`, `build/tb_scratchpad.vcd`, and `build/tb_mesh.vcd`. A later case of the same testbench overwrites its waveform; the file represents the last run of that bench, not the whole suite. For a particular earlier case, invoke the compiled simulator with its saved input plus `+VCD=1`. Inspect with GTKWave or another VCD viewer. Waveforms are optional and intentionally excluded from the source archive.

## Change discipline

Before optimizing RTL, preserve the failing vector or add a directed case that demonstrates the issue. Run the affected suite and lint. Rerun synthesis if the structure changed. Regenerate the measured report only after all required suites complete; do not present stale JSON as a new measurement.

The CI workflow uses the same make targets. A green workflow establishes these checks on that commit, not timing closure or exhaustive functional correctness.
