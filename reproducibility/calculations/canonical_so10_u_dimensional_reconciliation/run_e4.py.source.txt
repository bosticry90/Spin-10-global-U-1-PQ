from pathlib import Path
from hashlib import sha256
import ast,json,sys,time,traceback
O=Path(__file__).resolve().parent;R=O.parents[1]
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-dimensional-reconciliation-v1-2026-10-26')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,z):
    with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    assert not (O/'e4_capture.json').exists() and not (O/'e4_preparation.json').exists()
    for name in ['E4_RECORD.md','run_e4.py']:
        pp=O/name
        if pp.suffix=='.py':ast.parse(pp.read_bytes())
        with (O/(name+'.source.txt')).open('xb') as f:f.write(pp.read_bytes())
    files=[R/'AGENTS.md',R/'project_state.json',R/'tools/research_check.py',O/'E4_RECORD.md',O/'run_e4.py',O/'ir_validation_receipt_v2.json',O/'RESULT.md']
    command=[sys.executable,'-B','tools/research_check.py','e4']
    dump(O/'e4_preparation.json',{'command':command,'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in files},'scientific_acceptance':'NOT_PERFORMED'})
    tick=time.perf_counter();z=capture(command);z['elapsed_seconds']=time.perf_counter()-tick
    dump(O/'e4_capture.json',z);dump(C/'e4_full_capture.json',z)
    assert z['exit_code']==0 and z['calculation_completed'] and z['post_run_observations_qualified'] and z['elapsed_seconds']<300
    events=[json.loads(line) for line in z['stdout_and_stderr'].splitlines() if line.startswith('{')];dump(O/'e4_events.json',events)
    print('E4 native0 '+json.dumps(events[-1],sort_keys=True),flush=True)
except BaseException:
    dump(O/'e4_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
