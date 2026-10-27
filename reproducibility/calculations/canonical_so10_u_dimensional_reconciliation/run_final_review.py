from pathlib import Path
from hashlib import sha256
import ast,json,sys,traceback
O=Path(__file__).resolve().parent;R=O.parents[1]
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-dimensional-reconciliation-v1-2026-10-26')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
def dump(p,z):
    with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    bindings={}
    for prep in O.glob('*preparation*.json'):
        for pp,h in read(prep)['input_sha256'].items():
            assert H(Path(pp))==h,pp
            if pp in bindings:assert bindings[pp]==h
            bindings[pp]=h
    for name in ['RESULT.md','FINAL_REVIEW_RECORD.md','final_review.py','run_final_review.py']:
        pp=O/name
        if pp.suffix=='.py':ast.parse(pp.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in pp.read_bytes().splitlines()),name
        with (O/(name+'.source.txt')).open('xb') as f:f.write(pp.read_bytes())
    files=list(O.iterdir())+[R/'docs/RESEARCH_EXECUTION_HANDOFF_V658.md',C/'old_git_tree.txt',
      R/'calculations/canonical_so10_unprobed_log3_support/T_log3_complete_comparison_v2.json.gz',
      R/'calculations/canonical_so10_unprobed_marginal_C3/F_log3_complete_comparison.json.gz']
    for pp in files:
        if pp.is_file():bindings[str(pp)]=H(pp)
    dump(O/'final_preparation.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    z=capture([sys.executable,'-B',str(O/'final_review.py')]);dump(O/'final_review_capture.json',z);dump(C/'final_review_full_capture.json',z)
    assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified']
    result=read(O/'final_review_result.json');assert result['elapsed_after_imports']<180
    files=sorted([p for p in O.rglob('*') if p.is_file()]+[R/'docs/RESEARCH_EXECUTION_HANDOFF_V658.md'])
    assert sum(p.stat().st_size for p in files)<16*1024**2
    hashes={str(p.relative_to(R)).replace('\\','/'):H(p) for p in files}
    receipt={'schema':'UDR5_FINAL_VALIDATION_AND_NEW_BYTE_SEAL','base_HEAD':'a78b35931a67863375cbd969df27b972df6ced6a',
      'new_files_sha256':hashes,'final_review_result_sha256':H(O/'final_review_result.json'),'evidence_validation':'PASS_BOUNDED_COMPLETE_LOCAL_SYMBOL_AND_FIRST_U_DOMAIN',
      'full_Ward_QAP_E5_or_physical_claim':False,'full_finite_quantum_Ward_terms_remain_open':True,'E4_step_exits':result['E4_step_exits'],
      'custody':'EXIT2_SEVEN_UNRESOLVED_NOTPASS','state_sha256':result['state_sha256'],
      'largest_successful_sampled_private_bytes':max(result['largest_successful_sampled_private_bytes'],max(v['private_bytes'] for v in z['all_resource_samples'])),
      'new_files_bytes_excluding_this_receipt':sum(p.stat().st_size for p in files),'self_hash_excluded':True,'scientific_acceptance':'NOT_PERFORMED'}
    dump(O/'final_review_validation_receipt.json',receipt)
    print('SEALED UDR5 '+json.dumps({k:v for k,v in receipt.items() if k!='new_files_sha256'},sort_keys=True),flush=True)
except BaseException:
    dump(O/'final_review_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
