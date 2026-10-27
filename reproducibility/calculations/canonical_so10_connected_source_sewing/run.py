from pathlib import Path
from hashlib import sha256
import ast,json,subprocess,sys,traceback
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/connected-source-sewing-v1-2026-10-26')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('xb') as f:f.write((json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='1e6344f26c0978ec74472584e8654f571b0804d1'
    C.mkdir(parents=True,exist_ok=True)
    with(C/'old_git_tree.txt').open('xb') as f:f.write(subprocess.check_output(['git','ls-tree','-r','--full-tree','HEAD']))
    files=[R/n for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md',
      'docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','docs/RESEARCH_EXECUTION_HANDOFF_V660.md',
      'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']]
    inherited=read(R/'calculations/canonical_so10_nonminimal_source_products/preparation_v3.json')['input_sha256']
    for folder,names in {
      'canonical_so10_full_jet_source_master_bridge':['jets.py','primary_tables.json.gz','replay_tables.json.gz','PROOF.md'],
      'canonical_so10_u_maximal_heat_cutoff':['primary_inputs.json.gz','replay_inputs.json.gz'],
      'canonical_so10_intrinsic_full_source_descent':['coefficient_ring.py'],
      'canonical_so10_u_dimensional_reconciliation':['IR_PROOF.md','PROOF.md'],
      'canonical_so10_joint_born_ir_trace_domain':['DERIVATION_V2.md'],
      'canonical_so10_nonminimal_source_products':['SOURCE_PRODUCT_SCOPE.md','PROOF.md','PROOF_CLARIFICATION_V2.md','finite_algebra_v2.py','validation_receipt_v2.json','RESULT.md','final_review_validation_receipt.json']}.items():
        base=R/'calculations'/folder
        owner=read(base/'final_review_validation_receipt.json') if (base/'final_review_validation_receipt.json').exists() else {}
        for name in names:
            p=base/name;h=digest(p)
            expected=owner.get('new_files_sha256',{}).get(p.relative_to(R).as_posix())
            if expected is None:expected=inherited.get(str(p))
            if name!='final_review_validation_receipt.json':assert h==expected,('NO_AUTHENTICATED_OWNER',str(p))
            files.append(p)
        if owner:files.append(base/'final_review_validation_receipt.json')
    # User-owned assessments are immutable input commentary, not scientific receipts.
    for folder in ['8aa0c302-c080-41bc-9701-fb9133b1c76c','d379d70d-c84f-4a00-a223-902f63e888a0']:
        files.append(Path('C:/Users/psboy/.codex/attachments')/folder/'Pasted text.txt')
    files.append(C/'readonly_tool_observations.json')
    for p in list(O.iterdir()):
        if p.is_file():
            if p.suffix=='.py':ast.parse(p.read_bytes())
            assert all(line==line.rstrip(b' \t') for line in p.read_bytes().splitlines()),p
            with(O/(p.name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
    files.extend(p for p in O.iterdir() if p.is_file())
    dump(O/'preparation.json',{'base':'1e6344f26c0978ec74472584e8654f571b0804d1','input_sha256':{str(p):digest(p) for p in files},'scientific_acceptance':'NOT_PERFORMED'})
    cap=capture([sys.executable,'-B',str(O/'native.py')])
    dump(O/'native_capture.json',cap);dump(C/'native_full_capture.json',cap)
    assert cap['exit_code']==0 and cap['execution_state']=='COMPLETED' and cap['calculation_completed'] and cap['post_run_observations_qualified']
    print('COMPLETED CNS1A native support and nonlinear check',flush=True)
except BaseException:
    dump(O/'controller_failure.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
