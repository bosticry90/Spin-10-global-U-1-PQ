from pathlib import Path
from hashlib import sha256
import ast,json,sys,traceback
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/connected-source-sewing-v1-2026-10-26')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    bindings={}
    for prep in O.glob('*preparation*.json'):
        for name,h in read(prep)['input_sha256'].items():
            assert digest(Path(name))==h,(prep.name,name)
            if name in bindings:assert bindings[name]==h
            bindings[name]=h
    for p in list(O.iterdir()):
        if p.suffix in ['.py','.md'] and not (O/(p.name+'.source.txt')).exists():
            if p.suffix=='.py':ast.parse(p.read_bytes())
            with(O/(p.name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
    for p in list(O.iterdir())+[R/'docs/RESEARCH_EXECUTION_HANDOFF_V661.md',C/'old_git_tree.txt']:
        if p.is_file():bindings[str(p)]=digest(p)
    dump(O/'final_preparation.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    cap=capture([sys.executable,'-B',str(O/'final_review.py')]);dump(O/'final_review_capture.json',cap);dump(C/'final_review_full_capture.json',cap)
    assert cap['exit_code']==0 and cap['execution_state']=='COMPLETED' and cap['calculation_completed'] and cap['post_run_observations_qualified']
    review=read(O/'final_review_result.json');assert review['elapsed_after_imports']<180
    files=sorted([p for p in O.rglob('*') if p.is_file()]+[R/'docs/RESEARCH_EXECUTION_HANDOFF_V661.md'])
    assert sum(p.stat().st_size for p in files)<16*1024**2
    receipt={'schema':'CNS_FINAL_VALIDATION_AND_NEW_BYTE_SEAL','base_HEAD':'1e6344f26c0978ec74472584e8654f571b0804d1',
      'new_files_sha256':{p.relative_to(R).as_posix():digest(p) for p in files},
      'evidence_validation':review['evidence_validation'],'full_connected_QAP_E5_physical_claim':False,
      'E4_step_exits':review['E4_step_exits'],'custody':review['custody'],'state_sha256':review['state_sha256'],
      'largest_accepted_worker_private_sample':max(review['largest_accepted_worker_private_sample'],max(x['private_bytes'] for x in cap['all_resource_samples'])),
      'largest_all_captures_private_sample':max(review['largest_all_captures_private_sample'],max(x['private_bytes'] for x in cap['all_resource_samples'])),
      'new_files_bytes_excluding_this_receipt':sum(p.stat().st_size for p in files),
      'scientific_acceptance':'NOT_PERFORMED','self_hash_excluded':True}
    dump(O/'final_review_validation_receipt.json',receipt)
    print('SEALED '+json.dumps({k:v for k,v in receipt.items() if k!='new_files_sha256'},sort_keys=True),flush=True)
except BaseException:
    dump(O/'final_review_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
