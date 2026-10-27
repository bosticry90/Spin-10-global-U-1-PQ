from pathlib import Path
from hashlib import sha256
import ast,json,sys,traceback
output_path=Path(__file__).resolve().parent;repository_path=output_path.parents[1]
control_path=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-projected-ward-terms-v1-2026-10-26')
sys.path.insert(0,str(repository_path/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
file_hash=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
def dump(path,value):
    with path.open('xb') as f:f.write((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    bindings={}
    for prep in output_path.glob('*preparation*.json'):
        for path,digest in read(prep)['input_sha256'].items():
            assert file_hash(Path(path))==digest,path
            if path in bindings:assert bindings[path]==digest
            bindings[path]=digest
    for name in ['RESULT.md','EXECUTION_TIMING_ADDENDUM.md','FINAL_REVIEW_RECORD.md','final_review.py','run_final_review.py']:
        path=output_path/name
        if path.suffix=='.py':ast.parse(path.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in path.read_bytes().splitlines()),name
        with (output_path/(name+'.source.txt')).open('xb') as f:f.write(path.read_bytes())
    files=list(output_path.iterdir())+[repository_path/'docs/RESEARCH_EXECUTION_HANDOFF_V659.md',control_path/'old_git_tree.txt']
    for path in files:
        if path.is_file():bindings[str(path)]=file_hash(path)
    dump(output_path/'final_preparation.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    result=capture([sys.executable,'-B',str(output_path/'final_review.py')])
    dump(output_path/'final_review_capture.json',result);dump(control_path/'final_review_full_capture.json',result)
    assert result['exit_code']==0 and result['execution_state']=='COMPLETED' and result['calculation_completed'] and result['post_run_observations_qualified']
    review=read(output_path/'final_review_result.json');assert review['elapsed_after_imports']<180
    files=sorted([p for p in output_path.rglob('*') if p.is_file()]+[repository_path/'docs/RESEARCH_EXECUTION_HANDOFF_V659.md'])
    assert sum(p.stat().st_size for p in files)<16*1024**2
    hashes={str(p.relative_to(repository_path)).replace('\\','/'):file_hash(p) for p in files}
    receipt={'schema':'UWT4_FINAL_VALIDATION_AND_NEW_BYTE_SEAL','base_HEAD':'414a45fee0aa4b7c235bca0ff9ad9c06399cfc2a',
      'new_files_sha256':hashes,'final_review_result_sha256':file_hash(output_path/'final_review_result.json'),
      'evidence_validation':review['evidence_validation'],'selected_local_first_u_TF_Ward_relation_qualified_in_scope':True,
      'full_momentum_Ward_QAP_measure_E5_physical_claim':False,'E4_step_exits':review['E4_step_exits'],
      'custody':'EXIT2_SEVEN_UNRESOLVED_NOTPASS','state_sha256':review['state_sha256'],
      'largest_successful_sampled_private_bytes':max(review['largest_successful_sampled_private_bytes'],max(v['private_bytes'] for v in result['all_resource_samples'])),
      'new_files_bytes_excluding_this_receipt':sum(p.stat().st_size for p in files),
      'self_hash_excluded':True,'scientific_acceptance':'NOT_PERFORMED'}
    dump(output_path/'final_review_validation_receipt.json',receipt)
    print('SEALED UWT4 '+json.dumps({k:v for k,v in receipt.items() if k!='new_files_sha256'},sort_keys=True),flush=True)
except BaseException:
    dump(output_path/'final_review_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
