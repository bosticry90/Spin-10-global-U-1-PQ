from pathlib import Path
from hashlib import sha256
import json,ast
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());b=dict(read(O/'preparation.json')['input_sha256'])
for p,h in b.items():assert H(Path(p))==h,p
assert read(O/'controller_failure.json')['stage']=='replay' and read(O/'replay_capture.json')['execution_state']=='FAILED' and not read(O/'replay_capture.json')['calculation_completed']
assert 'Object of type Integer is not JSON serializable' in read(O/'replay_capture.json')['stdout_and_stderr']
original=(O/'native.py').read_text(encoding='utf-8')
expected=original.replace('[[i,j,str(v)] for','[[int(i),int(j),str(v)] for',1).replace("read(O/'preparation.json')","read(O/'continuation_preparation_v2.json')",1).replace("(O/(role+'_tables.json.gz'))","(O/('replay_v2_tables.json.gz'))",1)
assert (O/'native_v2.py').read_text(encoding='utf-8')==expected
for n in ['CORRECTION_V2.md','native_v2.py','verify_v2.py','prepare_v2.py','run_v2.py','generate_v2.py']:
 p=O/n
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
 with(O/(n+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 b[str(p)]=H(p);b[str(O/(n+'.source.txt'))]=H(O/(n+'.source.txt'))
for n in ['preparation.json','preparation_capture.json','primary_result.json','primary_capture.json','primary_tables.json.gz','replay_capture.json','controller_failure.json']:b[str(O/n)]=H(O/n)
with(O/'continuation_preparation_v2.json').open('xb') as f:f.write((json.dumps({'input_sha256':b,'seconds_after_imports':180,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':12*1024**2,'original_replay':'FAILED_SERIALIZATION_NOT_RELABELLED','scientific_acceptance':'NOT_PERFORMED'},sort_keys=True)+'\n').encode())
print('PREPARED_NVT2',len(b),flush=True)
