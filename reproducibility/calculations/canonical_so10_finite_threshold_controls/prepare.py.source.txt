"""FCT1 prospective immutable closure; no scientific calculation."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='1aa7dd63c3da4be55c94279843b573f3bc8aaf46'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/finite-threshold-controls-v1-2026-10-21')
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bindings={};cache={}
def add(p,h=None):
    p=p.resolve();key=str(p)
    if key not in cache:cache[key]=sha256(p.read_bytes()).hexdigest()
    if h is not None:assert cache[key]==h,key
    if key in bindings:assert bindings[key]==cache[key]
    bindings[key]=cache[key]
def write(p,raw):
    with p.open('xb') as f:f.write(raw)
parent=ROOT/'calculations/canonical_so10_source_region_matching'
names=['preparation.json','preparation_v2.json','validation_preparation_v2.json','validation_preparation_v3.json']
assert {p.name for p in parent.glob('*preparation*.json')}==set(names)
for n in names:
    for p,h in json.loads((parent/n).read_bytes())['input_sha256'].items():add(Path(p),h)
for p in parent.iterdir():
    if p.is_file():add(p)
add(parent/'validation_receipt_v3.json','29c52102d9d720777cc6bcc37a9e93c7f1a6b52d8e1a3604062ecbc02e36a3ef')
for folder,files in {
 'canonical_so10_scalar_cubic_spectral_measure':['primary_tables.json.gz'],
 'canonical_so10_scalar_quartic_charge_projection':['primary_tables.json.gz','replay_tables.json.gz'],
 'canonical_so10_scalar_sm_frame':['replay_tables.json.gz'],
 'canonical_so10_finite_counterterm_insertion':['replay_v3_tables.json.gz'],
 'canonical_so10_matrix_threshold':['scalar_matrix_log.json']}.items():
    for n in files:add(ROOT/'calculations'/folder/n)
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V460.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:add(ROOT/n)
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');write(cp,raw);add(p);add(cp)
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';add(ROOT/'project_state.json',state)
tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==28924
CONTROL.mkdir(parents=True,exist_ok=False);write(CONTROL/'old_git_tree.txt',tree)
write(HERE/'preparation.json',(json.dumps({'schema':'FCT1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bindings.items())),
 'inherited_manifest_inventory':names,'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,
 'whole_package_bytes':24*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('FCT1_FROZEN',len(bindings),'bindings',flush=True)
