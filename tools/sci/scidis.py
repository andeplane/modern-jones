import struct, sys, os, glob
R=sys.argv[1]; OUT=sys.argv[2]
def rd(f): return open(os.path.join(R,f),'rb').read()
k=rd('vocab.999').split(b'\0'); KERNEL=[x.decode('latin1') for x in k]
v=rd('vocab.997'); n=struct.unpack_from('<H',v,0)[0]; SEL=[]
for i in range(n+1):
    o=struct.unpack_from('<H',v,2+i*2)[0]
    if o+2>len(v): SEL.append('sel%d'%i); continue
    l=struct.unpack_from('<H',v,o)[0]; SEL.append(v[o+2:o+2+l].decode('latin1'))
def sel(i): return SEL[i] if 0<=i<len(SEL) else 'sel_%d'%i
OPS=['bnot','add','sub','mul','div','mod','shr','shl','xor','and','or','neg','not','eq?','ne?','gt?','ge?','lt?','le?','ugt?','uge?','ult?','ule?','bt','bnt','jmp','ldi','push','pushi','toss','dup','link','call','callk','callb','calle','ret','send','op38','op39','class','op41','self','super','&rest','lea','selfID','op47','pprev','pToa','aTop','pTos','sTop','ipToa','dpToa','ipTos','dpTos','lofsa','lofss','push0','push1','push2','pushSelf','op63']
VT='gltp'
# operand spec: list of 'W' (word/byte by flag), 'B' (byte always), 'w' (word always)
SPEC={'bt':'W','bnt':'W','jmp':'W','ldi':'W','pushi':'W','link':'W','call':'WB','callk':'WB','callb':'WB','calle':'WWB','send':'B','class':'W','self':'B','super':'WB','&rest':'W','lea':'WW','lofsa':'w','lofss':'w'}
for o in range(49,57): SPEC[OPS[o]]='W'
def blocks(d):
    p=0
    while p+4<=len(d):
        t,s=struct.unpack_from('<HH',d,p)
        if t==0: break
        yield t,p,s; p+=s
def strat(d,o):
    e=d.find(b'\0',o); return d[o:e].decode('latin1') if e>=0 else ''
def dis(d,start,end,labels,strings):
    out=[];p=start
    while p<end:
        b=d[p]; op=b>>1; bw=b&1; q=p+1
        if op<64: name=OPS[op]; spec=SPEC.get(name,'')
        else:
            t=op&3; s=op&4; idx=op&8; kind=(op>>4)&3
            name=['l','s','+','-'][kind]+('s' if s else 'a')+VT[t]+('i' if idx else ''); spec='W'
        args=[]
        for c in spec:
            if c=='B' or (c=='W' and bw): args.append(d[q] if q<len(d) else 0); q+=1
            else: args.append(struct.unpack_from('<H',d,q)[0] if q+1<len(d) else 0); q+=2
        cm=''
        if name in('bt','bnt','jmp','call'):
            a=args[0]
            if bw: a=a-256 if a>127 else a
            else: a=a-65536 if a>32767 else a
            tgt=q+a; args[0]='L%04x'%tgt; labels.add(tgt)
        elif name=='callk': cm=KERNEL[args[0]] if args[0]<len(KERNEL) else '?'
        elif name in('pushi','ldi'):
            a=args[0]
            if name=='ldi' and not bw and a>32767: a-=65536
            nb=d[q]>>1 if q<len(d) else 0
            if name=='pushi' and 0<=args[0]<len(SEL) and nb in (59,60,61,62,28,27,0x2c,0x3e) : cm='sel:'+sel(args[0])
            args[0]=a
        elif name in('pToa','aTop','pTos','sTop','ipToa','dpToa','ipTos','dpTos') and CUR[0] is not None:
            vs=CLASSES.get(CUR[0],(None,()))[1]; i=args[0]//2
            if i<len(vs): cm='prop:'+sel(vs[i])
        elif name=='class': cm=CLASSES.get(args[0],('?',))[0]
        elif name=='super': cm=CLASSES.get(args[0],('?',))[0]
        elif name in('lofsa','lofss'):
            a=args[0]; a=a-65536 if a>32767 else a; tgt=(q+a)&0xffff
            st=strings.get(tgt)
            cm=('"%s"'%st) if st is not None else ('obj@%04x'%tgt)
            args[0]='%04x'%tgt
        out.append((p,'  %-8s %s%s'%(name,', '.join(str(x) for x in args),('   ; '+cm) if cm else '')))
        p=q
        if name=='ret' and False: break
    return out
