"""BSR1 prospective byte closure; never read unfinished VSG outputs."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='e9380aab3b0f347f2a71c81a36f5f438bbdda68b'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/benchmark-scope-reconciliation-v1-2026-10-22')
git=lambda *v:subprocess.check_output(['git',*v],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bindings={}
def add(p,h=None):
 p=p.resolve();v=sha256(p.read_bytes()).hexdigest()
 if h is not None:assert v==h,str(p)
 if str(p) in bindings:assert bindings[str(p)]==v
 bindings[str(p)]=v
parent=ROOT/'calculations/canonical_so10_common_scale_bound'
for p in sorted(parent.glob('*preparation*.json')):
 for f,h in json.loads(p.read_bytes())['input_sha256'].items():add(Path(f),h)
for p in parent.iterdir():
 if p.is_file():add(p)
add(parent/'validation_receipt.json','6d023c609cd577486d510fdf8b61d95cc39fa3c76b37bdacbcd852528758380c')
for folder,names in {
 'canonical_so10_direct_two_loop_gauge_scalar_threshold':['RECORD.md'],
 'canonical_so10_uv_radial_tadpoles':['inputs.py'],
 'canonical_so10_finite_counterterm_insertion':['geometry_v2.py'],
 'canonical_so10_scalar_benchmark':['STAGE1_POINT.json'],
 'canonical_so10_positive_higgs':['POINT.json'],
 'canonical_so10_bounded_scalar_feasibility':['RESULT.md','validation_receipt.json'],
 'canonical_so10_eta_offdiagonal_bound':['RESULT.md','validation_receipt.json'],
 'canonical_so10_coherent_joint_witness':['POINT.json','witness.py','RESULT.md','validation_receipt.json'],
 'canonical_so10_complete_contact_bound':['RESULT.md','validation_receipt.json'],
 'canonical_so10_finite_full_bfb':['RESULT.md','validation_receipt.json'],
 'canonical_so10_finite_radial_control':['primary_result.json','assess.py','RESULT.md','validation_receipt.json','BOSONIC_RESULT_V2.md','bosonic_validation_receipt.json'],
 'canonical_so10_finite_physical_input_screen':['RESULT.md','validation_receipt.json']}.items():
 for name in names:add(ROOT/'calculations'/folder/name)
add(Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/common-scale-bound-v1-2026-10-22/postcommit_seal.json'))
for name in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V469.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:add(ROOT/name)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8')
for name in ['RECORD.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
 if name.endswith('.py'):ast.parse(raw)
 with (HERE/(name+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(name+'.source.txt'))
tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==29768
CONTROL.mkdir(parents=True,exist_ok=False)
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'BSR1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bindings.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':24*1024**2,'unfinished_VSG_inputs_read':False,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('BSR1_FROZEN',len(bindings),'bindings',flush=True)
