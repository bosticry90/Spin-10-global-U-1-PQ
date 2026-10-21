"""Authenticate predecessor bytes, then freeze QIR1 before mathematics."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-quartic-ir-matching-v1-2026-10-20')
BASE='750ee76b4ad0d9b5378c430f44ebb1caf966fe75'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def write(p,b):
    with p.open('xb') as out:out.write(b)
deps={}
for name in ['validation_preparation_v2.json','validation_preparation_v3.json']:
    p=CAL/'canonical_so10_vector_quartic_primitive'/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
    for n,h in json.loads(p.read_bytes())['input_sha256'].items():
        assert sha256(Path(n).read_bytes()).hexdigest()==h,n
        if n in deps:assert deps[n]==h
        deps[n]=h
direct=['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V398.md',
 'calculations/canonical_so10_vector_quartic_primitive/validation_receipt_v3.json',
 'calculations/canonical_so10_vector_quartic_primitive/RESULT.md',
 'calculations/canonical_so10_vector_quartic_primitive/NEXT_RESEARCH_QUESTION.md',
 'calculations/canonical_so10_vector_quartic_primitive/primary_v2_tables.json.gz',
 'calculations/canonical_so10_vector_quartic_primitive/replay_v2_tables.json.gz',
 'calculations/canonical_so10_one_soft_factorization/DERIVATION.md',
 'calculations/canonical_so10_one_soft_factorization/validation_receipt_v4.json']
for name in direct:
    p=ROOT/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for name in ['prepare.py','run.py','ir_match.py','verify.py','RECORD.md','DERIVATION.md']:
    p=HERE/name;b=p.read_bytes()
    if p.suffix=='.py':ast.parse(b,filename=str(p))
    write(HERE/(name+'.source.txt'),b)
    for q in [p,HERE/(name+'.source.txt')]:deps[str(q)]=sha256(q.read_bytes()).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
assert sha256((CAL/'canonical_so10_vector_quartic_primitive/validation_receipt_v3.json').read_bytes()).hexdigest()=='fb2c3f4557b203c4975b020f5bc0b1c583106385c2ddeab0c485b2b330744cd3'
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==25393
write(CONTROL/'old_git_tree.txt',old)
value={'schema':'C1_VECTOR_QUARTIC_IR_MATCHING_PREPARATION_V1','base_commit':BASE,
       'input_sha256':dict(sorted(deps.items())),'state_sha256':state,
       'native_seconds':180,'verifier_seconds':240,'private_sample_cap':8*1024**3,
       'launch_floor':350*1024**2,'new_package_bytes':2*1024**2,'scientific_acceptance':'NOT_PERFORMED'}
write(HERE/'preparation.json',(json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings and25393 oldblobs; no science executed')
