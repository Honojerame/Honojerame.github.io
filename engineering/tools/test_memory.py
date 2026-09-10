import random,re
from common import BUILD,compile_sv,simulate,save_result
MASK=0xffffffff
def main():
    sectors_cases=[];bank_cases=[];comparisons=0;max_outstanding=0;reorder_pairs=0
    for lanes in (8,32):
        exe=compile_sv('03_warp_memory','tb_coalescer',{'LANES':lanes})
        cases=[];rng=random.Random(90210+lanes)
        for stride in (0,1,2,4,8,16,32):
            for offset in (0,1,7):cases.append(('stride',stride,[(offset+i*stride)*4 for i in range(lanes)],(1<<lanes)-1))
        for seed in range(60):
            a=[rng.randrange(1024)*4 for _ in range(lanes)];mask=rng.getrandbits(lanes)
            if seed==0:mask=0
            if seed==1:a[0]=3;mask|=1
            cases.append(('random',seed,a,mask))
        inp=BUILD/f'coalescer{lanes}.txt';out=BUILD/f'coalescer{lanes}.out'
        inp.write_text(str(len(cases))+'\n'+'\n'.join(f'{m:x} '+' '.join(f'{x:x}' for x in a) for _,_,a,m in cases)+'\n')
        log=simulate(exe,INPUT=inp,OUTPUT=out,SEED=lanes)
        max_outstanding=max(max_outstanding,int(re.search(r'max_outstanding=(\d+)',log)[1]));reorder_pairs+=int(re.search(r'reordered=(\d+)',log)[1])
        lines=out.read_text().splitlines();assert len(lines)==len(cases)
        for j,((kind,param,a,mask),line) in enumerate(zip(cases,lines)):
            fields=line.split();tag,err,sectors,active,latency=map(int,fields[:5]);got=[int(v,16) for v in fields[5:]]
            bad=any((x%4) and ((mask>>i)&1) for i,x in enumerate(a))
            want=[(0x9e3779b9^(((x>>2)*0x01010101)&MASK)) if ((mask>>i)&1) and not bad else 0 for i,x in enumerate(a)]
            expected_sectors=0 if bad else len({x//32 for i,x in enumerate(a) if (mask>>i)&1})
            assert (tag,err,sectors,active,got)==(j,int(bad),expected_sectors,mask.bit_count(),want),(lanes,j,line,want)
            comparisons+=lanes;sectors_cases.append({'lanes':lanes,'pattern':kind,'parameter':param,'offset_words':a[0]//4 if kind=='stride' else None,'sectors':sectors,'active_lanes':active,'latency_cycles':latency,'error':err})
        for banks in (4,8,16):
            exe=compile_sv('03_warp_memory','tb_scratchpad',{'LANES':lanes,'BANKS':banks})
            mem=[0]*256;ops=[];expected=[];meta=[]
            def add(store,a,v,mask,kind,param):
                bad=any(x>=256 and ((mask>>i)&1) for i,x in enumerate(a));got=[0]*lanes
                cycles=0 if bad else max([len({x for i,x in enumerate(a) if ((mask>>i)&1) and x%banks==b}) for b in range(banks)])
                if not bad:
                    for i,x in enumerate(a):
                        if (mask>>i)&1:
                            if store:mem[x]=v[i]
                            else:got[i]=mem[x]
                ops.append(f'{int(store)} {mask:x} '+' '.join(f'{x:x} {y:x}' for x,y in zip(a,v)))
                expected.append((int(bad),cycles,got));meta.append((kind,param))
            for base in range(0,256,lanes):add(True,list(range(base,base+lanes)),[rng.getrandbits(32) for _ in range(lanes)],(1<<lanes)-1,'initialize',base)
            for stride in (0,1,2,4,8,16,32):add(False,[(i*stride)%256 for i in range(lanes)],[0]*lanes,(1<<lanes)-1,'stride',stride)
            # Same-word stores, masks, random bank conflicts, empty and invalid requests.
            add(True,[3]*lanes,list(range(lanes)),(1<<lanes)-1,'collision',0)
            add(False,[3]*lanes,[0]*lanes,(1<<lanes)-1,'broadcast',0)
            add(False,[999]*lanes,[0]*lanes,1,'invalid',0)
            add(False,[999]*lanes,[0]*lanes,0,'empty',0)
            for j in range(100):add(j%3==0,[rng.randrange(256) for _ in range(lanes)],[rng.getrandbits(32) for _ in range(lanes)],rng.getrandbits(lanes),'random',j)
            inp=BUILD/f'scratchpad{lanes}_{banks}.txt';out=BUILD/f'scratchpad{lanes}_{banks}.out'
            inp.write_text(str(len(ops))+'\n'+'\n'.join(ops)+'\n');simulate(exe,INPUT=inp,OUTPUT=out,SEED=banks)
            lines=out.read_text().splitlines();assert len(lines)==len(expected)
            for j,(line,want,(kind,param)) in enumerate(zip(lines,expected,meta)):
                f=line.split();got=(int(f[0]),int(f[1]),[int(v,16) for v in f[2:]])
                assert got==want,(lanes,banks,j,got,want)
                comparisons+=lanes;bank_cases.append({'lanes':lanes,'banks':banks,'pattern':kind,'parameter':param,'service_cycles':got[1]})
    save_result('memory',{'tests':len(sectors_cases)+len(bank_cases),'lane_values_compared':comparisons,'max_sector_requests_outstanding_observed':max_outstanding,'out_of_order_response_pairs_observed':reorder_pairs,'coalescer_cases':sectors_cases,'scratchpad_cases':bank_cases})
if __name__=='__main__':main()
