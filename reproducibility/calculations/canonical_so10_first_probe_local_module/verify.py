from pathlib import Path
from hashlib import sha256
from collections import Counter
import gzip,json,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()))
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'validation_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
P=load(O/'primary_tables.json.gz');Z=load(O/'replay_tables.json.gz')
for k in P:
 if k!='role':assert P[k]==Z[k],k
d=load(O/'primary_inputs.json.gz');receipts={k:v['data'] for k,v in d['receipts'].items()}
for key,row in d['receipts'].items():assert H(Path(row['path']))==row['sha256'] and read(Path(row['path']))==row['data']
def family(row):
 c=Counter(row['fields']);m,j=row['mass_degree'],row['ordinary_jet_degree'];probe='rho' if c['rho'] else'uC';remaining=c.copy()
 for v,n in [('rho',1),('u',1),('C',int(probe=='uC')),('P',2)]:remaining[v]-=min(remaining[v],n)
 if c['P']==2 and not c['KP']:
  remaining=+remaining
  if not remaining and(m,j)==(0,1):return probe+'_PP_jet'
  if not remaining and(m,j)==(1,0):return probe+'_PP_intrinsic'
  if remaining==Counter(B=1) and(m,j)==(0,0):return probe+'_BPP'
  if remaining==Counter(x=1) and(m,j)==(0,0):return probe+'_xPP'
 if c==Counter({'rho':1,'C':1,'KP':1,'P':1}) and(m,j)==(0,0):return'rhoC_KPP'
 if c==Counter({'u':1,'C':2,'KP':1,'P':1}) and(m,j)==(0,0):return'uCC_KPP'
 return'UNCLASSIFIED:'+json.dumps(row,sort_keys=True)
families=[family(x) for x in P['breaking_type_envelope']];missing=sorted(set(families)-set(receipts));extra=sorted(set(receipts)-set(families));coverage={key:False for key in receipts}
r=receipts['rho_PP_jet'];assert r['ordinary_rho_PP_both_labels_chiralities_p_q_remainders_zero'] and r['generic_odd_density_IBP_and_negative_flow_derivation_passed'];coverage['rho_PP_jet']=True
r=receipts['uC_PP_jet'];assert all(z['full_ucPP_p_q_s_both_chiralities_zero'] and z['ordinary_rho_PP_and_old_K_source_projections_preserved'] for z in r['diagnostics']);coverage['uC_PP_jet']=True
comparison_positions={}
def zero_matrices(v):
 if isinstance(v,dict):
  if'shape'in v and'entries'in v:assert not v['entries'];return v['shape'][0]*v['shape'][1]
  return sum(zero_matrices(x) for x in v.values())
 if isinstance(v,list):return sum(zero_matrices(x) for x in v)
 return 0
for key,folder,n,flag in [('rho_BPP','canonical_so10_rho_vector_support','loop_comparison_v2_tables.json.gz','single_candidate_matches_complete_selected_rhoBPP'),('uC_BPP','canonical_so10_probe_ghost_vector_vertices','loop_comparison_v3_tables.json.gz','fixed_candidate_matches_complete_uCBPP')]:
 r=receipts[key];assert r[flag];p=O.parent/folder/n;blob=p.read_bytes();assert sha256(blob).hexdigest()==r['comparison_packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==r['comparison_raw_sha256'];v=load(p);comparison_positions[key]=zero_matrices(v['remainders']);assert comparison_positions[key]>0;coverage[key]=True
g,xi,eta=s.symbols('g10 xi eta_H',real=True);loc={'g10':g,'xi':xi,'eta_H':eta};dec=lambda d:s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z,locals=loc) for i,j,z in d['entries']});tidy=lambda M:s.SparseMatrix(M).applyfunc(s.expand)
def zero(M):assert not tidy(M).todok()
rx=load(O.parent/'canonical_so10_probe_scalar_support/quantum_primary_v3_tables.json.gz');K=list(map(dec,d['K_mass']))
for r in range(2):zero(dec(rx['operators'][r]['total'])+K[r])
rs=receipts['rho_xPP'];assert rs['alternating_half_and_odd_left_u_derivative_pass'] and rs['symmetric_carrier_preserved'] and all(z['compact_operator_matches_full_measured_input'] and z['five_prior_scalar_zero_images']=='ZERO_BY_MONOMIAL_SUPPORT' for z in rs['checks']);coverage['rho_xPP']=True
rs=receipts['uC_xPP'];assert rs['all90_ordered_responses_and_five_full_mass_operators_agree'] and not rs['any_counterterm_or_physical_input_changed'];comparison_positions['uC_xPP']=zero_matrices(rs['complete_remainder_operators']);assert comparison_positions['uC_xPP']==2*45*256**2;coverage['uC_xPP']=True
for key in ['rho_PP_intrinsic','uC_PP_intrinsic']:
 r=receipts[key];assert r['intrinsic_bare_graded_subfamily_structural_zero_in_reused_full_D_reference'] and r['all_four_component_actual_polynomial_tensors_and_zero_complements_match'] and r['ordered_symbolic_rescaling_and_both_inverse_orders_pass'];coverage[key]=True
