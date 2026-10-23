"""BMC1 typed transitive freeze and finite-demand-free old RG projection."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='8891dd45eac34a8524128e9f4dfea773d2c9a3c5'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/background-matching-conversion-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
deps={};cache={}
def add(p,h=None):
    p=p.resolve();key=str(p)
    if key not in cache:cache[key]=sha256(p.read_bytes()).hexdigest()
    if h is not None:assert cache[key]==h,key
    if key in deps:assert deps[key]==cache[key]
    deps[key]=cache[key]
def write(p,raw):
    with p.open('xb') as f:f.write(raw)
parent=ROOT/'calculations/canonical_so10_msbar_tadpole_allocation'
inventory=['preparation.json','execution_preparation_v2.json','execution_preparation_v3.json','validation_preparation_v3.json']
assert {p.name for p in parent.glob('*preparation*.json')}==set(inventory)
for n in inventory:
    for p,h in json.loads((parent/n).read_bytes())['input_sha256'].items():add(ROOT/Path(p),h)
for p in parent.iterdir():
    if p.is_file():add(p)
add(parent/'validation_receipt_v3.json','c2f1facbb3e9c9f0d6677772b5aa42f45cab07d8de8253cd1c79d95d4522d054')
assert json.loads((parent/'validation_receipt_v3.json').read_bytes())['status']=='QUALIFIED_MSBAR_PARENT_CONSTRAINT_AND_CORRELATED_RADIAL_TADPOLE_ALLOCATION'
names=['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V447.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md',
    'calculations/canonical_so10_direct_gauge_matching/derive_and_solve.py','calculations/canonical_so10_direct_gauge_matching/RECORD.md',
    'calculations/canonical_so10_direct_two_loop_heavy_threshold/analyze_boundary.py','calculations/canonical_so10_direct_two_loop_heavy_threshold/two_loop_boundary.json',
    'calculations/canonical_so10_direct_two_loop_heavy_threshold/RECORD.md','calculations/canonical_so10_direct_two_loop_heavy_threshold/RESULT.md',
    'calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/RECORD.md',
    'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py','tools/pole_blind_validation_guard/sitecustomize.py']
for n in names:add(ROOT/n)
source=ROOT/'calculations/canonical_so10_direct_two_loop_heavy_threshold/two_loop_boundary.json'
old=json.loads(source.read_bytes())['part_A_gauge_scalar']
fields=['parent_b_one_loop','parent_B_two_loop_yukawa_independent','SM_B_row_sums_at_unified_coupling']
operands={n:old[n] for n in fields}
rowkeys=['delta_b','delta_B_yukawa_independent','L2_coefficient','L_coefficient_without_C0_term']
operands['rg_log_kernel']=[{k:row[k] for k in rowkeys} for row in old['rg_log_kernel']]
packet={'schema':'BMC1_ALLOWLISTED_OLD_RG_INPUT_PROJECTION','source':source.relative_to(ROOT).as_posix(),'source_sha256':sha256(source.read_bytes()).hexdigest(),
    'source_pointers':['/part_A_gauge_scalar/'+n for n in fields]+['/part_A_gauge_scalar/rg_log_kernel/*/'+k for k in rowkeys],
    'excluded':'finite_threshold_demand;one_loop_C0_at_mu_eq_omega;diagnostic coupling;all physical targets','operands':operands}
write(HERE/'old_RG_input_projection.json',(json.dumps(packet,sort_keys=True,indent=2)+'\n').encode());add(HERE/'old_RG_input_projection.json')
for n in ['RECORD.md','DERIVATION.md','io_data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');write(cp,raw);add(p);add(cp)
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';add(ROOT/'project_state.json',state)
tree=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(tree.splitlines())==28408
CONTROL.mkdir(parents=True,exist_ok=False);write(CONTROL/'old_git_tree.txt',tree)
write(HERE/'preparation.json',(json.dumps({'schema':'BMC1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
    'inherited_manifest_inventory':inventory,'old_RG_projection_source_sha256':sha256(source.read_bytes()).hexdigest(),
    'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'whole_package_bytes':24*1024**2,
    'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('BMC1_FROZEN',len(deps),'bindings; old physical demand excluded from operand projection',flush=True)
