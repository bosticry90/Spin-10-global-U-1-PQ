"""BWF1 authenticated input/source freeze before scientific computation."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/bosonic-fermion-finite-ward-v1-2026-10-22');BASE='398412c797235402d55141c69492fbbcea700146'
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bind={}
def add(path,expected=None):
 path=path.resolve();h=sha256(path.read_bytes()).hexdigest()
 if expected:assert h==expected,str(path)
 bind[str(path)]=h
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V513.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:add(ROOT/n)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8');add(PK/'export_a10_e5_antighost_vector.py')
for folder,names in {'canonical_so10_sterile_matter_action':['ACTION_V1.md','validation_receipt.json'],'canonical_so10_yukawa_carrier_transport':['validation_receipt.json'],'canonical_so10_scalar_yukawa_reference':['RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_mixed_bosonic_finite_difference':['RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_finite_gauge_ward_functional':['RESULT.md','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json']}.items():
 for n in names:add(ROOT/'calculations'/folder/n)
source=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/scalar-yukawa-reference-v1-2026-10-22')
for n in ['readiness.jsonl','readiness_stderr.txt','postcommit_seal.json']:add(source/n)
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 f=HERE/n;raw=f.read_bytes();assert b'\r' not in raw
 if f.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as h:h.write(raw)
 add(f);add(HERE/(n+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==31120
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'BWF1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bind.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
for n in ['readiness.jsonl','readiness_stderr.txt']:
 with (CONTROL/n).open('xb') as f:f.write((source/n).read_bytes())
with (CONTROL/'readiness_reuse.json').open('xb') as f:f.write((json.dumps({'fresh_readiness_execution_here':False,'source_was_fresh_in_this_logical_goal_turn':True,'source_sha256':{str(source/n):sha256((source/n).read_bytes()).hexdigest() for n in ['readiness.jsonl','readiness_stderr.txt']},'expensive_historical_science_replayed':False},sort_keys=True)+'\n').encode())
print('BWF1_FROZEN',len(bind),'bindings',flush=True)
