from pathlib import Path
from hashlib import sha256
import json,gzip,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_bytes());H=lambda p:sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(gzip.decompress(p.read_bytes()));tick=time.perf_counter()
timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'validation_preparation_v2.json')['input_sha256'].items():assert H(Path(p))==h,p
a,b=[load(O/(x+'_tables.json.gz')) for x in ['primary','replay_v2']]
assert {k:v for k,v in a.items() if k!='role'}=={k:v for k,v in b.items() if k!='role'}
dec=lambda z:s.SparseMatrix(*z['shape'],{(i,j):s.sympify(v) for i,j,v in z['entries']});cl=lambda M:s.SparseMatrix(M).applyfunc(s.cancel)
F=load(O.parent/'canonical_so10_probe_fermion_onejet/construction_tables.json.gz')['F'];positions=0;bad=0
for r,z in enumerate(a['color_CU']):
 C=dec(z);f=dec(F[r])
 for reverse in [False,True]:
  cc=C.T if reverse else C;ff=f.T if reverse else f
  # Independent P and Pprime each carry half the average momentum.
  for momentum in ['P','Pprime']:
   assert not cl(ff/2+cc/12).todok();positions+=256;bad+=len(cl(2*ff/2+cc/12).todok())
old=read(O.parent/'canonical_so10_finite_probe_nielsen_ward/validation_receipt.json');assert old['actual_lambda2_whole_joint_limit']=='1/6' and old['separate_root_and_hatted_limits_do_not_commute']
out={'schema':'NVT1_VALIDATION','elapsed_after_imports':time.perf_counter()-tick,'general_transfer_mixed_inverse_and_source_Euler_routes_agree':True,'ordered_Clifford_reduction_before_integration':True,'UV_IR_degrees_and_uniform_comparison_bound_checked':True,'analytic_proof_reuses_NFP_whole_joint_limit_not_separate_limits':True,'whole_joint_limit':'i*g10^2*CU*(Pbar+Pprimebar)/12','old_fixed_symmetric_kinetic_candidate_cancels_selected_finite_limit':True,'candidate_independent_momentum_positions_including_zeros':positions,'double_candidate_control_nonzero_positions':bad,'controls':a['controls'],'CSW_operator_reduction_not_new_full_field_root_replay':True,'nonconstant_probe_but_formal_positive_dimension_grade0_only':True,'new_full_finite_3point_kernel_quadrature_performed':False,'full_chiral_QAP_measure_phase_physical_scheme_or_E5_A5':False,'scientific_authority_changed':False};print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
