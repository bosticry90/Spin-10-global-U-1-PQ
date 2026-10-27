from pathlib import Path
from hashlib import sha256
import ast,gzip,json,subprocess
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()));b={}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='f117ec76cea032348da9811e617e17e3214fd4ae'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=R).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V598.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md','tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/export_a10_e5_antighost_vector.py']:
 p=R/n;b[str(p)]=H(p)
pf=O.parent/'canonical_so10_probe_fermion_onejet';ep=O.parent/'canonical_so10_even_probe_vertices';rx=O.parent/'canonical_so10_probe_scalar_support';pm=O.parent/'canonical_so10_probe_matter_source_consistency';cg=O.parent/'canonical_so10_probe_chiral_ghost_kernel'
def bound(p,m):
 assert H(p)==read(m)['input_sha256'][str(p)],p;b[str(p)]=H(p);b[str(m)]=H(m)
bound(pf/'construction_tables.json.gz',pf/'construction_validation_preparation.json');bound(ep/'gauge_tables.json.gz',ep/'gauge_validation_preparation_v2.json');bound(rx/'construction_receipt.json',O.parent/'canonical_so10_probe_ghost_scalar_kernel/quantum_validation_preparation.json');bound(rx/'quantum_primary_v3_tables.json.gz',rx/'quantum_validation_preparation_v3.json')
p=pm/'primitive_tables.json.gz';assert H(p)==read(pm/'primitive_receipt.json')['packed_sha256'];b[str(p)]=H(p)
receipts={'rho_PP_jet':pf/'construction_check_receipt.json','uC_PP_jet':ep/'gauge_validation_receipt_v2.json','rho_BPP':O.parent/'canonical_so10_rho_vector_support/loop_validation_receipt_v2.json','uC_BPP':O.parent/'canonical_so10_probe_ghost_vector_vertices/loop_validation_receipt_v3.json','rho_xPP':rx/'construction_receipt.json','uC_xPP':O.parent/'canonical_so10_probe_ghost_scalar_kernel/quantum_validation_receipt.json','rho_PP_intrinsic':O.parent/'canonical_so10_probe_mass_dimension_one/symbol_receipt.json','uC_PP_intrinsic':O.parent/'canonical_so10_probe_mass_dimension_one/symbol_receipt.json','rhoC_KPP':pm/'primitive_receipt.json','uCC_KPP':pm/'primitive_receipt.json'}
for p in set(receipts.values()):b[str(p)]=H(p)
for key,folder,n in [('rho_BPP','canonical_so10_rho_vector_support','loop_comparison_v2_tables.json.gz'),('uC_BPP','canonical_so10_probe_ghost_vector_vertices','loop_comparison_v3_tables.json.gz')]:
 p=O.parent/folder/n;assert H(p)==read(receipts[key])['comparison_packed_sha256'];b[str(p)]=H(p)
for folder,ns in [('canonical_so10_sterile_matter_action',['ACTION_V1.md','validation_receipt.json']),('canonical_so10_chiral_probe_support',['RESULT.md','validation_receipt.json']),('canonical_so10_probe_fermion_onejet',['COMPANION_CONSTRUCTION.md']),('canonical_so10_probe_mass_dimension_one',['RESULT.md']),('canonical_so10_probe_scalar_support',['CONSTRUCTION_RECORD.md','quantum_validation_receipt_v3.json']),('canonical_so10_probe_ghost_scalar_kernel',['RESULT_V2.md'])]:
 for n in ns:
  p=O.parent/folder/n;b[str(p)]=H(p)
F=load(pf/'construction_tables.json.gz');K=load(ep/'gauge_tables.json.gz');M=read(rx/'construction_receipt.json')
for role in ['primary','replay']:
 p=cg/(role+'_inputs.json.gz');bound(p,cg/'validation_preparation_v2.json');d=load(p)
 z={'names':d['names'],'geometry':d['geometry'],'physical_G':d['physical_G'],'physical_QG':d['physical_QG'],'F':F['F'],'x_source':F['x_source'],'K_vector':[row['plane'] for row in K['candidate']],'K_mass':M['K_mass_operators_without_outer_g10_squared'],'source_primitive':load(pm/'primitive_tables.json.gz'),'receipts':{key:{'path':str(p),'sha256':H(p),'data':read(p)} for key,p in receipts.items()},'extraction':'INTEGRATION_OF_ALREADY_MEASURED_INPUTS_NOT_A_NEW_UNKNOWN_QUANTUM_CALCULATION'}
 p=O/(role+'_inputs.json.gz')
 with p.open('xb') as out:out.write(gzip.compress((json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
 b[str(p)]=H(p)
for n in ['RECORD.md','prepare.py','native.py','verify.py','run.py']:
 p=O/n
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
 with(O/(n+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 b[str(p)]=H(p);b[str(O/(n+'.source.txt'))]=H(O/(n+'.source.txt'))
with(O/'preparation.json').open('xb') as out:out.write((json.dumps({'input_sha256':b,'seconds_after_imports':180,'sampled_private_bytes':8*1024**3,'launch_floor':350*1024**2,'packet_bytes':12*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,separators=(',',':'))+'\n').encode())
print('PREPARED_LFM1',len(b),flush=True)
