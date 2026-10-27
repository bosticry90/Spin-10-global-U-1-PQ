from pathlib import Path
from hashlib import sha256
import ast,json,os,subprocess,threading,time
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/connected-source-sewing-v1-2026-10-26')
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
bindings={};preps=[]
for p in sorted(O.glob('*preparation*.json')):
    preps.append(p.name)
    for name,h in read(p)['input_sha256'].items():
        assert digest(Path(name))==h,(p.name,name)
        if name in bindings:assert bindings[name]==h
        bindings[name]=h
copies=list(O.glob('*.source.txt'))
for p in copies:assert p.read_bytes()==p.with_name(p.name[:-11]).read_bytes(),p
for p in O.glob('*.py'):ast.parse(p.read_bytes())
for p in O.iterdir():
    if p.suffix in ['.py','.md','.txt']:assert all(z==z.rstrip(b' \t') for z in p.read_bytes().splitlines()),p
failed={'review_capture.json':'assert i>=1241','adjoint_capture.json':"unhashable type: 'list'"}
accepted={'native_capture.json','review_capture_v2.json','adjoint_capture_v2.json','late_capture.json','e4_capture.json'}
seen=set();samples={}
for p in sorted(O.glob('*capture*.json')):
    cap=read(p);seen.add(p.name)
    assert not cap['failed_or_incomplete_counted_as_PASS'] and cap['launch']['creation_after_observation']
    assert cap['launch']['memory']['available_pagefile']>=350*1024**2
    assert cap['all_resource_samples'] and all('query_error' not in x and 0<x['private_bytes']<=8*1024**3 for x in cap['all_resource_samples'])
    samples[p.name]=max(x['private_bytes'] for x in cap['all_resource_samples'])
    if p.name in failed:
        assert cap['execution_state']=='FAILED' and cap['exit_code']!=0 and not cap['calculation_completed']
        assert failed[p.name] in cap['stdout_and_stderr']
    else:
        assert p.name in accepted and cap['execution_state']=='COMPLETED' and cap['exit_code']==0 and cap['calculation_completed'] and cap['post_run_observations_qualified']
assert seen==set(failed)|accepted
assert {p.name for p in O.glob('*controller_failure*.json')}=={'review_controller_failure.json','adjoint_controller_failure.json'}
assert not(O/'validation_receipt.json').exists() and not(O/'adjoint_result.json').exists()
native=read(O/'native_result.json');review=read(O/'validation_receipt_v2.json');adj=read(O/'adjoint_result_v2.json');late=read(O/'late_validation_receipt.json')
assert native['elapsed_after_imports']<300 and adj['elapsed_after_imports']<300
assert review['elapsed_after_imports']<180 and late['elapsed_after_imports']<180
assert native['full_connected_distributional_extension']==review['full_connected_extension']==adj['full_connected_extension']=='NOT_ESTABLISHED'
assert review['native_background_covariance_interpretation']=='NOT_ACCEPTED_SEE_CLARIFICATION'
assert adj['adjoint_invariant_dimension']==2 and adj['restricted_BRST_invariant_dimension']==13
assert adj['adjoint_invariants_in_restricted_BRST_annihilator'] and late['exact_adjoint_rank']==43
assert all(z['difference_rows']==0 for z in late['source_Euler_and_spatial_divergence_replay'])
assert late['actual_tadpole_membership_and_complete_mean_response']=='NOT_ESTABLISHED'
assert not late['full_connected_QAP_or_physical_claim']
assert review['delta_smoothing_path_limits']==['0','11/18','1'] and review['proper_before_sewing_finite_difference']=='T1*a'
assert 'NOT accepted as covariance theorems' in (O/'COVARIANCE_CLARIFICATION.md').read_text()
assert 'Focused result-to-claim assessment' in (O/'RESULT.md').read_text()
events=read(O/'e4_events.json');steps=[x for x in events if x['event']=='step_finished'];exits=[x['exit_code'] for x in steps]
assert exits==[0,0,0,0,0,2] and events[-1]['execution_state']=='COMPLETED' and not events[-1]['fresh_requested']
assert 'HISTORICAL_REFERENCE_INTEGRITY_UNRESOLVED 7' in steps[-1]['stdout'] and read(O/'e4_capture.json')['elapsed_seconds']<300
git=lambda *args:subprocess.run(['git',*args],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()=='1e6344f26c0978ec74472584e8654f571b0804d1'
assert git('branch','--show-current').decode().strip()=='main'
assert git('ls-tree','-r','--full-tree','HEAD')==(C/'old_git_tree.txt').read_bytes()
git('diff','--quiet','HEAD','--')
state=digest(R/'project_state.json');assert state=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
size=sum(p.stat().st_size for p in O.rglob('*') if p.is_file());assert size<16*1024**2
out={'schema':'CNS_FINAL_EVIDENCE_REVIEW','evidence_validation':'PASS_BOUNDED_SOURCE_ENDPOINT_AND_NONLINEAR_SEWING_ALGEBRA',
 'preparations':preps,'input_bindings_authenticated':len(bindings),'source_copies_equal':len(copies),
 'accepted_completed_captures':sorted(accepted),'failed_captures_preserved':sorted(failed),
 'auxiliary_background_label_not_accepted_and_separate_adjoint_result_checked':True,
 'actual_source_endpoint_domain_and_nonlinear_finite_identity_qualified_in_scope':True,
 'actual_tadpole_membership_complete_regulated_mean_and_connected_extension':False,
 'full_QAP_E5_A5_physical_or_external_theorem_promotion':False,
 'E4_step_exits':exits,'custody':'EXIT2_SEVEN_UNRESOLVED_NOTPASS','state_sha256':state,
 'old_tracked_tree_and_state_unchanged':True,'largest_accepted_worker_private_sample':max(samples[p] for p in accepted),
 'largest_all_captures_private_sample':max(samples.values()),'packet_bytes_before_final_capture_and_seal':size,
 'elapsed_after_imports':time.perf_counter()-tick,'scientific_acceptance':'NOT_PERFORMED'}
with(O/'final_review_result.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
