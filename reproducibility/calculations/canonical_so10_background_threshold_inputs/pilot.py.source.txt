"""Fresh C1 kinematic input construction; two coefficient routes, no amplitude."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
from collections import defaultdict,Counter
from itertools import combinations
import json,sys,time,threading,os,gzip
import sympy as s
from inventory import build,encoded
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
P=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'

@lru_cache(None)
def clean(x):return s.cancel(s.expand(x))
@lru_cache(None)
def parse(x):return s.sympify(x)
def tidy(d):return {k:clean(v) for k,v in d.items() if clean(v)!=0}
def matrix(row):return {(i,j):parse(z) for i,j,z in row['entries']}
def mult(a,b):
 ix=defaultdict(list);out=defaultdict(lambda:s.S.Zero)
 for (j,k),z in b.items():ix[j].append((k,z))
 for (i,j),z in a.items():
  for k,t in ix[j]:out[i,k]+=z*t
 return tidy(out)
def sub(a,b):
 out=defaultdict(lambda:s.S.Zero,a)
 for k,v in b.items():out[k]-=v
 return tidy(out)
def rows(d):return [[*k,str(v)] for k,v in sorted(d.items())]

def main(role):
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((D/'preparation.json').read_bytes())
 for n,h in prep['input_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
 data=json.loads((P/('frozen_a10_physical_reconciliation/full_'+role+'.json')).read_bytes())
 rho=[{} for _ in range(45)];off=0
 for sector,n in [('Phi',54),('Sigma',252),('phi',20),('S',2)]:
  for a,row in enumerate(data['representation_matrices'][sector]):
   for (i,j),z in matrix(row).items():rho[a][i+off,j+off]=z
  off+=n
 v={i:parse(z) for i,j,z in data['vacuum']['VEV']['entries']};O={}
 for a,rr in enumerate(rho):
  accum=defaultdict(lambda:s.S.Zero)
  for (i,j),z in rr.items():accum[i]+=z*v.get(j,0)
  for i,z in tidy(accum).items():O[i,a]=z
 assert O==matrix(data['vacuum']['orbit'])
 Ot={(a,i):z for (i,a),z in O.items()};Gram=mult(Ot,O)
 assert Gram==matrix(data['vacuum']['orbit_Gram'])
 print('STAGE orbit',time.perf_counter()-tick,flush=True)
 # Faithful representation routes for the same ordered Lie constants.
 f={};pairs=list(combinations(range(10),2));rt=1/s.sqrt(2)
 if role=='primary':
  hs=[{(i,j):rt,(j,i):-rt} for i,j in pairs];lookup={p:c for c,p in enumerate(pairs)}
  for a in range(45):
   for b in range(45):
    comm=sub(mult(hs[a],hs[b]),mult(hs[b],hs[a]))
    for (i,j),z in comm.items():
     if i<j:f[a,b,lookup[i,j]]=clean(s.sqrt(2)*z)
 else:
  pp=[matrix(z) for z in data['representation_matrices']['phi']]
  lookup=defaultdict(list)
  for c,rr in enumerate(pp):
   for (i,j),z in rr.items():lookup[j,i].append((c,z))
  for a in range(45):
   for b in range(45):
    accum=defaultdict(lambda:s.S.Zero)
    for key,z in mult(pp[a],pp[b]).items():
     for c,t in lookup[key]:accum[c]-=z*t
    for c,z in tidy(accum).items():f[a,b,c]=z
  # Confirm index2 and faithful closure, not a numerical trace diagnostic.
  for a in range(45):
   for b in range(a+1,45):
    expected=defaultdict(lambda:s.S.Zero)
    for c in range(45):
     z=f.get((a,b,c),0)
     if z:
      for key,t in pp[c].items():expected[key]+=z*t
    assert sub(sub(mult(pp[a],pp[b]),mult(pp[b],pp[a])),tidy(expected))=={}
 assert len(f)==720
 print('STAGE structure_constants',time.perf_counter()-tick,flush=True)
 T={}
 if role=='primary':
  for b,rr in enumerate(rho):
   for (a,i),z in mult(Ot,rr).items():T[a,b,i]=z
 else:
  U=[mult(rr,O) for rr in rho];fx=defaultdict(list)
  for (a,b,c),z in f.items():fx[a,b].append((c,z))
  for a in range(45):
   for b in range(45):
    indices={i for i,col in U[a] if col==b}|{i for i,col in U[b] if col==a}
    indices|={i for c,z in fx[a,b] for i,col in O if col==c}
    for i in indices:
     val=clean((-U[a].get((i,b),0)-U[b].get((i,a),0)+sum(z*O.get((i,c),0) for c,z in fx[a,b]))/2)
     if val:T[a,b,i]=val
 # Full support and zero-complement identities; no sample field choice.
 antisym_fail=0;projection=defaultdict(lambda:s.S.Zero);fx=defaultdict(list)
 for (a,b,c),z in f.items():fx[a,b].append((c,z))
 for a in range(45):
  for b in range(45):
   for i in range(328):
    anti=sum(z*O.get((i,c),0) for c,z in fx[a,b])
    assert clean(T.get((a,b,i),0)-T.get((b,a,i),0)-anti)==0
    if anti:antisym_fail+=1
    if i in v:projection[a,b]+=v[i]*T.get((a,b,i),0)
 assert tidy(projection)==Gram and antisym_fail>0
 assert not any(i>=306 for a,b,i in T) # phi and S have zero orbit.
 print('STAGE ghost_scalar_tensor',time.perf_counter()-tick,flush=True)
 M=matrix(data['C3_plane_to_parent']);MH={(a,h):z for (a,h),z in M.items() if h<12}
 assert mult(O,MH)=={}
 # Full H-orbit intertwining, including complex root coordinates.
 for h in range(12):
  rr=defaultdict(lambda:s.S.Zero);ad=defaultdict(lambda:s.S.Zero)
  for a in range(45):
   z=MH.get((a,h),0)
   if z:
    for key,t in rho[a].items():rr[key]+=z*t
    for (aa,b,c),t in f.items():
     if aa==a:ad[c,b]+=z*t
  assert mult(tidy(rr),O)==mult(O,tidy(ad)),h
 # Exact spectral projectors, not floating eigenvalue clustering.
 gm=s.SparseMatrix(45,45,Gram);evs=[s.S.Zero,s.Rational(3,10),s.Rational(3,2),s.Integer(25),s.Rational(253,10)]
 multiplicities=[]
 for lam in evs:
  proj=s.SparseMatrix(s.eye(45))
  for nu in evs:
   if nu!=lam:proj=proj*(gm-nu*s.eye(45))/(lam-nu)
  proj=proj.applyfunc(clean);assert proj*gm==lam*proj and proj*proj==proj
  multiplicities.append(int(s.trace(proj)))
 assert multiplicities==[12,8,1,12,12]
 # D-dimensional one-loop normalization and two-width CT jets.
 ep,x1,x2,g,q,eta=s.symbols('ep x1 x2 g q eta',real=True);Ddim=4-2*ep
 heat=clean((Ddim/12-2)/2+s.Rational(1,24)-s.Rational(1,12));assert heat==-s.Rational(7,8)-ep/12
 scalarheat=s.Rational(1,24);assert heat.subs(ep,0)/scalarheat==-21
 assert clean(heat.coeff(ep)/(-heat.subs(ep,0)))==-s.Rational(2,21)
 # Matching lambda uses log M=log(M^2)/2: finite/log(M)=-1/21.
 widths={}
 for name,expr in [('longitudinal',1/x1),('scalar',x2),('ghost',s.sqrt(x1*x2)),('mix',s.sqrt(x2/x1)-1)]:
  widths[name]=[str(clean(s.diff(expr,x).subs({x1:1,x2:1}))) for x in [x1,x2]]
 assert widths=={'longitudinal':['-1','0'],'scalar':['0','1'],'ghost':['1/2','1/2'],'mix':['-1/2','1/2']}
 assert s.expand(-g*eta*q+g*eta*q)==0 and s.expand(-g*eta*q-g*eta*q)!=0
 # A commuting width is only a diagnostic subset of general deltaK.
 summary,catalog=build(role)
 payload={'convention':'barc_a c_b eta_I; coefficient xi*g10^2*T_abI',
 'f_shape':[45,45,45],'f':rows(f),'T_shape':[45,45,328],'T':rows(T),
 'orbit':rows(O),'Gram':rows(Gram),'background_words':catalog}
 raw=encoded(payload)
 with (D/(role+'_tables.json.gz')).open('xb') as out:out.write(gzip.compress(raw,mtime=0))
 bysector=dict(Counter('Phi' if i<54 else 'Sigma' for a,b,i in T))
 out={'schema':'C1_BACKGROUND_THRESHOLD_INPUT_NATIVE_V1','role':role,
 'tensor_positions':664200,'tensor_nonzero':len(T),'tensor_zero':664200-len(T),
 'tensor_sector_support':bysector,'structure_positions':91125,'structure_nonzero':len(f),
 'orbit_nonzero':len(O),'Gram_nonzero':len(Gram),'mass_eigenvalues':list(map(str,evs)),
 'mass_multiplicities':multiplicities,'H_generators_checked':12,
 'antisymmetric_support':antisym_fail,'v_contraction_blind_to_antisymmetric_omission':True,
 'one_loop_heat_coefficient':str(heat),'width_first_jets':widths,'inventory':summary,
 'table_sha256':sha256(raw).hexdigest(),'table_compressed_sha256':sha256((D/(role+'_tables.json.gz')).read_bytes()).hexdigest(),
 'mass_VEV_tadpole_finite_CT_prescription_fully_defined':False,'C1_GS_calculated':False,
 'historical_A10_or_E1_action_adopted':False,'authority_changed':False,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+encoded(out).decode().strip(),flush=True);timer.cancel()
if __name__=='__main__':main(sys.argv[1])
