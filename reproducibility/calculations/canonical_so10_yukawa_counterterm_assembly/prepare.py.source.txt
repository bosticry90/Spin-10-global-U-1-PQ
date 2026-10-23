"""YCA1 immutable measured inputs and eight-source freeze before assembly."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='ea7a728691587690ff1d908cc5ce65c467567bef';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/yukawa-counterterm-assembly-v1-2026-10-22')
git=lambda *v:subprocess.check_output(['git',*v],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
b={}
def add(p,h=None):
 p=p.resolve();v=sha256(p.read_bytes()).hexdigest()
 if h is not None:assert v==h,str(p)
 b[str(p)]=v
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V490.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']:add(ROOT/n)
for folder,names in {
 'canonical_so10_yukawa_carrier_transport':['RECORD.md','RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],
 'canonical_so10_sterile_matter_action':['ACTION_V1.md','validation_receipt.json'],
 'canonical_so10_fermion_yukawa_self_energy':['RECORD.md','RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],
 'canonical_so10_fermion_kinetic_mass_poles':['RECORD.md','RESULT.md','primary_tables.json.gz','replay_v2_tables.json.gz','validation_receipt_v2.json'],
 'canonical_so10_yukawa_polarization_poles':['RESULT.md','validation_receipt_v2.json'],
 'canonical_so10_gauge_yukawa_vertex_poles':['RECORD.md','DERIVATION.md','RESULT.md','primary_tables.json.gz','replay_v2_tables.json.gz','validation_receipt_v2.json','orientation_receipt_v2.json']}.items():
 for n in names:add(ROOT/'calculations'/folder/n)
for n,h in {
 'project_state.json':'d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8',
 'calculations/canonical_so10_yukawa_carrier_transport/validation_receipt.json':'4e39b499d32e4203c1d159e5946abfaf9adb05552e9a43c3005c8ee04eee312b',
 'calculations/canonical_so10_sterile_matter_action/validation_receipt.json':'21d4816d5ea079b28b41783e8d65aa3bd52d779349c90106d4dec5e99e10bd41',
 'calculations/canonical_so10_fermion_yukawa_self_energy/validation_receipt.json':'960dd63d9aacb2a8ef30bb13b029470458c0cfef761db7f758945e101e44b3b8',
 'calculations/canonical_so10_fermion_kinetic_mass_poles/validation_receipt_v2.json':'c0e8ecdcea6776433be31abc513bb5532512a358e7c8eb22e6f46e2ae720df06',
 'calculations/canonical_so10_yukawa_polarization_poles/validation_receipt_v2.json':'6abceb30000f6ab8521a502119e58f50404cd44473d7134e6ea9f7b7ae911ccd',
 'calculations/canonical_so10_gauge_yukawa_vertex_poles/validation_receipt_v2.json':'d8627df20f8cb21d820a3c284474d17447b8b83f909cf508facb395d2e00c666',
 'calculations/canonical_so10_gauge_yukawa_vertex_poles/orientation_receipt_v2.json':'edf690ae4bb58e69b8e4e9607526d5a848ffee72fada2064c72b46ee5c6c1a44'}.items():add(ROOT/n,h)
for name in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(name+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(name+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==30419
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'YCA1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(b.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':16*1024**2,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('YCA1_FROZEN',len(b),'bindings',flush=True)
