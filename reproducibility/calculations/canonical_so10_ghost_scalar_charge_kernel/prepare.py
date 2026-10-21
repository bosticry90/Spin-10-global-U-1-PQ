"""GSK1 initial byte freeze,qualified dependencies and old tree custody."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='3a60e708bbf0da14dd7f2efcbcce02d99fa6f1f2'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/ghost-scalar-charge-kernel-v1-2026-10-20')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={};qualified={}
for folder,want in [
 ('canonical_so10_ghost_scalar_support','QUALIFIED_COMPLETE_GHOST_SCALAR_MASS_SUPPORT'),
 ('canonical_so10_spinzero_cubic_kernel','QUALIFIED_COMPLETE_SPINZERO_CUBIC_F2_MATCHING_KERNEL'),
 ('canonical_so10_scalar_current_sm_kernel','QUALIFIED_FULL_SCALAR_COMMUTANT_KERNEL_AND_U1_QUANTUM_LIGHT_BRANCH')]:
    parent=ROOT/'calculations'/folder
    for prep in sorted(parent.glob('*preparation*.json')):
        for n,h in json.loads(prep.read_bytes())['input_sha256'].items():
            if n not in cache:cache[n]=sha256(Path(n).read_bytes()).hexdigest()
            assert cache[n]==h,n
            if n in deps:assert deps[n]==h,n
            deps[n]=h
    for p in sorted(parent.iterdir()):
        if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
    p=parent/'validation_receipt.json';v=json.loads(p.read_bytes());assert v['status']==want
    qualified[folder]=sha256(p.read_bytes()).hexdigest()
assert qualified['canonical_so10_ghost_scalar_support']=='5ac5516fd6db67aa73d4a7c8ed36f1be1b246e06d0cda70035a04b5924d0531e'
assert qualified['canonical_so10_spinzero_cubic_kernel']=='fce3be82ab650672b444b354f436bf4975992486b954d95a93c4731f54dcecf3'
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V420.md','docs/RESEARCH_EXECUTION_HANDOFF_V419.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','data.py','measure.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw,n
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==26519
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'GSK1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
 'qualified_receipts':qualified,'old_blobs':26519,'seconds_each':600,'sampled_private_cap':8*1024**3,
 'launch_floor':350*1024**2,'whole_package_bytes':6*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings;26519oldblobs;no science executed',flush=True)
