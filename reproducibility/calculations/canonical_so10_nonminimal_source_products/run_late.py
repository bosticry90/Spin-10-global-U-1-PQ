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
    bindings=dict(read(output_path/'review_preparation_v2.json')['input_sha256'])
    for path,digest in bindings.items():assert file_hash(Path(path))==digest,path
    for name in ['LATE_SEAGULL_REVIEW.md','late_seagull.py','run_late.py']:
        path=output_path/name
        if path.suffix=='.py':ast.parse(path.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in path.read_bytes().splitlines()),name
        with(output_path/(name+'.source.txt')).open('xb') as f:f.write(path.read_bytes())
    root=repository_path/'calculations/canonical_so10_remaining_u_contact_vertices'
    seal=read(root/'final_review_validation_receipt.json')['new_files_sha256']
    for name in ['vertices_primary_tables.json.gz','vertices_replay_tables.json.gz','vertices_v2.py']:
        path=root/name;assert file_hash(path)==seal[str(path.relative_to(repository_path)).replace('\\','/')];bindings[str(path)]=file_hash(path)
    for path in output_path.iterdir():
        if path.is_file():bindings[str(path)]=file_hash(path)
    dump(output_path/'late_preparation.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    result=capture([sys.executable,'-B',str(output_path/'late_seagull.py')])
    dump(output_path/'late_capture.json',result);dump(control_path/'late_full_capture.json',result)
    assert result['exit_code']==0 and result['execution_state']=='COMPLETED' and result['calculation_completed'] and result['post_run_observations_qualified']
    print('COMPLETED NSP3 late actual seagull review',flush=True)
except BaseException:
    dump(output_path/'late_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
