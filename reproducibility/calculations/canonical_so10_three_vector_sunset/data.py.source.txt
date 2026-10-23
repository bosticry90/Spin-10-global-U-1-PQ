"""V3A1 actual vector roles, complete matched functions and evidence IO."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
x,y,z,eps,d=s.symbols('x y z eps d',positive=True);M=[x,y,z];Hs=s.symbols('H0:5');AXES=['0','1','2'];J=s.Symbol('J',real=True);j=s.Symbol('j',real=True)
LOC={str(v):v for v in M+[eps,d,J,j,*Hs]}
def clean(v):return s.cancel(s.expand(v))
def expr(v):return s.sympify(v,locals=LOC)
def q(v):
    v=s.Rational(v);return mp.mpf(int(v.p))/int(v.q)
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def begin(prep='preparation.json'):
    start=time.perf_counter();watch=threading.Timer(600,lambda:os._exit(124));watch.daemon=True;watch.start()
    assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
    for p,h in json.loads((HERE/prep).read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    return start
def save(role,v,start):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
    with (HERE/f'{role}_tables.json.gz').open('xb') as f:f.write(blob)
    print('RESULT '+json.dumps({'role':role,'elapsed_after_imports':time.perf_counter()-start,'tables_sha256':sha256(raw).hexdigest(),
      'packed_sha256':sha256(blob).hexdigest(),'raw_bytes':len(raw),'packed_bytes':len(blob)},sort_keys=True),flush=True)
def num(v):return q(v) if s.sympify(v).is_Rational else mp.mpf(str(s.N(v,mp.mp.dps)))
def source(role):
    src=packed(CAL/'canonical_so10_ghost_vector_support'/f'{role}_tables.json.gz')
    if role=='primary':rows=packed(CAL/'canonical_so10_three_vector_support/primary_tables.json.gz')['rows']
    else:rows=[{'roles':[r['vector'],r['antighost_edge'],r['ghost_edge']],'norm':str(-expr(r['signed_raw'])),
      'charges':list(map(lambda v:str(-expr(v)),r['signed_charges_ideal_then_leg']))} for r in src['rows']]
    return list(map(expr,src['mass_coefficients'])),sorted(rows,key=lambda r:r['roles']),src
def weights(row):
    ww=list(map(expr,row['charges']));return [ww[3*i:3*i+3] for i in range(3)]
def kind(row):
    if expr(row['norm'])==0:return 'zero'
    k=row['roles'].count(0)
    if k==0:return 'positive'
    if k==1:return 'one_light'
    assert k==3;return 'all_light'
def canonical(roles):
    order=sorted(range(3),key=lambda k:roles[k]);return ','.join(str(roles[k]) for k in order),order
def hard_light(roles,masses):
    old=json.loads((CAL/'canonical_so10_three_vector_soft_matching/hard_forest_correction_receipt.json').read_bytes())
    assert old['status']=='QUALIFIED_CORRECTED_GAMMA_COMPLETE_ONE_LIGHT_THREE_VECTOR_HARD_FOREST'
    heavy=[masses[k] for k in roles if k];assert len(heavy)==2 and heavy[0]==heavy[1]
    key,order=canonical(roles);byaxis=[];cc=heavy[0]
    for i in range(3):
        slot=order.index(i);hh=old['axes'][str(slot)];finite=clean(expr(hh['hard_Rprime_scale'][2]).subs(j,J-s.log(cc)))
        pp1=clean(expr(hh['hard_Rprime_scale'][1]).subs(j,J-s.log(cc)))
        byaxis.append((num(finite.subs(J,0)),clean(finite.coeff(J,1)),clean(finite.coeff(J,2)),expr(hh['hard_Rprime_scale'][0]),clean(pp1.subs(J,0)),clean(pp1.coeff(J,1))))
    return tuple([v[k] for v in byaxis] for k in range(6))
class Units:
    def __init__(self,role):
        self.role=role;self.leak=mp.mpf(0);self.fallbacks=0
        self.master=load('v3a_cck_'+role,CAL/'canonical_so10_charged_current_kernel/data.py').finite_master_coefficients()
        bb=packed(CAL/'canonical_so10_three_vector_bare_kernel'/f'{role}_v3_tables.json.gz')['axes']
        ff=packed(CAL/'canonical_so10_three_vector_uv_forests'/f'{role}_tables.json.gz')['axes'];self.forms=[]
        for i in range(3):
            b=list(map(expr,bb[str(i)]['bare_Laurent_Q1']));f=list(map(expr,ff[str(i)]['forest_Laurent_Q1']))
            val=clean(b[2]+f[2]);tokens=sorted(val.free_symbols-set(M),key=str);assert all(str(v).startswith('I') for v in tokens)
            self.forms.append((s.lambdify([*M,*tokens],val,modules='mpmath',cse=True),tokens,clean(2*b[1]+f[1]),clean(2*b[0]+f[0]/2),clean(b[0]+f[0]),clean(b[1]+f[1])))
        self.tokens=sorted(set().union(*(set(v[1]) for v in self.forms)),key=str);self.derivatives={}
        if role=='primary':
            p=CAL/'canonical_so10_r3_scalar_current';raw=gzip.decompress((p/'analytic_derivatives_v10_tables.json.gz').read_bytes())
            assert sha256(raw).hexdigest()==json.loads((p/'backend_receipt_v10.json').read_bytes())['tables_sha256'];tab=json.loads(raw);II=s.Symbol('Ifin',positive=True)
            for token in self.tokens:
                pair=tab['functions'][str(token)[1:]];v=expr(pair[0])*II+expr(pair[1]);self.derivatives[token]=s.lambdify([*M,II],v,modules='mpmath',cse=True)
    def value(self,masses):
        mm=list(map(q,masses));xx,yy,zz=mm;lam=xx*xx+yy*yy+zz*zz-2*(xx*yy+xx*zz+yy*zz)
        guard=abs(lam)/(1+xx+yy+zz)**2<=mp.mpf('1e-20');self.fallbacks+=int(guard)
        base=self.master.sunset(*mm,q2=1,method='dilog') if self.role=='primary' and not guard else None;values={}
        for token in self.tokens:
            vv=self.derivatives[token](*mm,base) if self.role=='primary' and not guard else self.master.imaster_derivative(tuple(map(str,mm)),tuple(map(int,str(token)[1:])));self.leak=max(self.leak,abs(mp.im(vv))/(1+abs(vv)));values[token]=mp.re(vv)
        ff=[];sc1=[];sc2=[];pp2=[];pp1=[];sub=dict(zip(M,masses))
        for fun,tokens,a,b,c,e in self.forms:
            vv=fun(*mm,*[values[t] for t in tokens]);self.leak=max(self.leak,abs(mp.im(vv))/(1+abs(vv)));ff.append(mp.re(vv))
            sc1.append(clean(a.subs(sub)));sc2.append(clean(b.subs(sub)));pp2.append(clean(c.subs(sub)));pp1.append(clean(e.subs(sub)))
        return ff,sc1,sc2,pp2,pp1,[s.S.Zero]*3
def full_forest(row,masses):
    roles=row['roles'];ms=[d,*masses[1:]];ww=weights(row);full=[];soft=[]
    for ws in ww:
        vv=0;ss=0
        for k,slot in enumerate(roles):
            mass=ms[slot];other=sum(ms[r] for i,r in enumerate(roles) if i!=k)
            term=ws[k]*Hs[slot]*(-24/eps+R(67,6)+15*other/mass+eps*(R(19,18)+3*other/(2*mass)))/2
            vv+=term
            if slot==0:ss+=term
        full.append(clean(vv));soft.append(clean(ss))
    return full,soft
R=s.Rational
