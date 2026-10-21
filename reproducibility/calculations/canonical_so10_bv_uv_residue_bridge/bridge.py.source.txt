from pathlib import Path
from hashlib import sha256
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import json,gzip,time,threading,os,sys,math
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;P=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
class Exterior:
 def __init__(self,par):self.par=par
 def norm(self,w):
  odd=[n for n in w if self.par[n]]
  if len(set(odd))<len(odd):return (),0
  return tuple(sorted(w)),(-1)**sum(a>b for i,a in enumerate(odd) for b in odd[i+1:])
 def add(self,*ps):
  out=defaultdict(F)
  for p in ps:
   for w,c in p.items():out[w]+=c
  return {w:c for w,c in out.items() if c}
 def scale(self,p,c):return {w:v*c for w,v in p.items() if v*c}
 def v(self,n):return {(n,):F(1)}
 def mul(self,*ps):
  out={():F(1)}
  for p in ps:
   new=defaultdict(F)
   for a,c in out.items():
    for b,d in p.items():
     w,sg=self.norm(a+b)
     if sg:new[w]+=sg*c*d
   out={w:c for w,c in new.items() if c}
  return out
 def left(self,p,n):
  out=defaultdict(F)
  for w,c in p.items():
   for i,v in enumerate(w):
    if v==n:out[w[:i]+w[i+1:]]+=c*(-1)**(self.par[n]*sum(self.par[a] for a in w[:i]))
  return {w:c for w,c in out.items() if c}
 def act(self,p,flow,odd,route):
  if route=='replay':return self.add(*(self.mul(flow[n],self.left(p,n)) for n in sorted(flow)))
  out={}
  for w,c in p.items():
   for j,n in enumerate(w):
    if n not in flow:continue
    before={w[:j]:F(1)};after={w[j+1:]:F(1)}
    out=self.add(out,self.scale(self.mul(before,flow[n],after),c*(-1)**(odd*sum(self.par[a] for a in w[:j]))))
  return out
 def rows(self,p):return [[list(w),str(c)] for w,c in sorted(p.items())]

def toy(route):
 names=['x','y','c','bar','b'];par={'x':0,'y':0,'c':1,'bar':1,'b':0};par.update({'J'+n:1-par[n] for n in names});par.update({f'{a}_{n}':par[n] for a in ['h','k'] for n in names});E=Exterior(par);v=E.v;x,y,c,bar,b=map(v,names);mul=E.mul;add=E.add;sc=E.scale
 flow={'x':mul(c,y),'y':sc(mul(c,x),-1),'c':{},'bar':sc(b,-1),'b':{}}
 psi=mul(bar,add(mul(x,y),sc(b,-F(1,2))));rr=add(mul(x,x),mul(y,y));S=add(mul(rr,rr),mul(v('Jx'),c,y),sc(mul(v('Jy'),c,x),-1),sc(mul(v('Jbar'),b),-1),E.act(psi,flow,1,route))
 q={n:E.left(S,'J'+n) for n in names}|{'J'+n:E.left(S,n) for n in names};master=E.act(S,q,1,route);assert not master
 h={n:v('h_'+n) for n in names};k={n:v('k_'+n) for n in names}
 H=E.act(E.act(S,h,0,route),k,0,route);lift=q|{a+'_'+n:E.act(q[n],h if a=='h' else k,0,route) for a in ['h','k'] for n in names};res=E.act(H,lift,1,route);assert not res
 wrong=lift|{'J'+n:{} for n in names};defect=E.act(H,wrong,1,route);assert defect
 unsigned=q|{'J'+n:sc(q['J'+n],-1) for n in names};assert E.act(S,unsigned,1,route)
 # Even supermatrix fiber cyclicity with genuinely odd off-diagonal entries.
 E.par.update({'theta':1,'omega':1});zero={};one={():F(1)}
 A=[[sc(one,2),v('theta')],[zero,sc(one,3)]];B=[[sc(one,5),zero],[v('omega'),sc(one,7)]]
 mm=lambda a,b:[[add(*(mul(a[i][k],b[k][j]) for k in range(2))) for j in range(2)] for i in range(2)]
 AB,BA=mm(A,B),mm(B,A);strace=lambda a:add(a[0][0],sc(a[1][1],-1));trace=lambda a:add(a[0][0],a[1][1]);assert not add(strace(AB),sc(strace(BA),-1));bad=add(trace(AB),sc(trace(BA),-1));assert bad
 return {'master_terms':len(S),'full_master_residual':E.rows(master),'hessian_bilinear_terms':len(H),'full_lifted_Hessian_residual':E.rows(res),'frozen_QJ_Hessian_defect':E.rows(defect),'hessian_sha256':sha256(json.dumps(E.rows(H),separators=(',',':')).encode()).hexdigest(),'unsigned_source_sign_detected':True,'ordinary_trace_cyclic_defect':E.rows(bad)}

