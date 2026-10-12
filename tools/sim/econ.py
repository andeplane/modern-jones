import random, statistics as st
def tdiv(a,b):
    q=abs(a)//abs(b); return q if (a>=0)==(b>0) else -q
R=lambda lo,hi: random.randint(lo,hi)
class Idx:
    def __init__(s,risk): s.index=0; s.reading=100; s.risk=risk
    def step(s,crash,boom,arg):
        i=s.index; r=s.reading
        if crash:
            if i>-3: i=max(i-3,-3)
            else: i-=1
        elif boom:
            if i<3: i=min(i+3,3)
            else: i+=1
        high=2 if r<40 else (1 if r<70 else 0)
        low=2 if r>160 else (1 if r>130 else 0)
        t=R(-3-low,3+high)
        if t<i:
            i-=1; i=max(i,-3-low)
        elif t>i:
            i+=1; i=min(i,3+high)
        lr,ur=-3,3
        if i<0: lr=-3+2*i
        elif i>0: ur=3+2*i
        adj=R(lr,ur)
        if adj==lr: adj-=R(0,s.risk*abs(i))
        r=r+adj+tdiv(arg,3)
        if crash: r=tdiv(r*(16+crash),20)
        elif boom: r=tdiv(r*11,10)
        r=max(10,min(190,r))
        s.index=i; s.reading=r
def mult(r):
    t= r - tdiv((100-r)*2,3) if r<100 else r+tdiv((r-100)*2,3)
    return max(50,t)
def run(players=1,weeks=50,seeds=2000):
    out={k:[] for k in ['main','gds','gold','sil','pork','bc','pen']}; crashes=booms=0; turns=0
    for sd in range(seeds):
        random.seed(sd)
        main=Idx(4); inv=Idx(4); gds=Idx(4)
        com={'gold':Idx(2),'sil':Idx(2),'pork':Idx(4),'bc':Idx(1),'pen':Idx(10)}
        for w in range(1,weeks+1):
            for p in range(players):
                turns+=1
                crash=0;boom=0
                if main.reading>=80 and w>=4 and R(0,players*20)==0: crash=R(1,3)
                elif main.reading<=120: boom= R(0,players*30)==0
                crashes+= crash>0; booms+=boom
                main.step(crash,boom,0); inv.step(crash,boom,main.index); gds.step(crash,boom,main.index)
                for c in com.values(): c.step(crash,boom,inv.index)
                out['main'].append(main.reading); out['gds'].append(mult(gds.reading))
                for k,c in com.items(): out[k].append(mult(c.reading))
    print('players',players,'turns',turns,'crash/turn %.4f boom/turn %.4f'%(crashes/turns,booms/turns))
    for k,v in out.items():
        v=sorted(v); n=len(v)
        print(k,'p5',v[n//20],'p25',v[n//4],'med',v[n//2],'p75',v[3*n//4],'p95',v[19*n//20],'mean %.1f'%st.mean(v))
run(1); run(4)
def vol(seeds=2000,weeks=50):
    d={'gds':[], 'gold':[], 'pen':[]}
    for sd in range(seeds):
        random.seed(sd); main=Idx(4); inv=Idx(4); gds=Idx(4); g=Idx(2); p=Idx(10)
        prev=None
        for w in range(1,weeks+1):
            crash=0;boom=0
            if main.reading>=80 and w>=4 and R(0,20)==0: crash=R(1,3)
            elif main.reading<=120: boom=R(0,30)==0
            main.step(crash,boom,0); inv.step(crash,boom,main.index); gds.step(crash,boom,main.index); g.step(crash,boom,inv.index); p.step(crash,boom,inv.index)
            cur=(mult(gds.reading),mult(g.reading),mult(p.reading))
            if prev:
                for k,a,b in zip(d,cur,prev): d[k].append(abs(a-b))
            prev=cur
    for k,v in d.items(): v.sort(); print(k,'abs weekly change of multiplier: med',v[len(v)//2],'p90',v[9*len(v)//10],'mean %.1f'%st.mean(v))
vol()