for key in ['rhoC_KPP','uCC_KPP']:
 r=receipts[key];assert r['complete_primitive_image_matches_measured_probe_part'] and r['each_independent_label_image_matches'] and P['measured_source_projection_patterns'][key]>0;coverage[key]=True
assert len(P['concrete_functional_program'])==4 and sum(x['term']=='source_flow' for x in P['concrete_functional_program'])==1
assert P['source_X_matches_actual_PMC_primitive'] and P['all_coefficient_reality_and_mass_symmetry_pass'] and all(x['candidate_BV_overlap_pairs']==0 for x in P['actual_G_QG_vs_candidate_BV_ports']) and not P['full_Q_assumed_nilpotent']
controls={'omit_scalar_family_uncovered_types':sorted(set(families)&{'rho_xPP','uC_xPP'}),'omit_jet_family_uncovered_types':sorted(set(families)&{'rho_PP_jet','uC_PP_jet'}),'omit_source_family_uncovered_types':sorted(set(families)&{'rhoC_KPP','uCC_KPP'}),'artificial_antighost_or_JB_controls_are_port_overlap_only':True,'rho_KP_P_is_allowed_but_not_in_this_particular_candidate':any(Counter(x['fields'])==Counter({'rho':1,'KP':1,'P':1}) for x in P['counterterm_type_envelope'])}
assert all(len(controls[x])==2 for x in ['omit_scalar_family_uncovered_types','omit_jet_family_uncovered_types','omit_source_family_uncovered_types']) and controls['rho_KP_P_is_allowed_but_not_in_this_particular_candidate']
complete=not missing and not extra and all(coverage.values())
out={'schema':'FIRST_PROBE_LOCAL_MODULE_VALIDATION_V1','elapsed_after_imports':time.perf_counter()-tick,'two_type_enumerations_and_actual_candidate_ports_agree':True,'breaking_type_count':len(P['breaking_type_envelope']),'counterterm_type_count':len(P['counterterm_type_envelope']),'carrier_families':families,'receipt_coverage_reused_not_fresh_quantum_replay':coverage,'comparison_zero_positions_reauthenticated':comparison_positions,'missing_types':missing,'unused_receipt_types':extra,'complete_projected_unshifted_first_probe_bare_local_cancellation':complete,'new_source_or_scalar_coefficient_fitted':False,'full_augmented_operator_restricted_by_actual_BV_ports_not_nilpotence':True,'full_Q_curvature_retained':'Q_full^2=(Ihat,.)','jet_placements_before_IBP':{'rho_PP':['rho','P_left','P_right'],'uC_PP':['u','C','P_left','P_right']},'retained_independent_momentum_slots':{'rho_PP':['p','q'],'uC_PP':['p','q','s']},'controls':controls,'new_quantum_loop_calculations':0,'new_physical_vacuum_or_massive_transport_proved':False,'full_QAP_measure_phase_or_E5_A5_promoted':False,'authority_changed':False}
print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True)
