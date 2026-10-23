"""S4A1 exact input support, full scalar spectrum and contraction tools."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
sys.path.insert(0,str(CAL/'canonical_so10_scalar_quartic_functional'))
sys.path.insert(0,str(CAL/'canonical_so10_finite_counterterm_insertion'))
from geometry_v2 import red,tidy,zero,w,QUAD,dec
from inputs import coeffs
spec=importlib.util.spec_from_file_location('s4a_wick',CAL/'canonical_so10_scalar_quartic_functional/data.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def begin(prep='preparation.json'):
    start=time.perf_counter();watch=threading.Timer(600,lambda:os._exit(124));watch.daemon=True;watch.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def save(role,value,start):
    raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'tables_sha256':sha256(raw).hexdigest(),
      'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def norm(M):return max([abs(z) for z in M] or [mp.mpf(0)])
def real(z):assert abs(mp.im(z))<mp.mpf('1e-80')*(1+abs(z));return mp.re(z)
def fmt(z):return mp.nstr(real(z),65)
def complex_fmt(z):return [mp.nstr(mp.re(z),65),mp.nstr(mp.im(z),65)]
def root_value(role):
    aa,bb,cc=[mp.mpf(str(s.N(z,mp.mp.dps+8))) for z in QUAD]
    r=(-bb+mp.sqrt(bb*bb-4*aa*cc))/(2*aa) if role=='primary' else -2*cc/(bb+mp.sqrt(bb*bb-4*aa*cc))
    assert mp.mpf('.00530')<r<mp.mpf('.00531');return r
@lru_cache(20000)
def number(z,root):
    a,b=s.expand(red(s.sympify(z,locals={'w':w}))).as_real_imag();v={w:s.Float(mp.nstr(root,mp.mp.dps+4),mp.mp.dps+4)}
    return mp.mpc(str(s.N(a.subs(v),mp.mp.dps+6)),str(s.N(b.subs(v),mp.mp.dps+6)))
def numeric(M,root):return mp.matrix([[number(str(v),root) for v in row] for row in M.tolist()])
def input_data(role):
    frame=packed(CAL/'canonical_so10_scalar_sm_frame'/f'{role}_tables.json.gz')
    cov=packed(CAL/'canonical_so10_scalar_quartic_covariance'/f'{role}_tables.json.gz')
    func=packed(CAL/'canonical_so10_scalar_quartic_functional'/f'{role}_tables.json.gz')
    fci=packed(CAL/'canonical_so10_finite_counterterm_insertion'/f'{role}_v3_tables.json.gz')
    cc=coeffs()[1];coefficients={}
    for name in F.physical_poly(func['kernels']):
        n,_,part=name.partition(':');coefficients[name]=s.im(cc[n]) if part=='im' else s.re(cc[n])
    polys=F.physical_poly(func['kernels']);charges=packed(CAL/'canonical_so10_scalar_quartic_charge_projection'/f'{role}_tables.json.gz')['class_values']
    blocks=[];counts=[0]*6
    for aa,b in enumerate(frame['blocks']):
        src=fci['blocks'][aa];H=dec(src['H']);proj=[dec(src['physical']),dec(src['soft']),*map(dec,src['gold_mass_projectors'])]
        for j,P in enumerate(proj):
            zero(P*P-P);zero(P-P.H);counts[j]+=b['dimension']*int(red(s.trace(P)))
            for Z in proj[:j]:zero(P*Z)
        zero(sum(proj,s.zeros(H.rows))-s.eye(H.rows));zero(H-H.H);zero(H*(s.eye(H.rows)-proj[0]))
        if role=='replay':
            HH=s.zeros(H.rows)
            for k,slot in enumerate(frame['slots']):
                name,_,part=slot.partition(':');c=s.im(cc[name]) if part=='im' else s.re(cc[name])
                HH+=c*dec(frame['parent_blocks'][aa][k])
            HH=tidy(HH);zero(H-HH);H=HH
        G=tidy(sum((s.sympify(lam)*P for lam,P in zip(fci['vector_mass_eigenvalues'],proj[2:])),s.zeros(H.rows)))
        zero(H*G);blocks.append({'H':H,'G':G,'P':proj,'definition':b})
    assert counts==[290,5,8,1,12,12]
    return frame,cov,polys,coefficients,charges,fci,blocks,counts
def form_values(matrices,cov,root,diagonal_only=False):
    vv=[]
    for slot in cov['slot_definitions']:
        i,j=slot['i'],slot['j'];vv.append(mp.mpc(0) if diagonal_only and i!=j else matrices[slot['block']][i,j])
    return [mp.fsum(number(c,root)*vv[k] for k,c in row) for row in cov['program']['forms']]
def spectrum(block,g2,lams,root,role):
    H=numeric(block['H'],root);G=numeric(block['G'],root);M=H+g2*G;m=M.rows
    P0=numeric(block['P'][1],root);z=int(red(s.trace(block['P'][1])));states=[]
    if role=='primary':
        ev,U=mp.eighe(M);assert all(abs(ev[i])<mp.mpf('1e-80') for i in range(z))
        for i in range(z,m):
            assert ev[i]>0;v=U[:,i];states.append((ev[i],v*v.H))
    else:
        rank=int(red(s.trace(block['P'][0])))
        if rank:
            P=numeric(block['P'][0],root);U,sv,V=mp.svd(P);ids=[i for i in range(m) if i<rank]
            assert all(abs(sv[i]-1)<mp.mpf('1e-80') for i in ids)
            assert all(abs(sv[i])<mp.mpf('1e-80') for i in range(rank,m))
            B=mp.matrix([[U[i,j] for j in ids] for i in range(m)]);assert norm(B*B.H-P)<mp.mpf('1e-80')
            W,T=mp.schur(B.H*H*B);assert max([abs(T[i,j]) for i in range(rank) for j in range(rank) if i!=j] or [0])<mp.mpf('1e-80')*(1+norm(H))
            for i in range(rank):
                ev=real(T[i,i]);assert ev>0;v=B*W[:,i];states.append((ev,v*v.H))
        for lam,P in zip(lams,block['P'][2:]):
            if int(red(s.trace(P))):states.append((g2*real(number(lam,root)),numeric(P,root)))
    A0=mp.zeros(m);A1=mp.zeros(m);R=mp.zeros(m);Pr=mp.zeros(m)
    for ev,P in states:
        assert norm(M*P-ev*P)<mp.mpf('1e-80')*(1+norm(M));Pr+=P;R+=P/ev
        A0+=ev*(1+mp.log(60/ev))*P;A1+=ev*P
    err=max(norm(Pr+P0-mp.eye(m)),norm(M*R-Pr),norm(A1-M))
    assert err<mp.mpf('1e-80')*(1+norm(M))
    return A0,A1,R,P0,err,min([ev for ev,P in states] or [mp.inf])
def pair_function(polys,coeff,root,role):
    weighted={name:[(i,j,number(str(c*coeff[name]),root)) for i,j,c in poly if c*coeff[name]!=0] for name,poly in polys.items()}
    def parts(A,B):
        out={}
        for name,poly in weighted.items():
            if role=='primary':v=4*mp.fsum(c*(A[i]*B[j]+A[j]*B[i]) for i,j,c in poly)
            else:
                g=[mp.mpc(0)]*356
                for i,j,c in poly:g[i]+=c*A[j];g[j]+=c*A[i]
                v=4*mp.fsum(u*v for u,v in zip(g,B))
            out[name]=real(v)
        return out
    def pair(A,B):return mp.fsum(parts(A,B).values())
    return pair,parts
