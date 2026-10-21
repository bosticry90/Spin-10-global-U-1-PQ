"""GSA1 generic exclusive phase capture,with explicit completion gates."""
from pathlib import Path
from hashlib import sha256
import json,sys,re,gzip
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/ghost-scalar-sunset-v1-2026-10-20')
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
phase,label,script=sys.argv[1:4];assert all(re.fullmatch('[a-z0-9_]+',s0) for s0 in [phase,label])
source=HERE/script;assert source.parent==HERE
prep=json.loads((HERE/(phase+'_preparation.json')).read_bytes())
for p,h in prep['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
cap=HERE/f'{label}_{phase}_capture.json';assert not cap.exists()
sys.path.insert(0,str(ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
c=capture([sys.executable,'-B',str(source),*sys.argv[4:]]);dump(cap,c);dump(CONTROL/f'{label}_{phase}_full_capture.json',c)
print('TERMINAL_PHASE',label,phase,c['execution_state'],c['exit_code'],flush=True)
if c['exit_code']!=0:print(c['stdout_and_stderr'],flush=True)
assert c['execution_state']=='COMPLETED' and c['exit_code']==0 and c['calculation_completed'] and c['post_run_observations_qualified']
assert c['launch']['memory']['available_pagefile']>=prep['launch_floor'] and max(v['private_bytes'] for v in c['all_resource_samples'])<=prep['sampled_private_cap']
r=[json.loads(v[7:]) for v in c['stdout_and_stderr'].splitlines() if v.startswith('RESULT ')];assert len(r)==1 and r[0]['elapsed_after_imports']<prep['seconds_each'];v=r[0]
if 'receipt_filename' in v:
    p=HERE/v['receipt_filename'];assert p.parent==HERE and sha256(p.read_bytes()).hexdigest()==v['receipt_sha256']
else:
    p=HERE/f"{v['role']}_{v['kind']}_tables.json.gz";blob=p.read_bytes();assert sha256(blob).hexdigest()==v['packed_sha256'] and sha256(gzip.decompress(blob)).hexdigest()==v['tables_sha256']
dump(HERE/f'{label}_{phase}_result.json',v);print('COMPLETED_PHASE',label,phase,flush=True)
