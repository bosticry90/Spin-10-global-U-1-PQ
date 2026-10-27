from pathlib import Path
from hashlib import sha256
import ast,json,sys,traceback
repository_path=Path(__file__).resolve().parents[2];output_path=Path(__file__).resolve().parent
control_path=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/nonminimal-source-products-v1-2026-10-26')
sys.path.insert(0,str(repository_path/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
file_hash=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
def dump(path,value):
    with path.open('xb') as f:f.write((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    bindings=dict(read(output_path/'review_preparation.json')['input_sha256'])
    for path,digest in bindings.items():assert file_hash(Path(path))==digest,path
    failed=read(output_path/'review_capture.json');assert failed['execution_state']=='FAILED' and failed['exit_code']!=0 and not failed['calculation_completed']
    assert 'SHARED_ACTION_TO_HESSIAN_CONVENTION_MISMATCH' in failed['stdout_and_stderr'] and not (output_path/'validation_receipt.json').exists()
    for name in ['GAUSSIAN_CORRECTION_V3.md','finite_algebra_v2.py','audit_v3.py','run_v3.py']:
        path=output_path/name
        if path.suffix=='.py':ast.parse(path.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in path.read_bytes().splitlines()),name
        with(output_path/(name+'.source.txt')).open('xb') as f:f.write(path.read_bytes())
    for path in output_path.iterdir():
        if path.is_file() and path.name!='verify_v2.py':bindings[str(path)]=file_hash(path)
    dump(output_path/'preparation_v3.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    result=capture([sys.executable,'-B',str(output_path/'audit_v3.py')])
    dump(output_path/'audit_capture_v3.json',result);dump(control_path/'audit_full_capture_v3.json',result)
    assert result['exit_code']==0 and result['execution_state']=='COMPLETED' and result['calculation_completed'] and result['post_run_observations_qualified']
    assert read(output_path/'product_result_v3.json')['elapsed_after_imports']<300
    print('COMPLETED NSP1 V3 action-correct source products',flush=True)
except BaseException:
    dump(output_path/'controller_failure_v3.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
