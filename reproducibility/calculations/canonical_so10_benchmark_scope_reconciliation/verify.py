"""BSR1 exact point/parameter and selected qualified-scope comparison."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
packed=lambda p:json.loads(gzip.decompress(p.read_bytes()));A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
fields=['old_point_sha256','finite_point_sha256','old_quartics','finite_quartics','old_eta','finite_eta','receipt_statuses','stale_domain_recommendation_requires_correction','old_numerical_results_reinterpreted_as_finite_point','new_physics_or_benchmark_adopted']
for n in fields:assert A[n]==B[n],n
assert A['old_point_sha256']!=A['finite_point_sha256'] and F(A['old_eta'])==F(3,10) and F(A['finite_eta'])==F(1,10000)
changed=[n for n in NAMES if F(A['old_quartics'][n])!=F(A['finite_quartics'][n])];assert changed
expected={'search':'COMPLETED_BOUNDED_SEARCH_INCONCLUSIVE_TWO_REJECTED_CANDIDATES_CERTIFIED',
 'eta_exclusion':'COMPLETED_FIXED_ETA_EIGHT_QUARTIC_TREE_PERTURBATIVITY_EXCLUSION',
 'finite_witness':'COMPLETED_FINITE_LISTED_NECESSARY_SET_WITNESS','finite_contact':'COMPLETED_FULL_SCALAR_CONTACT_UPPER_BELOW_HALF',
 'finite_BFB':'COMPLETED_STRICT_GLOBAL328_QUARTIC_CERTIFICATE',
 'finite_scalar_warning':'COMPLETED_SCALAR_REFERENCE_LARGE_RADIAL_RESPONSE_FULL_QUANTUM_UNDERDETERMINED',
 'finite_bosonic_warning':'COMPLETED_CONDITIONAL_BOSONIC_WORSENING_FULL_QUANTUM_UNDERDETERMINED',
 'finite_input_warning':'COMPLETED_ONE_LOOP_MISMATCH_AND_MASS_ONLY_TRANSLATION_WARNING'}
assert A['receipt_statuses']==expected and A['C1_static_source_selects_positive_higgs'] and B['C1_contract_selects_positive_higgs']
assert B['xSigma_not_gauge_x'] and B['finite_classical_certificates_do_not_establish_quantum_control']
print('RESULT '+json.dumps({'status':'QUALIFIED_DISTINCT_REFERENCE_SCOPES_AND_NAVIGATION_CORRECTION','elapsed_after_imports':time.perf_counter()-start,
 'quartic_coefficients_compared':16,'changed_quartic_names':changed,'receipt_scopes_checked':8,'old_eta':'3/10','finite_eta':'1/10000',
 'old_fixed_eta_comparison_excluded':True,'finite_witness_classical_certificates_preserved':True,'finite_witness_quantum_control_unqualified':True,
 'old_threshold_transferred_to_finite_witness':False,'static_audit_not_full_runtime_replay':True,'navigation_interpretation_error_preserved':True,
 'scientific_authority_changed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
