import struct, sys, os, collections
gd, out = sys.argv[1], sys.argv[2]
TYPES=['view','pic','script','text','sound','memory','vocab','font','cursor','patch','bitmap','palette','cdaudio','audio','sync','message','map','heap']
m=open(os.path.join(gd,'resource.map'),'rb').read()
ents=[]
for i in range(0,len(m)-5,6):
    rid,loc=struct.unpack_from('<HI',m,i)
    if rid==0xffff: break
    ents.append((rid>>11, rid&0x7ff, loc>>26, loc&0x3ffffff))
class BR:
    def __init__(s,d): s.d=d; s.p=0; s.buf=0; s.n=0
    def msb(s,k):
        while s.n<k:
            s.buf=(s.buf<<8)|(s.d[s.p] if s.p<len(s.d) else 0); s.p+=1; s.n+=8
        s.n-=k; v=(s.buf>>s.n)&((1<<k)-1); s.buf&=(1<<s.n)-1; return v
def lzw1(d,size,early):
    br=BR(d); res=bytearray(); dic={}; nb=9; cur=0x102; end=0x1ff; prev=None
    while len(res)<size:
        t=br.msb(nb)
        if t==0x101: break
        if t==0x100:
            nb=9;cur=0x102;end=0x1ff;dic={};prev=None;continue
        if t<0x100: s=bytes([t])
        elif t in dic: s=dic[t]
        elif t==cur and prev is not None: s=prev+prev[:1]
        else: raise ValueError('bad token')
        res+=s
        if prev is not None and cur<=end:
            dic[cur]=prev+s[:1]; cur+=1
            if (cur==end if early else cur>end) and nb<12:
                nb+=1; end=(end<<1)+1
        prev=s
    return bytes(res)
def huff(d,size):
    nn=d[0]; term=d[1]; nodes=d[2:2+nn*2]; br=BR(d[2+nn*2:]); res=bytearray()
    while len(res)<size:
        i=0
        while nodes[i*2+1]:
            if br.msb(1):
                nx=nodes[i*2+1]&0xf
                if nx==0:
                    res.append(br.msb(8)); break
                i+=nx
            else: i+=nodes[i*2+1]>>4
        else:
            res.append(nodes[i*2]); continue
    return bytes(res)
os.makedirs(out,exist_ok=True)
stats=collections.Counter()
vols={}
for t,n,v,o in ents:
    vf=vols.setdefault(v,open(os.path.join(gd,'resource.%03d'%v),'rb').read())
    rid,cs,ds,meth=struct.unpack_from('<HHHH',vf,o)
    data=vf[o+8:o+4+cs]
    name=TYPES[t]
    stats[(name,meth)]+=1
    if name not in ('script','text','vocab','memory','patch'): continue
    try:
        if meth==0: r=data
        elif meth==2:
            r=lzw1(data,ds,True)
            if len(r)!=ds: r=lzw1(data,ds,False)
        elif meth==1: r=huff(data,ds)
        else: continue
    except Exception as e:
        print('fail',name,n,meth,e); continue
    if len(r)!=ds: print('size mismatch',name,n,meth,len(r),ds)
    open(os.path.join(out,'%s.%03d'%(name,n)),'wb').write(r)
print(stats)
