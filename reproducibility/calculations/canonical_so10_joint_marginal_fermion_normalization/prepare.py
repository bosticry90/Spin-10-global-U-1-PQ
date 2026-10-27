from pathlib import Path
from hashlib import sha256
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/joint-marginal-fermion-normalization-v1-2026-10-23')
OLD=CONTROL.with_name('closed-heat-ward-normalization-v1-2026-10-23')
BASE='e721c31dab7f3e0ea5c160ed32ad69b45f221a8e';STATE='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest();git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main' and digest(ROOT/'project_state.json')==STATE
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
CONTROL.mkdir(parents=True,exist_ok=False);bind={}
def add(p):p=p.resolve();bind[str(p)]=digest(p)
def dump(p,d):
 with p.open('xb') as f:f.write((json.dumps(d,sort_keys=True,indent=2)+'\n').encode())
old=git('ls-tree','-r',BASE);assert len(old.splitlines())==33278
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(old)
add(CONTROL/'old_git_tree.txt')
for n in ['postcommit_seal.json','after_seal_full_capture.json','seal.py']:add(OLD/n)
assert read(OLD/'postcommit_seal.json')['clean'] and read(OLD/'after_seal_full_capture.json')['native_exit']==0
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V569.md','docs/CSH1_COMPACT_CURVATURE_FACTOR_CORRECTION_V1.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md']:add(ROOT/n)
for folder in ['canonical_so10_complete_heat_scalar_response','canonical_so10_complete_heat_matter_response','canonical_so10_complete_heat_vector_response','canonical_so10_heat_highest_matter_source','canonical_so10_closed_heat_ward_normalization','canonical_so10_dimensional_stokes_primitive','canonical_so10_bosonic_source_onejet_finite','canonical_so10_source_vector_finite_transport','canonical_so10_lower_source_vector_finite','canonical_so10_scalar_source_finite_comparison','canonical_so10_ghost_source_finite_comparison','canonical_so10_cutoff_source_ward_operator','canonical_so10_odd_gauge_local_coverage','canonical_so10_sterile_matter_action']:
 for n in ['RECORD.md','DERIVATION.md','RESULT.md']:
  p=CAL/folder/n
  if p.exists():add(p)
 for p in (CAL/folder).glob('validation_receipt*.json'):add(p)
 for pattern in ['*tables.json.gz','*family.json.gz']:
  for p in (CAL/folder).glob(pattern):add(p)
add(CAL/'canonical_so10_sterile_matter_action/ACTION_V1.md')
for tag in ['cd7c60f9-60ac-40e2-ad7b-f76925b47a3f','c3dc08cd-3864-4f1d-87e0-52d7ee3c1554']:
 add(Path('C:/Users/psboy/.codex/attachments')/tag/'Pasted text.txt')
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/n;b=p.read_bytes();assert b'\r' not in b
 if p.suffix=='.py':compile(b,str(p),'exec')
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(b)
 add(p);add(HERE/(n+'.source.txt'))
# New bounded E4 observation, not --fresh scientific calculation replay.
with (CONTROL/'readiness.jsonl').open('xb') as out,(CONTROL/'readiness_stderr.txt').open('xb') as err:
 r=subprocess.run([sys.executable,'-B',str(ROOT/'tools/research_check.py'),'e4'],stdout=out,stderr=err,cwd=ROOT)
events=[json.loads(v) for v in (CONTROL/'readiness.jsonl').read_text(encoding='utf-8').splitlines() if v.strip()]
steps=[v['exit_code'] for v in events if v.get('event')=='step_finished']
dump(CONTROL/'readiness_native_exit.json',{'native_exit':r.returncode,'step_exits':steps,'scientific_replay_requested':False,'historical_custody':'EXIT2_SEVEN_NOTPASS' if steps==[0,0,0,0,0,2] else 'UNQUALIFIED'})
assert r.returncode==0 and steps==[0,0,0,0,0,2] and events[-1]['execution_state']=='COMPLETED'
for n in ['readiness.jsonl','readiness_stderr.txt','readiness_native_exit.json']:add(CONTROL/n)
with (CONTROL/'prelaunch_preflight.json').open('xb') as out,(CONTROL/'prelaunch_preflight_stderr.txt').open('xb') as err:
 r=subprocess.run([sys.executable,'-B',str(ROOT/'tools/research_session_preflight.py')],stdout=out,stderr=err,cwd=ROOT)
d=read(CONTROL/'prelaunch_preflight.json');assert r.returncode==0 and d['git_HEAD']==BASE and not d['active_A10_M08_python_processes']
for n in ['prelaunch_preflight.json','prelaunch_preflight_stderr.txt']:add(CONTROL/n)
dump(HERE/'preparation.json',{'schema':'JMF1_PREPARATION','input_sha256':dict(sorted(bind.items())),'base_commit':BASE,'seconds_each':600,'private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'})
print('JMF1_FROZEN',len(bind),'bindings',flush=True)
