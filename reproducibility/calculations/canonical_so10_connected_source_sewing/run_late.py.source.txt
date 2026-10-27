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
    bindings=dict(read(O/'adjoint_preparation_v2.json')['input_sha256'])
    for p,h in bindings.items():assert digest(Path(p))==h,p
    for p in list(O.iterdir()):
        if p.is_file() and str(p) not in bindings and p.suffix in ['.md','.py']:
            if p.suffix=='.py':ast.parse(p.read_bytes())
            with(O/(p.name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
    for p in O.iterdir():
        if p.is_file():bindings[str(p)]=digest(p)
    dump(O/'late_preparation.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    cap=capture([sys.executable,'-B',str(O/'late_verify.py')]);dump(O/'late_capture.json',cap);dump(C/'late_full_capture.json',cap)
    assert cap['exit_code']==0 and cap['execution_state']=='COMPLETED' and cap['calculation_completed'] and cap['post_run_observations_qualified']
    print('COMPLETED CNS1B independent adjoint reduction review',flush=True)
except BaseException:
    dump(O/'late_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
