"""FYV1 actual versioned dependency/source freeze and compilation gate."""
from pathlib import Path
from hashlib import sha256
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/finite-yukawa-vertex-comparison-v1-2026-10-22');BASE='b84047fb21d972c0f64ff4377f75dc731ff566cd'
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main' and not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bind={}
def add(p,want=None):
 p=p.resolve();h=sha256(p.read_bytes()).hexdigest()
 if want:assert h==want,str(p)
 bind[str(p)]=h
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V516.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:add(ROOT/n)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8');add(PK/'export_a10_e5_antighost_vector.py')
deps={'canonical_so10_sterile_matter_action':(['ACTION_V1.md','validation_receipt.json'],'validation_receipt.json','21d4816d5ea079b28b41783e8d65aa3bd52d779349c90106d4dec5e99e10bd41'),
 'canonical_so10_sterile_massive_propagator':(['RESULT.md','validation_receipt.json'],'validation_receipt.json','53a99e56ee95c247efd4e07d3ff7a4fb8817d284dd4f7a0cbfc63f449495c25c'),
 'canonical_so10_yukawa_carrier_transport':(['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'validation_receipt.json','4e39b499d32e4203c1d159e5946abfaf9adb05552e9a43c3005c8ee04eee312b'),
 'canonical_so10_gauge_yukawa_vertex_poles':(['DERIVATION.md','ORIENTATION_V2.md','orientation_receipt_v2.json','primary_tables.json.gz','replay_v2_tables.json.gz','validation_receipt_v2.json'],'validation_receipt_v2.json','d8627df20f8cb21d820a3c284474d17447b8b83f909cf508facb395d2e00c666'),
 'canonical_so10_fermion_scalar_vertex_support':(['RECORD.md','RESULT.md','validation_receipt_v3.json'],'validation_receipt_v3.json','cd3cce0713743819ff040a9d2c91bb886fbe6f48d747dfe25cd494446d8bf3c6'),
 'canonical_so10_yukawa_polarization_poles':(['primary_tables.json.gz','replay_v2_tables.json.gz','validation_receipt_v2.json'],'validation_receipt_v2.json','6abceb30000f6ab8521a502119e58f50404cd44473d7134e6ea9f7b7ae911ccd'),
 'canonical_so10_open_fermion_finite_kinetic':(['RECORD.md','RESULT.md','validation_receipt.json'],'validation_receipt.json','c01f53c4c4fafd6e88d3d66fdbd8a0a5e1fb711c84b68d7afa6c4036f4962439'),
 'canonical_so10_yukawa_finite_vertex_ward':(['RESULT.md','validation_receipt.json'],'validation_receipt.json','19c30c658e3662845a57026fbeaa0ce9e4a82d779c42eb274b298bcdeb5c20cb')}
for folder,(names,rn,rh) in deps.items():
 for n in names:add(ROOT/'calculations'/folder/n,rh if n==rn else None)
source=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/open-fermion-finite-kinetic-v1-2026-10-22')
for n in ['readiness.jsonl','readiness_stderr.txt','postcommit_seal.json']:add(source/n)
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':compile(raw,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(n+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==31229
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'FYV1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bind.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
for n in ['readiness.jsonl','readiness_stderr.txt']:
 with (CONTROL/n).open('xb') as f:f.write((source/n).read_bytes())
with (CONTROL/'readiness_reuse.json').open('xb') as f:f.write((json.dumps({'fresh_readiness_execution_here':False,'source_was_fresh_in_this_logical_goal_turn':True,'source_sha256':{str(source/n):sha256((source/n).read_bytes()).hexdigest() for n in ['readiness.jsonl','readiness_stderr.txt']},'expensive_historical_science_replayed':False},sort_keys=True)+'\n').encode())
print('FYV1_FROZEN',len(bind),'bindings',flush=True)
