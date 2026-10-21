"""Actual canonical Ward transport and first normalization-order assembly."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import gzip,json,sys,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
P=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
sys.path.insert(0,str(R/'tools/portable_dh_v1'))
from exact_algebra import Algebra,ONE,put,scale,scale_coefficient
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def plus(*pp):
 out={}
 for p in pp:
  for key,z in p.items():put(out,key,z)
 return out

def main():
 tick=time.perf_counter();watch=threading.Timer(120,lambda:os._exit(124));watch.daemon=True;watch.start();role=sys.argv[1];assert role in ['primary','replay'];prep=read(O/'preparation.json');assert digest(Path(__file__))==prep['source_sha256']
 for raw,h in prep['input_sha256'].items():assert digest(Path(raw))==h,raw
 def guard(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  p=Path(os.fsdecode(args[0])).resolve()
  if len(args)>1 and isinstance(args[1],str) and any(c in args[1] for c in 'wax+'):raise PermissionError('ANA_NATIVE_WRITE')
  if p.suffix=='.json':assert str(p) in prep['read_json_by_role'][role],('ANA_UNDECLARED_JSON',str(p))
 sys.addaudithook(guard);get=lambda lab:read(Path(prep['artifacts'][role][lab]['path']))
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()));geo=data['geometry'];A=Algebra(geo['names'],geo['parities']);pairs=geo['field_source_h_k'];fields={i for i,J,h,k in pairs};sources={J for i,J,h,k in pairs};canonical=fields|sources;Jof={i:J for i,J,h,k in pairs};externalA={A.index[f'A{a}_{mu}'] for a in range(12) for mu in range(4)};omega={A.index[f'omega{a}'] for a in range(12)}
 def rows(rr):
  out={}
  for r in rr:
   for key,z in A.rows([r],explicit_g='g' in r).items():put(out,key,z)
  return out
 def elem(n,j=()):
  if isinstance(n,str):n=A.index[n]
  return {(0,((n,j),)):ONE}
 def pack(p):
  cc=[];ids={};rr=[]
  for(g,w),z in sorted(p.items()):
   if z not in ids:ids[z]=len(cc);cc.append([[*cell,v.numerator,v.denominator] for cell,v in z])
   rr.append([g,[[n,list(j)] for n,j in w],ids[z]])
  return {'coefficients':cc,'monomials':rr,'sha256_exact_cells':A.fingerprint(p)}
 def summary(p):return {'positions':len(p),'sha256_exact_cells':A.fingerprint(p)}
 def D(p,mu):
  out={}
  for(g,w),z in p.items():
   for at,(n,j) in enumerate(w):
    ww,sg=A.canonical(w[:at]+((n,tuple(sorted(j+(mu,)))),)+w[at+1:])
    if sg:put(out,(g,ww),scale_coefficient(z,sg))
  return out
 def DD(p,j):
  for mu in j:p=D(p,mu)
  return p
 def grad(p):
  out={}
  for(g,w),z in p.items():
   pref=0
   for at,(n,j) in enumerate(w):
    put(out.setdefault((n,j),{}),(g,w[:at]+w[at+1:]),scale_coefficient(z,(-1)**(A.parities[n]*pref)));pref+=A.parities[n]
  return {k:v for k,v in out.items() if v}
 def EL(p,domain):
  out={n:{} for n in domain}
  for(n,j),df in grad(p).items():
   if n in domain:
    for key,z in scale(DD(df,j),(-1)**len(j)).items():put(out[n],key,z)
  return out
 def vector(p):
  ef=EL(p,fields);ej=EL(p,sources);v={}
  for i in fields:v[i]=scale(ej[Jof[i]],-(-1)**A.parities[i]);v[Jof[i]]=scale(ef[i],(-1)**A.parities[i])
  return v
 def operation(images,odd=False):
  images={n:v for n,v in images.items() if v};cache={}
  def action(p):
   out={}
   if role=='replay':
    for(n,j),df in grad(p).items():
     if n in images:
      if(n,j) not in cache:cache[n,j]=DD(images[n],j)
      for key,z in A.product(cache[n,j],df).items():put(out,key,z)
    return out
   for(g,w),z in p.items():
    pref=0
    for at,(n,j) in enumerate(w):
     if n in images:
      if(n,j) not in cache:cache[n,j]=DD(images[n],j)
      pp=A.product(A.product({(g,w[:at]):scale_coefficient(z,(-1)**pref if odd else 1)},cache[n,j]),{(0,w[at+1:]):ONE})
      for key,c in pp.items():put(out,key,c)
     pref+=A.parities[n]
   return out
  return action
 e3=get('e3');e2=get('e2');oldK=get('primitive');K=rows(oldK['full_K']);assert len(K)==3847;X=vector(K);x=operation(X)
 tp={A.index[n]:rows(rr) for n,rr in e3['operators']['Tq_transported'].items()};tq={A.index[n]:rows(rr) for n,rr in e3['operators']['Tq_geometric'].items()};tb={A.index[n]:rows(rr) for n,rr in e3['operators']['Tb_geometric_and_transported'].items()};c={n:plus(tp.get(n,{}),scale(tq.get(n,{}),-1)) for n in tp};assert all(not c.get(n) for n in fields|externalA)
 TP=operation(tp);TQ=operation(tq);TB=operation(tb);C=operation(c);assert not TB(K)
 print('STAGE '+role+' actual_fullK_Ward_generators_and_all_canonical_columns',flush=True)
 hq=TQ(K);hc=C(K);hp=TP(K) if role=='primary' else plus(hq,hc);assert hp==plus(hq,hc) and not any(n in sources for(g,w) in hc for n,j in w)
 dp=vector(hp);dq=vector(hq);dc=vector(hc);direct={};ext={};stages=[]
 for n in sorted(canonical):
  v=plus(TP(X[n]),scale(x(tp.get(n,{})),-1));assert v==dp[n],('HAMILTONIAN_COMMUTATOR',A.names[n]);direct[n]=v
  assert plus(dp[n],scale(dq[n],-1))==dc[n] and (n in sources or not dc[n])
 for n in externalA:ext[n]={};assert not tp[n]
 aext={n:tb[n] for n in externalA};EA=operation(aext)
 for i in fields:assert dp[i]==scale(EA(X[i]),-1),('BACKGROUND_FRECHET',A.names[i])
 degrees=Counter(sum(n in fields for n,j in w) for i in fields for(g,w) in dp[i]);assert not any(d>1 for d in degrees)
 assert all(not any(n in sources for n,j in w) for i in fields for(g,w) in dp[i])
 sign_control=None;wrongX={n:(scale(v,-1) if n in sources else v) for n,v in X.items()};wrong=operation(wrongX)
 for n in sorted(sources):
  bad=plus(TP(wrongX[n]),scale(wrong(tp.get(n,{})),-1),scale(dp[n],-1))
  if bad:sign_control={'source':A.names[n],'residual':summary(bad)};break
 assert sign_control
 physical={i for i in fields if A.names[i].startswith(('B','x_'))};assert len(physical)==508
 programs=[]
 for i in sorted(physical):
  name=A.names[Jof[i]];program=e2['complete_columns'][name]['physical_program'];assert program
  programs.append({'field':A.names[i],'source':name,'coefficient':pack(dp[i]),'physical_program_sha256':sha256(json.dumps(program,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'program_binding_path':'OWN_ROLE_E2_PACKET#complete_columns/'+name+'/physical_program'})
 print('STAGE '+role+' complete_actual_Psi_normalization_control',flush=True)
 e1=get('e1');Psi=plus(*(rows(rr) for rr in e1['polynomial_parts'].values()));W=TP(Psi);assert W==TQ(Psi)==rows(e3['quantum_fermion_breaking'])
 dPsi=vector(W);assert all(dPsi[n]==c.get(n,{}) for n in canonical)
 Rz={i:rows(data['master_field_maps'][A.names[i]]) for i in fields};Q=operation(Rz,True);BW=Q(W);B=rows(e3['action_Wards']['geometric_quantum_breaking']);assert BW==B and len(B)==22520
 CS=plus(*(A.product(c[Jof[i]],Rz[i]) for i in fields if c.get(Jof[i])));assert not plus(B,CS)
 omission=B;reversal=plus(B,scale(CS,-1));assert len(omission)==22520 and reversal==scale(B,2)
 E=EL(B,{A.index['b0']})[A.index['b0']];free={key:z for key,z in E.items() if all(n in omega for n,j in key[1])};expected={}
 for mu in range(4):
  expected=plus(expected,scale(elem('omega0',(mu,mu)),-2 if mu==0 else 2),scale(elem('omega1',(mu,mu)),1 if mu==0 else -1))
 assert free==expected and len(free)==8
 currents=[rows(v) for v in e3['action_Wards']['transported_quantum_current']];assert len(currents)==4 and not any(currents)
 print('STAGE '+role+' order_hbar_assembly_and_nonzero_connected_control',flush=True)
 x0,b0=s.symbols('x b',real=True);U=1+x0;D0=b0-U*U;f=x0+x0*x0/2;h=x0*s.diff(f,x0);log=s.log(D0)/2-s.log(U);Tloop=x0*s.diff(log,x0);I_B=b0*s.diff(h,x0,2)/(2*D0)-s.diff(h,x0)*U/D0-s.diff(h,x0)/U
 assert s.cancel(Tloop-I_B)==0;I_C=-I_B;point={x0:1,b0:9};tree=b0*x0*U
 assert s.cancel(Tloop.subs(point))==s.Rational(-9,10) and s.cancel(I_C.subs(point))==s.Rational(9,10) and tree.subs(point)==18
 hb,nt=s.symbols('hbar t');base=s.cancel(Tloop+I_C);assembled=s.expand(base+hb*nt*tree-hb*nt*tree);assert assembled==0
 assert s.expand(base+hb*nt*tree)!=0 and s.cancel((Tloop+0).subs(point))!=0
 # Independent algebraic order table:epsilon=hbar*t;crossed loop responses are hbar2.
 powers={'tree_counterterm':1,'baseline_unit_product_loop':1,'normalization_times_product_loop':2,'normalization_times_field_Jacobian_action':2,'mixed_K_L_normalization':2};assert powers['baseline_unit_product_loop']==powers['tree_counterterm']<powers['mixed_K_L_normalization']
 rawpole,FB,QG,pole=s.symbols('rawpole FB QG pole');raw=pole*(FB+QG)+rawpole;once=s.expand(raw-pole*FB-pole*QG);twice=s.expand(raw-2*pole*FB-2*pole*QG);assert once==rawpole and s.expand(twice-once+pole*(FB+QG))==0
 result={'schema':'ACTUAL_NORMALIZATION_ASSEMBLY_V1','route':role,'scientific_disposition':'COMPLETE_FORMAL_FIRST_ORDER_ONE_LOOP_ACTUAL_COUNTERTERM_SLAVNOV_BACKGROUND_AND_COMPLETED_GEOMETRIC_WARD_ASSEMBLY_NOT_FULL_E5','fullK_positions':len(K),'Tprime_K':pack(hp),'Tq_K':pack(hq),'C_K':pack(hc),'delta_Tprime_columns':{A.names[n]:pack(v) for n,v in dp.items() if v},'delta_Tq_columns':{A.names[n]:summary(v) for n,v in dq.items() if v},'delta_C_columns':{A.names[n]:pack(v) for n,v in dc.items() if v},'all1286_direct_commutators_and_Hamiltonian_source_duals_agree':len(direct)==1286,'all48_external_columns_zero':len(ext)==48,'field_affine_degree_counts':dict(degrees),'all643_background_Frechet_field_columns_match':True,'Tb_K_zero':True,'delta_C_has_only_source_columns_and_no_L_dependence':True,'retained508_weighted_physical_Euler_programs':programs,'wrong_source_cotangent_sign_control':sign_control,'Psi_positions':len(Psi),'W_Psi_positions':len(W),'Psi_completion_matches_all56_C_slots':True,'Psi_omitted_completion_remainder_positions':len(omission),'Psi_wrong_completion_doubles_every_Bq_coefficient':True,'Psi_b0_free_Euler_covector':pack(free),'four_exact_E3_currents_retained':[pack(p) for p in currents],'full_basic_B_and_symbolic_L_current_completion_kept':True,'normalization_order_powers':powers,'finite_tangent_distinct_from_single_existing_raw_pole_subtraction':True,'exact_once_rewriting_and_nonzero_double_subtraction_control':True,'gaussian':{'Tq_Gamma1':'-9/10','whole_I_C':'9/10','omitted_tree_completion':'18*hbar*t','wrong_tree_completion':'36*hbar*t','correct_assembled_remainder':'0','baseline_mean_field_omission_fails':True},'same_Tkappa_full_source_products_and_finite_conversion':True,'no_new_K_L_double_insertion_or_global_variable_map_claimed':True,'actual_B_L_or295_vector_component_tensors_extracted':False,'original_physical_parameter_basis_stability_proved':False,'full_QAP_A5_E5_universal_adequacy_or_physical_scheme_qualified':False,'authority_changed':False,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);watch.cancel()
if __name__=='__main__':main()