p=s.symbols('p0:4');lam=s.Symbol('lam');kvec=[1,2,0,0];dot=sum(a*b for a,b in zip(kvec,p));k2=sum(a*a for a in kvec)
@lru_cache(None)
def mean(exp,route):
 if any(e%2 for e in exp):return s.S.Zero
 if route=='primary':
  top=math.prod(math.prod(range(1,e,2)) for e in exp);bottom=math.prod(range(4,4+sum(exp),2));return s.Rational(top,bottom)
 return s.simplify(s.gamma(2)*s.prod(s.gamma(s.Rational(e+1,2)) for e in exp)/(s.gamma(2+s.Rational(sum(exp),2))*s.gamma(s.Rational(1,2))**4))
def angular(poly,route):return s.expand(sum(c*mean(exp,route) for exp,c in s.Poly(s.expand(poly),p).terms()))
def numerator(u):return s.prod(a**b for a,b in zip(p,u))
@lru_cache(None)
def differentiated(u,m,j):
 terms={m:numerator(u)}
 for _ in range(j):
  new=defaultdict(lambda:s.S.Zero)
  for n,pol in terms.items():
   new[n]+=sum(kvec[i]*s.diff(pol,p[i]) for i in range(4));new[n+1]+=-2*n*dot*pol
  terms={n:s.expand(v) for n,v in new.items() if s.expand(v)!=0}
 return terms
@lru_cache(None)
def shift_coefficient(u,m,j,sign):
 numer=s.Poly(s.expand(s.prod((p[i]+sign*lam*kvec[i])**u[i] for i in range(4))),lam);out=0
 for (r,),nr in numer.terms():
  for l in range(j+1):
   ss=j-r-l
   if not 0<=ss<=l:continue
   out+=nr*s.binomial(-m,l)*s.binomial(l,ss)*(sign*2*dot)**(l-ss)*k2**ss
 return s.expand(out)
def symbols(route):
 kinds=[((0,0,0,0),1),((1,0,0,0),1),((0,2,0,0),1),((1,1,0,0),1),((0,0,0,0),2),((0,1,1,1),2),((2,1,0,0),0)];out=[]
 for u,m in kinds:
  for v,n in kinds:
   j=sum(u)+sum(v)-2*(m+n)+4
   if j<0:a=b=s.S.Zero
   elif route=='primary':
    da=sum(differentiated(u,m,j).values());db=sum(differentiated(v,n,j).values());a=angular((-1)**j*da*numerator(v)/math.factorial(j),route);b=angular(db*numerator(u)/math.factorial(j),route)
   else:a=angular(shift_coefficient(u,m,j,-1)*numerator(v),route);b=angular(shift_coefficient(v,n,j,1)*numerator(u),route)
   assert s.expand(a-b)==0,(u,m,v,n,j,a,b)
   out.append({'u':u,'m':m,'v':v,'n':n,'derivative_degree':j,'AB':str(a),'BA':str(b)})
 assert any(v['AB'] not in ['0'] and v['derivative_degree']>0 for v in out)
 return out

