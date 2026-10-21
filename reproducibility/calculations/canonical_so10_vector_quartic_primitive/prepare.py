"""Exclusive prospective input/proof/code freeze; no science in preparation."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-quartic-primitive-v1-2026-10-20')
BASE='14f963be9ae8968cdf6704aaa89b104a616f69fc'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def write(p,b):
    with p.open('xb') as out:out.write(b)
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==25341
write(CONTROL/'old_git_tree.txt',old)
deps={}
inherited=CAL/'canonical_so10_threshold_exact_once/validation_preparation.json'
deps[str(inherited)]=sha256(inherited.read_bytes()).hexdigest()
for n,h in json.loads(inherited.read_bytes())['input_sha256'].items():
    assert sha256(Path(n).read_bytes()).hexdigest()==h,n;deps[n]=h
direct=['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V397.md',
 'calculations/canonical_so10_threshold_exact_once/validation_receipt.json',
 'calculations/canonical_so10_threshold_exact_once/RESULT.md',
 'calculations/canonical_so10_threshold_exact_once/NEXT_RESEARCH_QUESTION.md',
 'calculations/canonical_so10_vacuum_master_pilot/DERIVATION.md',
 'calculations/canonical_so10_vacuum_master_pilot/validation_receipt_v2.json',
 'calculations/canonical_so10_threshold_scheme_transport/DERIVATION.md',
 'calculations/canonical_so10_gauge_coupling_uv/DERIVATION.md',
 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_primary.json',
 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_replay.json']
for name in direct:
    p=ROOT/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for name in ['prepare.py','run.py','primitive.py','verify.py','RECORD.md','DERIVATION.md']:
    p=HERE/name;b=p.read_bytes()
    if p.suffix=='.py':ast.parse(b,filename=str(p))
    write(HERE/(name+'.source.txt'),b);deps[str(p)]=sha256(b).hexdigest()
    deps[str(HERE/(name+'.source.txt'))]=sha256(b).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
value={'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_PREPARATION_V1','base_commit':BASE,
       'input_sha256':dict(sorted(deps.items())),'state_sha256':state,
       'native_seconds':180,'verifier_seconds':240,'sampled_private_cap':8*1024**3,
       'launch_floor':350*1024**2,'new_package_bytes':2*1024**2,'scientific_acceptance':'NOT_PERFORMED'}
write(HERE/'preparation.json',(json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings and25341 old Gitblobs; no science executed')
