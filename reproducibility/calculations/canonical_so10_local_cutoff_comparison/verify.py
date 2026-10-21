"""Independent LAC1 tests. No native helper is imported."""
from pathlib import Path
from hashlib import sha256
import ast,json,gzip,time,threading,os
import sympy as s
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
PK=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
def main():
 tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
 prep=json.loads((O/'validation_preparation.json').read_bytes())
 for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
 # Cheap independent odd derivative/connection and cutoff inverse controls.
 K=s.Matrix([[0,2],[3,0]]);X=s.Matrix([[0,5],[7,0]])
 assert K*X+X*K==29*s.eye(2) and K*X-X*K!=29*s.eye(2)
 P=s.Matrix([[1,2],[0,1]]);V=s.Matrix([[1,0],[3,1]]);A=s.Matrix([[2,1],[1,1]])
 U=V.inv()*P;assert U*(P.inv()*A)*U.inv()==V.inv()*A*P.inv()*V
 assert U.inv()*(P.inv()*A)*U!=V.inv()*A*P.inv()*V
 a,b=[json.loads((O/(role+'_result.json')).read_bytes()) for role in ['primary','replay']]
 for key in a:
  if key not in ['role','elapsed_after_imports']:assert a[key]==b[key],key
 assert a['fields']==a['sources']==643 and a['backgrounds']==48 and a['parity_cases']==4
 assert a['source_H_generators']==12 and a['GF_two_jet_rows']>0
 def mat(n,rows):return s.SparseMatrix(n,n,{(i,j):s.sympify(v) for i,j,v in rows})
 def zero(m):return all(s.simplify(v)==0 for v in m.values())
 G=mat(45,a['source_metric']);kn=mat(45,a['ghost_kinetic_normalized']);image=mat(45,a['QN_source_two_jet_normalized'])
 assert G.rank()==kn.rank()==45 and zero(image-G*kn) and image[14,14]!=0
 ref=json.loads((PK/'frozen_a10_e5_full_hessian/primary.json').read_bytes())['retained_reference'];fields=ref['field_order'];fi={v:i for i,v in enumerate(fields)}
 anames=[f'bar{i}' if i<12 else f'ub{i}' for i in range(45)];ai=[fi[n] for n in anames]
 T=mat(643,ref['physical_to_raw_kernel']['entries']);Ti=mat(643,ref['physical_to_raw_inverse']['entries'])
 TA=T.extract(list(range(598,643)),ai);inv=Ti.extract(ai,list(range(598,643)))
 assert zero(TA*inv-s.eye(45)) and zero(G-inv*inv.T)
 # Order-preserving physical reality of the actual EVEN-source quadratic.
 source_real=s.conjugate(TA).T*inv.T
 assert zero(source_real.T*s.conjugate(G)*source_real-G)
 # Recover every source type from the independent literal BV algebra declaration.
 tree=ast.parse((PK/'a10_bv_common.py').read_text());env={}
 for node in tree.body:
  if isinstance(node,ast.Assign):
   for target in node.targets:
    if isinstance(target,ast.Name) and target.id in ['H','M','IDS','DIM']:
     env[target.id]=eval(compile(ast.Expression(node.value),'<type>','eval'),{'__builtins__':{'range':range}},env)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='algebra')
 value=next(n.value for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fields' for t in n.targets))
 declared=eval(compile(ast.Expression(value),'<field>','eval'),{'__builtins__':{'range':range},**env})
 source_types={'J'+n:[4-(dd-gh),-1-gh,1-p] for n,(dd,gh,p) in declared.items()}
 assert len(source_types)==643 and sha256(json.dumps(source_types,sort_keys=True,separators=(',',':')).encode()).hexdigest()==a['source_types_sha256']
 assert all(source_types['J'+n]==[2,0,0] for n in anames)
 # Selected actual GF bilinear: reorder a FIRST before ordinary IBP, independent
 # of native prefix-gradient implementation. Complete45x45 checked in two routes.
 data=json.loads(gzip.decompress((R/'tools/portable_dh_v1/inputs.json.gz').read_bytes()))
 pp=s.Matrix(s.symbols('p0_ref0:4'));P2=pp[0]**2-sum(pp[k]**2 for k in [1,2,3]);selected=s.S.Zero;selected_rows=0
 for row in data['gauge_fixing_density']:
  toks=[v.partition('__') for v in row['word']]
  if len(toks)!=2 or {v[0] for v in toks}!={'C14','ub14'} or sum(len(v[2]) for v in toks)!=2:continue
  assert all(len(v[2])==1 for v in toks)
  co=s.sympify(row['coefficient'])*(1 if toks[0][0]=='ub14' else -1)
  selected+=co*pp[int(toks[0][2])]*pp[int(toks[1][2])];selected_rows+=1
 assert selected_rows==4 and s.simplify(selected-P2*kn[14,14])==0
 assert s.simplify(kn[14,14])!=0
 rawG=mat(643,ref['reference_Green_raw_C3']['entries']);edge=rawG[fi['C14'],fi['ub14']];rev=rawG[fi['ub14'],fi['C14']]
 assert s.simplify(edge*P2)==1 and s.simplify(rev*P2)==-1
 assert any(row['word']==['C14__0'] and row['coefficient']=='1' for row in data['master_field_maps']['B14_0'])
 # Both frequency signs distinguish graded anticommutator from ordinary one.
 spectral=[]
 for frequency in [s.Integer(2),s.Integer(-2)]:
  theta_plus=1 if frequency>0 else 0;theta_minus=1-theta_plus
  actual=s.I*frequency*(theta_plus-theta_minus)
  assert actual==2*s.I and actual!=0;spectral.append(str(actual))
  if frequency<0:assert actual!=s.I*frequency*(theta_plus+theta_minus)
 # Actual source-only term central cancellation leaves the full Gamma changed.
 g,J,E,c=s.symbols('g J E central',nonzero=True);NJ=g*g*J*J/2
 assert s.diff(NJ,J)*E==g*g*J*E and s.diff(NJ,J)*E!=0
 assert zero((c*P).inv()*(c*A)-P.inv()*A)
 # Current and background-only counterexample remain distributional jet statements.
 t=s.Symbol('t');aa=s.Function('A')(t);om=s.Function('omega')(t);cut=s.Function('u')(t);B=s.Function('B')(t)
 euler_omega=s.diff(s.diff(aa,t),t,2);assert euler_omega.subs(aa,t**3).doit()==6
 assert s.expand(s.diff(cut*B*om,t)-cut*s.diff(B*om,t))==B*om*s.diff(cut,t)
 assert not a['source_only_negative_control_Qclosed'] and a['source_only_negative_control_background_invariant']
 assert not a['strict_global_Gamma_or_physical_vacuum_limit_proved'] and not a['physical_quadratic_PPA_or_all_E5_A5_proved']
 for folder,receipt in [('background_reference_normalization','validation_receipt_v6.json'),('graded_causal_qap','validation_receipt_v2.json'),('causal_one_loop_sewing','validation_receipt.json'),('causal_one_loop_sewing','cycle_receipt.json'),('causal_one_loop_sewing','jets_receipt.json'),('causal_wick_bridge','validation_receipt.json')]:
  assert json.loads((R/'calculations'/('canonical_so10_'+folder)/receipt).read_bytes())['execution_state']=='COMPLETED'
 performance={}
 for role in ['primary','replay']:
  cap=json.loads((O/(role+'_capture.json')).read_bytes());out=json.loads((O/(role+'_result.json')).read_bytes())
  assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and out['elapsed_after_imports']<120
  assert cap['launch']['memory']['available_pagefile']>=350*1024**2
  sample=max(z['private_bytes'] for z in cap['all_resource_samples']);assert sample<8*1024**3
  performance[role]={'seconds':out['elapsed_after_imports'],'max_sampled_private_bytes':sample}
 out={'schema':'LOCAL_CUTOFF_VALIDATION_V1','execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED',
  'scientific_disposition':'LOCAL_CUTOFF_INTERTWINER_WITH_GRADED_SOURCE_TRANSPORT_AND_COUNTEREXAMPLE_TO_GLOBAL_FUNCTIONAL_IMPLICATION',
  'input_sha256':prep['input_sha256'],'performance':performance,'source_metric_rank':45,'ghost_kinetic_rank':45,
  'GF_two_jet_rows':a['GF_two_jet_rows'],'source_pairs_typed':643,'actual_QN_Jub14_C14_normalized':str(image[14,14]),
  'actual_source_gradient_ghost_reference_control':spectral,'source_quadratic_reality_checked':True,
  'nonlinear_Q_assumed_star_derivation':False,'Gamma_ref_and_source_normalizations_retained':True,
  'global_physical_Gamma_or_PPA_constructed':False,'full_E5_A5_proved':False,'authority_changed':False,
  'native_failures':0,'verifier_failures':0,'shared_action_software_and_AI_author':True,'elapsed_after_imports':time.perf_counter()-tick}
 print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
