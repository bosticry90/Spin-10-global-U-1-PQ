from pathlib import Path
from hashlib import sha256
import ast,json,sys,time,traceback
output_path=Path(__file__).resolve().parent;repository_path=output_path.parents[1]
control_path=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/connected-source-sewing-v1-2026-10-26')
sys.path.insert(0,str(repository_path/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(path,value):
    with path.open('xb') as f:f.write((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    for name in ['E4_RECORD.md','run_e4.py']:
        path=output_path/name
        if path.suffix=='.py':ast.parse(path.read_bytes())
        with (output_path/(name+'.source.txt')).open('xb') as f:f.write(path.read_bytes())
    files=[repository_path/'AGENTS.md',repository_path/'project_state.json',repository_path/'tools/research_check.py',output_path/'E4_RECORD.md',output_path/'run_e4.py',output_path/'validation_receipt_v2.json',output_path/'RESULT.md']
    command=[sys.executable,'-B','tools/research_check.py','e4']
    dump(output_path/'e4_preparation.json',{'command':command,'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in files},'scientific_acceptance':'NOT_PERFORMED'})
    tick=time.perf_counter();result=capture(command);result['elapsed_seconds']=time.perf_counter()-tick
    dump(output_path/'e4_capture.json',result);dump(control_path/'e4_full_capture.json',result)
    assert result['exit_code']==0 and result['calculation_completed'] and result['post_run_observations_qualified'] and result['elapsed_seconds']<300
    events=[json.loads(line) for line in result['stdout_and_stderr'].splitlines() if line.startswith('{')]
    dump(output_path/'e4_events.json',events)
    print('E4 native0 '+json.dumps(events[-1],sort_keys=True),flush=True)
except BaseException:
    dump(output_path/'e4_controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
