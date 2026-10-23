"""S4A1 freeze exact action/projector ancestry and all source bytes."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='68136fb7f5bdaec5c78a74d71b095c408934a1b9'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/scalar-quartic-amplitude-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={};qualified={}
for folder,receipt,want,wantsha in [('canonical_so10_scalar_quartic_functional', 'validation_receipt.json', 'QUALIFIED_COMPLETE_PARENT_QUARTIC_GAUSSIAN_FUNCTIONAL', '397459477bc57d85834f11cbdf538f1b6177f20d8829d7c00ec0fa48d0d5176a'), ('canonical_so10_finite_counterterm_insertion', 'validation_receipt_v5.json', 'QUALIFIED_PRESCRIBED_POLE_POSITIVE_HEAVY_CT_LAURENT_AND_FINITE_CONTRIBUTION', '8001162677d2281016e3fb7ef8da53b91dd788fa82feec673f38b91becd156d7')]:
    parent=ROOT/'calculations'/folder
    for prep in sorted(parent.glob('*preparation*.json')):
        for n,h in json.loads(prep.read_bytes())['input_sha256'].items():
            if n not in cache:cache[n]=sha256(Path(n).read_bytes()).hexdigest()
            assert cache[n]==h,n
            if n in deps:assert deps[n]==h,n
            deps[n]=h
    for p in sorted(parent.iterdir()):
        if p.is_file():deps[str(p)]=sha256(p.read_bytes()).hexdigest()
    p=parent/receipt;v=json.loads(p.read_bytes())
    if want:assert v['status']==want
    if wantsha:assert sha256(p.read_bytes()).hexdigest()==wantsha
    qualified[folder+'/'+receipt]=sha256(p.read_bytes()).hexdigest()
for n in ['tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_action_ast_a3/A38_parent_potential_ASTs.json', 'calculations/canonical_so10_scalar_reconstruction/certify_sigma_quartics.py', 'calculations/canonical_so10_scalar_reconstruction/certify_simple_invariant_slots.py', 'calculations/canonical_so10_scalar_reconstruction/count_d5_singlets.py', 'calculations/canonical_so10_scalar_reconstruction/test_eta1_invariant.py', 'calculations/canonical_so10_scalar_reconstruction/verify_action_inventory.py', 'calculations/canonical_so10_scalar_reconstruction/verify_eta1_doublet_mixing.py', 'calculations/canonical_so10_scalar_reconstruction/verify_pq.py', 'calculations/canonical_so10_scalar_reconstruction/verify_scalar_phases.py', 'calculations/canonical_so10_full_hessian/check_charged_singlet_goldstone.py', 'calculations/canonical_so10_full_hessian/check_full_block_rank_witness.py', 'calculations/canonical_so10_full_hessian/check_gauge_orbit_quadratics.py', 'calculations/canonical_so10_full_hessian/compile_sm_multiplicity_representatives.py', 'calculations/canonical_so10_full_hessian/construct_symmetry_orbits.py', 'calculations/canonical_so10_full_hessian/decompose_sm_tangent.py', 'calculations/canonical_so10_full_hessian/define_generic_nullity_test.py', 'calculations/canonical_so10_full_hessian/derive_neutral_singlet_block.py', 'calculations/canonical_so10_full_hessian/derive_vector10_self_block.py', 'calculations/canonical_so10_full_hessian/evaluate_sm_hessian_blocks.py', 'calculations/canonical_so10_full_hessian/parent_bilinear_oracle.py', 'calculations/canonical_so10_full_hessian/probe_mixed_orbit_bilinear.py', 'calculations/canonical_so10_full_hessian/verify_doublet_block_independent.py', 'calculations/canonical_so10_full_hessian/verify_oracle_controls.py', 'calculations/canonical_so10_full_hessian/verify_oracle_goldstone_rows.py', 'calculations/canonical_so10_vacuum_kernel/derive_doublet_block.py', 'calculations/canonical_so10_vacuum_kernel/derive_radial_hessian.py', 'calculations/canonical_so10_vacuum_kernel/derive_stabilizers.py', 'calculations/canonical_so10_vacuum_kernel/derive_vacuum.py', 'calculations/canonical_so10_vacuum_kernel/verify_sm_singlets_modular.py']:
    pp=ROOT/n;deps[str(pp)]=sha256(pp.read_bytes()).hexdigest()
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V430.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','DERIVATION.md','data.py','pilot.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw,n
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==27266
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'S4A1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
 'qualified_receipts':qualified,'old_blobs':27266,'seconds_each':600,'sampled_private_cap':8*1024**3,
 'launch_floor':350*1024**2,'whole_package_bytes':16*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings;27266oldblobs;no science executed',flush=True)
