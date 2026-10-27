from pathlib import Path
from hashlib import sha256
import ast,json,os,subprocess,threading,time
O=Path(__file__).resolve().parent;R=O.parents[1]
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-dimensional-reconciliation-v1-2026-10-26')
tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
file_hash=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
bindings={};preps=[]
for prep in sorted(O.glob('*preparation*.json')):
    preps.append(prep.name)
    for pp,h in read(prep)['input_sha256'].items():
        assert file_hash(Path(pp))==h,(prep.name,pp)
        if pp in bindings:assert bindings[pp]==h
        bindings[pp]=h
copies=list(O.glob('*.source.txt'))
for pp in copies:assert pp.read_bytes()==pp.with_name(pp.name[:-11]).read_bytes(),pp
for pp in O.glob('*.py'):ast.parse(pp.read_bytes())
for pp in O.iterdir():
    if pp.suffix in ['.py','.md','.txt']:assert all(line==line.rstrip(b' \t') for line in pp.read_bytes().splitlines()),pp
failures={'review_capture.json':'AssertionError','ir_capture.json':"unsupported operand type(s) for /: 'dict' and 'str'",'ir_review_capture.json':"'list' object is not callable"}
complete=[];failed=[];largest=0
for pp in sorted(O.glob('*capture*.json')):
    z=read(pp)
    assert not z['failed_or_incomplete_counted_as_PASS'] and z['launch']['creation_after_observation']
    assert z['launch']['memory']['available_pagefile']>=350*1024**2
    assert z['all_resource_samples'] and all(0<v['private_bytes']<=8*1024**3 and 'query_error' not in v for v in z['all_resource_samples'])
    if pp.name in failures:
        assert z['execution_state']=='FAILED' and z['exit_code']!=0 and not z['calculation_completed'] and failures[pp.name] in z['stdout_and_stderr'];failed.append(pp.name)
    else:
        assert z['execution_state']=='COMPLETED' and z['exit_code']==0 and z['calculation_completed'] and z['post_run_observations_qualified'],pp
        largest=max(largest,max(v['private_bytes'] for v in z['all_resource_samples']));complete.append(pp.name)
assert set(failed)==set(failures) and len(complete)==5
assert set(p.name for p in O.glob('*controller_failure*.json'))=={'review_controller_failure.json','ir_controller_failure.json','ir_review_controller_failure.json'}
assert not (O/'validation_receipt.json').exists() and not (O/'ir_support_result.json').exists() and not (O/'ir_validation_receipt.json').exists()
for name in ['audit_result','ir_support_result_v2']:assert read(O/(name+'.json'))['elapsed_after_imports']<300
for name in ['validation_receipt_v2','ir_validation_receipt_v2']:assert read(O/(name+'.json'))['elapsed_after_imports']<180
d=read(O/'validation_receipt_v2.json');i=read(O/'ir_validation_receipt_v2.json');s=read(O/'ir_support_result_v2.json')
assert d['four_stages_and_ten_native_root_domains_match'] and d['complete_declared_local_relative_T_F_symbol_zero'] and d['sixteen_prior_complete_coefficient_sums_authenticated']==16
assert not d['full_continuum_trace_product_QAP_E5_claim']
assert i['first_u_direct_one_variation_common_trace_extension_within_scope'] and i['arbitrary_old_constant_chain_closure_proved_by_nonpositive_cycles']
assert i['V1_failure_preserved_not_PASS_and_exact_alias_fix_checked'] and not i['two_independent_insertions_full_QAP_measure_or_physical_claim']
assert s['first_u_soft_bound_disposition']=='MATCHES_INHERITED_STRICT_NODE_BOUNDS' and all(z['new_edge_maximum_pole']==2 and z['one_tangent_maximum_merged_pole']==3 for z in s['results'])
events=read(O/'e4_events.json');steps=[z for z in events if z['event']=='step_finished']
assert [z['exit_code'] for z in steps]==[0,0,0,0,0,2] and events[-1]['execution_state']=='COMPLETED' and not events[-1]['fresh_requested']
assert 'HISTORICAL_REFERENCE_INTEGRITY_UNRESOLVED 7' in steps[-1]['stdout'] and read(O/'e4_capture.json')['elapsed_seconds']<300
git=lambda *args:subprocess.run(['git',*args],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()=='a78b35931a67863375cbd969df27b972df6ced6a' and git('branch','--show-current').decode().strip()=='main'
assert git('ls-tree','-r','--full-tree','HEAD')==(C/'old_git_tree.txt').read_bytes();git('diff','--quiet','HEAD','--')
state=file_hash(R/'project_state.json');assert state=='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
size=sum(p.stat().st_size for p in O.rglob('*') if p.is_file());assert size<16*1024**2
out={'schema':'UDR5_FINAL_DIMENSIONAL_AND_FIRST_U_DOMAIN_REVIEW','preparation_bindings_authenticated':len(bindings),'preparations':preps,'source_copies_equal':len(copies),
 'completed_captures_authenticated':complete,'failed_captures_preserved_not_PASS':failed,'largest_successful_sampled_private_bytes':largest,
 'packet_bytes_before_final_capture_and_seal':size,'bounded_evidence_validation':'PASS_MATCHED_DIMENSIONAL_CLOSURE_AND_FIRST_U_TRACE_DOMAIN',
 'complete_declared_local_T_F_symbol_zero':True,'first_u_trace_domain_scope':'positive_scalar_reference_masses;Schwartz;EuclideanA0;intrinsic0/1;UV_FP_then_IR;directONEvariation',
 'full_quantum_Ward_QAP_E5_or_physical_claim':False,'E4_step_exits':[z['exit_code'] for z in steps],'custody':'EXIT2_SEVEN_UNRESOLVED_NOTPASS',
 'old_tracked_tree_and_state_unchanged':True,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED','elapsed_after_imports':time.perf_counter()-tick}
with (O/'final_review_result.json').open('xb') as f:f.write((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode())
print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
