"""MGN1 fixed input and source freeze, no authority or historical-policy rebind."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/matter-gauge-vertex-normalization-v1-2026-10-22');BASE='5ab95f81b3be33059fb0f9e9e3b152d63c731063'
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bind={}
def add(path,expected=None):
 path=path.resolve();hsh=sha256(path.read_bytes()).hexdigest()
 if expected is not None:assert hsh==expected,str(path)
 bind[str(path)]=hsh
for name in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V506.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:add(ROOT/name)
for name in ['export_a10_e5_antighost_vector.py','frozen_a10_physical_reconciliation/full_primary.json','frozen_a10_physical_reconciliation/full_replay.json']:add(PK/name)
for folder,names in {'canonical_so10_pure_gauge_matter_vertex_assembly':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','RESULT.md'],'canonical_so10_yukawa_dependent_gauge_vertices':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','sum_tables.json.gz','RESULT.md'],'canonical_so10_fermion_gauge_kinetic_pole':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_fermion_yukawa_self_energy':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_yukawa_carrier_transport':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_matter_field_source_image':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','RESULT.md'],'canonical_so10_matter_source_uv_assembly':['validation_receipt.json','RESULT.md'],'canonical_so10_matter_source_vertex_support':['validation_receipt.json','RESULT.md','SUPPORT_PROOF.md'],'canonical_so10_local_source_primitive':['primary_v2_result.json','replay_v2_result.json','validation_receipt.json'],'canonical_so10_sterile_matter_action':['ACTION_V1.md','primary.py','validation_receipt.json'],'canonical_so10_fermion_gauge_vertex_support':['RESULT.md','validation_receipt.json']}.items():
 for name in names:add(ROOT/'calculations'/folder/name)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8');add(ROOT/'calculations/canonical_so10_yukawa_dependent_gauge_vertices/validation_receipt.json','cbbfc2ae64e876bd99e7c8bf59b3bfb66b50f188ee2f6e0ea53d82d77907d3e6')
oldbase=ROOT/'calculations/canonical_so10_local_source_primitive';oldrec=json.loads((oldbase/'validation_receipt.json').read_bytes());assert oldrec['execution_state']=='COMPLETED'
for name in ['primary_v2_result.json','replay_v2_result.json']:
 path=(oldbase/name).resolve();assert bind[str(path)]==oldrec['input_sha256'][str(path)]
origin=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/yukawa-dependent-gauge-vertices-v1-2026-10-22')
for name in ['readiness.jsonl','readiness_stderr.txt','postcommit_seal.json']:add(origin/name)
for name in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 path=HERE/name;raw=path.read_bytes();assert b'\r' not in raw
 if path.suffix=='.py':ast.parse(raw)
 with (HERE/(name+'.source.txt')).open('xb') as handle:handle.write(raw)
 add(path);add(HERE/(name+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==30909
with (CONTROL/'old_git_tree.txt').open('xb') as handle:handle.write(tree)
with (HERE/'preparation.json').open('xb') as handle:handle.write((json.dumps({'schema':'MGN1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bind.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('MGN1_FROZEN',len(bind),'bindings',flush=True)
