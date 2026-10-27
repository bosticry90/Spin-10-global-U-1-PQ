from pathlib import Path
from hashlib import sha256
import ast,json
HERE=Path(__file__).resolve().parent;dig=lambda p:sha256(p.read_bytes()).hexdigest();b=dict(json.loads((HERE/'preparation.json').read_bytes())['input_sha256'])
for p,h in b.items():assert dig(Path(p))==h,p
c=json.loads((HERE/'primary_capture.json').read_bytes());assert c['exit_code']==1 and "UNCLASSIFIED_AUXILIARY_EULER" in c['stdout_and_stderr'] and "('Ap0_0', (0,))" in c['stdout_and_stderr'] and not c['calculation_completed']
assert not any((HERE/n).exists() for n in ['primary_tables.json.gz','replay_capture.json','verify_capture.json','validation_preparation.json','validation_receipt.json'])
for p in HERE.iterdir():
 if p.is_file():b[str(p)]=dig(p)
for n in ['CONTINUATION_V2.md','data_v2.py','primary_v2.py','replay_v2.py','verify_v2.py','prepare_v2.py','run_v2.py']:
 p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(raw)
 b[str(HERE/(n+'.source.txt'))]=dig(HERE/(n+'.source.txt'))
with (HERE/'preparation_v2.json').open('xb') as f:f.write((json.dumps({'schema':'DSW1_V2_PREPARATION','input_sha256':dict(sorted(b.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'original_failure_preserved':True,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('DSW1_V2_FROZEN',len(b),'bindings',flush=True)
