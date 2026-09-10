"""Structural lint and generic synthesis; no technology-specific PPA claims."""
import argparse,gzip,json,re,subprocess,time
from common import ROOT,BUILD,RESULTS,command,run
TOPS=[('01_rv32_cluster','rv32_cluster'),('02_systolic_int8','systolic_tile'),
      ('03_warp_memory','warp_coalescer'),('03_warp_memory','banked_scratchpad'),('04_mesh_noc','mesh_noc')]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['lint','synth']);args=parser.parse_args()
    rows=[]
    for project,top in TOPS:
        sources=[p.relative_to(ROOT) for p in sorted((ROOT/'projects'/project/'rtl').glob('*.sv'))]
        if args.mode=='lint':
            # Integer configuration/count ports deliberately share 32-bit host fields.
            cmd=command('verilator')+['--lint-only','-Wall','-Wno-WIDTH','-Wno-UNUSEDSIGNAL','-Wno-UNUSEDPARAM','-Wno-UNSIGNED','--top-module',top]+list(map(str,sources))
            log=run(cmd,cwd=ROOT)
            rows.append({'top':top,'status':'pass'})
        else:
            script='read_verilog -sv '+' '.join(map(str,sources))+f'; hierarchy -check -top {top}; synth -top {top} -noabc; check -assert; stat -json'
            log=run(command('yosys')+['-p',script],timeout=240,cwd=ROOT)
            if re.search(r'\$_(?:D?LATCH)',log):raise AssertionError(f'Latch in {top}')
            start=log.rfind('\n{');end=log.find('\n}',start)+2
            stats=json.loads(log[start:end]);design=stats.get('design',stats['modules'].get('\\'+top))
            rows.append({'top':top,'generic_cells':design['num_cells'],'wire_bits':design['num_wire_bits'],'cell_types':design['num_cells_by_type']})
        if args.mode=='synth':
            (RESULTS/f'synth_{top}.log.gz').write_bytes(gzip.compress(log.encode(),mtime=0))
        else:
            (RESULTS/f'lint_{top}.log').write_text(log)
        print(f'PASS {args.mode} {top}',flush=True)
    (RESULTS/(args.mode+'.json')).write_text(json.dumps({'mode':args.mode,'tops':rows},indent=2)+'\n')
if __name__=='__main__':main()
