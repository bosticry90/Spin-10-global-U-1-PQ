"""Freeze bounded inputs and execution controllers before native calculation."""
from pathlib import Path
from hashlib import sha256
import json,subprocess
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
C=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/background-threshold-inputs-v1-2026-10-20')
C.mkdir(parents=True,exist_ok=False)
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert base=='e179dcafc59e2d012e2658a6b6e46e802f24f118'
P=R/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
files=[R/n for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/SOLO_REVIEW_POLICY_V1.md',
'docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/ai_research_epistemic_ladder_v1/AI_RESEARCH_EPISTEMIC_LADDER_V1.md',
'docs/RESEARCH_EXECUTION_HANDOFF_V372.md',
'calculations/canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md','calculations/canonical_so10_positive_higgs/POINT.json',
'calculations/canonical_so10_direct_gauge_matching/RECORD.md','calculations/canonical_so10_direct_gauge_matching/derive_and_solve.py',
'calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/RECORD.md',
'calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/MASTER_BASIS_CONTRACT.md',
'calculations/canonical_so10_direct_two_loop_gauge_scalar_threshold/compile_scalar_vertices.py',
'calculations/canonical_so10_gauge_matching/vector_ledger.json','calculations/canonical_so10_gauge_matching/scalar_sm_ledger.json',
'calculations/canonical_so10_full_hessian/RESULT.md','calculations/canonical_so10_vacuum_master_pilot/validation_receipt_v2.json',
'calculations/canonical_so10_vacuum_master_pilot/DERIVATION.md']]
files +=[P/n for n in ['frozen_a10_physical_reconciliation/full_primary.json','frozen_a10_physical_reconciliation/full_replay.json',
'frozen_a10_physical_reconciliation/validation_receipt.json','a10_physical_reconciliation.py',
'export_a10_e5_antighost_vector.py','audit_a10_e5_antighost_vector.py']]
owned=[p for p in D.iterdir() if p.is_file() and not p.name.endswith('.source.txt')]
for p in owned:
 if p.suffix in ['.py','.md']:
  with (D/(p.name+'.source.txt')).open('xb') as out:out.write(p.read_bytes())
files+=list(D.iterdir())
# Preserve every old Git object mapping; no evidence under old paths is edited.
tree=subprocess.check_output(['git','ls-tree','-r',base],cwd=R)
with (C/'old_git_tree.txt').open('xb') as out:out.write(tree)
files.append(C/'old_git_tree.txt')
assert sha256((R/'calculations/canonical_so10_scalar_reconstruction/PARENT_ACTION_V1.md').read_bytes()).hexdigest()=='01323e0f6a025edd6f6669b43e7c730f5350e28d8561e72df89636862ca358ed'
assert sha256((R/'calculations/canonical_so10_positive_higgs/POINT.json').read_bytes()).hexdigest()=='476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816'
v={'schema':'C1_BACKGROUND_THRESHOLD_INPUT_PREPARATION_V1','base_commit':base,'old_git_blobs':len(tree.splitlines()),
'input_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in files},
'native_seconds_after_imports':120,'verifier_seconds_after_imports':180,
'sampled_private_limit':8*1024**3,'launch_available_commit_floor':350*1024**2,'package_limit':4*1024**2}
with (D/'preparation.json').open('xb') as out:out.write((json.dumps(v,indent=2,sort_keys=True)+'\n').encode())
print('FROZEN',len(files),'bindings;',v['old_git_blobs'],'old tracked blobs',flush=True)
