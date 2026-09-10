"""Instruction-level differential verification, independent of pipeline timing."""
import random, re
from common import BUILD, compile_sv, simulate, save_result

MASK = 0xffffffff
def sx(v,b): return (v & ((1<<(b-1))-1)) - (v & (1<<(b-1)))
def I(op,rd,f3,rs,imm): return ((imm&4095)<<20)|(rs<<15)|(f3<<12)|(rd<<7)|op
def R(rd,f3,a,b,f7=0): return (f7<<25)|(b<<20)|(a<<15)|(f3<<12)|(rd<<7)|0x33
def S(f3,a,b,imm): return ((imm&0xfe0)<<20)|(b<<20)|(a<<15)|(f3<<12)|((imm&31)<<7)|0x23
def B(f3,a,b,off):
    return ((off&0x1000)<<19)|((off&0x7e0)<<20)|(b<<20)|(a<<15)|(f3<<12)|((off&0x1e)<<7)|((off&0x800)>>4)|0x63
def J(rd,off): return ((off&0x100000)<<11)|(off&0xff000)|((off&0x800)<<9)|((off&0x7fe)<<20)|(rd<<7)|0x6f

def program(seed, ending=0):
    r=random.Random(seed)
    # Each hart owns 256 bytes. a0 is initialized by reset to the hart index.
    p=[I(0x13,1,1,10,8),I(0x13,1,0,1,1024)]
    for rd in range(2,32):
        if rd!=10:p += [I(0x13,rd,0,0,r.randrange(-2048,2048))]
    p += [0x812342b7,0x00001317]  # LUI, AUIPC
    # Directed signed shift, forwarding, byte lanes, sign extension, load-use.
    p += [I(0x13,2,0,0,-128),S(2,1,2,0),I(3,3,0,1,0),R(4,0,3,2),
          I(3,5,4,1,0),S(0,1,5,3),I(3,6,1,1,2),I(3,7,5,1,2),
          I(0x13,8,5,2,0x403),I(0x13,9,5,2,3),R(11,5,2,5,0x20)]
    for _ in range(180):
        rd=r.choice([x for x in range(2,32) if x!=10]);a=r.randrange(32);b=r.randrange(32)
        choice=r.randrange(5)
        if choice==0:
            f=r.randrange(8);f7=r.choice([0,0x20]) if f in (0,5) else 0;p.append(R(rd,f,a,b,f7))
        elif choice==1:
            f=r.randrange(8);v=r.randrange(-2048,2048)
            if f in (1,5):v=r.randrange(32)|(r.choice([0,0x400]) if f==5 else 0)
            p.append(I(0x13,rd,f,a,v))
        elif choice==2:
            f=r.choice([0,1,2]);off=r.randrange(0,64)//(1<<f)*(1<<f);p.append(S(f,1,b,off))
        elif choice==3:
            f=r.choice([0,1,2,4,5]);size={0:1,1:2,2:4,4:1,5:2}[f];off=r.randrange(64)//size*size
            p += [I(3,rd,f,1,off),R(rd,0,rd,b)]
        else:
            p += [B(r.choice([0,1,4,5,6,7]),a,b,8),I(0x13,rd,0,rd,1)]
    # A counted loop exercises negative branch offsets and repeated retirement PCs.
    p += [I(0x13,20,0,0,12),I(0x13,21,0,0,0),R(21,0,21,20),I(0x13,20,0,20,-1),B(1,20,0,-8)]
    p += [J(22,8),I(0x13,21,0,0,999)]
    dest=(len(p)+3)*4
    p += [I(0x13,23,0,0,dest),I(0x67,24,0,23,0),I(0x13,21,0,0,888)]
    p += [S(2,1,21,128),0x0ff0000f,I(0x13,0,0,0,123)]
    p += [[0x73],[I(3,3,2,1,1)],[S(2,1,2,2)],[0xffffffff],[J(0,2)],[0x00100073]][ending]
    p += [S(2,1,2,132)]  # Must be squashed after every terminal trap.
    return p