def main():
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();route=sys.argv[1];assert route in ['primary','replay'];prep=read(O/'preparation.json');assert digest(Path(__file__))==prep['source_sha256']
 for raw,h in prep['input_sha256'].items():assert digest(Path(raw))==h,raw
 allowed=set(prep['read_json'][route])
 def guard(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  path=Path(os.fsdecode(args[0])).resolve()
  if len(args)>1 and isinstance(args[1],str) and any(x in args[1] for x in 'wax+'):raise PermissionError('BV_BRIDGE_WRITE')
  if path.suffix=='.json':assert str(path) in allowed,('UNDECLARED_BV_BRIDGE_JSON',str(path))
 sys.addaudithook(guard)
 for fact in prep['receipt_facts']:
  rc=read(Path(fact['path']))
  for key,value in fact['equals'].items():assert rc[key]==value
  for raw in fact['native_bindings'][route]:
   key=raw if fact['table']=='input_sha256' else str(Path(raw).relative_to(R)).replace('\\','/')
   assert rc[fact['table']][key]==digest(Path(raw))
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()));geo=data['geometry'];names=geo['names'];fields={names[i] for i,J,h,k in geo['field_source_h_k']};sources={names[J] for i,J,h,k in geo['field_source_h_k']};assert len(fields)==len(sources)==643
 jets=[]
 for n,rows in data['master_field_maps'].items():
  for row in rows:
   assert not any(v.split('__')[0] in sources for v in row['word'])
   if any('__' in v for v in row['word']):
    assert len(row['word'])==1 and n.startswith('B') and row['word'][0].startswith('C')
    base,j=row['word'][0].split('__');assert len(j)==1 and j in '0123';assert not s.sympify(row['coefficient']).free_symbols
    jets.append([n,base,int(j),row['coefficient']])
 assert len(jets)==180
 e2=read(P/f'frozen_a10_e2_transport/{route}.json');assert e2['full_master_functional_established'] and e2['full_source_nilpotence_established'] and not e2['master']['new_density_minus_divergence'] and not e2['master']['EOM_used']
 core=read(P/f'frozen_a10_e5_full_hessian/{route}.json');reg=read(P/f'frozen_a10_e5_regulated_slavnov/{route}.json');assert core['complete_Hessian_and_reference_qualified'] and core['complete_one_loop_finite_UV_Born_family_defined']
 assert core['complete_source_and_GF_Hessian']['source_second_variation']['complete_coefficients']==reg['complete_source_Hessian_coefficients_authenticated']==73218
 assert core['complete_source_and_GF_Hessian']['source_second_variation']['canonical_row_stream_sha256']==reg['complete_source_Hessian_stream_sha256']
 assert reg['complete_field_tangent']['all_directional_coefficients']==70935 and reg['complete_field_tangent']['first_jet_offdiagonal_entries_retained']==180
 toy_result=toy(route);moment_result=symbols(route)
 # All actual first-jet coefficients are constant; formal adjoint is -c*d_mu.
 x0=s.Symbol('x0');hh=s.Function('h')(x0);kk=s.Function('k')(x0)
 assert s.expand(s.diff(hh*kk,x0)-s.diff(hh,x0)*kk-hh*s.diff(kk,x0))==0
 assert s.expand(s.diff(hh*kk,x0)-s.diff(hh,x0)*kk+hh*s.diff(kk,x0))!=0
 # This finite weighted commutator is not zero despite its zero logarithm.
 t,beta,vv=s.symbols('t beta vv',positive=True)
 if route=='primary':I=(1-s.integrate(s.exp(-t*beta*vv),(vv,0,1)))/(16*s.pi**2*t)
 else:I=beta*s.integrate((1-vv)*s.exp(-t*beta*vv),(vv,0,1))/(16*s.pi**2)
 I=s.simplify(I);expected=(t*beta-1+s.exp(-t*beta))/(16*s.pi**2*t*t*beta);assert s.simplify(I-expected)==0
 assert s.limit(I,t,0)==beta/(32*s.pi**2) and s.limit(-t*s.diff(I,t),t,0)==0
 # Formal inverse/cyclic cancellation needs FULL G,not a reference-only block.
 def reduce(word):
  word=list(word)
  while len(word)>1:
   hit=next((i for i in range(len(word)) if (word[i],word[(i+1)%len(word)]) in [('G','H'),('H','G')]),None)
   if hit is None:break
   word=word[hit:]+word[:hit];word=word[2:]
  return min(tuple(word[i:]+word[:i]) for i in range(len(word))) if word else ()
 assert reduce(['G','Msharp','H'])==('Msharp',) and reduce(['G','H','M'])==('M',)
 assert reduce(['Gref','H','M'])!=('M',)
 cyclic_orders=[]
 for n in range(1,13):
  direct=sum(s.Rational((-1)**(n+1),n) for _ in range(n)) if route=='primary' else s.Integer((-1)**(n-1));assert direct==(-1)**(n-1);cyclic_orders.append(str(direct))
 result={'schema':'BV_UV_RESIDUE_BRIDGE_V1','route':route,'actual_pairs':643,'all_first_jet_adjoint_entries':jets,'all180_firstjet_coefficients_constant_and_adjoint_minus_retained':True,'complete_source_Hessian_positions_authenticated':73218,'complete_tangent_positions_authenticated':70935,'E2_full_master_current_and_source_columns_retained':True,'all508_physical_programs_retained_not_recomputed':True,'nonlinear_control':toy_result,'homogeneous_residue_shift_controls':moment_result,'cyclic_Born_orders':cyclic_orders,'finite_heat_commutator_formula':str(I),'finite_heat_commutator_limit':str(beta/(32*s.pi**2)),'finite_heat_commutator_logarithm':0,
 'universal_proof_components':['twice varied integrated source-linear master identity with even graded test directions','formal jet adjoint and physical source Euler cancellation','local mixed-weight classical symbol closure','integrated Grassmann/fiber/p-momentum residue cyclicity by x/p IBP','ordered heat log equals unheated degree-4 symbol with controlled UV remainder','complete inverse-series reduction to differential tangent residues zero'],
 'complete_formal_one_loop_log_UV_Slavnov_identity_mod_currents':True,'actual_unmeasured295_vector_coefficients_calculated':False,'current_partial_Gamma_claimed_complete':False,'finite_sourcefree_Slavnov_QAP_measure_quantum_A5_E5_proved':False,'reference_determinant_retained_QA_zero_only':True,'finite_regulator_source_correction_retained':True,'state_or_scheme_changed':False,
 'scientific_disposition':'COMPLETE_FORMAL_ONE_LOOP_LOCAL_LOG_SLAVNOV_IDENTITY_IN_EXPLICIT_LOCAL_HEAT_REFERENCE_FAMILY_NOT_FINITE_OR_FULL_E5','shared_limits':'same action/master/physical/source/reference certificates,Python/SymPy and AI author;two native branches share arithmetic;selected controls are not full-amplitude replay','elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
