"""SRM1 explicit inherited byte closure and prospective source freeze."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='4c2de406c8993d954d6a05dcd61d5191bf857abe'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/source-region-matching-v1-2026-10-21')
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bindings={};cache={}
def add(p,h=None):
    p=p.resolve();n=str(p)
    if n not in cache:cache[n]=sha256(p.read_bytes()).hexdigest()
    if h is not None:assert cache[n]==h,n
    if n in bindings:assert bindings[n]==cache[n]
    bindings[n]=cache[n]
def write(p,b):
    with p.open('xb') as f:f.write(b)
names=['preparation.json','validation_preparation.json']
for dirname in ['canonical_so10_source_heavy_elimination']:
    parent=ROOT/'calculations'/dirname
    assert {p.name for p in parent.glob('*preparation*.json')}==set(names)
    for name in names:
        for p,h in json.loads((parent/name).read_bytes())['input_sha256'].items():add(Path(p),h)
    for p in parent.iterdir():
        if p.is_file():add(p)
add(ROOT/'calculations/canonical_so10_source_heavy_elimination/validation_receipt.json','2eaeca6270e57451936f11eadd8e3db0dab95a0b759397e527d39ce4445c62bf')
add(Path('C:/Users/psboy/.codex/attachments/cb3de026-98f0-4778-a1c0-046cf4c112d8/Pasted text.txt'))
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V459.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:
    add(ROOT/n)
for n in ['RECORD.md','DERIVATION.md','REFERENCE_REVIEW_2026_10_21.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');write(cp,raw);add(p);add(cp)
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';add(ROOT/'project_state.json',state)
tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==28861
CONTROL.mkdir(parents=True,exist_ok=False);write(CONTROL/'old_git_tree.txt',tree)
write(HERE/'preparation.json',(json.dumps({'schema':'SRM1_PREPARATION','base_commit':BASE,
    'input_sha256':dict(sorted(bindings.items())),'inherited_manifest_inventory':names,'seconds_each':600,
    'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'whole_package_bytes':24*1024**2,
    'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('SRM1_FROZEN',len(bindings),'bindings; actual source-region construction without a fitted Nielsen remainder',flush=True)
