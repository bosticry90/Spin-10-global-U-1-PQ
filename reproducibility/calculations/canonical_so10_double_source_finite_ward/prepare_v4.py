from pathlib import Path
from hashlib import sha256
import json,ast
HERE=Path(__file__).resolve().parent;dig=lambda p:sha256(p.read_bytes()).hexdigest();b=dict(json.loads((HERE/'validation_preparation_v3.json').read_bytes())['input_sha256'])
for p,h in b.items():assert dig(Path(p))==h,p
r=json.loads((HERE/'validation_receipt_v3.json').read_bytes());assert r['status']=='QUALIFIED_FULL_ACTUAL_FINITE_CONTACT_WARD_IMAGE_AND_TWO_SOURCE_DERIVATIVE_RELATION' and r['full_Ward_image_nonzero']==708732
assert not r['generic_z_GF_source_degree1_qualified']
for p in HERE.iterdir():
 if p.is_file():b[str(p)]=dig(p)
for n in ['GENERIC_W_EXTENSION_V4.md','orbit_data_v4.py','orbit_primary_v4.py','orbit_replay_v4.py','orbit_verify_v4.py','prepare_v4.py','run_v4.py']:
 p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(raw)
 b[str(HERE/(n+'.source.txt'))]=dig(HERE/(n+'.source.txt'))
with (HERE/'preparation_v4.json').open('xb') as f:f.write((json.dumps({'schema':'DSW1_V4_PREPARATION','input_sha256':dict(sorted(b.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'old_frozen_Ward_image_reused_not_rerun':True,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('DSW1_V4_FROZEN',len(b),'bindings',flush=True)
