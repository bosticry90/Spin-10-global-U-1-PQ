"""Actual H-D commutator, complete local candidate rank, nonlocal control."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import importlib.util,json,os,sys,time,threading
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);u=importlib.util.module_from_spec(z);z.loader.exec_module(u);return u
a=load('qualified_odd_anchor_and_actions',OUT.parent/'canonical_so10_antighost_linear_identity/test_v2.py');b=a.b;m=a.m;h=a.h;l=a.l;s=a.s;ex=a.ex;read=a.read;digest=a.digest;PKG=a.PKG

def main():
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];prep=read(OUT/'preparation.json');assert role in ['primary','replay'] and digest(Path(__file__))==prep['source_sha256']
 for p,k in prep['input_sha256'].items():assert digest(Path(p))==k,p
 allow={str(Path(p).resolve()) for p in prep['read_json_by_role'][role]}
 def guard(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  p=Path(os.fsdecode(args[0]))
  if len(args)>1 and isinstance(args[1],str) and any(c in args[1] for c in 'wax+'):raise PermissionError('BACKGROUND_LOCALITY_WRITE')
  if p.suffix=='.json':assert str(p.resolve()) in allow,('UNDECLARED_OR_PEER_JSON',str(p))
 sys.addaudithook(guard);w=m.setup();stages=[]
 def stage(n,fn):
  print('STAGE '+role+' '+n,flush=True);t=time.perf_counter();v=fn();stages.append({'name':n,'seconds':time.perf_counter()-t});return v
 for i in range(45):n='zz_da'+str(i).zfill(2);m.index[n]=len(m.names);m.names.append(n);m.par.append(1)
 eps=m.index['zz_da12'];E=m.elementary(eps);ub=m.index['ub12'];root=b.auth('canonical_so10_broken_antighost_operator',role+'_v2_result.json','validation_v2_receipt.json');V={m.index[n]:h.from_result([r for r in rows if 'zz_da12' in r['word']]) for n,rows in root['all33_kernel_maps'].items()};V={n:P for n,P in V.items() if P};assert len(V)==61
 D={ub:E,**{n:m.scale(P,-1) for n,P in V.items()}};data,db=b.sealed('frozen_a10_e3_symmetry',role);T={m.index[n]:m.decode(rows) for n,rows in data['operators']['Tb_geometric_and_transported'].items()};assert len(T)==1334 and not T[ub]
 def act(P,I):return m.action(P,I,'primary',True) if role=='primary' else m.action(P,I,'replay')
 def commutators():
  bad={m.names[n]:l.rows(m.add(act(P,D),m.scale(act(D.get(n,{}),T),-1))) for n,P in T.items() if act(P,D)!=act(D.get(n,{}),T)};assert not bad,('ACTUAL_H_D_COMMUTATOR',bad);return {'tested':len(T),'zero':True}
 comm=stage('all1334_actual_even_H_D_commutators',commutators);T0={n:{key:z for key,z in P.items() if key[0]==0} for n,P in T.items()};OH={m.index['omega'+str(i)] for i in range(12)}
 A=[[m.index[f'A{i}_{mu}'] for mu in range(4)] for i in range(12)];BH=[[m.index[f'B{i}_{mu}'] for mu in range(4)] for i in range(12)];BM=[[m.index[f'B{i}_{mu}'] for mu in range(4)] for i in range(12,45)]
 affine=[]
 for i in range(12):
  for mu in range(4):
   expected=m.D(m.elementary(m.index['omega'+str(i)]),mu);assert T0[A[i][mu]]==T0[BH[i][mu]]==expected;affine.append([m.names[A[i][mu]],m.names[BH[i][mu]],'omega'+str(i)+'__'+str(mu)])
 affset={n for row in A+BH for n in row};assert {n for n,P in T0.items() if P}==affset and len(affset)==96
 assert all(all(any(k in m.sources for k,j in key) for gp,key in T[n]) for n in m.sources)
 grades=w.grades|w.external;assert all(grades['C'+str(i)]==(1,1,1) for i in range(45));assert all(grades['B'+str(i)+'_0']==(1,0,0) for i in range(45));assert all(grades['A'+str(i)+'_0']==(1,0,0) for i in range(12));assert grades['ub12']==(1,-1,1)
 cl=b.auth('canonical_so10_broken_antighost_CL_identity',role+'_result.json');tj=b.auth('canonical_so10_ub12_twojet_insertion',role+'_v2_result.json');print('STAGE '+role+' flat_measured_pole_H_behavior',flush=True)
 # Locate the authenticated normalized CL insertion by its qualified source.
 cor=b.auth('canonical_so10_broken_antighost_CL_correspondence',role+'_result.json');
 Icl=h.from_result(cor['normalized_selected_insertion'])
 Itj=h.from_result(tj['source_left_loop_density']);flat=m.add(Icl,Itj);assert flat and all(gp==1 and not any(m.names[n].startswith(('A','B','J')) for n,j in key) for gp,key in flat)
 assert not act(flat,T),('FLAT_INSERTION_NOT_H_INVARIANT',l.rows(act(flat,T)))
 C=m.elementary(m.index['C12']);eta=(1,-1,-1,-1)
 def dot(U,V):return m.add(*(m.scale(m.mul(u,v),eta[mu]) for mu,(u,v) in enumerate(zip(U,V))))
 avec=[[m.elementary(n) for n in row] for row in A];bvec=[[m.elementary(n) for n in row] for row in BH];mvec=[[m.elementary(n) for n in row] for row in BM];ec=m.mul(E,C);dC=[m.D(C,mu) for mu in range(4)];dE=[m.D(E,mu) for mu in range(4)];basis=[]
 for i in range(12):basis.extend([(('A_eps_dC',i),dot(avec[i],[m.mul(E,x) for x in dC])),(('A_deps_C',i),dot(avec[i],[m.mul(x,C) for x in dE]))])
 for i in range(12):
  for j in range(i,12):basis.append((('AA',i,j),m.mul(ec,dot(avec[i],avec[j]))))
 for i in range(12):
  for j in range(12):basis.append((('ABH',i,j),m.mul(ec,dot(avec[i],bvec[j]))))
  for j in range(33):basis.append((('ABM',i,j+12),m.mul(ec,dot(avec[i],mvec[j]))))
 assert len(basis)==642 and Counter(k[0] for k,P in basis)==Counter({'A_eps_dC':12,'A_deps_C':12,'AA':78,'ABH':144,'ABM':396})
 def rank_all():
  piv={};cert=[];imagecounts=[]
  for label,P in basis:
   W=act(P,T0);EL=m.EL_all(W,OH);col={}
   for n,U in EL.items():
    for (gp,key),z in U.items():
     assert gp==0;v=ex.D.to_sympy(z);assert v.is_Rational;col[n,key]=Fraction(int(v.p),int(v.q))
   imagecounts.append(len(col))
   while col:
    key=min(col);value=col[key]
    if key not in piv:
     col={k:z/value for k,z in col.items()};piv[key]=col;cert.append([list(label),m.names[key[0]],[m.serialize_token(t) for t in key[1]],str(value)]);break
    for k,z in piv[key].items():
     v=col.get(k,Fraction(0))-value*z
     if v:col[k]=v
     else:col.pop(k,None)
   else:raise AssertionError(('LOCAL_WARD_KERNEL_COLUMN_DEPENDENCE',label))
  return cert,imagecounts
 certificate,imagecounts=stage('complete642_column_exact_Ward_Euler_injectivity',rank_all)
 # Actual derivative basis and the explicit divergence for derivative-on-A.
 da=dot(avec[0],[m.mul(E,x) for x in dC]);de=dot(avec[0],[m.mul(x,C) for x in dE]);divA=m.add(*(m.scale(m.mul(m.D(avec[0][mu],mu),ec),eta[mu]) for mu in range(4)));curr=[m.scale(m.mul(avec[0][mu],ec),eta[mu]) for mu in range(4)];assert m.add(divA,da,de)==m.add(*(m.D(J,mu) for mu,J in enumerate(curr)))
 # Both connection affines are necessary for this zero; suppressing B is wrong.
 Q=dot([m.add(x,m.scale(y,-1)) for x,y in zip(bvec[0],avec[0])],[m.add(x,m.scale(y,-1)) for x,y in zip(bvec[0],avec[0])]);wrong={n:P for n,P in T0.items() if n not in {z for row in BH for z in row}};assert not act(Q,T0) and act(Q,wrong)
 wrongA={n:P for n,P in T0.items() if n not in {z for row in A for z in row}};assert not act(da,wrongA) and act(da,T0)
 k=s.symbols('k0:4');p=s.symbols('p0:4');av=s.symbols('avec0:4');dotp=lambda u,v:sum(e*x*y for e,x,y in zip(eta,u,v));K=dotp(k,k);P=dotp(p,p);N=s.expand(-K*dotp(av,p)+dotp(k,p)*dotp(av,k));assert N!=0 and s.expand(N.subs(dict(zip(av,k)),simultaneous=True))==0
 _,rem=s.div(N,P,*p,*k,*av);assert rem!=0;ondivisor={p[0]:1,p[1]:1,p[2]:0,p[3]:0,k[0]:1,k[1]:0,k[2]:0,k[3]:0,av[0]:0,av[1]:1,av[2]:0,av[3]:0};assert P.subs(ondivisor)==0 and N.subs(ondivisor)!=0
 qc,qb=b.sealed('frozen_a10_e5_quantum_contract',role);flags={key:qc[key] for key in ['QAP_proved_for_model','actual_renormalization_prescription_constructed','all_order_class_nonempty_proved','joint_restoration_proved','quantum_insertions_renormalized','quantum_canonical_equivalence_proved','measure_or_anomaly_freedom_proved']};assert not any(flags.values())
 result={'schema':'UB12_ACTUAL_H_COMMUTATION_CONDITIONAL_LOCALITY_V1','route':role,'scientific_disposition':'ACTUAL_CLASSICAL_COMMUTATION_AND_CONDITIONAL_LOCAL_BACKGROUND_UNIQUENESS_ONLY','complete_actual_H_D_commutator':comm,'actual61_source_kernels':{m.names[n]:l.rows(P) for n,P in V.items()},'actual96_affine_columns_rank48':affine,'H_source_columns_preserve_source_zero':True,'measured_flat_g1_insertion':l.rows(flat),'measured_flat_insertion_actual_H_variation':[],'local_candidate_counts':{'derivative_A':24,'AA':78,'ABH':144,'ABM':396,'per_ghost':642,'ghost_components':45,'total':28890},'all642_actual_Ward_Euler_column_rank':len(certificate),'exact_sparse_pivot_certificate':certificate,'Ward_Euler_image_positions_per_basis':imagecounts,'ghost_index_identity_tensorization':True,'derivative_on_A_IBP_four_currents':list(map(l.rows,curr)),'conditional_g0_and_g1_offflat_local_kernel_zero':True,'essential_unproved_premise':'actual local power-counted logarithmic UV limit of full covariant-reference/heat family','nonlocal_transverse_control':{'numerator':str(N),'denominator':str(P),'transverse_for_A_equals_k':True,'numerator_not_divisible_by_p_squared':True,'nonzero_on_polynomial_divisor':str(N.subs(ondivisor))},'controls':{'delete_A_affine_makes_nonzero_local_column_invisible':True,'incorrectly_homogeneous_B_changes_connection_difference_invariant':True,'dropping_locality_admits_nonzero_flat_invisible_transverse_symbol':True},'quantum_flags_unchanged':flags,'actual_background_UV_locality_or_full_QAP_Slavnov_E5_A5_proved':False,'no_functional_source_input_scheme_benchmark_or_authority_change':True,'shared_premises':'action/reference/conventions/power_counted_ring/software/AI_author; not expert independence','stages':stages,'elapsed_after_imports':time.perf_counter()-tick};print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
