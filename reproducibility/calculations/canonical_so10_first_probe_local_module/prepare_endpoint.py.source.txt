from pathlib import Path
from hashlib import sha256
import ast,gzip,json
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()));b=dict(read(O/'validation_preparation.json')['input_sha256'])
for p,h in b.items():assert H(Path(p))==h,p
assert read(O/'validation_receipt.json')['complete_projected_unshifted_first_probe_bare_local_cancellation'];b[str(O/'validation_receipt.json')]=H(O/'validation_receipt.json')
md=O.parent/'canonical_so10_probe_mass_dimension_one';ep=O.parent/'canonical_so10_even_probe_vertices';rx=O.parent/'canonical_so10_probe_scalar_support'
for role in ['primary','replay']:
 p=md/('ending_'+role+'_tables.json.gz');assert H(p)==read(md/'ending_validation_preparation.json')['input_sha256'][str(p)];b[str(p)]=H(p);b[str(md/'ending_validation_preparation.json')]=H(md/'ending_validation_preparation.json')
 dst=O/('endpoint_'+role+'_inputs.json.gz')
 with dst.open('xb') as f:f.write(gzip.compress((json.dumps(load(p),sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
 b[str(dst)]=H(dst)
for folder,ns in [('canonical_so10_even_probe_vertices',['primary_tables.json.gz','replay_tables.json.gz','validation_preparation.json','validation_receipt.json','RESULT.md']),('canonical_so10_probe_auxiliary_resolvent',['compression_receipt.json','validation_receipt_v2.json','RESULT.md']),('canonical_so10_probe_mass_dimension_one',['symbol_receipt.json','ending_validation_receipt.json','RESULT.md']),('canonical_so10_probe_scalar_support',['quantum_primary_inputs.json.gz','quantum_validation_preparation_v3.json']),('canonical_so10_chiral_probe_support',['RESULT.md'])]:
 for n in ns:
  p=O.parent/folder/n;b[str(p)]=H(p)
for n in ['ENDPOINT_RECORD.md','prepare_endpoint.py','endpoint.py','verify_endpoint.py','run_endpoint.py']:
 p=O/n
 if p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'))
 with(O/(n+'.source.txt')).open('xb') as f:f.write(p.read_bytes())
 b[str(p)]=H(p);b[str(O/(n+'.source.txt'))]=H(O/(n+'.source.txt'))
with(O/'endpoint_preparation.json').open('xb') as f:f.write((json.dumps({'input_sha256':b,'seconds_after_imports':180,'sampled_private_bytes':8*1024**3,'launch_floor':350*1024**2,'packet_bytes':12*1024**2,'scientific_acceptance':'NOT_PERFORMED'},sort_keys=True,separators=(',',':'))+'\n').encode())
print('PREPARED_HP1',len(b),flush=True)
