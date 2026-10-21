"""Freeze VSSA1 exact kernel with complete qualified threshold ancestry."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='1eb24da4d38f9016d3458d3d230008c6d3827548'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vss-assembly-v1-2026-10-20')
def dump(p,b):
    with p.open('xb') as f:f.write(b)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
deps={};checked={}
for folder,receipt,want in [
 ('canonical_so10_r0_scalar_current','validation_receipt_v3.json','563445cc51f97490f91db123e2f5d3906b0cde35f644fa397d4eb137960a9799')]:
    parent=ROOT/'calculations'/folder
    for prep in sorted(parent.glob('*preparation*.json')):
        deps[str(prep)]=sha256(prep.read_bytes()).hexdigest()
        for n,h in json.loads(prep.read_bytes())['input_sha256'].items():
            if n not in checked:checked[n]=sha256(Path(n).read_bytes()).hexdigest()
            assert checked[n]==h,n
            if n in deps:assert deps[n]==h,n
            deps[n]=h
    for p in sorted(parent.iterdir()):
        if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
    assert sha256((parent/receipt).read_bytes()).hexdigest()==want
    assert json.loads((parent/receipt).read_bytes())['status']=='QUALIFIED_COMPLETE_R0_SCALAR_CURRENT_SPECTRAL_FUNCTION'
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V417.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','data.py','assemble.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes()
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    q=HERE/(n+'.source.txt');dump(q,raw);deps[str(p)]=deps[str(q)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==26312
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'VSSA1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),'seconds_per_worker':300,'working_digits':110,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'whole_package_bytes':4*1024**2,
 'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode());print('FROZEN',len(deps),'bindings;26312oldblobs;no science executed')