os.makedirs(OUT,exist_ok=True)
CLASSES={}
for f in sorted(glob.glob(os.path.join(R,'script.*'))):
    d=open(f,'rb').read()
    strs={}
    for t,p,s_ in blocks(d):
        if t==5:
            o=p+4
            while o<p+s_:
                st=strat(d,o); strs[o]=st; o+=len(st)+1
    for t,p,s_ in blocks(d):
        if t==6:
            b=p+4; magic,lofs,fofs,nv=struct.unpack_from('<HHHH',d,b)
            vals=struct.unpack_from('<%dH'%nv,d,b+8); vs=struct.unpack_from('<%dH'%nv,d,b+8+nv*2)
            CLASSES[vals[0]]=(strs.get(vals[3],'?'),vs)
CUR=[None]
for f in sorted(glob.glob(os.path.join(R,'script.*'))):
    num=int(f.split('.')[-1]); d=open(f,'rb').read(); lines=[]
    strings={}; objs=[]; codes=[]; exports=[]; methods={}
    for t,p,s in blocks(d):
        if t==5:
            o=p+4
            while o<p+s:
                st=strat(d,o); strings[o]=st; o+=len(st)+1
    for t,p,s in blocks(d):
        if t in (1,6):
            b=p+4; magic,lofs,fofs,nv=struct.unpack_from('<HHHH',d,b)
            vals=struct.unpack_from('<%dH'%nv,d,b+8)
            fa=b+6+fofs if False else b+4+fofs+2  # adjust below
            # find func area: SCI0: funcSelector offset is relative to its own location (b+4)
            fa=b+6+fofs
            vsel=None
            if t==6: vsel=struct.unpack_from('<%dH'%nv,d,b+8+nv*2)
            nm=struct.unpack_from('<H',d,fa)[0]
            msel=struct.unpack_from('<%dH'%nm,d,fa+2); moff=struct.unpack_from('<%dH'%nm,d,fa+4+nm*2)
            objs.append((t,b,vals,vsel,list(zip(msel,moff))))
            for ms,mo in zip(msel,moff): methods[mo]=(b,sel(ms))
        elif t==2: codes.append((p+4,p+s))
        elif t==7:
            ne=struct.unpack_from('<H',d,p+4)[0]; exports=list(struct.unpack_from('<%dH'%ne,d,p+6))
        elif t==10: lines.append('LOCALS @%04x: %s'%(p+4, list(struct.unpack_from('<%dh'%((s-4)//2),d,p+4))))
    objname={}
    for t,b,vals,vsel,ms in objs:
        objname[b+8]=strings.get(vals[3], '?')  # name at index 3
    lines.insert(0,'SCRIPT %d  exports=%s'%(num,['%04x'%e for e in exports]))
    for t,b,vals,vsel,ms in objs:
        nm=strings.get(vals[3],'?') if len(vals)>3 else '?'
        lines.append('%s %s @%04x species=%d super=%d'%('CLASS' if t==6 else 'OBJECT',nm,b+8,vals[0],vals[1]))
        if vsel: lines.append('   props: '+', '.join('%s=%d'%(sel(a),bv) for a,bv in zip(vsel,vals)))
        else:
            cv=CLASSES.get(vals[0],('?',()))
            lines.append('   (%s) props: '%cv[0]+', '.join(('%s=%r'%(sel(a),strings[bv]) if (bv in strings and sel(a) in ('name','text','title')) else '%s=%d'%(sel(a),(bv-65536 if bv>32767 else bv))) for a,bv in zip(cv[1],vals) if sel(a) not in ('underBits','lsTop','lsLeft','lsBottom','lsRight','client','-oldPort-','keyMouseX','keyMouseY','offsetX','offsetY','said','species','superClass','-info-')) if cv[1] else '   propvals: '+str(list(vals)))
        lines.append('   methods: '+', '.join('%s@%04x'%(sel(a),o) for a,o in ms))
    labels=set(exports)|set(methods)
    allc=[]
    ostarts=sorted(methods)
    for a,e in codes:
        # split code by method starts so property names resolve
        cuts=[a]+[m for m in ostarts if a<m<e]+[e]
        for i in range(len(cuts)-1):
            m=cuts[i]
            if m in methods:
                ob=methods[m][0]; sp=[o for o in objs if o[1]==ob][0]
                CUR[0]=sp[2][0]
            elif i==0: CUR[0]=None
            allc+=dis(d,cuts[i],cuts[i+1],labels,strings)
    for p,l in allc:
        if p in methods: lines.append('\n;;; method %s::%s'%(objname.get(methods[p][0]+8,'?'),methods[p][1]))
        if p in exports: lines.append('\n;;; export #%d'%exports.index(p))
        if p in labels: lines.append('L%04x:'%p)
        lines.append(l)
    lines.append('\nSTRINGS:'); lines+=['  %04x: %r'%(k,v) for k,v in sorted(strings.items())]
    open(os.path.join(OUT,'script%03d.asm'%num),'w').write('\n'.join(lines))
print(len(SEL),'selectors',len(KERNEL),'kernels')
