"""SPS1 freeze selected inherited derivation and gate-only bindings."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE='1f343f288e5966fb50bf828b83f9119cf903a2e7'
CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/singlet-portal-scope-v1-2026-10-22')
git=lambda *v:subprocess.check_output(['git',*v],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
bindings={};gates={}
def add(p,h=None,dest=bindings):
 p=p.resolve();value=sha256(p.read_bytes()).hexdigest()
 if h is not None:assert value==h,str(p)
 if str(p) in dest:assert dest[str(p)]==value
 dest[str(p)]=value
rsc=ROOT/'calculations/canonical_so10_scalar_kernel_reconciliation'
for prep in sorted(rsc.glob('*preparation*.json')):
 for n,h in json.loads(prep.read_bytes())['input_sha256'].items():add(Path(n),h)
for name in ['RECORD.md','RESULT.md','kernels.py','verify.py','primary_tables.json.gz','validation_receipt.json']:add(rsc/name)
add(rsc/'validation_receipt.json','537e0d12ce964611510133575f0442b30af4f211ed10b13e4bc86907b78bf645')
for name in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V470.md','docs/SOLO_REVIEW_POLICY_V1.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md',
 'calculations/canonical_so10_benchmark_scope_reconciliation/CORRECTION.md','calculations/canonical_so10_benchmark_scope_reconciliation/validation_receipt.json',
 'calculations/canonical_so10_positive_higgs/POINT.json','calculations/canonical_so10_scalar_benchmark/STAGE1_POINT.json',
 'calculations/canonical_so10_coherent_joint_witness/POINT.json','calculations/canonical_so10_finite_radial_control/primary_result.json','calculations/canonical_so10_finite_radial_control/validation_receipt.json']:
 add(ROOT/name)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8')
for folder,names in {
 'canonical_so10_singlet_pole_rg_check':['primary_result.json','validation_receipt.json','RECORD.md','RESULT.md','rg.py'],
 'canonical_so10_singlet_pole_control':['validation_receipt.json','RECORD.md','RESULT.md'],
 'canonical_so10_singlet_quartic_running':['validation_receipt.json','source_receipt.json','RESULT.md']}.items():
 for name in names:add(ROOT/'calculations'/folder/name,dest=gates)
add(Path('C:/Users/psboy/.codex/attachments/5adbce2e-1054-4c29-af2c-523f42088434/Pasted text.txt'),dest=gates)
for name in ['RECORD.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
 if name.endswith('.py'):ast.parse(raw)
 with (HERE/(name+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(name+'.source.txt'))
tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==29796
CONTROL.mkdir(parents=True,exist_ok=False)
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'SPS1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(bindings.items())),
 'gate_only_sha256':dict(sorted(gates.items())),'seconds_each':120,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':8*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('SPS1_FROZEN',len(bindings),'derivation bindings',len(gates),'gate-only bindings',flush=True)
