"""HPR1 observed supplemental validation; no native replay."""
from pathlib import Path
from hashlib import sha256
import sys,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/hard-pole-remainder-v1-2026-10-21')
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
for p,h in json.loads((HERE/'supplement_preparation.json').read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
c=capture([sys.executable,'-B',str(HERE/'adversarial.py')]);dump(HERE/'adversarial_capture.json',c);dump(CONTROL/'adversarial_full_capture.json',c)
if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['post_run_observations_qualified'] and c['calculation_completed']
assert c['launch']['memory']['available_pagefile']>=350*1024**2 and max(v['private_bytes'] for v in c['all_resource_samples'])<=8*1024**3
v=[json.loads(z[7:]) for z in c['stdout_and_stderr'].splitlines() if z.startswith('RESULT ')];assert len(v)==1
assert v[0]['status']=='QUALIFIED_HPR1_MUTATION_CONTROLS' and v[0]['elapsed_after_imports']<600
dump(HERE/'adversarial_receipt.json',v[0]);assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file())<24*1024**2
print('adversarial COMPLETED',v[0]['elapsed_after_imports'],flush=True)
