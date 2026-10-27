from pathlib import Path
from hashlib import sha256
import ast,json,sys,traceback
O=Path(__file__).resolve().parent;R=O.parents[1]
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/u-dimensional-reconciliation-v1-2026-10-26')
sys.path.insert(0,str(R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'))
from export_a10_e5_antighost_vector import capture
H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes())
def dump(p,z):
    with p.open('xb') as f:f.write((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode())
try:
    bindings=dict(read(O/'ir_preparation.json')['input_sha256'])
    for pp,h in bindings.items():assert H(Path(pp))==h,pp
    assert read(O/'validation_receipt_v2.json')['complete_declared_local_relative_T_F_symbol_zero']
    for folder,names in [('canonical_so10_joint_born_ir_trace_domain',['RECORD.md','DERIVATION_V2.md','validation_receipt.json']),
      ('canonical_so10_full_jet_source_master_bridge',['free_tangent_tables.json.gz','free_tangent_result.json','final_review_validation_receipt.json']),
      ('canonical_so10_u_maximal_heat_cutoff',['primary_inputs.json.gz','replay_inputs.json.gz']),
      ('canonical_so10_u_F_fourth_support',['operators.py'])]:
        for name in names:
            pp=R/'calculations'/folder/name;bindings[str(pp)]=H(pp)
    for name in ['IR_CORRECTION_V2.md','ir_support_v2.py','run_ir_v2.py']:
        pp=O/name
        if pp.suffix=='.py':ast.parse(pp.read_bytes())
        assert all(line==line.rstrip(b' \t') for line in pp.read_bytes().splitlines()),name
        with (O/(name+'.source.txt')).open('xb') as f:f.write(pp.read_bytes())
    for pp in O.iterdir():
        if pp.is_file():bindings[str(pp)]=H(pp)
    dump(O/'ir_preparation_v2.json',{'input_sha256':bindings,'scientific_acceptance':'NOT_PERFORMED'})
    z=capture([sys.executable,'-B',str(O/'ir_support_v2.py')]);dump(O/'ir_capture_v2.json',z);dump(C/'ir_full_capture_v2.json',z)
    assert z['exit_code']==0 and z['execution_state']=='COMPLETED' and z['calculation_completed'] and z['post_run_observations_qualified']
    assert read(O/'ir_support_result_v2.json')['elapsed_after_imports']<300
    print('COMPLETED UDR3 actual first-u IR support',flush=True)
except BaseException:
    dump(O/'ir_controller_failure_v2.json',{'execution_state':'FAILED_OR_INCOMPLETE','traceback':traceback.format_exc(),'failure_relabelled_PASS':False});raise
