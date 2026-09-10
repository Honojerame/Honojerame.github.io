"""Portfolio case studies backed by the checked-in RTL verification results."""
import json
from pathlib import Path
BASE='https://github.com/Honojerame/Honojerame.github.io/tree/main/engineering'
ROOT=Path(__file__).resolve().parents[1]/'engineering'
RESULTS={name:json.loads((ROOT/'results'/f'{name}.json').read_text()) for name in ('cpu','systolic','memory','noc')}

ENGINEERING=[
 dict(slug='rv32-cluster',title='Four-Core RV32I Cluster',category='CPU architecture / RTL',kind='cpu',folder='01_rv32_cluster',
      stack=['SystemVerilog','RV32I','Pipeline design','Python verification'],
      description='Four five-stage integer pipelines sharing a memory port, with forwarding, hazard control, precise terminal traps, and architectural trace verification.',
      overview='A processor must preserve the meaning of a program while instructions overlap and memory takes an unpredictable amount of time. This project makes that correctness problem visible across four independent RISC-V integer pipelines.',
      approach='Each hart uses IF, ID, EX, MEM, and WB stages. Forwarding handles arithmetic dependencies, a load-use interlock inserts bubbles, and branch resolution flushes younger work. A locked round-robin arbiter serializes shared-memory transactions without changing a stalled request.',
      contributions=['Implemented the RV32I integer datapath, subword loads and stores, branch/jump control, and a hard-wired zero register.','Preserved WB forwarding values when an older memory operation freezes EX; drained WB exactly once during stalls.','Added terminal illegal-instruction, misalignment, ECALL, and EBREAK handling, including a younger-store squash check.','Built an independent Python instruction interpreter and compared every retirement event and every final byte of RAM.'],
      takeaway='Adding cores increases available compute, but does not create shared-memory bandwidth. With always-ready memory in seed 0, the single hart completes in 430 clocks; four contending harts complete in 508–511 clocks each. These are mixed-program completion times, not an application speedup benchmark.',
      note='An educational integer architecture study. No caches, coherence, atomics, interrupts, privileged runtime, or RISC-V compliance certification.',
      evidence=[('Program/core configurations','32'),('Retirement events compared',f"{RESULTS['cpu']['retirements_compared']:,}"),('Tested core counts','1 and 4'),('Generic synthesis','35,644 cells')],
      command='make cpu',metric='25,668',metric_label='retirement events checked'),
 dict(slug='systolic-int8',title='INT8 Systolic Accelerator',category='AI accelerator / dataflow',kind='systolic',folder='02_systolic_int8',
      stack=['SystemVerilog','INT8 / INT32','Systolic arrays','Dataflow'],
      description='An output-stationary MAC array with skewed operand delivery, tail masking, backpressured results, and measured fill-and-drain utilization.',
      overview='Peak arithmetic capacity tells only part of an accelerator’s story. This project explores how operands reach processing elements, where partial sums live, and how a finite tile uses a physical array.',
      approach='Signed INT8 operands move right and down through an N×N array while INT32 accumulators remain stationary. Row and column skew aligns each product. A descriptor sets reduction length and active shape; a ready/valid stream drains results in row-major order.',
      contributions=['Implemented signed multiply-accumulate processing elements and a parameterized nearest-neighbor array.','Built operand storage, descriptor validation, skew scheduling, active-shape masking, and stable result serialization.','Checked 2×2, 4×4, and 8×8 arrays against independent Python matrix products using random data and signed extrema.','Measured useful MACs, compute clocks, output stalls, and compute utilization with explicit transfer-time boundaries.'],
      takeaway='A full 4×4 tile with K=16 performs 256 useful MACs in 22 compute clocks: 72.73% of the physical compute slots. Preload and result transfer add further cost. Larger arrays need sufficiently large workloads to amortize fill and drain.',
      note='One resident tile. DMA, double buffering, quantization scaling, floating point, and a software compiler/runtime remain extension work.',
      evidence=[('Tile configurations','48'),('Matrix elements compared',f"{RESULTS['systolic']['outputs_compared']:,}"),('4×4, K=16 compute clocks','22'),('Compute utilization, same tile','72.73%')],
      command='make systolic',metric='1,344',metric_label='matrix elements checked'),
 dict(slug='warp-memory',title='GPU-Style Warp Memory',category='GPU memory / parallel systems',kind='memory',folder='03_warp_memory',
      stack=['SystemVerilog','SIMT memory','Coalescing','Banked storage'],
      description='Tagged sector coalescing and a banked scratchpad that expose the cost of strided accesses, broadcasts, conflicts, and out-of-order memory replies.',
      overview='The layout of a warp’s addresses can matter as much as its arithmetic. This project studies two complementary structures: a global-load coalescer and shared-memory banks with conflict replay.',
      approach='The coalescer groups active word addresses into 32-byte sectors, issues uniquely tagged requests, and gathers reordered replies into lane order. The scratchpad chooses one distinct word per bank per clock, broadcasts matching loads, and replays unresolved conflicts.',
      contributions=['Implemented lane masks, sector grouping, concurrent outstanding requests, response-tag tracking, and complete-warp assembly.','Built explicit storage banks with one write port per bank and deterministic same-word store behavior.','Checked contiguous, offset, strided, broadcast, empty, invalid, and random access patterns at 8 and 32 lanes.','Verified every lane value, sector count, and bank-service count against independent models under randomized timing.'],
      takeaway='Thirty-two contiguous aligned words require four sector requests; shifting the first address by one word requires five. A stride of eight words requires 32. The verification run observed 17 sector requests in flight and exercised reply reordering.',
      note='Original educational structures, not NVIDIA implementation details. One resident warp; no cache, TLB, DRAM controller, or CUDA execution engine.',
      evidence=[('Warp operations','948'),('Lane values compared',f"{RESULTS['memory']['lane_values_compared']:,}"),('Observed requests in flight','17'),('Tested scratchpad banks','4 / 8 / 16')],
      command='make memory',metric='18,096',metric_label='lane values checked'),
 dict(slug='mesh-noc',title='Mesh Network-on-Chip',category='Interconnect / computer architecture',kind='noc',folder='04_mesh_noc',
      stack=['SystemVerilog','XY routing','FIFO design','Performance analysis'],
      description='Buffered mesh routers with deterministic routing, fair output arbitration, stable grants under backpressure, and packet-level contention experiments.',
      overview='Compute units need a communication fabric that preserves data when traffic converges and consumers stall. This project builds a mesh from small, inspectable routers and measures the consequences of contention.',
      approach='Each five-port router buffers its inputs, routes in X before Y, and arbitrates independently for each output. A grant stays locked while stalled. The traffic environment injects unique packets and checks their exact identity, payload, destination, and delivery time.',
      contributions=['Implemented parameterized FIFOs, five-port routers, neighbor links, and non-wrapping mesh boundaries.','Added per-output round-robin arbitration with retained ownership during backpressure.','Ran uniform, complement, hotspot, and ring-destination workloads on 2×2, 3×2, and 3×3 meshes.','Checked packet conservation and integrity while measuring accepted-injection latency and finite-workload delivery rate.'],
      takeaway='A hotspot can dominate network behavior even when most links are lightly used. In the selected 3×3 experiment, mean accepted-packet latency rises from 8.448 clocks for uniform traffic to 67.872 for hotspot traffic under the same offer and sink settings.',
      note='Single-flit packets and one clock domain. No virtual channels, wormhole routing, formal deadlock proof, or steady-state saturation claim.',
      evidence=[('Traffic experiments','48'),('Packets checked',f"{RESULTS['noc']['packets_checked']:,}"),('Tested mesh sizes','2×2 / 3×2 / 3×3'),('Routing','Deterministic XY')],
      command='make noc',metric='33,120',metric_label='packets checked'),
]
for project in ENGINEERING:
    project.update(repo=BASE+'/projects/'+project['folder'],year='2026',role='RTL implementation & verification',context='Independent architecture study',engineering=True)

