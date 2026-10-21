"""Freeze GSA1's full spectral stage before native calculation."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='3a60e708bbf0da14dd7f2efcbcce02d99fa6f1f2'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/ghost-scalar-sunset-v1-2026-10-20')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={}
parent=ROOT/'calculations/canonical_so10_ghost_scalar_charge_kernel'
for prep in sorted(parent.glob('*preparation*.json')):
    for p,h in json.loads(prep.read_bytes())['input_sha256'].items():
        if p not in cache:cache[p]=sha256(Path(p).read_bytes()).hexdigest()
        assert cache[p]==h,p
        if p in deps:assert deps[p]==h,p
        deps[p]=h
for p in sorted(parent.iterdir()):
    if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
p=parent/'validation_receipt.json';assert sha256(p.read_bytes()).hexdigest()=='d4ab813f970df5dabfb7b814ce62df09f2abb721a5fe78eccef407b4ff23baee'
assert json.loads(p.read_bytes())['status']=='QUALIFIED_COMPLETE_ORDERED_GHOST_SCALAR_CHARGE_OPERATORS'
for p in [ROOT/'calculations/canonical_so10_r1_scalar_current/data.py',ROOT/'AGENTS.md',ROOT/'project_state.json']:
    h=sha256(p.read_bytes()).hexdigest()
    if str(p) in deps:assert deps[str(p)]==h
    deps[str(p)]=h
for n in ['RECORD.md','data.py','measure.py','prepare.py','run_measure.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==26519
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'GSA1_MEASURE_PREPARATION','input_sha256':dict(sorted(deps.items())),'base_commit':BASE,
 'seconds_each':600,'digits':110,'mass_output_digits':85,'weight_output_digits':75,
 'measure_comparison_gate':'1e-60 relative','scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN_FULL_MEASURE',len(deps),'bindings',flush=True)
