from pathlib import Path
from hashlib import sha256
import ast,json,subprocess,sys,traceback
repository_path=Path(__file__).resolve().parents[2];output_path=Path(__file__).resolve().parent
control_path=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/nonminimal-source-products-v1-2026-10-26')
sys.path.insert(0,str(repository_path/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
file_hash=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
def dump(path,value):
    with path.open('xb') as f:f.write((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    control_path.mkdir(parents=True,exist_ok=True)
    base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    assert base=='2e04fbfd74c5b977be2d7345d2ae29c570173272'
    with(control_path/'old_git_tree.txt').open('xb') as f:f.write(subprocess.check_output(['git','ls-tree','-r','--full-tree','HEAD']))
    files=[repository_path/n for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','docs/RESEARCH_EXECUTION_HANDOFF_V659.md','tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']]
    specs={
     'canonical_so10_full_jet_source_master_bridge':['jets.py','PROOF.md','final_review_validation_receipt.json'],
     'canonical_so10_intrinsic_full_source_descent':['coefficient_ring.py','DERIVATION.md'],
     'canonical_so10_u_maximal_heat_cutoff':['primary_inputs.json.gz','replay_inputs.json.gz','final_review_validation_receipt.json'],
     'canonical_so10_u_dimensional_reconciliation':['IR_PROOF.md','PROOF.md','validation_receipt_v2.json','ir_validation_receipt_v2.json','final_review_validation_receipt.json'],
     'canonical_so10_u_projected_ward_terms':['PROOF.md','validation_receipt.json','final_review_validation_receipt.json'],
     'canonical_so10_joint_born_ir_trace_domain':['DERIVATION_V2.md','validation_receipt.json'],
     'canonical_so10_u_source_ward_bridge':['DERIVATION.md','final_review_validation_receipt.json'],
     'canonical_so10_cutoff_source_ward_operator':['DERIVATION.md','validation_receipt.json'],
     'canonical_so10_sterile_matter_action':['ACTION_V1.md','validation_receipt.json'],
     'canonical_so10_chiral_probe_support':['DERIVATION.md','validation_receipt.json'],
     'canonical_so10_intrinsic_quadratic_source_contacts':['RESULT.md','color_validation_receipt.json','final_review_validation_receipt.json'],
     'canonical_so10_remaining_u_contact_vertices':['RESULT.md','k_model_validation_receipt.json','validation_receipt.json','final_review_validation_receipt.json'],
     'canonical_so10_u_pair_contact_model':['RESULT.md','validation_receipt.json','lowering_validation_receipt.json','final_review_validation_receipt.json'],
     'canonical_so10_joint_marginal_fermion_normalization':['RESULT.md','validation_receipt.json'],
     'canonical_so10_probe_matter_source_consistency':['RESULT.md'],
     'canonical_so10_probe_auxiliary_resolvent':['RESULT.md']}
    for folder,names in specs.items():files.extend(repository_path/'calculations'/folder/name for name in names)
    for folder,names in [('canonical_so10_u_maximal_heat_cutoff',['primary_inputs.json.gz','replay_inputs.json.gz']),('canonical_so10_u_dimensional_reconciliation',['IR_PROOF.md','PROOF.md','validation_receipt_v2.json','ir_validation_receipt_v2.json']),('canonical_so10_u_projected_ward_terms',['PROOF.md','validation_receipt.json'])]:
        root=repository_path/'calculations'/folder;seal=read(root/'final_review_validation_receipt.json')['new_files_sha256']
        for name in names:
            path=root/name;assert file_hash(path)==seal[str(path.relative_to(repository_path)).replace('\\','/')]
    for name in ['.gitattributes','RECORD.md','PROOF.md','finite_algebra.py','audit.py','run.py']:
        path=output_path/name
        if path.suffix=='.py':ast.parse(path.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in path.read_bytes().splitlines()),name
        with(output_path/(name+'.source.txt')).open('xb') as f:f.write(path.read_bytes())
        files.extend([path,output_path/(name+'.source.txt')])
    dump(output_path/'preparation.json',{'input_sha256':{str(p):file_hash(p) for p in files},'base_HEAD':base,
      'scientific_acceptance':'NOT_PERFORMED','limits':{'native_seconds_after_imports':300,'review_seconds_after_imports':180,
       'sampled_private_bytes':8*1024**3,'launch_available_pagefile_bytes':350*1024**2,'packet_bytes':16*1024**2}})
    result=capture([sys.executable,'-B',str(output_path/'audit.py')])
    dump(output_path/'audit_capture.json',result);dump(control_path/'audit_full_capture.json',result)
    assert result['exit_code']==0 and result['execution_state']=='COMPLETED' and result['calculation_completed'] and result['post_run_observations_qualified']
    assert read(output_path/'product_result.json')['elapsed_after_imports']<300
    print('COMPLETED NSP1 source products',flush=True)
except BaseException:
    dump(output_path/'controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
