"""MSU1 exact inputs and extraction of qualified Lie data without loop targets."""
from pathlib import Path
from hashlib import sha256
import ast,gzip,json,subprocess
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
BASE='5d2e707250454ec32adff1e058ef386217334e15';CONTROL=Path('C:/Users/psboy/.codex/research-control-records/ToE-Next/matter-source-uv-assembly-v1-2026-10-22')
git=lambda *v:subprocess.check_output(['git',*v],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
b={}
def add(p,h=None):
 p=p.resolve();v=sha256(p.read_bytes()).hexdigest()
 if h is not None:assert v==h,str(p)
 b[str(p)]=v
for n in ['AGENTS.md','CHARTER.md','project_state.json','docs/RESEARCH_EXECUTION_HANDOFF_V499.md','docs/LOCAL_RESEARCH_CONVENTIONS_V1.md','docs/SOLO_REVIEW_POLICY_V1.md']:add(ROOT/n)
for n in ['export_a10_e5_antighost_vector.py','frozen_a10_physical_reconciliation/full_primary.json','frozen_a10_physical_reconciliation/full_replay.json']:add(PK/n)
for folder,names in {'canonical_so10_yukawa_carrier_transport':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_sterile_matter_action':['ACTION_V1.md','validation_receipt.json'],'canonical_so10_matter_field_source_image':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','RESULT.md'],'canonical_so10_matter_vector_source_pole':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','RESULT.md'],'canonical_so10_matter_auxiliary_source_pole':['primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json'],'canonical_so10_local_source_primitive':['primary_v2_result.json','replay_v2_result.json','validation_receipt.json','primitive_v2.py','RESULT.md'],'canonical_so10_scalar_source_g3_color':['RESULT.md'],'canonical_so10_matter_source_vertex_support':['RESULT.md','validation_receipt.json']}.items():
 for n in names:add(ROOT/'calculations'/folder/n)
add(ROOT/'project_state.json','d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8');add(ROOT/'calculations/canonical_so10_local_source_primitive/validation_receipt.json','f3dca97f46713f82deb10f8b462e375f475d608a58a9e9cca91fa10bbeb54748');add(ROOT/'calculations/canonical_so10_matter_field_source_image/validation_receipt.json','c7b41c7ef2825a10f0ce362a01af5f395ae74360d280295588879184fddf8ef3')
parent=ROOT/'calculations/canonical_so10_matter_auxiliary_source_pole/replay_tables.json.gz';data=json.loads(gzip.decompress(parent.read_bytes()));extracted={'schema':'MSU1_REUSED_QUALIFIED_LIE_FIELD_ONLY','source_sha256':sha256(parent.read_bytes()).hexdigest(),'source_field':'plane_f','plane_f':data['plane_f']}
with (HERE/'qualified_lie_constants.json.gz').open('xb') as f:f.write(gzip.compress((json.dumps(extracted,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
add(HERE/'qualified_lie_constants.json.gz')
for name in ['RECORD.md','DERIVATION.md','data.py','primary.py','replay.py','verify.py','prepare.py','run.py']:
 p=HERE/name;raw=p.read_bytes();assert b'\r' not in raw
 if p.suffix=='.py':ast.parse(raw)
 with (HERE/(name+'.source.txt')).open('xb') as f:f.write(raw)
 add(p);add(HERE/(name+'.source.txt'))
CONTROL.mkdir(parents=True,exist_ok=False);tree=git('ls-tree','-r',BASE);assert len(tree.splitlines())==30684
with (CONTROL/'old_git_tree.txt').open('xb') as f:f.write(tree)
with (HERE/'preparation.json').open('xb') as f:f.write((json.dumps({'schema':'MSU1_PREPARATION','base_commit':BASE,'input_sha256':dict(sorted(b.items())),'seconds_each':600,'sampled_private_cap':8*1024**3,'launch_floor':350*1024**2,'package_cap':16*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,indent=2)+'\n').encode())
print('MSU1_FROZEN',len(b),'bindings',flush=True)
