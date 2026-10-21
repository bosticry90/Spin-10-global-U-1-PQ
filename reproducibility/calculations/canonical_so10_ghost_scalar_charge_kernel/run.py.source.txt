"""GSK1 exclusive native output capture; independent role ownership."""
from pathlib import Path
from hashlib import sha256
import json,sys,gzip
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/ghost-scalar-charge-kernel-v1-2026-10-20')
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
role=sys.argv[1];assert role in ['primary','replay']
for p,h in json.loads((HERE/'preparation.json').read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
assert not (HERE/f'{role}_capture.json').exists()
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
c=capture([sys.executable,'-B',str(HERE/'measure.py'),role]);dump(HERE/f'{role}_capture.json',c);dump(CONTROL/f'{role}_full_capture.json',c)
print('TERMINAL',role,c['execution_state'],c['exit_code'],flush=True)
if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
assert c['execution_state']=='COMPLETED' and c['calculation_completed'] and c['post_run_observations_qualified']
assert c['launch']['memory']['available_pagefile']>=350*1024**2 and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
r=[json.loads(v[7:]) for v in c['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(r)==1 and r[0]['elapsed_after_imports']<600
blob=(HERE/f'{role}_tables.json.gz').read_bytes();assert sha256(gzip.decompress(blob)).hexdigest()==r[0]['tables_sha256']
dump(HERE/f'{role}_result.json',r[0]);print('COMPLETED_NATIVE',role,flush=True)
