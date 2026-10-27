"""OFK1 byte and source freeze before scientific workers."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/open-fermion-finite-kinetic-v1-2026-10-22');BASE='7db0a6cbbcffc14009e7641afcfb4e9d5d408a78'
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bind={}
def add(p,expected=None):
 p=p.resolve();h=sha256(p.read_bytes()).hexdigest()
 if expected:assert h==expected,str(p)
 bind[str(p)]=h
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V514.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:add(ROOT/n)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8');add(PK/'export_a10_e5_antighost_vector.py')
deps={'canonical_so10_sterile_matter_action':(['ACTION_V1.md','validation_receipt.json'],'21d4816d5ea079b28b41783e8d65aa3bd52d779349c90106d4dec5e99e10bd41'),
 'canonical_so10_sterile_massive_propagator':(['RESULT.md','validation_receipt.json'],'53a99e56ee95c247efd4e07d3ff7a4fb8817d284dd4f7a0cbfc63f449495c25c'),
 'canonical_so10_yukawa_carrier_transport':(['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'4e39b499d32e4203c1d159e5946abfaf9adb05552e9a43c3005c8ee04eee312b'),
 'canonical_so10_fermion_gauge_kinetic_pole':(['RECORD.md','RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'d29b95ea3d6d463f765fe940a1cc25a89cd62d04bf0ba8e0efc94157f8ffd376'),
 'canonical_so10_fermion_yukawa_self_energy':(['RECORD.md','RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'960dd63d9aacb2a8ef30bb13b029470458c0cfef761db7f758945e101e44b3b8'),
 'canonical_so10_scalar_yukawa_reference':(['DERIVATION.md','RESULT.md','validation_receipt.json'],'f4e94141cb63ee12ac955b3460ced5a4b1cadd3b76a1d3047ae8a138b63c42a7'),
 'canonical_so10_bosonic_fermion_finite_ward':(['RECORD.md','RESULT.md','validation_receipt.json'],'49a9e814cde68fd165d1d42732cc12b2fc1421be8407b48290da23d0c65a6e0a')}
for folder,(names,receipt) in deps.items():
 for n in names:add(ROOT/'calculations'/folder/n,receipt if n=='validation_receipt.json' else None)
for ident in ['cd7c60f9-60ac-40e2-ad7b-f76925b47a3f','c3dc08cd-3864-4f1d-87e0-52d7ee3c1554']:add(Path('C:/Users/psboy/.codex/attachments')/ident/'Pasted text.txt')
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(n+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==31149
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'OFK1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bind.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('OFK1_FROZEN',len(bind),'bindings',flush=True)
