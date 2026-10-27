from pathlib import Path
from hashlib import sha256
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()=='4ef90c58da071496672431008db417af9c94ae6c'
assert read(HERE/'validation_receipt.json')['status']=='QUALIFIED_COMPLETE_EXTRA_GF_VACUUM_ORDERED_HEAT_ROOT_SUPPORT';bind=dict(read(HERE/'validation_preparation.json')['input_sha256'])
for p in HERE.iterdir():
 if p.is_file():bind[str(p)]=digest(p)
for n in ['COEFFICIENT_CONTRACT_V2.md','free_words_v2.py','paired_words_v2.py','verify_words_v2.py','prepare_v2.py','run_v2.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 bind[str(HERE/(n+'.source.txt'))]=digest(HERE/(n+'.source.txt'))
with (HERE/'preparation_v2.json').open('xb') as f:f.write((json.dumps({'schema':'VHR1_V2_PREPARATION','input_sha256':dict(sorted(bind.items())),'seconds_each':600,'private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('VHR1_V2_FROZEN',len(bind),'bindings',flush=True)
