"""GVA1 freeze exact action/projector ancestry and all source bytes."""
from pathlib import Path
from hashlib import sha256
import json,ast,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='d7e1911fa983935714ee13cd9562556347fbe934'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/ghost-vector-sunset-v1-2026-10-21')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).strip() and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
def dump(p,b):
    with p.open('xb') as f:f.write(b)
deps={};cache={};qualified={}
for folder,receipt,want,wantsha in [
 ('canonical_so10_ghost_vector_support','validation_receipt.json','QUALIFIED_COMPLETE_GHOST_VECTOR_ACTION_CHARGE_AND_MASS_SUPPORT','480297602bdb2e3cf2d723eebc7ae6c66527c372b747ab7b4534e11892cedf21'),
 ('canonical_so10_ghost_vector_reduction','validation_receipt.json','QUALIFIED_GHOST_VECTOR_REGULATED_BARE_CURRENT_CONTACT_REDUCTION','9c8c486f25c4d7dc26c09b7d0c29b61730ffb0c7f713375366dcb3d377e4fc41'),
 ('canonical_so10_ghost_vector_reduction','pairing_receipt_v2.json','QUALIFIED_GHOST_VECTOR_FIXED_ROLE_MIXED_PLACEMENT_SCOPE','88ad4b9b45152eb67a6773e683560e2c2e1dfffeebd37053624b1438b6f4edf1'),
 ('canonical_so10_quantum_vector_derivative_uv','validation_receipt.json','QUALIFIED_FIXED_REFERENCE_QUANTUM_VECTOR_DERIVATIVE_AND_CURVATURE_UV_POLES','49dac2034b108e37abfaaf6f5f5f470d18e77a8dbaa7b583502fe293d543637f'),
 ('canonical_so10_quantum_vector_derivative_uv','validation_receipt_v2.json','QUALIFIED_FIXED_REFERENCE_QUANTUM_VECTOR_DERIVATIVE_AND_CURVATURE_UV_POLES','58a4e975eefd7a8926c5d50b4d580bc361c071c8334f25350d9aa906f344c47d'),
 ('canonical_so10_quantum_vector_mass_uv','validation_receipt.json','QUALIFIED_FULL_VECTOR_MASS_UV_POLE_AND_EXACT_FIELD_NORMALIZATION_RECONCILIATION','fedbac91e74fbe319bc6960add48a3cc0f2349670abba45746e3c0cee758a15a'),
 ('canonical_so10_charged_current_kernel','validation_receipt_v2.json','QUALIFIED_THREE_CHARGE_POSITIVE_MASS_CURRENT_KERNEL_AND_ACTUAL_FORESTS','19ef4e88094128111c0557455efe880a12479fd4ec253bccf67eb1ef88b29be5'),
 ('canonical_so10_scalar_current_forests','validation_receipt_v2.json','QUALIFIED_CURRENT_SUNSET_UV_FOREST_AND_MASS_INDEPENDENT_RPRIME_POLE',None),
 ('canonical_so10_spinzero_cubic_kernel','validation_receipt.json','QUALIFIED_COMPLETE_SPINZERO_CUBIC_F2_MATCHING_KERNEL','fce3be82ab650672b444b354f436bf4975992486b954d95a93c4731f54dcecf3'),
 ('canonical_so10_ghost_vector_uv_forests','validation_receipt.json','QUALIFIED_GHOST_VECTOR_ORIGINAL_PROPER_FORESTS_AND_POSITIVE_MASS_KERNEL_TRANSFER','d4a11257197a76136eaa027b9b88b925de2c02309d687cf73b1bf54069be7f5a'),
 ('canonical_so10_ghost_vector_soft_kernel','validation_receipt.json','QUALIFIED_BOTH_ACTUAL_GHOST_VECTOR_ONE_LIGHT_MATCHED_KERNELS','47991f7777b4629054eb757f716f14b59df10305241ab0ccddd7b2bc5fd846b2'),
 ('canonical_so10_r3_scalar_current','backend_receipt_v10.json','QUALIFIED_POSITIVE_MASS_MASTER_ANALYTIC_DERIVATIVE_BACKEND','56b3f303d55fc90d3f29654ef92ce50ffb3aaefe0a0159cbf0961d4ded558e65')]:
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
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V425.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md']:
    p=ROOT/n;deps[str(p)]=sha256(p.read_bytes()).hexdigest()
for n in ['RECORD.md','DERIVATION.md','data.py','measure.py','verify.py','prepare.py','run.py']:
    p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw,n
    if p.suffix=='.py':ast.parse(raw,filename=str(p))
    cp=HERE/(n+'.source.txt');dump(cp,raw);deps[str(p)]=deps[str(cp)]=sha256(raw).hexdigest()
state='d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8';assert sha256((ROOT/'project_state.json').read_bytes()).hexdigest()==state
old=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT);assert len(old.splitlines())==26886
CONTROL.mkdir(parents=True,exist_ok=False);dump(CONTROL/'old_git_tree.txt',old)
v={'schema':'GVA1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(deps.items())),
 'qualified_receipts':qualified,'old_blobs':26886,'seconds_each':600,'sampled_private_cap':8*1024**3,
 'launch_floor':350*1024**2,'whole_package_bytes':6*1024**2,'state_sha256':state,'scientific_acceptance':'NOT_PERFORMED'}
dump(HERE/'preparation.json',(json.dumps(v,sort_keys=True,indent=2)+'\n').encode())
print('FROZEN',len(deps),'bindings;26886oldblobs;no science executed',flush=True)
