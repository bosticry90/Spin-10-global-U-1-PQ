from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/double-source-finite-ward-v1-2026-10-24');BASE='c3d457dc400931fdf2226284693f04d81467d44c'
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT);dig=lambda p:sha256(p.read_bytes()).hexdigest();b={}
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main' and not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
def add(p,h=None):
 p=p.resolve();v=dig(p)
 if h is not None:assert v==h,p
 b[str(p)]=v
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/RESEARCH_EXECUTION_HANDOFF_V582.md']:add(ROOT/n)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8')
add(Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/double-source-finite-contact-v1-2026-10-24/postcommit_seal.json'))
for folder,ns in {'canonical_so10_double_source_finite_contact':['RECORD.md','DERIVATION.md','CONTINUATION_V2.md','RESULT.md','validation_receipt.json','validation_receipt_v2.json','selected_double_source_finite_contact.json.gz'],'canonical_so10_double_auxiliary_source_pole':['PROOF.md','actual_primary_v2_result.json','actual_replay_v2_result.json','validation_receipt.json'],'canonical_so10_cutoff_source_ward_operator':['DERIVATION.md','validation_receipt.json','primary_inputs.json.gz','replay_inputs.json.gz'],'canonical_so10_tangent_source_operation':['DERIVATION.md','CONTINUATION_V2.md','validation_receipt_v2.json'],'canonical_so10_sourcequadratic_primitive_probe':['DERIVATION.md','TRACE_DOMAIN_NOTE.md','validation_receipt.json']}.items():
 for n in ns:add(CAL/folder/n)
add(CAL/'canonical_so10_double_source_finite_contact/validation_receipt.json','0936ea9c668f7a693379dbf8fd8b8699c894790ebe88c712ebff32051b6d7da7');add(CAL/'canonical_so10_double_source_finite_contact/validation_receipt_v2.json','8f9fda77d948c04efdd3d64da7a23b457e119a82d7deef990346fb05f18cefb4')
for role in ['primary','replay']:
 for folder,name in [('frozen_a10_physical_reconciliation','full_'+role+'.json'),('frozen_a10_e1_fermion',role+'.json'),('frozen_a10_e5_ghost_normalization',role+'.json'),('frozen_a10_bv_master',role+'.json'),('frozen_a10_e2_transport',role+'.json')]:add(PK/folder/name)
add(PK/'export_a10_e5_antighost_vector.py')
for n in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/n;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(n+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(n+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==34001
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'DSW1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(b.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'packet_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('DSW1_FROZEN',len(b),'bindings',flush=True)
