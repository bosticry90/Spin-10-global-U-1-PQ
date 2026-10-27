from pathlib import Path
from hashlib import sha256
import ast,json,os,subprocess,threading,time
output_path=Path(__file__).resolve().parent;repository_path=output_path.parents[1]
control_path=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-projected-ward-terms-v1-2026-10-26')
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
file_hash=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
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
complete=[];largest=0
for path in sorted(output_path.glob('*capture*.json')):
    result=read(path)
    assert result['execution_state']=='COMPLETED' and result['exit_code']==0 and result['calculation_completed'] and result['post_run_observations_qualified'],path
    assert not result['failed_or_incomplete_counted_as_PASS'] and result['launch']['creation_after_observation']
    assert result['launch']['memory']['available_pagefile']>=350*1024**2
    assert result['all_resource_samples'] and all(0<v['private_bytes']<=8*1024**3 and 'query_error' not in v for v in result['all_resource_samples'])
    largest=max(largest,max(v['private_bytes'] for v in result['all_resource_samples']));complete.append(path.name)
assert set(complete)=={'audit_capture.json','review_capture.json','e4_capture.json'}
assert not list(output_path.glob('*controller_failure*.json'))
native=read(output_path/'ward_support_result.json');review=read(output_path/'validation_receipt.json')
assert native['elapsed_after_imports']<300 and review['elapsed_after_imports']<180
assert review['selected_local_finite_first_u_T_F_Ward_relation']=='QUALIFIED_WITHIN_INHERITED_FORMAL_DOMAIN'
assert review['paired_positive_heat_trace_step_before_FP_matched_to_UDR_domain']
assert review['no_arbitrary_finite_part_cyclicity_or_separate_trace_defect_zero_claim']
assert not review['full_momentum_Ward_functional_QAP_measure_E5_physical_claim']
assert native['hatted_master_insertion_projection_zero_before_integration'] and native['direct_supertrace_T_F_zero_by_actual_ports_and_dimension']
assert '4.2479' in (output_path/'RESULT.md').read_text()
addendum=(output_path/'EXECUTION_TIMING_ADDENDUM.md').read_text()
assert str(review['elapsed_after_imports']) in addendum and str(native['elapsed_after_imports']) in addendum
assert 'editorial transcription error' in addendum and 'No scientific execution failed' in addendum
events=read(output_path/'e4_events.json');steps=[v for v in events if v['event']=='step_finished']
exits=[v['exit_code'] for v in steps]
assert exits==[0,0,0,0,0,2] and events[-1]['execution_state']=='COMPLETED' and not events[-1]['fresh_requested']
assert 'HISTORICAL_REFERENCE_INTEGRITY_UNRESOLVED 7' in steps[-1]['stdout']
assert read(output_path/'e4_capture.json')['elapsed_seconds']<300
git=lambda *args:subprocess.run(['git',*args],cwd=repository_path,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()=='414a45fee0aa4b7c235bca0ff9ad9c06399cfc2a'
assert git('branch','--show-current').decode().strip()=='main'
assert git('ls-tree','-r','--full-tree','HEAD')==(control_path/'old_git_tree.txt').read_bytes()
git('diff','--quiet','HEAD','--')
state=file_hash(repository_path/'project_state.json');assert state=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
size=sum(p.stat().st_size for p in output_path.rglob('*') if p.is_file());assert size<16*1024**2
out={'schema':'UWT4_FINAL_PROJECTED_WARD_EVIDENCE_REVIEW','preparations':preps,
 'preparation_bindings_authenticated':len(bindings),'source_copies_equal':len(copies),
 'completed_captures_authenticated':complete,'scientific_worker_or_review_failures':0,
 'printed_runtime_error_preserved_with_receipt_correction':True,
 'native_seconds_after_imports':native['elapsed_after_imports'],'review_seconds_after_imports':review['elapsed_after_imports'],
 'largest_successful_sampled_private_bytes':largest,'packet_bytes_before_final_capture_and_seal':size,
 'evidence_validation':'PASS_BOUNDED_LOCAL_FIRST_U_T_F_WARD_RELATION',
 'scope':'original_unshifted_SMA_CSW_EDS;A0;constant_u;intrinsic1;local_relative_TF;Schwartz;positive_scalar_reference_masses;Euclidean_one_loop_directONEvariation;UV_FP_then_IR',
 'full_momentum_Ward_QAP_measure_E5_physical_claim':False,
 'E4_step_exits':exits,'custody':'EXIT2_SEVEN_UNRESOLVED_NOTPASS',
 'old_tracked_tree_and_state_unchanged':True,'state_sha256':state,
 'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with (output_path/'final_review_result.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
