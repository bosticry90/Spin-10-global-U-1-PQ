from pathlib import Path
from hashlib import sha256
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()=='4ef90c58da071496672431008db417af9c94ae6c'
assert read(HERE/'word_receipt_v2.json')['status']=='QUALIFIED_UNIVERSAL_HEAT_WORD_SPIN_COLOR_TEMPLATES_AND_CONSTANT_ROOT_PAIRS';bind=dict(read(HERE/'validation_preparation_v2.json')['input_sha256'])
for p in HERE.iterdir():
 if p.is_file():bind[str(p)]=digest(p)
for p in [CAL/'canonical_so10_cutoff_source_ward_operator/replay_inputs.json.gz',CAL/'canonical_so10_ghost_vertex_order_reconciliation/order_corrected_vacuum_family.json.gz',CAL/'canonical_so10_vacuum_tangent_source_finite/selected_vacuum_source_relative_member.json.gz',PK/'frozen_a10_physical_reconciliation/full_primary.json',PK/'frozen_a10_physical_reconciliation/full_replay.json']:
 bind[str(p)]=digest(p)
for n in ['COLOR_CONTRACT_V3.md','DOMAIN_REVIEW_V3.md','color_data_v3.py','color_primary_v3.py','color_replay_v3.py','verify_color_v3.py','prepare_v3.py','run_v3.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 bind[str(HERE/(n+'.source.txt'))]=digest(HERE/(n+'.source.txt'))
with (HERE/'preparation_v3.json').open('xb') as f:f.write((json.dumps({'schema':'VHR1_V3_PREPARATION','input_sha256':dict(sorted(bind.items())),'seconds_each':600,'private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('VHR1_V3_FROZEN',len(bind),'bindings',flush=True)
