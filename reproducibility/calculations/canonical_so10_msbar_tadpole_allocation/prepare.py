"""MTA1 explicit immutable evidence inventory and pre-computation freeze."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='e94b6f59fbf7f933f273a46b6a1364f348005029'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/msbar-tadpole-allocation-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
deps={};cache={}
def add(p,h=None):
    p=p.resolve();key=str(p)
    if key not in cache:cache[key]=sha256(p.read_bytes()).hexdigest()
    if h is not None:assert cache[key]==h,key
    if key in deps:assert deps[key]==cache[key]
    deps[key]=cache[key]
def dump(p,raw):
    with p.open('xb') as f:f.write(raw)
hpr=ROOT/'calculations/canonical_so10_hard_pole_remainder'
inventory=['preparation.json','validation_preparation.json','supplement_preparation.json','recovery_preparation_v2.json']
assert {p.name for p in hpr.glob('*preparation*.json')}==set(inventory)
for name in inventory:
    p=hpr/name;d=json.loads(p.read_bytes());assert d['input_sha256']
    for n,h in d['input_sha256'].items():add(ROOT/Path(n),h)
    add(p)
for p in hpr.iterdir():
    if p.is_file():add(p)
receipt=hpr/'validation_receipt.json';add(receipt,'b7f6e4b4f8e2cd8731429c87bef62d878fcd28932d879fac9e2571cf9c85a5d1')
assert json.loads(receipt.read_bytes())['status']=='QUALIFIED_PRESCRIBED_HARD_POLE_CLOSURE_OVERALL_MS_POLE_AND_FINITE_INPUT_WITNESS'
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V446.md',
    'docs/SOLO_REVIEW_POLICY_V1.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md',
    'tools/two_loop_qft_compiler_v1/PROGRAM.md','tools/two_loop_qft_compiler_v1/LAYER5_RESULT.md',
    'tools/two_loop_qft_compiler_v1/layer5_counterterm_contract.py','tools/two_loop_qft_compiler_v1/layer5_counterterm_contract.json',
    'tools/two_loop_qft_compiler_v1/independent_counterterm_roundtrip.py','tools/two_loop_qft_compiler_v1/layer5_counterterm_independent_replay.json',
    'calculations/canonical_so10_scalar_benchmark/STAGE1_POINT.json','calculations/canonical_so10_positive_higgs/POINT.json',
    'calculations/canonical_so10_background_threshold_inputs/RECORD.md','calculations/canonical_so10_background_threshold_inputs/DERIVATION.md',
    'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_primary.json',
    'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_replay.json']:
    add(ROOT/n)
sources=['RECORD.md','DERIVATION.md','io_data.py','primary.py','replay.py','verify.py','prepare.py','run.py']
for n in sources:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);add(p);add(cp)
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';add(ROOT/'project_state.json',state)
tree=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(tree.splitlines())==28353
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',tree)
dump(HERE/'preparation.json',(json.dumps({'schema':'MTA1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
    'inherited_manifest_inventory':inventory,'state_sha256':state,'seconds_each':600,'sampled_private_cap':8*1024**3,
    'launch_floor':350*1024**2,'whole_package_bytes':24*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('MTA1_FROZEN',len(deps),'bindings; inherited physical-screen failure remains failure',flush=True)
