"""VVA1 initial ancestry/source freeze; no scientific execution."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='3fcfe61f452f3002cdf493b9c2b9abf741843c48'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vvs-sunset-v1-2026-10-20')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={};qualified={}
for folder,receipt,want,wantsha in [
 ('canonical_so10_two_vector_cubic_kernel','validation_receipt.json','QUALIFIED_COMPLETE_TWO_VECTOR_CUBIC_F2_MATCHING_KERNEL','bd7b5365bf612511c719600a55e2baea86b626d7fc0dcf83f76637ef03281c5a'),
 ('canonical_so10_ghost_scalar_sunset','measure_receipt.json','QUALIFIED_COMPLETE_GHOST_SCALAR_SPECTRAL_MEASURE','261d97642d3ee08b45b1fee2fc8aa1899f8fe731bb965055191d4b6202d2f39b')]:
    parent=ROOT/'calculations'/folder
    for prep in sorted(parent.glob('*preparation*.json')):
        for n,h in json.loads(prep.read_bytes())['input_sha256'].items():
            if n not in cache:cache[n]=sha256(Path(n).read_bytes()).hexdigest()
            assert cache[n]==h,n
            if n in deps:assert deps[n]==h,n
            deps[n]=h
    for p in sorted(parent.iterdir()):
        if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
    p=parent/receipt;v=json.loads(p.read_bytes());assert v['status']==want and sha256(p.read_bytes()).hexdigest()==wantsha
    qualified[folder]=wantsha
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V422.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','data.py','measure.py','units.py','finish.py','prepare.py','prepare_phase.py','capture_phase.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw,n
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==26659
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'VVA1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
 'qualified_receipts':qualified,'old_blobs':26659,'seconds_each':600,'sampled_private_cap':8*1024**3,
 'launch_floor':350*1024**2,'whole_package_bytes':6*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings;26659oldblobs;no science executed',flush=True)
