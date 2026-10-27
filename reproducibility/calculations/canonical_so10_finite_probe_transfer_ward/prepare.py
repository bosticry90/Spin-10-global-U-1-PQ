from pathlib import Path
from hashlib import sha256
import json,gzip,subprocess,ast
O=Path(__file__).resolve().parent;R=O.parents[1];read=lambda p:json.loads(p.read_bytes());H=lambda p:sha256(p.read_bytes()).hexdigest();b={};assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='36ced0de8f1570986cd21ff233ddc087112f455a'
N=O.parent/'canonical_so10_finite_probe_nielsen_ward';m=read(N/'review_preparation.json')['input_sha256']
for role in ['primary','replay']:
 ip=N/(role+'_inputs.json.gz');assert H(ip)==m[str(ip)];b[str(ip)]=H(ip)
 with(O/(role+'_inputs.json.gz')).open('xb') as f:f.write(ip.read_bytes())
 b[str(O/(role+'_inputs.json.gz'))]=H(O/(role+'_inputs.json.gz'))
for folder,ns in [('canonical_so10_finite_probe_nielsen_ward',['DERIVATION.md','REVIEW.md','RESULT.md','preparation.json','validation_preparation.json','review_preparation.json','validation_receipt.json','review_receipt.json']),('canonical_so10_even_probe_vertices',['DERIVATION.md','RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','validation_preparation.json']),('canonical_so10_probe_fermion_onejet',['DERIVATION.md','validation_receipt.json']),('canonical_so10_cutoff_source_ward_operator',['DERIVATION.md','RESULT.md','validation_receipt.json']),('canonical_so10_first_probe_local_module',['RESULT.md','validation_receipt.json'])]:
 for n in ns:
  p=O.parent/folder/n;b[str(p)]=H(p)
em=read(O.parent/'canonical_so10_even_probe_vertices/validation_preparation.json')['input_sha256']
for role in ['primary','replay']:
 p=O.parent/'canonical_so10_even_probe_vertices'/(role+'_tables.json.gz');assert H(p)==em[str(p)]
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V606.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']:
 p=R/n;b[str(p)]=H(p)
for n in ['RECORD.md','DERIVATION.md','native.py','verify.py','prepare.py','run.py']:
 p=O/n
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
 with(O/(n+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 b[str(p)]=H(p);b[str(O/(n+'.source.txt'))]=H(O/(n+'.source.txt'))
with(O/'preparation.json').open('xb') as f:f.write((json.dumps({'input_sha256':b,'seconds_after_imports':180,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':12*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True)+'\n').encode())
print('PREPARED_NVT1',len(b),flush=True)
