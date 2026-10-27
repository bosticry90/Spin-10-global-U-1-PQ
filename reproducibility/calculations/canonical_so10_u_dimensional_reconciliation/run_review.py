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
    bindings=dict(read(O/'preparation.json')['input_sha256'])
    for pp,h in bindings.items():assert H(Path(pp))==h,pp
    for name in ['REVIEW_RECORD.md','verify.py','run_review.py']:
        pp=O/name
        if pp.suffix=='.py':ast.parse(pp.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in pp.read_bytes().splitlines()),name
        with (O/(name+'.source.txt')).open('xb') as f:f.write(pp.read_bytes())
    for pp in O.iterdir():
        if pp.is_file():bindings[str(pp)]=H(pp)
    dump(O/'review_preparation.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    z=capture([sys.executable,'-B',str(O/'verify.py')]);dump(O/'review_capture.json',z);dump(C/'review_full_capture.json',z)
    assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified']
    assert read(O/'validation_receipt.json')['elapsed_after_imports']<180
    print('COMPLETED UDR2 scope and dimensional proof review',flush=True)
except BaseException:
    dump(O/'review_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
