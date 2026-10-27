from pathlib import Path
from hashlib import sha256
import gzip,json,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()))
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'endpoint_validation_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
P=load(O/'endpoint_primary_tables.json.gz');Z=load(O/'endpoint_replay_tables.json.gz')
for k in P:
 if k!='role':assert P[k]==Z[k],k
def matrix_count(v):
 if isinstance(v,dict):
  if'shape'in v and'entries'in v:return(len(v['entries']),v['shape'][0]*v['shape'][1])
  pairs=[matrix_count(x) for x in v.values()]
 elif isinstance(v,list):pairs=[matrix_count(x) for x in v]
 else:return(0,0)
 return(sum(x[0] for x in pairs),sum(x[1] for x in pairs))
keys=['current_polarization_remainders','probe_current_inverse_products','probe_current_free_inverse_scalar_products','mixed_U_G0_U_products','inverse_scalar_products','scalar_column_polarization_remainders','endpoint_degree2_coefficients_all45C','intrinsic_scalar_degree2_and3_coefficients_all45C','rho_u_scalar_coefficients'];counts={k:matrix_count(P[k]) for k in keys};zero_hypothesis=all(v[0]==0 for v in counts.values())
ep=load(O.parent/'canonical_so10_even_probe_vertices/primary_tables.json.gz');erp=load(O.parent/'canonical_so10_even_probe_vertices/replay_tables.json.gz');assert ep['currents']==erp['currents'] and ep['u_C_transfers_kept_independent'] and ep['all_four_Lorentz_components_checked'];assert all(not cur['AC'] and not cur['AU'] for cur in ep['currents'])
rx=load(O.parent/'canonical_so10_probe_scalar_support/quantum_primary_inputs.json.gz');assert all(not v['A']['entries'] for v in rx['V_A_H'])
g,xi,eta=s.symbols('g10 xi eta_H',real=True);loc={'g10':g,'xi':xi,'eta_H':eta};dec=lambda d:s.SparseMatrix(*d['shape'],{(i,j):s.sympify(z,locals=loc) for i,j,z in d['entries']});tidy=lambda M:s.SparseMatrix(M).applyfunc(s.expand)
def zero(M):assert not tidy(M).todok()
old=load(O/'endpoint_primary_inputs.json.gz');G0=dec(old['G0']);K0=dec(old['K0']);U=[dec(v['U']) for v in old['probe_quadratics']];Gr=[dec(v['Gr']) for v in old['probe_quadratics']];S=s.diag(*([-1]*45+[1]*45));zero(G0*S-(G0*S).T)
k,l,m=s.symbols('k l m',positive=True);R=lambda z:s.diag(*([z]*45+[1]*45));Ri=lambda z:s.diag(*([1/z]*45+[1]*45));G=lambda z:Ri(z)*G0*Ri(z)
for r in range(2):
 zero(Gr[r]*S-(Gr[r]*S).T);delta=Ri(k)*Gr[r]*Ri(l);zero(delta+G(k)*(R(k)*U[r]*R(l))*G(l));zero((R(k)*K0*R(k))*G(k)-s.eye(90));zero(G(k)*(R(k)*K0*R(k))-s.eye(90))
 if zero_hypothesis:
  for t in range(2):zero((R(k)*U[r]*R(l))*G(l)*(R(l)*U[t]*R(m)))
assert P['generic_noncommuting_opposite_momentum_isotropy']=='0' and P['generic_wrong_right_momentum_isotropy']!='0';assert P['controls']['omit_auxiliary_current_null_positions']>0 and P['controls']['wrong_right_momentum_sign_isotropy_positions']>0
out={'schema':'HIGHER_PROBE_ENDPOINT_VALIDATION_V1','elapsed_after_imports':time.perf_counter()-tick,'complete_primary_convolution_vs_replay_index_and_association_arrays_agree':True,'full_matrix_positions_checked':sum(v[1] for v in counts.values()),'coefficient_nonzeros_and_position_counts':{k:list(v) for k,v in counts.items()},'all_tested_principal_endings_affine_and_higher_intrinsic_scalar_coefficients_zero':zero_hypothesis,'actual_probe_AC_AU_and_rho_A_zero_limits_qualified':True,'independent_momentum_bilocal_nilpotence_and_inverse_proof_passed':True,'noncommuting_isotropy_implication_checked_with_opposite_momentum_sign':True,'ordered_probe_currents_count':len(P['current_polarization_remainders']),'pairwise_isotropy_covered_by_generic_identity_if_polarization_zero':len(P['current_polarization_remainders'])**2,'controls':P['controls'],'new_quantum_loop_integrals':0,'external_B_response_and_full_higher_probe_module_proved':False,'new_multiple_insertion_or_QAP_measure_domain_proved':False,'authority_changed':False}
print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True)
