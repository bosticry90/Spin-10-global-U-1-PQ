from pathlib import Path
from hashlib import sha256
import ast,json,os,subprocess,threading,time
output_path=Path(__file__).resolve().parent;repository_path=output_path.parents[1]
control_path=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/nonminimal-source-products-v1-2026-10-26')
read=lambda p:json.loads(p.read_bytes());file_hash=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
bindings={};preps=[]
for prep in sorted(output_path.glob('*preparation*.json')):
    preps.append(prep.name)
    for path,digest in read(prep)['input_sha256'].items():
        assert file_hash(Path(path))==digest,(prep.name,path)
        if path in bindings:assert bindings[path]==digest
        bindings[path]=digest
copies=list(output_path.glob('*.source.txt'))
for path in copies:assert path.read_bytes()==path.with_name(path.name[:-11]).read_bytes(),path
for path in output_path.glob('*.py'):ast.parse(path.read_bytes())
for path in output_path.iterdir():
    if path.suffix in ['.py','.md','.txt']:assert all(line==line.rstrip(b' \t') for line in path.read_bytes().splitlines()),path
expected_failed={'audit_capture.json':'cannot unpack non-iterable int object','review_capture.json':'SHARED_ACTION_TO_HESSIAN_CONVENTION_MISMATCH'}
accepted={'audit_capture_v3.json','review_capture_v2.json','late_capture_v2.json','e4_capture.json'}
rejected={'audit_capture_v2.json'};seen=set();samples={}
for path in sorted(output_path.glob('*capture*.json')):
    cap=read(path);seen.add(path.name)
    assert not cap['failed_or_incomplete_counted_as_PASS'] and cap['launch']['creation_after_observation']
    assert cap['launch']['memory']['available_pagefile']>=350*1024**2
    assert cap['all_resource_samples'] and all(0<v['private_bytes']<=8*1024**3 and 'query_error' not in v for v in cap['all_resource_samples'])
    samples[path.name]=max(v['private_bytes'] for v in cap['all_resource_samples'])
    if path.name in expected_failed:
        assert cap['execution_state']=='FAILED' and cap['exit_code']!=0 and not cap['calculation_completed']
        assert expected_failed[path.name] in cap['stdout_and_stderr']
    else:
        assert path.name in accepted|rejected
        assert cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
assert seen==set(expected_failed)|accepted|rejected
assert set(p.name for p in output_path.glob('*controller_failure*.json'))=={'controller_failure.json','review_controller_failure.json','late_controller_failure.json'}
assert "new_files_sha256" in read(output_path/'late_controller_failure.json')['traceback']
assert not(output_path/'late_capture.json').exists() and not(output_path/'validation_receipt.json').exists()
assert (output_path/'product_result.json').exists() # rejected original outputs preserved
native=read(output_path/'product_result_v3.json');review=read(output_path/'validation_receipt_v2.json');late=read(output_path/'late_validation_receipt.json')
assert native['elapsed_after_imports']<300 and review['elapsed_after_imports']<180 and late['elapsed_after_imports']<180
assert review['common_independently_smeared_nonminimal_product_extension']=='QUALIFIED_IN_INHERITED_FIRST_U_FORMAL_DOMAIN'
assert review['all_finite_k_formula_proved_by_induction_and_recurrence']
assert not review['two_unlabeled_symmetry_tangents_or_diagonal_pullback_licensed']
assert not review['full_Ward_normalization_mixing_QAP_measure_E5_physical_claim']
assert late['actual_model_source_derivative_code_unchanged_by_fixture_correction']
assert all(x['all_coefficients_equal'] for x in late['comparisons'])
assert [x['direct_Wick_Berezin'] for x in review['third_direct_action_Wick_Berezin_checks']]==['5/8','21/50','14/45','12/49']
scope=(output_path/'SOURCE_PRODUCT_SCOPE.md').read_text()
assert 'PROPER (1PI' in scope and 'not all\nconnected derivatives of W' in scope
assert 'Gamma1_phi[y_ij]' in scope and 'cannot be\ndropped' in scope
result=(output_path/'RESULT.md').read_text();assert 'completed connected Green-function prescription' in result
assert 'REJECTED' in (output_path/'GAUSSIAN_CORRECTION_V3.md').read_text()
events=read(output_path/'e4_events.json');steps=[x for x in events if x['event']=='step_finished'];exits=[x['exit_code'] for x in steps]
assert exits==[0,0,0,0,0,2] and events[-1]['execution_state']=='COMPLETED' and not events[-1]['fresh_requested']
assert 'HISTORICAL_REFERENCE_INTEGRITY_UNRESOLVED 7' in steps[-1]['stdout'] and read(output_path/'e4_capture.json')['elapsed_seconds']<300
git=lambda *args:subprocess.run(['git',*args],cwd=repository_path,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()=='2e04fbfd74c5b977be2d7345d2ae29c570173272' and git('branch','--show-current').decode().strip()=='main'
assert git('ls-tree','-r','--full-tree','HEAD')==(control_path/'old_git_tree.txt').read_bytes();git('diff','--quiet','HEAD','--')
state=file_hash(repository_path/'project_state.json');assert state=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
size=sum(p.stat().st_size for p in output_path.rglob('*') if p.is_file());assert size<16*1024**2
out={'schema':'NSP5_FINAL_PROPER_SOURCE_PRODUCT_EVIDENCE_REVIEW','preparations':preps,'preparation_bindings_authenticated':len(bindings),'source_copies_equal':len(copies),
 'accepted_completed_captures':sorted(accepted),'failed_captures_preserved':sorted(expected_failed),
 'completed_calculation_rejected_by_review':sorted(rejected),'late_preparer_failed_before_worker_launch':True,
 'shared_action_to_Gaussian_error_detected_by_third_route_and_corrected':True,
 'actual_model_source_derivative_program_unchanged_and_old3344_coefficients_match':True,
 'proper_source_integrable_extension_qualified_in_scope':True,'full_connected_W_products_qualified':False,
 'nonlinear_mean_tadpole_Legendre_response_remains_to_construct':True,
 'finite_A2_Ward_constraints_full_QAP_measure_E5_physical_claim':False,
 'largest_accepted_worker_private_sample':max(samples[n] for n in accepted),
 'largest_all_captures_private_sample':max(samples.values()),'packet_bytes_before_final_capture_and_seal':size,
 'evidence_validation':'PASS_BOUNDED_PROPER_NONMINIMAL_SOURCE_PRODUCT_CONSTRUCTION',
 'E4_step_exits':exits,'custody':'EXIT2_SEVEN_UNRESOLVED_NOTPASS','old_tracked_tree_and_state_unchanged':True,
 'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with(output_path/'final_review_result.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
