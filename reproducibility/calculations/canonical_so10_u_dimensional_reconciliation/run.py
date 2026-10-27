from pathlib import Path
from hashlib import sha256
import ast,json,subprocess,sys,traceback
O=Path(__file__).resolve().parent;R=O.parents[1]
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-dimensional-reconciliation-v1-2026-10-26')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
def dump(p,z):
    with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    C.mkdir(parents=True,exist_ok=True)
    with (C/'old_git_tree.txt').open('xb') as f:f.write(subprocess.run(['git','ls-tree','-r','--full-tree','HEAD'],stdout=subprocess.PIPE,check=True).stdout)
    bindings=dict(read(R/'calculations/canonical_so10_unprobed_baseline_C2/final_preparation.json')['input_sha256'])
    for pp,h in bindings.items():assert H(Path(pp))==h,pp
    specs={
     'canonical_so10_intrinsic_auxiliary_source':['kernel_validation_receipt.json','RESULT.md'],
     'canonical_so10_intrinsic_auxiliary_ghost_source':['kernel_primary_tables.json.gz','kernel_validation_receipt.json','DERIVATION.md'],
     'canonical_so10_intrinsic_quadratic_source_contacts':['kernel_validation_receipt_v2.json','RESULT.md'],
     'canonical_so10_remaining_u_contact_vertices':['validation_receipt.json','RESULT.md'],
     'canonical_so10_unprobed_antighost_kernel':['universal_validation_receipt.json','PROOF.md'],
     'canonical_so10_unprobed_auxiliary_source_kernel':['universal_validation_receipt.json'],
     'canonical_so10_unprobed_source_root_module':['kernel_primary_tables.json.gz','kernel_validation_receipt.json','RESULT.md'],
     'canonical_so10_unprobed_marginal_C3':['primary_blocks.json.gz','replay_blocks.json.gz','F_log3_complete_comparison.json.gz','final_review_validation_receipt.json'],
     'canonical_so10_unprobed_baseline_C2':['kernel_primary_tables.json.gz','kernel_replay_tables.json.gz','baseline_complete_comparison_v2.json.gz','final_review_validation_receipt.json'],
     'canonical_so10_u_lower_cutoff_contraction':['lorentz_result.json','PROOF.md'],
     'canonical_so10_u_F_fourth_support':['review_result.json','PROOF.md'],
     'canonical_so10_intrinsic_correlated_source_contacts':['CONTACT_DERIVATION.md','contact_kernel_validation_receipt.json'],
     'canonical_so10_full_jet_source_master_bridge':['PROOF.md','RESULT.md','final_review_validation_receipt.json'],
     'canonical_so10_intrinsic_full_source_descent':['variation_primary_inputs.json.gz','variation_replay_inputs.json.gz','variation_validation_receipt_v3.json','DERIVATION.md'],
     'canonical_so10_u_operation_root_inventory':['root_primary_tables.json.gz','validation_receipt.json'],
     'canonical_so10_unprobed_log2_completion':['log2_complete_comparison.json.gz','final_review_validation_receipt.json'],
     'canonical_so10_unprobed_log3_support':['T_log3_complete_comparison_v2.json.gz','RESULT.md','final_review_validation_receipt.json'],
     'canonical_so10_u_T_cutoff_tensor':['late_remainders_v2.json.gz','review_result_v2.json','final_review_validation_receipt.json'],
     'canonical_so10_u_F_remaining_contraction':['late_remainders.json.gz','final_review_validation_receipt.json']}
    for folder,names in specs.items():
        for name in names:
            pp=R/'calculations'/folder/name;bindings[str(pp)]=H(pp)
    for pp in [R/'AGENTS.md',R/'CHARTER.md',R/'project_state.json',R/'docs/LOCAL_RESEARCH_CONVENTIONS_V1.md',R/'docs/RESEARCH_EXECUTION_HANDOFF_V657.md']:bindings[str(pp)]=H(pp)
    for name in ['.gitattributes','RECORD.md','PROOF.md','audit.py','run.py']:
        pp=O/name
        if pp.suffix=='.py':ast.parse(pp.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in pp.read_bytes().splitlines()),name
        with (O/(name+'.source.txt')).open('xb') as f:f.write(pp.read_bytes())
        bindings[str(pp)]=H(pp);bindings[str(O/(name+'.source.txt'))]=H(pp)
    dump(O/'preparation.json',{'input_sha256':bindings,'base_HEAD':'a78b35931a67863375cbd969df27b972df6ced6a','scientific_acceptance':'NOT_PERFORMED','native_seconds_after_imports':300,'review_seconds_after_imports':180,'packet_limit_bytes':16*1024**2})
    z=capture([sys.executable,'-B',str(O/'audit.py')]);dump(O/'audit_capture.json',z);dump(C/'audit_full_capture.json',z)
    assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified']
    assert read(O/'audit_result.json')['elapsed_after_imports']<300
    print('COMPLETED UDR1 dimensional reconciliation',flush=True)
except BaseException:
    dump(O/'controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
