"""Freeze completed-input supplementary controls, capture once, never mutate earlier evidence."""
from pathlib import Path
from hashlib import sha256
import ast,json,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-scalar-quartic-v1-2026-10-20')
def dump(p,v):
    with p.open('xb') as out:out.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
prep=json.loads((HERE/'validation_preparation.json').read_bytes());bindings=dict(prep['input_sha256'])
for n,h in bindings.items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
v=json.loads((HERE/'validation_receipt.json').read_bytes());assert v['status']=='QUALIFIED_VVSS_GRAPH_LOCAL_UV_AND_LIGHT_MATCHED_FINITE_F2'
for name in ['validation_preparation.json','validation_receipt.json','CONTROLS.md','controls.py','run_controls.py']:
    p=HERE/name;bb=p.read_bytes()
    if p.suffix=='.py':ast.parse(bb)
    if name in ['CONTROLS.md','controls.py','run_controls.py']:
        q=HERE/(name+'.source.txt')
        with q.open('xb') as out:out.write(bb)
        bindings[str(q)]=sha256(bb).hexdigest()
    bindings[str(p)]=sha256(bb).hexdigest()
dump(HERE/'control_preparation.json',{'schema':'VSP1_CONTROL_PREPARATION','input_sha256':dict(sorted(bindings.items())),
 'seconds':300,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'whole_package_cap':4*1024**2})
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
c=capture([sys.executable,'-B',str(HERE/'controls.py')]);dump(HERE/'controls_capture.json',c);dump(CONTROL/'controls_full_capture.json',c)
if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
assert c['execution_state']=='COMPLETED' and c['calculation_completed'] and c['post_run_observations_qualified']
assert c['all_resource_samples'] and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
assert c['launch']['memory']['available_pagefile']>=350*1024**2
records=[json.loads(x[7:]) for x in c['stdout_and_stderr'].splitlines() if x.startswith('RESULT ')];assert len(records)==1
result=records[0];assert result['elapsed_after_imports']<300
dump(HERE/'controls_receipt.json',result);print(json.dumps(result,sort_keys=True),flush=True)