def engineering_visual(kind,uid,accessible=False):
    descriptions={
      'cpu':'Four five-stage RV32I cores connect through a locked round-robin arbiter to shared memory.',
      'systolic':'A four-by-four processing-element array moves A operands right and B operands down while accumulating results.',
      'memory':'Four groups of eight contiguous lane words map to four aligned 32-byte sectors, with tagged replies.',
      'noc':'A three-by-three non-wrapping mesh connects routers horizontally and vertically.'}
    if kind=='cpu':
        body='<text class="svg-small" x="22" y="24">01 / PIPELINED INTEGER COMPUTE</text>'
        for i,x in enumerate((34,149,264,379)):
            body+=f'<rect x="{x}" y="49" width="86" height="62" rx="4"/><text class="svg-title" x="{x+43}" y="74" text-anchor="middle">RV32I</text><text class="svg-small" x="{x+43}" y="96" text-anchor="middle">HART {i}</text><path d="M{x+43} 111v25H250v19"/>'
        body+='<rect x="148" y="155" width="204" height="32" rx="3"/><text x="250" y="176" text-anchor="middle">ARBITER + SHARED MEMORY</text>'
        signal='M77 111v25H250v19 M422 111v25H250'
    elif kind=='systolic':
        body='<text class="svg-small" x="22" y="24">02 / OUTPUT-STATIONARY DATAFLOW</text><text class="svg-accent" x="76" y="111">A →</text><text class="svg-accent" x="361" y="111">Σ → C</text>'
        for r in range(4):
            for c in range(4):
                x=147+c*43;y=46+r*36
                body+=f'<rect x="{x}" y="{y}" width="26" height="24" rx="2"/>'
                if c<3:body+=f'<path d="M{x+26} {y+12}h17"/>'
                if r<3:body+=f'<path d="M{x+13} {y+24}v12"/>'
        body+='<path d="M111 94h36 M302 94h42"/><text class="svg-small" x="250" y="194" text-anchor="middle">INT8 × INT8 → INT32 / LOCAL ACCUMULATION</text>'
        signal='M111 94h36 M173 94h17 M216 94h17 M259 94h17 M302 94h42'
    elif kind=='memory':
        body='<text class="svg-small" x="22" y="24">03 / 32 LANES · ALIGNED CONTIGUOUS LOAD</text>'
        for i,x in enumerate((29,149,269,389)):
            body+=f'<rect x="{x}" y="51" width="82" height="35" rx="3"/><text x="{x+41}" y="73" text-anchor="middle">8 LANES</text><path d="M{x+41} 86v36"/><rect x="{x}" y="122" width="82" height="35" rx="3"/><text class="svg-accent" x="{x+41}" y="144" text-anchor="middle">32 B</text>'
        body+='<text class="svg-small" x="250" y="189" text-anchor="middle">COALESCE → TAG → GATHER REORDERED REPLIES</text>'
        signal='M70 86v36 M190 86v36 M310 86v36 M430 86v36'
    else:
        body='<text class="svg-small" x="22" y="24">04 / BUFFERED MESH FABRIC</text>'
        for r in range(3):
            for c in range(3):
                x=160+c*90;y=52+r*49
                body+=f'<rect x="{x-15}" y="{y-13}" width="30" height="26" rx="3"/>'
                if c<2:body+=f'<path d="M{x+15} {y}h60"/>'
                if r<2:body+=f'<path d="M{x} {y+13}v23"/>'
        body+='<text class="svg-small" x="250" y="193" text-anchor="middle">XY ROUTING / INPUT FIFOS / LOCKED GRANTS</text>'
        signal='M175 52h60 M265 52h60 M340 65v23 M340 114v23'
    attrs=f'role="img" aria-labelledby="{uid}-title"' if accessible else 'aria-hidden="true"'
    title=f'<title id="{uid}-title">{descriptions[kind]}</title>' if accessible else ''
    pulse='' if accessible else f'<path class="card-signal" d="{signal}" pathLength="100"/>'
    return f'<div class="project-visual"><svg class="project-svg" viewBox="0 0 500 210" {attrs}>{title}{body}{pulse}</svg></div>'
