"""Freeze VSP1 before computation; retain all inherited bindings and Git bytes."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/vector-scalar-quartic-v1-2026-10-20')
BASE='0ae17d9b8d085e3fa587d8187d13906fb89a54ab'
def dump(p,b):
    with p.open('xb') as out:out.write(b)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
deps={};p=CAL/'canonical_so10_vector_field_normalization_trace/validation_preparation.json';deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n,h in json.loads(p.read_bytes())['input_sha256'].items():
    assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    deps[n]=h
direct=['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V404.md',
 'calculations/canonical_so10_vector_field_normalization_trace/validation_receipt.json',
 'calculations/canonical_so10_scalar_sm_frame/RECORD.md',
 'calculations/canonical_so10_background_threshold_inputs/DERIVATION.md',
 'calculations/canonical_so10_vector_quartic_ir_matching/DERIVATION.md',
 'calculations/canonical_so10_one_soft_factorization/validation_receipt_v4.json',
 'calculations/canonical_so10_finite_counterterm_insertion/geometry_v2.py']
for role in ['primary','replay']:
    for x in ['canonical_so10_scalar_sm_frame','canonical_so10_vector_quartic_ir_matching','canonical_so10_width_hard_projection','canonical_so10_background_threshold_inputs']:
        direct.append(f'calculations/{x}/{role}_tables.json.gz')
    direct += [f'calculations/canonical_so10_finite_counterterm_insertion/{role}_v3_tables.json.gz',
      f'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_physical_reconciliation/full_{role}.json']
for name in direct:
    p=ROOT/name;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for name in ['prepare.py','run.py','data.py','color.py','amplitude.py','verify.py','RECORD.md','DERIVATION.md']:
    p=HERE/name;b=p.read_bytes()
    if p.suffix=='.py':ast.parse(b,filename=str(p))
    dump(HERE/(name+'.source.txt'),b)
    for q in [p,HERE/(name+'.source.txt')]:deps[str(q)]=sha256(q.read_bytes()).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8'
assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==25591
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
value={'schema':'C1_VECTOR_SCALAR_QUARTIC_PREPARATION_V1','base_commit':BASE,
 'input_sha256':dict(sorted(deps.items())),'state_sha256':state,'native_seconds':300,'verifier_seconds':300,
 'private_sample_cap':8*1024**3,'launch_floor':350*1024**2,'new_package_bytes':4*1024**2,
 'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(value,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings and25591 oldblobs; no science executed')
