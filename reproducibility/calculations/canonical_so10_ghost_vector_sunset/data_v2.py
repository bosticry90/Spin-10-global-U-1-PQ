"""GVA1 actual input roles, exact bookkeeping and absolute master interfaces."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,sys,time,threading,os,importlib.util
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
x,y,z,eps,d=s.symbols('x y z eps d',positive=True);M=[x,y,z];Hs=s.symbols('H0:5');AXES=['left','right','vector']
LOC={str(v):v for v in M+[eps,d,*Hs]}
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
def weights(row):
    w=list(map(expr,row['signed_charges_ideal_then_leg']));return [[w[3*i+1],w[3*i+2],w[3*i]] for i in range(3)]
def ids(row):return row['vector'],row['antighost_edge'],row['ghost_edge']
def source(role):return packed(CAL/'canonical_so10_ghost_vector_support'/f'{role}_tables.json.gz')
def kind(row):
    if expr(row['signed_raw'])==0:return 'zero'
    count=ids(row).count(0)
    if count==0:return 'positive'
    if count==1:return 'one_light'
    assert count==3;return 'all_light'
def key_of(row):
    r,a,b=ids(row);return f'{a},{b},{r}'
def canonical(row):
    r,a,b=ids(row);swap=a>b;return f'{min(a,b)},{max(a,b)},{r}',swap
def light_kernel(row,masses):
    r,a,b=ids(row);k=0 if r==0 else 1;soft=json.loads((CAL/'canonical_so10_ghost_vector_soft_kernel/validation_receipt.json').read_bytes())['kernels']
    data=soft['vector_light' if k==0 else 'ghost_light'];ff=list(map(expr,data['finite']));ss=list(map(expr,data['scale']))
    if b==0:ff[0],ff[1]=ff[1],ff[0];ss[0],ss[1]=ss[1],ss[0]
    heavy=[masses[v] for v in [r,a,b] if v!=0];assert heavy[0]==heavy[1]
    return [q(f)-q(b)*mp.log(q(heavy[0])) for f,b in zip(ff,ss)],ss
class Units:
    def __init__(self,role):
        self.role=role;self.leak=mp.mpf(0);self.fallbacks=0;old=load('gva_cck_'+role,CAL/'canonical_so10_charged_current_kernel/data.py');self.master=old.finite_master_coefficients()
        self.table=packed(CAL/'canonical_so10_ghost_vector_uv_forests'/f'{role}_tables.json.gz')['kernels'];self.forms={}
        for name in AXES:
            form=expr(self.table[name]['Rprime_finite_Q1']);tokens=sorted(form.free_symbols-set(M),key=str)
            self.forms[name]=(s.lambdify([*M,*tokens],form,modules='mpmath',cse=True),tokens)
        self.tokens=sorted(set().union(*(set(v[1]) for v in self.forms.values())),key=str);self.derivatives={}
        if role=='primary':
            p=CAL/'canonical_so10_r3_scalar_current';raw=gzip.decompress((p/'analytic_derivatives_v10_tables.json.gz').read_bytes())
            assert sha256(raw).hexdigest()==json.loads((p/'backend_receipt_v10.json').read_bytes())['tables_sha256'];tab=json.loads(raw)
            II=s.Symbol('Ifin',positive=True);loc={**LOC,'Ifin':II}
            for token in self.tokens:
                pair=tab['functions'][str(token)[1:]];f=s.sympify(pair[0],locals=loc)*II+s.sympify(pair[1],locals=loc)
                self.derivatives[token]=s.lambdify([*M,II],f,modules='mpmath',cse=True)
    def value(self,masses):
        mm=list(map(q,masses));xx,yy,zz=mm;lam=xx*xx+yy*yy+zz*zz-2*(xx*yy+xx*zz+yy*zz)
        guard=abs(lam)/(1+xx+yy+zz)**2<=mp.mpf('1e-20');self.fallbacks+=guard
        base=self.master.sunset(*mm,q2=1,method='dilog') if self.role=='primary' and not guard else None;values={}
        for token in self.tokens:
            vv=self.derivatives[token](*mm,base) if self.role=='primary' and not guard else self.master.imaster_derivative(tuple(map(str,mm)),tuple(map(int,str(token)[1:])))
            self.leak=max(self.leak,abs(mp.im(vv))/(1+abs(vv)));values[token]=mp.re(vv)
        ff=[];ss=[];pp=[]
        for name in AXES:
            fun,tokens=self.forms[name];vv=fun(*mm,*[values[t] for t in tokens]);self.leak=max(self.leak,abs(mp.im(vv))/(1+abs(vv)));ff.append(mp.re(vv))
            ss.append(clean(expr(self.table[name]['scale_j']).subs(dict(zip(M,map(s.Rational,masses))))))
            pp.append(expr(self.table[name]['Rprime_pole']))
        return ff,ss,pp
def full_forest(row,masses):
    r,a,b=ids(row);ms=[d,*masses[1:]];r0,a0,b0=ms[r],ms[a],ms[b]
    f=[-Hs[a]/3,-Hs[b]/3,Hs[r]*(-1-eps/9+(s.Rational(10,3)+eps/3)*(a0+b0)/r0)]
    soft=[v if slot==0 else s.S.Zero for slot,v in zip([a,b,r],f)];ww=weights(row)
    return [clean(s.Rational(3,4)*sum(w*v for w,v in zip(ws,f))) for ws in ww],[clean(s.Rational(3,4)*sum(w*v for w,v in zip(ws,soft))) for ws in ww]
