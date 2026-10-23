"""G2P1 freeze exact action/projector ancestry and all source bytes."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='d6a2d238e24b37a8715938728e06d23a8b8a66b8'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/nine-family-uv-assembly-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={};qualified={}
for folder,receipt,want,wantsha in [('canonical_so10_two_loop_gauge_beta', 'validation_receipt.json', 'QUALIFIED_INDEPENDENT_TWO_LOOP_GAUGE_SCALAR_PARENT_AND_LIGHT_RG_COMPARATOR', '658ccb86ed02611bd09816471fa4dd942f9099322416762db47a934c8c879d06'), ('canonical_so10_vector_quartic_ir_matching', 'validation_receipt_v2.json', 'QUALIFIED_ACTUAL_QUARTIC_MIXED_AND_ALL_LIGHT_IR_SUBTRACTION_WITH_BARE_HARD_REMAINDER', 'c0f72f4fd5f17011d1fbcdb7e2c291c47189f237b45b0858b28d1ff8ce46d734'), ('canonical_so10_vector_quartic_uv_subgraphs', 'validation_receipt_v2.json', 'QUALIFIED_FULL_INTERNAL_POLE_SPLIT_HEAVY_INSERTIONS_AND_KNOWN_PARENT_JET_LIMIT', 'c9b545e1c00c9750a587c6543315431ee0620f7e19fd2168db5fcf1533290fa4'), ('canonical_so10_vector_scalar_quartic', 'validation_receipt.json', 'QUALIFIED_VVSS_GRAPH_LOCAL_UV_AND_LIGHT_MATCHED_FINITE_F2', '7fc8e23487ea5eb31a32e6351c62688be3b6d0558e3bebe047b0811b4d77f5e8'), ('canonical_so10_scalar_current_vss_assembly', 'validation_receipt.json', 'QUALIFIED_COMPLETE_COMMON_SCALE_VSS_PRIMITIVE', '6b47bd50b75902c2f662921d04ffc4e6fbd348193f69c9493b141b05b0ac7410'), ('canonical_so10_ghost_scalar_sunset', 'validation_receipt.json', 'QUALIFIED_COMPLETE_COMMON_SCALE_GHOST_SCALAR_PRIMITIVE', '6a03b1c5935ddf03d5f33f1f77cc18e7bc178aa30ca521b5fb814f624bc9b970'), ('canonical_so10_vector_vector_scalar_sunset', 'validation_receipt.json', 'QUALIFIED_COMPLETE_COMMON_SCALE_VVS_PRIMITIVE', '18b66c847c5b09c937953b939e0d34469753c5b2c0262ffc15ad646f443402aa'), ('canonical_so10_ghost_vector_sunset', 'validation_receipt.json', 'QUALIFIED_COMPLETE_GHOST_VECTOR_MATCHED_PRIMITIVE_WITH_ORIGINAL_FORESTS', '5598f0b25d67a8fa864a8689e4d3619d24623f00d42aa24d93d62706983d2f09'), ('canonical_so10_three_vector_sunset', 'validation_receipt_v2.json', 'QUALIFIED_COMPLETE_THREE_VECTOR_MATCHED_PRIMITIVE_WITH_ORIGINAL_FORESTS', '82dbc81907516a52c5254eaa4d1d591bae42862b76b4a1d4a9b2ebb89f06c8e8'), ('canonical_so10_scalar_quartic_amplitude', 'validation_receipt.json', 'QUALIFIED_COMPLETE_SCALAR_QUARTIC_MATCHED_PRIMITIVE', '25737305b6729d56a353df89196d478bbc508022cdc4d5587a78cb72adc78242'), ('canonical_so10_scalar_cubic_amplitude', 'validation_receipt.json', 'QUALIFIED_COMPLETE_SCALAR_CUBIC_MATCHED_PRIMITIVE', '298979190845132e09dfcba4a2ac87c8896176a01e965e15310e64958aa5c463')]:
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
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V434.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw,n
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==27727
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'G2P1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
 'qualified_receipts':qualified,'old_blobs':27727,'seconds_each':600,'sampled_private_cap':8*1024**3,
 'launch_floor':350*1024**2,'whole_package_bytes':24*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings;27727oldblobs;no science executed',flush=True)
