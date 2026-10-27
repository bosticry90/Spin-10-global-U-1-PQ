from pathlib import Path
from hashlib import sha256
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vacuum-heat-root-completion-v1-2026-10-24');OLD=CONTROL.with_name('ghost-vertex-order-reconciliation-v1-2026-10-24')
BASE='4ef90c58da071496672431008db417af9c94ae6c';STATE='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest();git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main' and digest(ROOT/'project_state.json')==STATE
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
CONTROL.mkdir(parents=True,exist_ok=False);bind={}
def add(p):p=p.resolve();bind[str(p)]=digest(p)
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,indent=2)+'\n').encode())
old=git('ls-tree','-r',BASE);assert len(old.splitlines())==33660
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(old)
add(CONTROL/'old_git_tree.txt')
for n in ['postcommit_seal.json','after_seal_full_capture.json','seal.py','readiness.jsonl','readiness_stderr.txt','readiness_native_exit.json']:add(OLD/n)
assert read(OLD/'postcommit_seal.json')['clean'] and read(OLD/'after_seal_full_capture.json')['native_exit']==0 and read(OLD/'readiness_native_exit.json')['step_exits']==[0,0,0,0,0,2]
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V577.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md']:add(ROOT/n)
for fo in ['canonical_so10_cutoff_source_ward_operator','canonical_so10_tangent_heat_ward_bridge','canonical_so10_ghost_vertex_order_reconciliation','canonical_so10_vacuum_tangent_source_kernel','canonical_so10_ghost_triangle_field_insertion','canonical_so10_yukawa_carrier_transport']:
 for n in ['RECORD.md','DERIVATION.md','RESULT.md','data_v3.py','primary_v3.py','replay_v3.py','primary.py','replay.py']:
  p=CAL/fo/n
  if p.exists():add(p)
 for pat in ['*receipt*.json','*tables*.json.gz']:
  for p in (CAL/fo).glob(pat):add(p)
add(CAL/'canonical_so10_cutoff_source_ward_operator/primary_inputs.json.gz')
assert digest(CAL/'canonical_so10_cutoff_source_ward_operator/validation_receipt.json')=='55d18b53429b83ec4b8cd4dfde064dff138fce3931d99f972ba6436549ac4e65'
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 add(p);add(HERE/(n+'.source.txt'))
with (CONTROL/'prelaunch_preflight.json').open('xb') as out,(CONTROL/'prelaunch_preflight_stderr.txt').open('xb') as err:r=subprocess.run([sys.executable,'-B',str(ROOT/'tools/research_session_preflight.py')],stdout=out,stderr=err,cwd=ROOT)
d=read(CONTROL/'prelaunch_preflight.json');assert r.returncode==0 and d['git_HEAD']==BASE and not d['active_A10_M08_python_processes']
for n in ['prelaunch_preflight.json','prelaunch_preflight_stderr.txt']:add(CONTROL/n)
dump(HERE/'preparation.json',{'schema':'VHR1_PREPARATION','input_sha256':dict(sorted(bind.items())),'base_commit':BASE,'seconds_each':600,'private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'})
print('VHR1_FROZEN',len(bind),'bindings',flush=True)
