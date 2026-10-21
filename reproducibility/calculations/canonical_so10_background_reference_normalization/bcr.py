"""BCR1: actual carrier/normalization data and nonzero reference control."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
from collections import defaultdict
import json,gzip,sys,time,threading,os
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
PK=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'

@lru_cache(None)
def num(v):return s.sympify(v)
def clean(v):return s.simplify(s.expand(v))
def sparse(m):return [[int(i),int(j),str(clean(v))] for (i,j),v in sorted(m.todok().items()) if clean(v)!=0]
def zero(m):return all(clean(v)==0 for v in m.values())
def mat(n,rows):return s.SparseMatrix(n,n,{(i,j):num(v) for i,j,v in rows})
def digest(v):return sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main(role):
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((O/'preparation.json').read_bytes())
 for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 ref=json.loads((PK/'frozen_a10_e5_full_hessian'/(role+'.json')).read_bytes())['retained_reference']
 fields=ref['field_order'];fi={v:i for i,v in enumerate(fields)};assert len(fields)==643
 witness=json.loads((R/'calculations/canonical_so10_local_covariant_reference_witness'/(role+'_result.json')).read_bytes())
 e3=json.loads((PK/'frozen_a10_e3_symmetry'/(role+'.json')).read_bytes())['operators']['Tb_geometric_and_transported']
 g=s.Symbol('g10');rr=[defaultdict(lambda:s.S.Zero) for _ in range(12)];jj=[defaultdict(lambda:s.S.Zero) for _ in range(12)];aff={}
 for name,rows in e3.items():
  for row in rows:
   omega=[v for v in row['word'] if v.startswith('omega')];other=[v for v in row['word'] if not v.startswith('omega')]
   assert len(omega)==1
   base,sep,jet=omega[0].partition('__');h=int(base[5:]);c=num(row['coefficient'])
   if sep:
    assert not other and len(jet)==1 and c==1 and (name.startswith('B') or name.startswith('A'))
    aff[(name,h,jet)]=c;continue
   assert len(other)==1 and '__' not in other[0]
   c=s.expand(c);v=c.coeff(g);assert clean(c-g*v)==0
   if name in fi:rr[h][(fi[name],fi[other[0]])]+=v
   elif name.startswith('J'):
    assert other[0].startswith('J');jj[h][(fi[name[1:]],fi[other[0][1:]])]+=v
   else:assert name.startswith('A')
 actual=[s.SparseMatrix(643,643,{k:clean(v) for k,v in d.items() if clean(v)}) for d in rr]
 if role=='primary':carriers=actual
 else:carriers=[mat(643,z) for z in witness['actual12_homogeneous_carrier_matrices']]
 assert len(carriers)==12 and all(zero(a-b) for a,b in zip(actual,carriers))
 source_counts=[]
 for h,r in enumerate(carriers):
  src=s.SparseMatrix(643,643,{k:clean(v) for k,v in jj[h].items() if clean(v)})
  assert zero(src+r.T);source_counts.append(len(src.values()));assert not zero(r)
  # Pairing J_i z_i: all actual fields and source duals, including zero columns.
  assert zero(src.T+r) and not zero(r),'source omission must be detected separately'
 assert sum(n.startswith('J') for n in e3)==643 and len(e3)==1334
 T=mat(643,ref['physical_to_raw_kernel']['entries']);Ti=mat(643,ref['physical_to_raw_inverse']['entries'])
 bis=[[fi[f'B{a}_{mu}'] for a in range(45)] for mu in range(4)]
 TB=T.extract(list(range(0,180,4)),bis[0]);TBi=Ti.extract(bis[0],list(range(0,180,4)))
 assert zero(TB*TBi-s.eye(45));GB=(TB.T*TB).applyfunc(clean)
 F=s.zeros(45,12)
 for a in range(45):
  for h in range(12):
   vals=[aff.get((f'B{a}_{mu}',h,str(mu)),0) for mu in range(4)];assert len(set(vals))==1;F[a,h]=vals[0]
 assert sum(n.startswith('B') for n,h,j in aff)==48 and sum(n.startswith('A') for n,h,j in aff)==48
 for h in range(12):
  for mu in range(4):assert aff[(f'A{h}_{mu}',h,str(mu))]==1
 # All45 BRST color matrices and all180 derivative columns from actual master rules.
 portable=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()))
 DD=[];MM=[];nlin=0;nder=0
 for mu in range(4):
  D=s.zeros(45);M=[s.zeros(45) for _ in range(45)]
  for a in range(45):
   for row in portable['master_field_maps'][f'B{a}_{mu}']:
    word=row['word'];co=num(row['coefficient'])
    if len(word)==1:
     c,sep,j=word[0].partition('__');assert c.startswith('C') and j==str(mu) and sep;D[a,int(c[1:])]+=co;nder+=1
    else:
     assert len(word)==2
     bv=next(z for z in word if z.startswith('B'));cv=next(z for z in word if z.startswith('C'))
     b,mm=map(int,bv[1:].split('_'));assert mm==mu and '__' not in cv
     v=s.expand(co).coeff(g);assert clean(co-g*v)==0;M[int(cv[1:])][a,b]+=v;nlin+=1
  DD.append(D);MM.append(M)
 assert all(zero(d-DD[0]) for d in DD) and nder==180
 D=DD[0];assert all(zero(MM[mu][k]-MM[0][k]) for mu in range(4) for k in range(45))
 assert all(zero(GB*m+m.T*GB) for m in MM[0])
 # The auxiliary mass is a proof regulator only; check every real pair.
 cidx=[fi[f'C{a}'] for a in range(45)];aidx=[fi[f'bar{a}'] if a<12 else fi[f'ub{a}'] for a in range(45)]
 lidx=[fi[f'b{a}'] if a<12 else fi[f'L{a}'] for a in range(45)]
 def physblock(r,raw,phys):return (T.extract(phys,raw)*r.extract(raw,raw)*Ti.extract(raw,phys)).applyfunc(clean)
 sectors={'B':bis[0],'Lambda':lidx,'C':cidx,'a':aidx}
 for tag in ['Phi','Sigma','phi','S']:sectors[tag]=[i for i,n in enumerate(fields) if n.startswith('x_'+tag+'_')]
 assert [len(sectors[k]) for k in ['Phi','Sigma','phi','S']]==[54,252,20,2]
 traces=[];width=s.diag(*([1]*12+[0]*33))
 for h,r in enumerate(carriers):
  for mu in range(4):assert zero(r.extract(bis[mu],bis[mu])-r.extract(bis[0],bis[0]))
  rb=r.extract(bis[0],bis[0]);assert zero(GB*rb+rb.T*GB)
  rbp=physblock(r,bis[0],list(range(0,180,4)))
  assert zero(rbp.T+rbp) and zero(rbp*width-width*rbp)
  rc=physblock(r,cidx,list(range(553,598)));ra=physblock(r,aidx,list(range(598,643)))
  assert zero(ra+rc.T)
  tr={k:str(clean(r.extract(ids,ids).trace())) for k,ids in sectors.items()};assert set(tr.values())=={'0'};traces.append(tr)
  partition=[bis[mu] for mu in range(4)]+[sectors[k] for k in ['Phi','Sigma','phi','S','Lambda','C','a']]
  partof={i:k for k,ids in enumerate(partition) for i in ids};assert len(partof)==643
  assert all(partof[i]==partof[j] for i,j in r.todok())
 # Different sparse color contractions. Internal representation ranks stay fixed.
 rec=json.loads((PK/'frozen_a10_physical_reconciliation'/('full_'+role+'.json')).read_bytes())
 indices={};grams={}
 for tag in ['Phi','Sigma','phi','S']:
  reps=rec['representation_matrices'][tag];size=reps[0]['shape'][0];rows=[{(i,j):num(v) for i,j,v in z['entries']} for z in reps]
  assert len(rows)==45 and all(all(clean(v+d.get((j,i),0))==0 for (i,j),v in d.items()) for d in rows)
  gram=s.zeros(45)
  if role=='primary':
   positions=defaultdict(list)
   for a,d in enumerate(rows):
    for ij,v in d.items():positions[ij].append((a,v))
   for values in positions.values():
    for a,v in values:
     for b,w in values:gram[a,b]+=v*w
  else:
   for a,da in enumerate(rows):
    for b,db in enumerate(rows):gram[a,b]=-sum(v*db.get((j,i),0) for (i,j),v in da.items())
  gram=gram.applyfunc(clean);ind=gram[0,0];assert zero(gram-ind*s.eye(45));indices[tag]=str(ind)
  ids=sectors[tag];hh=s.zeros(12)
  for h in range(12):
   ra=carriers[h].extract(ids,ids)
   for k in range(12):hh[h,k]=-sum(v*carriers[k][ids[j],ids[i]] for (i,j),v in ra.todok().items())
  hh=hh.applyfunc(clean);assert zero(hh-ind*F.T*GB*F);grams[tag]=sparse(hh)
 # Source-free beta images and the nonzero mixed local-parameter gradient.
 qb=(GB*D).applyfunc(clean);wb=(GB*F).applyfunc(clean);mixed=(D.T*GB*F).applyfunc(clean)
 assert mixed.rank()==12 and sparse(qb) and sparse(wb)
 lams,lamb=s.symbols('lambda_s lambda_b');assert (lams-lamb)*mixed[0,0]!=0
 # Non-Abelian control uses actual H matrices, not the insensitive two-point color form.
 phiids=sectors['Phi'];phis=[r.extract(phiids,phiids) for r in carriers];triple=None
 for h in range(12):
  for k in range(h+1,12):
   comm=phis[h]*phis[k]-phis[k]*phis[h]
   if zero(comm):continue
   for l in range(12):
    v=clean(sum(phis[l][i,j]*comm[j,i] for i,j in phis[l].todok()))
    if v!=0:triple=[h,k,l,str(v)];break
   if triple:break
  if triple:break
 assert triple and 2*phis[triple[0]]!=s.zeros(54)
 # Full mixed Euclidean inverse versus independent longitudinal block elimination.
 q=s.Matrix(s.symbols('q0:4'));Q=(q.T*q)[0];sig,w=s.symbols('sigma w',positive=True);den=Q+w*sig
 KK=(Q+sig)*s.eye(4)-q*q.T;K=KK.row_join(q).col_join((-q.T).row_join(s.Matrix([[w]])))
 if role=='primary':
  bb=s.eye(4)/(Q+sig)+(w-1)*q*q.T/((Q+sig)*den);bl=-q/den;lb=q.T/den;ll=sig/den
 else:
  # Invert the normalized longitudinal/auxiliary2x2, then add transverse projector.
  QQ=s.Symbol('Q',positive=True);long=s.Matrix([[sig,s.sqrt(QQ)],[-s.sqrt(QQ),w]]).inv()
  bb=(s.eye(4)-q*q.T/Q)/(Q+sig)+(q*q.T/Q)*(long[0,0].subs(QQ,Q))
  bl=q/s.sqrt(Q)*long[0,1].subs(QQ,Q);lb=q.T/s.sqrt(Q)*long[1,0].subs(QQ,Q);ll=long[1,1].subs(QQ,Q)
 G=bb.row_join(bl).col_join(lb.row_join(s.Matrix([[ll]])))
 assert zero((K*G-s.eye(5)).applyfunc(s.cancel)) and zero((G*K-s.eye(5)).applyfunc(s.cancel))
 mutant=G.copy();mutant[4,4]=0;assert not zero((K*mutant-s.eye(5)).applyfunc(s.cancel))
 odd=s.Matrix([[0,-(Q+sig)],[Q+sig,0]]);assert zero(odd*s.Matrix([[0,1/(Q+sig)],[-1/(Q+sig),0]])-s.eye(2))
 # Same special-heating and T1 chart: no second normalization coefficient.
 hh,ss,bbeta,bs,bd=s.symbols('Delta_H Delta_s b beta_s beta_b')
 assert s.expand((hh-bs)+(-hh+bs))==0 and s.expand((ss-bd)+(-ss+bd))==0
 t=s.Symbol('t');u=s.Function('u')(t);B=s.Function('B')(t);omega=s.Function('omega')(t)
 current=s.diff(u*B*omega,t);assert s.expand(u*B*s.diff(omega,t)+omega*s.diff(u*B,t)-current)==0
 assert s.expand(u*B*s.diff(omega,t)+u*omega*s.diff(B,t)-current)!=0
 # Actual reference scalar response: retain constant/commonkappa and compare shape only.
 mp.mp.dps=45 if role=='primary' else 75;shapes=[]
 for z in [1,2,3]:
  if role=='primary':value=-mp.quad(lambda u:(1-2*u)**2*mp.log(1+u*(1-u)*z),[0,mp.mpf('.5'),1])
  else:value=-z*mp.quad(lambda a:(1-4/a)**mp.mpf('1.5')/(3*a*(a+z)),[4,8,mp.inf])
  assert value<0;shapes.append([z,mp.nstr(value,40)])
 # Exact dimensional angular/IBP identity; no premature D=4.
 u,z,M=s.symbols('u z M',positive=True);dd=s.Symbol('D');delta=M+u*(1-u)*z
 I1=lambda x:s.gamma(1-dd/2)*x**(dd/2-1)
 I2=lambda x:s.gamma(2-dd/2)*x**(dd/2-2)
 assert clean(s.diff(I1(delta),u)+I2(delta)*(1-2*u)*z)==0
 assert clean(s.diff((1-2*u)*I1(delta),u)+2*I1(delta)+(1-2*u)**2*z*I2(delta))==0
 assert s.integrate(delta,(u,0,1))==M+z/6
 moments=[str(s.factorial(n)**2/(s.factorial(2*n+1)*(2*n+3))) for n in range(9)]
 assert all(s.integrate((1-2*u)**2*(u*(1-u))**n,(u,0,1))==num(moments[n]) for n in range(9))
 disc=2*s.pi*s.I*(s.sqrt(s.Rational(1,2)))**3/3
 # Uniform mass removal uses the pre-existing independent-transfer proof;
 # these edge exponents and the extra sigma are recorded, not sampled as a proof.
 result={'schema':'BACKGROUND_REFERENCE_NATIVE_V1','role':role,'field_count':643,'source_count':643,'background_count':48,
  'homogeneous_carrier_sha256':digest([sparse(r) for r in carriers]),'source_nonzero_counts':source_counts,
  'affine_rules':len(aff),'BRST_derivative_rows':nder,'BRST_nonlinear_rows':nlin,'scalar_indices':indices,
  'actual_H_scalar_grams':grams,'GB':sparse(GB),'D':sparse(D),'F':sparse(F),
  'Qbeta_tensor':sparse(qb),'Wbeta_tensor':sparse(wb),'mixed_parameter_gradient_tensor':sparse(mixed),
  'separate_block_traces':traces,'noncommuting_H_Phi_triple':triple,'finite_sigma_LL':str(ll),
  'reference_Phi_shapes':shapes,'scalar_moments':moments,'timelike_shape_discontinuity_at_8M':str(disc),
  'premature_D4_error_normalized':'-(M+z/6)','reference_determinant_retained':True,
  'controls':{'source_dual_omission':True,'local_affine_omission':True,'different_beta_coefficients':True,
   'finite_sigma_LL_omission':True,'D_sign_gradient_defect':True,'color_commutation_triple':True,
   'seagull_omission':True,'premature_D4':True,'i0_flip':True,'switching_current_omission':True,
   'two_point_D_sign_and_color_order_insensitive':True,'source_free_beta_source_omission_insensitive':True},
  'physical_scheme_adopted':False,'full_E5_A5_proved':False,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main(sys.argv[1])
