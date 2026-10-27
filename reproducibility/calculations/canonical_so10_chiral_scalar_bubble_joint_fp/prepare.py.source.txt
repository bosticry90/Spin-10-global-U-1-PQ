from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1];H=lambda p:sha256(p.read_bytes()).hexdigest();b={}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='15cbd4ae408566f21baa2b813c53cf298ab838df'
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V603.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']:
 p=R/n;b[str(p)]=H(p)
for folder,ns in [('canonical_so10_chiral_joint_heat_pilot',['DERIVATION.md','RESULT.md','validation_receipt_v3.json','review_receipt.json','primary_v2_tables.json.gz','replay_v2_tables.json.gz','validation_preparation_v3.json']),('canonical_so10_chiral_transverse_joint_limit',['DERIVATION.md','RESULT.md','validation_receipt.json','primary_tables.json.gz','replay_tables.json.gz','validation_preparation.json']),('canonical_so10_auxiliary_insertion_source_bubble',['DERIVATION.md','RESULT.md','validation_receipt.json']),('canonical_so10_closed_fermion_quadratic_heat',['DERIVATION.md','RESULT.md','validation_receipt.json']),('canonical_so10_matter_gauge_vertex_finite_units',['DERIVATION.md','validation_receipt.json']),('canonical_so10_two_probe_lifted_ward',['PROOF.md','validation_receipt_v2.json'])]:
 for n in ns:
  p=O.parent/folder/n;b[str(p)]=H(p)
for folder,manifest in [('canonical_so10_chiral_joint_heat_pilot','validation_preparation_v3.json'),('canonical_so10_chiral_transverse_joint_limit','validation_preparation.json')]:
 F=O.parent/folder;m=json.loads((F/manifest).read_bytes())['input_sha256']
 for p in F.glob('*tables.json.gz'):assert H(p)==m[str(p)],p
for n in ['RECORD.md','DERIVATION.md','prepare.py','native.py','verify.py','run.py']:
 p=O/n
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
 with(O/(n+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 b[str(p)]=H(p);b[str(O/(n+'.source.txt'))]=H(O/(n+'.source.txt'))
with(O/'preparation.json').open('xb') as f:f.write((json.dumps({'input_sha256':b,'seconds_after_imports':180,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':8*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True)+'\n').encode())
print('PREPARED_SBJ1',len(b),flush=True)
