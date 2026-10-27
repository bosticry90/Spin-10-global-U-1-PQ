from pathlib import Path
from hashlib import sha256
import json,gzip,subprocess,ast
O=Path(__file__).resolve().parent;R=O.parents[1];H=lambda p:sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(gzip.decompress(p.read_bytes()));bindings={}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()=='55b04dd31e6a3fc3f4c6610d7daa0616848aab7e'
def bind(p):
 assert p.read_bytes()==subprocess.check_output(['git','show','HEAD:'+p.relative_to(R).as_posix()],cwd=R);bindings[str(p)]=H(p)
S=O.parent/'canonical_so10_intrinsic_scalar_source_ghost';F=O.parent/'canonical_so10_finite_intrinsic_scalar_source'
for role in ['primary','replay']:
 ip=S/(role+'_inputs.json.gz');tp=S/(role+'_tables.json.gz');fp=F/(role+'_v2_tables.json.gz')
 for p in [ip,tp,fp]:bind(p)
 a,b,c=load(ip),load(tp),load(fp);data={k:a[k] for k in ['xs','source_Qx','source_QC','frame']};data.update({k:b[k] for k in ['scalar_representation','outputs']});data['source_vectors']=c['source_vectors'];dst=O/(role+'_inputs.json.gz')
 with dst.open('xb') as f:f.write(gzip.compress((json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
 bindings[str(dst)]=H(dst)
for folder,ns in [('canonical_so10_intrinsic_scalar_source_ghost',['validation_receipt.json','review_receipt.json','shift_receipt.json','yukawa_bridge_receipt.json','RESULT.md']),('canonical_so10_finite_intrinsic_scalar_source',['validation_receipt_v2.json','lift_receipt.json','LIFT_RECORD.md']),('canonical_so10_cutoff_source_ward_operator',['DERIVATION.md','validation_receipt.json']),('canonical_so10_intrinsic_regulator_root_v2',['RESULT.md','validation_receipt.json']),('canonical_so10_intrinsic_hatted_insertion',['LOCAL_GROUP_PROOF.md','gaussian_validation_receipt.json']),('canonical_so10_intrinsic_ghost_root_schur',['RESULT.md','euler_receipt.json','assembly_receipt_v2.json','joint_receipt.json'])]:
 for name in ns:bind(O.parent/folder/name)
for name in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V616.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']:bind(R/name)
for name in ['RECORD.md','DESCENT.md','PRELAUNCH_CORRECTION_V2.md','native.py','prepare.py','verify.py','run_v2.py']:
 p=O/name
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
 with(O/(name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 bindings[str(p)]=H(p);bindings[str(O/(name+'.source.txt'))]=H(p)
for name in ['run.py','prelaunch_tool_observation.json']:
 p=O/name
 with(O/(name+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 bindings[str(p)]=H(p);bindings[str(O/(name+'.source.txt'))]=H(p)
with(O/'preparation.json').open('xb') as f:f.write((json.dumps({'input_sha256':bindings,'seconds_after_imports':300,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True)+'\n').encode())
print('PREPARED_IFC1',len(bindings),flush=True)
