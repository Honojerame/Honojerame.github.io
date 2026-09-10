import random,re
from common import BUILD,compile_sv,simulate,save_result

def main():
    cases=[];values=0
    for n in (2,4,8):
        exe=compile_sv('02_systolic_int8','tb_systolic',{'N':n})
        for seed in range(16):
            rng=random.Random(1700+seed);k=(1,2,7,16)[seed%4]
            rows=n if seed<8 else max(1,n-1);cols=n if seed%3 else max(1,n-1)
            a=[[rng.randrange(-128,128) for _ in range(16)] for _ in range(n)]
            b=[[rng.randrange(-128,128) for _ in range(n)] for _ in range(16)]
            if seed==0:a=[[-128]*16 for _ in range(n)];b=[[-128]*n for _ in range(16)]
            if seed==1:a=[[127]*16 for _ in range(n)];b=[[-128]*n for _ in range(16)]
            inp=BUILD/f'systolic_{n}_{seed}.hex';out=BUILD/f'systolic_{n}_{seed}.txt'
            inp.write_text('\n'.join(f'{v&255:02x}' for mat in (a,b) for row in mat for v in row)+'\n')
            output=simulate(exe,INPUT=inp,OUTPUT=out,K=k,ROWS=rows,COLS=cols,SEED=seed+1)
            got=[int(line.split()[1]) for line in out.read_text().splitlines()]
            expected=[sum(a[r][x]*b[x][c] for x in range(k)) if r<rows and c<cols else 0 for r in range(n) for c in range(n)]
            assert got==expected,(n,seed,got,expected)
            m={key:int(v) for key,v in re.findall(r'(\w+)=(\d+)',output)}
            assert m['compute_cycles']==k+2*n-2,m
            assert m['useful_macs']==rows*cols*k,m
            m['array_utilization']=round(rows*cols*k/(n*n*m['compute_cycles']),6)
            m['seed']=seed;cases.append(m);values+=len(got)
    save_result('systolic',{'tests':len(cases),'outputs_compared':values,'cases':cases})
if __name__=='__main__':main()
