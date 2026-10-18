"""Actual643 mixed reference weights and local-symbol applicability boundary."""
from pathlib import Path
from functools import lru_cache
from collections import Counter,defaultdict
import importlib.util,json,os,sys,time,threading
import sympy as s
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);u=importlib.util.module_from_spec(z);z.loader.exec_module(u);return u
a=load('qualified_actual_alphabet_and_auth',OUT.parent/'canonical_so10_antighost_linear_identity/test_v2.py');b=a.b;read=a.read;digest=a.digest;PKG=a.PKG

@lru_cache(None)
def simp(z):return s.cancel(z)

def main():
 tick=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];prep=read(OUT/'preparation_v2.json');assert role in ['primary','replay'] and digest(Path(__file__))==prep['source_sha256']
 for p,k in prep['input_sha256'].items():assert digest(Path(p))==k,p
 allow={str(Path(p).resolve()) for p in prep['read_json_by_role'][role]}
 def guard(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  p=Path(os.fsdecode(args[0]))
  if len(args)>1 and isinstance(args[1],str) and any(z in args[1] for z in 'wax+'):raise PermissionError('REFERENCE_SYMBOL_WRITE')
  if p.suffix=='.json':assert str(p.resolve()) in allow,('UNDECLARED_OR_PEER_JSON',str(p))
 sys.addaudithook(guard);w=a.m.setup();data,db=b.sealed('frozen_a10_e5_full_hessian',role);ref=data['retained_reference'];names=ref['field_order'];grades=w.grades|w.external;t=[2-grades[n][0] for n in names];assert len(names)==643 and Counter(t)==Counter({1:598,0:45}) and all((t[i]==0)==(n.startswith('L') or (n.startswith('b') and not n.startswith('bar'))) for i,n in enumerate(names))
 pp=s.symbols('p0_ref:4',real=True);eta=s.diag(1,-1,-1,-1);P=(s.Matrix(pp).T*eta*s.Matrix(pp))[0];rad=s.symbols('radial_scale',positive=True);loc={str(p):p for p in pp};stages=[]
 def stage(n,fn):
  print('STAGE '+role+' '+n,flush=True);tt=time.perf_counter();v=fn();stages.append({'name':n,'seconds':time.perf_counter()-tt});return v
 @lru_cache(None)
 def num(txt):return s.sympify(txt,locals=loc)
 K={(i,j):num(txt) for i,j,txt in ref['reference_Hessian_raw_C3']['entries']};G={(i,j):num(txt) for i,j,txt in ref['reference_Green_raw_C3']['entries']};mass=sorted({z for U in [K,G] for v in U.values() for z in v.free_symbols if str(z).startswith('Mref_')},key=str);assert len(mass)==4
 @lru_cache(None)
 def homogeneous(z,weight):
  if role=='primary':return s.cancel(z.xreplace({p:rad*p for p in pp}|{M:rad**2*M for M in mass})-rad**weight*z)==0
  return s.cancel(sum(p*s.diff(z,p) for p in pp)+2*sum(M*s.diff(z,M) for M in mass)-weight*z)==0
 def allweights():
  for (i,j),z in K.items():assert homogeneous(z,t[i]+t[j]),('K_WEIGHT',i,j)
  for (i,j),z in G.items():assert homogeneous(z,-t[i]-t[j]),('G_WEIGHT',i,j)
  return [len(K),len(G)]
 checks=stage('all1597_K_and1550_G_weighted_scalings',allweights);zero={M:0 for M in mass};K0={ij:s.cancel(z.xreplace(zero)) for ij,z in K.items()};G0={ij:s.cancel(z.xreplace(zero)) for ij,z in G.items()};assert not any(M in z.free_symbols for z in [*K0.values(),*G0.values()] for M in mass)
 T={(i,j):num(z) for i,j,z in ref['physical_to_raw_kernel']['entries']};I={(i,j):num(z) for i,j,z in ref['physical_to_raw_inverse']['entries']};physw=[1]*508+[0]*45+[1]*90;assert len(physw)==643
 assert all(not z.free_symbols and physw[i]==t[j] for (i,j),z in T.items());assert all(not z.free_symbols and t[i]==physw[j] for (i,j),z in I.items())
 # Reconstruct every physical gauge/auxiliary block from actual raw matrices.
 ic=defaultdict(dict);tr=defaultdict(dict)
 for (i,j),z in I.items():ic[j][i]=z
 for (i,j),z in T.items():tr[i][j]=z
 @lru_cache(None)
 def physical_entry(i,j,which):
  M,L,R=(K0,ic[i],ic[j]) if which=='K' else (G0,tr[i],tr[j]);return simp(sum(a*M.get((v,k),0)*d for v,a in L.items() for k,d in R.items()))
 pv=s.Matrix(pp);up=eta*pv;widthH=s.Symbol('eta_H',real=True);widthM=s.Symbol('xi',real=True)
 @lru_cache(None)
 def check_block(Ktuple,Gtuple,width):
  kk=s.Matrix(5,5,Ktuple);gg=s.Matrix(5,5,Gtuple);expected=(-P*eta+up*up.T).row_join(s.I*up).col_join((-s.I*up.T).row_join(s.Matrix([[width]])))
  assert all(simp(v)==0 for v in kk-expected)
  assert all(simp(v)==0 for v in kk*gg-s.eye(5)) and all(simp(v)==0 for v in gg*kk-s.eye(5))
  assert simp(kk.det(method='domain-ge')+P**4)==0;return True
 def mixed():
  blocks=[]
  for color in range(45):
   addr=[4*color+mu for mu in range(4)]+[508+color];width=num('eta_H' if color<12 else 'xi');kk=s.Matrix(5,5,lambda i,j:physical_entry(addr[i],addr[j],'K'));gg=s.Matrix(5,5,lambda i,j:physical_entry(addr[i],addr[j],'G'));assert check_block(tuple(kk),tuple(gg),width);blocks.append([color,str(width),'-p_squared^4'])
  return blocks
 blocks=stage('all45_actual_raw_to_physical_mixed_principal_blocks',mixed)
 # All physical ghost orientations, and all328 scalar leading inverses.
 for color in range(45):
  i,j=553+color,598+color
  assert physical_entry(i,j,'K')==-P and physical_entry(j,i,'K')==P and physical_entry(i,j,'G')==1/P and physical_entry(j,i,'G')==-1/P
 for i in range(180,508):assert physical_entry(i,i,'K')==P and physical_entry(i,i,'G')==1/P
 q=s.symbols('q0:4',real=True);Q=sum(x*x for x in q);assert s.expand(P.xreplace({pp[0]:s.I*q[0],**{pp[i]:q[i] for i in range(1,4)}})+Q)==0
 maxwell=-P*eta+up*up.T;assert maxwell.det(method='domain-ge')==0;uniform2bad=any(not homogeneous(z,-2) for (i,j),z in G0.items() if t[i]!=t[j]);assert uniform2bad
 # Actual H adjoint matrix supplies a local curvature/order control.
 e3,e3b=b.sealed('frozen_a10_e3_symmetry',role);tb=e3['operators']['Tb_geometric_and_transported'];rho=s.zeros(12);g=s.Symbol('g10');
 for i in range(12):
  for row in tb['C'+str(i)]:
   body=[x for x in row['word'] if x.startswith('C')];omega=[x for x in row['word'] if x.startswith('omega')]
   if omega==['omega0']:assert len(body)==1;rho[i,int(body[0][1:])]+=s.cancel(s.sympify(row['coefficient'])/g)
 assert rho!=s.zeros(12);col=next(j for j in range(12) if rho[:,j]!=s.zeros(12,1));x,y=s.symbols('x y');f=s.zeros(12,1);f[col]=x*x
 d0=lambda z:z.diff(x);d1=lambda z:z.diff(y)+g*x*rho*z;lap=lambda z:-d0(d0(z))-d1(d1(z));F=lambda z:g*rho*z
 left=(lap(d1(f))-d1(lap(f))).applyfunc(s.expand);right=(-d0(F(f))-F(d0(f))).applyfunc(s.expand);assert left==right and left!=s.zeros(12,1)
 # Noncommutative inverse identity by exact free words with only L Li=Li L=1.
 def reduced(w):
  w=list(w);again=True
  while again:
   again=False
   for n in range(len(w)-1):
    if tuple(w[n:n+2]) in [('L','Li'),('Li','L')]:w[n:n+2]=[];again=True;break
  return tuple(w)
 def free(terms):
  out=Counter()
  for word,z in terms:out[reduced(word)]+=z
  return {k:v for k,v in out.items() if v}
 assert not free([(('Li','D'),1),(('D','Li'),-1),(('Li','L','D','Li'),1),(('Li','D','L','Li'),-1)])
 # Ordered two-dimensional matrix-potential symbol, finite jet inverse proof.
 z,p=s.symbols('z p');U=s.Matrix(2,2,lambda i,j:s.Function('u'+str(i)+str(j))(z));B=s.eye(2)/p**2-U/p**4-2*s.I*U.diff(z)/p**5+(U*U+3*U.diff(z,2))/p**6;A=s.eye(2)*p**2+U
 if role=='primary':product=A*B-2*s.I*p*B.diff(z)-B.diff(z,2)
 else:product=sum((((-s.I)**j/s.factorial(j))*B.diff(p,j)*A.diff(z,j) for j in range(5)),s.zeros(2))
 def trunc(e):return sum(s.expand(e).coeff(p,k)*p**k for k in range(-4,1))
 residual=(product-s.eye(2)).applyfunc(trunc);assert residual==s.zeros(2)
 # Actual structured reference program is flat; covariance is stated in prose.
 prog=data['finite_cutoff_loop_program'];assert isinstance(prog['reference'],str) and 'covariantized' in prog['reference'] and 'Dbar_H' in prog['cutoff'];flat_symbols={str(z) for z in [*K.values(),*G.values()] for z in z.free_symbols};assert not any(z.startswith(('A','Dbar','F_H')) for z in flat_symbols)
 qc,qcb=b.sealed('frozen_a10_e5_quantum_contract',role);flags={k:qc[k] for k in ['QAP_proved_for_model','actual_renormalization_prescription_constructed','all_order_class_nonempty_proved','joint_restoration_proved','quantum_insertions_renormalized','quantum_canonical_equivalence_proved','measure_or_anomaly_freedom_proved']};assert not any(flags.values())
 result={'schema':'UB12_ACTUAL_REFERENCE_WEIGHTED_SYMBOL_V1','route':role,'scientific_disposition':'ACTUAL_WEIGHTED_PRINCIPAL_INVERTIBILITY_QUALIFIED_BACKGROUND_LOCAL_CLASS_MEMBERSHIP_UNPROVED','field_weight_counts':dict(Counter(t)),'all1597_K1550_G_entries_homogeneous_with_mass_dimension':checks,'all_constant_frame_entries_preserve_weights':True,'all45_mixed_principal_blocks':blocks,'all45_ghost_orientation_pairs_and328_scalar_principals_checked':True,'Wick_principal_p_squared':'-sum_q_squared','Euclidean_nonzero_momentum_mixed_principal_determinant':'-sum_q_squared^4','no_width_g_or_reference_mass_inverted_in_principal':True,'whole_mixed_positive_Laplacian_used':False,'actual_H_curvature_order_control':{'generator':0,'column':col,'rho_entries':[[i,j,str(v)] for (i,j),v in rho.todok().items()],'nonzero_commutator':[[i,str(v)] for i,v in enumerate(left) if v],'identity_checked':True},'ordered_inverse_commutator_free_word_identity':True,'matrix_potential_parametrix_through_relative4':[[i,j,str(B[i,j])] for i in range(2) for j in range(2)],'left_and_right_inverse_jet_test_through_degree_minus4':True,'actual_retained_reference_fields':sorted(ref),'actual_covariant_reference_specification':prog['reference'],'actual_heat_specification':prog['cutoff'],'flat_matrix_symbols':sorted(flat_symbols),'structured_background_ordered_symbol_in_these_bound_fields':False,'local_parametrix_sufficiency_requires_actual_local_finite_jet_coefficient_class':True,'ordering_difference_does_not_prove_nonlocality':True,'counterexample_controls':{'delete_mixed_blocks_makes_gauge_symbol_singular':True,'uniform_order2_claim_fails_actual_mixed_inverse_homogeneity':True,'commuting_Delta_and_D_drops_nonzero_actual_H_curvature_term':True},'actual_local_UV_or_regulated_QAP_measure_IR_contacts_full_Slavnov_E5_A5_proved':False,'seven_quantum_flags_unchanged':flags,'no_new_covariant_reference_operator_or_physical_scheme_adopted':True,'no_full_Gamma_Hessian_or_qualified_dense_inverse_replay':True,'no_functional_source_benchmark_authority_change':True,'stages':stages,'elapsed_after_imports':time.perf_counter()-tick};print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