def reference(p,hart,mem):
    regs=[0]*32;regs[10]=hart;pc=0;trace=[]
    for _ in range(10000):
        ins=p[pc//4] if pc//4<len(p) else 0x73
        op=ins&127;rd=(ins>>7)&31;f=(ins>>12)&7;a=regs[(ins>>15)&31];b=regs[(ins>>20)&31];f7=ins>>25
        imm=sx(ins>>20,12);nextpc=pc+4;val=0;write=False;cause=None
        if op==0x37: val=ins&0xfffff000;write=True
        elif op==0x17: val=pc+(ins&0xfffff000);write=True
        elif op in (0x13,0x33):
            rhs=imm&MASK if op==0x13 else b;shift=rhs&31;write=True
            if f==0:val=a-rhs if op==0x33 and f7==32 else a+rhs
            elif f==1:val=a<<shift
            elif f==2:val=int(sx(a,32)<sx(rhs,32))
            elif f==3:val=int(a<rhs)
            elif f==4:val=a^rhs
            elif f==5:val=sx(a,32)>>shift if f7==32 else a>>shift
            elif f==6:val=a|rhs
            else:val=a&rhs
        elif op in (3,0x23):
            off=imm if op==3 else sx(((ins>>25)<<5)|((ins>>7)&31),12)
            address=(a+off)&MASK;size=1<<(f&3)
            if address%size:cause=4 if op==3 else 6
            elif op==3:
                val=int.from_bytes(mem[address:address+size],'little');write=True
                if f<4:val=sx(val,size*8)
            else:mem[address:address+size]=(b&((1<<(8*size))-1)).to_bytes(size,'little')
        elif op==0x63:
            off=sx(((ins>>31)<<12)|(((ins>>7)&1)<<11)|(((ins>>25)&63)<<5)|(((ins>>8)&15)<<1),13)
            cond={0:a==b,1:a!=b,4:sx(a,32)<sx(b,32),5:sx(a,32)>=sx(b,32),6:a<b,7:a>=b}[f]
            if cond:nextpc=pc+off
        elif op==0x6f:
            off=sx(((ins>>31)<<20)|(ins&0xff000)|(((ins>>20)&1)<<11)|(((ins>>21)&1023)<<1),21)
            val=pc+4;write=True;nextpc=pc+off
        elif op==0x67:val=pc+4;write=True;nextpc=(a+imm)&0xfffffffe
        elif op==0xf:pass
        elif op==0x73:cause=11 if ins==0x73 else 3 if ins==0x100073 else 2
        else:cause=2
        if nextpc%4:cause=0
        actual_rd=rd if write and cause is None else 0
        trace.append((pc,ins,actual_rd,(val&MASK) if actual_rd else None,cause))
        if cause is not None:return trace
        if actual_rd:regs[rd]=val&MASK
        regs[0]=0;pc=nextpc&MASK
    raise AssertionError('reference timeout')

def main():
    rows=[];total_instructions=0
    for cores in (1,4):
        exe=compile_sv('01_rv32_cluster','tb_cluster',{'CORES':cores})
        for seed in range(16):
            ending=seed%6;p=program(seed,ending)
            name=f'cpu_c{cores}_s{seed}';hexfile=BUILD/(name+'.hex');tracefile=BUILD/(name+'.trace');memfile=BUILD/(name+'.mem')
            hexfile.write_text('\n'.join(f'{x:08x}' for x in p)+'\n')
            mem=bytearray().join((0x10203040+i).to_bytes(4,'little') for i in range(1024))
            expected=[reference(p,c,mem) for c in range(cores)]
            output=simulate(exe,PROGRAM=hexfile,TRACE=tracefile,MEMORY=memfile,SEED=seed+1,WAIT_MASK=(0 if seed==0 else 3 if seed%2 else 7))
            actual=[[] for _ in range(cores)]
            for line in tracefile.read_text().splitlines():
                c,pc,ins,rd,val,trap,cause=line.split();rd=int(rd)
                actual[int(c)].append((int(pc,16),int(ins,16),rd,int(val,16) if rd else None,int(cause) if int(trap) else None))
            for c in range(cores):
                assert len(actual[c])==len(expected[c]),(name,c,'retirement length',len(actual[c]),len(expected[c]))
                for j,(got,want) in enumerate(zip(actual[c],expected[c])):assert got==want,(name,c,j,got,want)
            words=[int(line,16) for line in memfile.read_text().splitlines() if not line.startswith('//')]
            gotmem=b''.join(x.to_bytes(4,'little') for x in words)
            assert gotmem==mem,(name,'final memory mismatch')
            metrics=[{k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',line)} for line in output.splitlines() if line.startswith('METRIC')]
            total_instructions+=sum(map(len,expected));rows.append({'cores':cores,'seed':seed,'terminal_cause':expected[0][-1][-1],'cores_metrics':metrics})
    save_result('cpu',{'tests':len(rows),'retirements_compared':total_instructions,'cases':rows})
if __name__=='__main__':main()
