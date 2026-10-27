from pathlib import Path
from hashlib import sha256
import ast,json,gzip
HERE=Path(__file__).resolve().parent;dig=lambda p:sha256(p.read_bytes()).hexdigest();b=dict(json.loads((HERE/'preparation_v2.json').read_bytes())['input_sha256'])
for p,h in b.items():assert dig(Path(p))==h,p
c=json.loads((HERE/'primary_v2_capture.json').read_bytes());assert c['exit_code']==0 and c['execution_state']=='COMPLETED' and c['calculation_completed']
r=json.loads((HERE/'primary_v2_result.json').read_bytes());raw=(HERE/'primary_v2_tables.json.gz').read_bytes();assert sha256(raw).hexdigest()==r['packed_sha256'] and sha256(gzip.decompress(raw)).hexdigest()==r['tables_sha256']
failed=json.loads((HERE/'replay_v2_capture.json').read_bytes());assert failed['exit_code']==1 and "KeyError: 'architecture'" in failed['stdout_and_stderr'] and not failed['calculation_completed']
assert not any((HERE/n).exists() for n in ['replay_v2_tables.json.gz','verify_v2_capture.json','validation_preparation_v2.json','validation_receipt_v2.json'])
for p in HERE.iterdir():
 if p.is_file():b[str(p)]=dig(p)
for n in ['CONTINUATION_V3.md','data_v3.py','replay_v3.py','verify_v3.py','prepare_v3.py','run_v3.py']:
 p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(raw)
 b[str(HERE/(n+'.source.txt'))]=dig(HERE/(n+'.source.txt'))
with (HERE/'preparation_v3.json').open('xb') as f:f.write((json.dumps({'schema':'DSW1_V3_PREPARATION','input_sha256':dict(sorted(b.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'completed_primary_v2_reused_not_rerun':True,'original_failures_preserved':True,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('DSW1_V3_FROZEN',len(b),'bindings; completed primary reused',flush=True)
