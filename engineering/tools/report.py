"""Generate readable results from simulator-produced JSON, never invented benchmarks."""
import json,hashlib
from common import ROOT,RESULTS
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])+'\n'
def main():
    d={name:json.loads((RESULTS/(name+'.json')).read_text()) for name in ('cpu','systolic','memory','noc')}
    total=sum(x['tests'] for x in d.values())
    text=['# Measured RTL results','Generated from the checked-in JSON by `make report`. Run `make test`, `make lint`, and `make synth` first to produce new evidence. The reference simulation tool is Icarus Verilog 12.0; exact randomized cycle counts can vary with simulator versions.',
    table(['Suite','Cases / operations','Compared evidence'],[
      ['RV32 cluster',d['cpu']['tests'],f"{d['cpu']['retirements_compared']:,} retirement events + complete final RAM"],
      ['INT8 systolic',d['systolic']['tests'],f"{d['systolic']['outputs_compared']:,} matrix elements"],
      ['Warp memory',d['memory']['tests'],f"{d['memory']['lane_values_compared']:,} lane values"],
      ['Mesh NoC',d['noc']['tests'],f"{d['noc']['packets_checked']:,} packets"]]),f'**Total: {total:,} cases/operations.** These counts are different test units, not a coverage percentage.',
      '## CPU: contention is visible','The table shows seed 0 with memory ready on every clock. Every hart executes a private-data version of the same mixed instruction stream. These are full program completion clocks, including pipeline startup, redirects, and terminal trap drain; this is not an application speedup benchmark.',
      table(['Cores','Hart','Cycles','Retired','Memory wait clocks','Load-use bubbles','Redirects'],[[case['cores'],m['core'],m['cycles'],m['retired'],m['memory_stalls'],m['load_stalls'],m['redirects']] for case in d['cpu']['cases'] if case['seed']==0 for m in case['cores_metrics']]),
      '## Systolic: useful work versus fill/drain','Full active tiles with K=16. Select the first matching measured case for each physical size. Preload and result-drain time are excluded from compute utilization.',
      table(['Array','K','Useful MACs','Compute clocks','Compute utilization'],[[f'{n}×{n}',m['k'],m['useful_macs'],m['compute_cycles'],f"{100*m['array_utilization']:.2f}%"] for n in (2,4,8) for m in [next(x for x in d['systolic']['cases'] if x['n']==n and x['k']==16 and x['rows']==n and x['cols']==n)]]),
      'The larger physical array spends a larger fraction of this short reduction filling and draining. This is an inference from the schedule and measurements, not a claim that larger arrays are always slower.',
      '## Global loads: same warp, different transaction count',
      table(['Active lanes','Stride (words)','Offset (words)','Sector requests','ACTIVE clocks'],[[m['active_lanes'],m['parameter'],m['offset_words'],m['sectors'],m['latency_cycles']] for m in d['memory']['coalescer_cases'] if m['lanes']==32 and m['pattern']=='stride' and (m['parameter'] in (0,1,8,32)) and (m['offset_words']==0 or m['parameter']==1)]),
      f"The response model observed **{d['memory']['max_sector_requests_outstanding_observed']} concurrent outstanding requests** and **{d['memory']['out_of_order_response_pairs_observed']:,} out-of-order response pairs**. A pair counts an older outstanding request bypassed by a younger response; several pairs can arise from one response.",
      '## Scratchpad: distinct words determine conflict cost',
      table(['Lanes','Banks','Stride (words)','Service clocks'],[[m['lanes'],m['banks'],m['parameter'],m['service_cycles']] for m in d['memory']['scratchpad_cases'] if m['lanes']==32 and m['banks']==8 and m['pattern']=='stride']),
      'Repeated addresses broadcast within a service round. Stride wraps modulo 256 words in this experiment, so some large strides repeat addresses; the table must not be interpreted as an unbounded address stream.',
      '## Mesh: contention and endpoint service','Selected depth-4 experiments at 60% source offer probability and 70% random sink readiness, with forced sink progress every eighth clock. Mean/max latency begins at accepted injection. Delivery rate includes finite-workload drain.',
      table(['Mesh','Pattern','Packets','Total clocks','Mean latency','Max latency','Packets / node / clock'],[[f"{m['nx']}×{m['ny']}",['Uniform','Complement','Hotspot','Ring'][m['pattern']],m['packets'],m['cycles'],m['mean_latency'],m['max_latency'],m['accepted_packets_per_node_cycle']] for m in d['noc']['cases'] if m['depth']==4 and m['rate']==60 and m['pattern'] in (0,2)]),
      'Hotspot delivery is limited by the destination and its backpressure. These are seeded finite runs without confidence intervals; they do not establish a saturation throughput curve.',
      '## Structural checks']
    lint=json.loads((RESULTS/'lint.json').read_text());synth=json.loads((RESULTS/'synth.json').read_text())
    text += [f"Verilator lint passed for {len(lint['tops'])} top levels with the documented waivers. Yosys `synth -noabc` and `check -assert` completed for all five default top-level configurations.",table(['Top','Generic cells','Wire bits'],[[m['top'],m['generic_cells'],m['wire_bits']] for m in synth['tops']]),'Generic counts include lowered storage and are not technology-mapped area, FPGA LUTs, timing, or power. They should not be compared directly between unrelated architectures as a quality ranking. Full synthesis transcripts are in `results/synth_*.log.gz`.',
      '## Source identity','[source-manifest.json](../results/source-manifest.json) records SHA-256 hashes of RTL, testbenches, and Python tools present when this report was generated. A manifest is provenance, not a substitute for rerunning verification after edits.',
      'See [verification methodology](verification-methodology.md) and each project verification guide for assumptions and untested cases.']
    (ROOT/'docs/results.md').write_text('\n\n'.join(text)+'\n')
    files=sorted(p for folder in ('projects','tools') for p in (ROOT/folder).rglob('*') if p.suffix in ('.sv','.py'))
    (RESULTS/'source-manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
    print(f'Report generated from {total} measured cases/operations.')
if __name__=='__main__':main()
