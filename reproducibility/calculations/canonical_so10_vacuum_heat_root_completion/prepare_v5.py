from pathlib import Path
from hashlib import sha256
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()=='4ef90c58da071496672431008db417af9c94ae6c'
assert read(HERE/'heat_receipt_v4.json')['complete_selected_first_variation_identity'];bind=dict(read(HERE/'validation_preparation_v4.json')['input_sha256'])
for p in HERE.iterdir():
 if p.is_file():bind[str(p)]=digest(p)
JMF=CAL/'canonical_so10_joint_marginal_fermion_normalization';assert digest(JMF/'validation_receipt.json')=='668a24b045d8bd8b7391702c1e3915836a8ecbeb2c7add2ecf13bae1ab6b2039'
for n in ['validation_receipt.json','RECORD.md','DERIVATION.md','RESULT.md','data.py','primary.py','replay_v2.py','joint_selected_family.json.gz']:
 p=JMF/n
 if p.exists():bind[str(p)]=digest(p)
joint=json.loads(__import__('gzip').decompress((JMF/'joint_selected_family.json.gz').read_bytes()))
for k in ['bosonic_full_formula','HSC_family','CHW_family']:
 p=Path(joint[k]['path']);assert digest(p)==joint[k]['sha256'];bind[str(p)]=digest(p)
for n in ['JOINT_EXTENSION_V5.md','integrate_v5.py','prepare_v5.py','run_v5.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 bind[str(HERE/(n+'.source.txt'))]=digest(HERE/(n+'.source.txt'))
with (HERE/'preparation_v5.json').open('xb') as f:f.write((json.dumps({'schema':'VHR1_V5_PREPARATION','input_sha256':dict(sorted(bind.items())),'seconds_each':600,'private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('VHR1_V5_FROZEN',len(bind),'bindings',flush=True)
