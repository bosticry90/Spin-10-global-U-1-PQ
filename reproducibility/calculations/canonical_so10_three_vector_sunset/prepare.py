"""V3A1 freeze exact action/projector ancestry and all source bytes."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='8047f1213b6773f7633f18dd152da1f746e9bad4'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/three-vector-sunset-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={};qualified={}
for folder,receipt,want,wantsha in [('canonical_so10_three_vector_support', 'validation_receipt.json', 'QUALIFIED_ACTUAL_THREE_VECTOR_VERTEX_AND_COMPLETE_MASS_CHARGE_SUPPORT', 'd39535044d58a01dcccac5002698b9be13f5e846e25bcb75b261c3338a9915c7'), ('canonical_so10_three_vector_bare_kernel', 'validation_receipt.json', 'QUALIFIED_COMPLETE_POSITIVE_MASS_THREE_VECTOR_BARE_LAURENT_KERNEL', 'd35634cd4e5fa0d1f6c2af5b0ea9dbbc8dd75ab2993072ba07b96ae6e55500dd'), ('canonical_so10_three_vector_uv_forests', 'validation_receipt.json', 'QUALIFIED_ORIGINAL_CUBIC_VECTOR_UV_OPERATORS_AND_POSITIVE_MASS_PROPER_FOREST', '640e8e187c8acfea99762651e163c82cefba34e8db42daf78cdbcc1d5a8d9bb8'), ('canonical_so10_three_vector_soft_matching', 'validation_receipt_v2.json', 'QUALIFIED_ORIGINAL_THREE_VECTOR_EQUAL_HEAVY_ONE_LIGHT_MATCHING', '7c89a4f23ccb688564621ae72a1084da5f4d68e9a19360aeed5ddb7741d35bde'), ('canonical_so10_three_vector_soft_matching', 'hard_forest_correction_receipt.json', 'QUALIFIED_CORRECTED_GAMMA_COMPLETE_ONE_LIGHT_THREE_VECTOR_HARD_FOREST', '019db039094fadc591f6841c715beb9816f32a0f225ce2356eff0c8d064bb509'), ('canonical_so10_r3_scalar_current', 'backend_receipt_v10.json', 'QUALIFIED_POSITIVE_MASS_MASTER_ANALYTIC_DERIVATIVE_BACKEND', '56b3f303d55fc90d3f29654ef92ce50ffb3aaefe0a0159cbf0961d4ded558e65')]:
    parent=ROOT/'calculations'/folder
    for prep in sorted(parent.glob('*preparation*.json')):
        for n,h in json.loads(prep.read_bytes())['input_sha256'].items():
            if n not in cache:cache[n]=sha256(Path(n).read_bytes()).hexdigest()
            assert cache[n]==h,n
            if n in deps:assert deps[n]==h,n
            deps[n]=h
    for p in sorted(parent.iterdir()):
        if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
    p=parent/receipt;v=json.loads(p.read_bytes())
    if want:assert v['status']==want
    if wantsha:assert sha256(p.read_bytes()).hexdigest()==wantsha
    qualified[folder+'/'+receipt]=sha256(p.read_bytes()).hexdigest()
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V428.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','DERIVATION.md','data.py','measure.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw,n
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==27098
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'V3A1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
 'qualified_receipts':qualified,'old_blobs':27098,'seconds_each':600,'sampled_private_cap':8*1024**3,
 'launch_floor':350*1024**2,'whole_package_bytes':6*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings;27098oldblobs;no science executed',flush=True)
