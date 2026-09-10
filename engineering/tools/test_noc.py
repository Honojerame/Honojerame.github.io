import re
from common import BUILD,compile_sv,simulate,save_result
def main():
    cases=[];packets=0
    for nx,ny,depth in ((2,2,2),(2,2,4),(3,2,4),(3,3,4)):
        exe=compile_sv('04_mesh_noc','tb_mesh',{'NX':nx,'NY':ny,'DEPTH':depth})
        for pattern in range(4):
            for rate in (15,60,100):
                out=BUILD/f'noc_{nx}_{ny}_{depth}_{pattern}_{rate}.txt'
                log=simulate(exe,OUTPUT=out,SEED=100+pattern*7+rate,PATTERN=pattern,RATE=rate,SINK_RATE=(20 if rate==100 else 70))
                m={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',log)}
                rows=[list(map(int,l.split())) for l in out.read_text().splitlines()]
                assert len(rows)==nx*ny*120
                assert len({(src,seq) for src,seq,_,_ in rows})==len(rows)
                assert sum(r[3] for r in rows)==m['total_latency']
                m['mean_latency']=round(m['total_latency']/m['packets'],3)
                m['accepted_packets_per_node_cycle']=round(m['packets']/(nx*ny*m['cycles']),6)
                cases.append(m);packets+=len(rows)
    save_result('noc',{'tests':len(cases),'packets_checked':packets,'cases':cases})
if __name__=='__main__':main()
