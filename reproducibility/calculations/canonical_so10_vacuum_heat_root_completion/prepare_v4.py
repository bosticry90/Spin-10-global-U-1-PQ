from pathlib import Path
from hashlib import sha256
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vacuum-heat-root-completion-v1-2026-10-24');read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()=='4ef90c58da071496672431008db417af9c94ae6c'
assert read(HERE/'controller_failure_v3.json')['last_role']=='color_replay_v3' and read(HERE/'color_replay_v3_capture.json')['exit_code']==1
assert "KeyError: 'primitive_orbit_at_v'" in read(HERE/'color_replay_v3_capture.json')['stdout_and_stderr'] and read(HERE/'color_primary_v3_capture.json')['exit_code']==0
assert not (HERE/'heat_receipt_v3.json').exists() and not (HERE/'color_replay_v3_tables.json.gz').exists()
bind=dict(read(HERE/'preparation_v3.json')['input_sha256'])
for p in HERE.iterdir():
 if p.is_file():bind[str(p)]=digest(p)
for p in [PK/'frozen_a10_e1_fermion/replay.json',CONTROL/'make_v4_sources.py']:bind[str(p)]=digest(p)
for n in ['CONTINUATION_V4.md','color_data_v4.py','color_replay_v4.py','verify_color_v4.py','prepare_v4.py','run_v4.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 bind[str(HERE/(n+'.source.txt'))]=digest(HERE/(n+'.source.txt'))
with (HERE/'preparation_v4.json').open('xb') as f:f.write((json.dumps({'schema':'VHR1_V4_PREPARATION','input_sha256':dict(sorted(bind.items())),'seconds_each':600,'private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('VHR1_V4_FROZEN',len(bind),'bindings',flush=True)
