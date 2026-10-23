"""SRG1 freeze inherited execution evidence and the actual RG operator inputs."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='45352e8d446f60000c1caaa1900e03317e1f78e4'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/stationary-rg-pullback-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
deps={};cache={}
def add(p,h=None):
    p=p.resolve();n=str(p)
    if n not in cache:cache[n]=sha256(p.read_bytes()).hexdigest()
    if h is not None:assert cache[n]==h,n
    if n in deps:assert deps[n]==cache[n]
    deps[n]=cache[n]
def write(p,raw):
    with p.open('xb') as out:out.write(raw)
parent=ROOT/'calculations/canonical_so10_background_matching_conversion'
inventory=['preparation.json','validation_preparation.json']
assert {p.name for p in parent.glob('*preparation*.json')}==set(inventory)
for name in inventory:
    for p,h in json.loads((parent/name).read_bytes())['input_sha256'].items():add(ROOT/Path(p),h)
for p in parent.iterdir():
    if p.is_file():add(p)
add(parent/'validation_receipt.json','4841b39f3f0040ea074e5ec946c68cb52c5ec6f74bfafd973f55392e42249e7d')
assert json.loads((parent/'validation_receipt.json').read_bytes())['status']=='QUALIFIED_BACKGROUND_F2_COUPLING_CONVERSION_AND_RUNNING_INPUT_RG_LAW'
for folder in ['canonical_so10_scalar_quadratic_pullback','canonical_so10_scalar_kernel_reconciliation','canonical_so10_background_vev_uv',
    'canonical_so10_gauge_potential_uv','canonical_so10_gauge_quartic_hessian','canonical_so10_scalar_counterterm_family_closure',
    'canonical_so10_uv_radial_tadpoles','canonical_so10_finite_counterterm_insertion','canonical_so10_heavy_tadpole_bridge',
    'canonical_so10_nine_family_uv_assembly','canonical_so10_ghost_counterterm_trace_closure']:
    for p in (ROOT/'calculations'/folder).iterdir():
        if p.is_file():add(p)
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V448.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md',
    'calculations/canonical_so10_light_pole_reduction/verify.py','tools/two_loop_qft_compiler_v1/layer5_counterterm_contract.json',
    'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py','tools/pole_blind_validation_guard/sitecustomize.py']:
    add(ROOT/n)
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');write(cp,raw);add(p);add(cp)
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';add(ROOT/'project_state.json',state)
tree=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(tree.splitlines())==28438
CONTROL.mkdir(parents=True,exist_ok=False);write(CONTROL/'old_git_tree.txt',tree)
write(HERE/'preparation.json',(json.dumps({'schema':'SRG1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
    'inherited_manifest_inventory':inventory,'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,
    'whole_package_bytes':24*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('SRG1_FROZEN',len(deps),'bindings; native finite-slope read prohibited',flush=True)
