"""JMF1 immutable IO/types; scientific comparison routes are separate."""
from pathlib import Path
from hashlib import sha256
from functools import lru_cache
import json,gzip,os,sys,time,threading
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
read=lambda p:json.loads(p.read_bytes())
packed=lambda p:json.loads(gzip.decompress(p.read_bytes()))
digest=lambda p:sha256(p.read_bytes()).hexdigest()
eta,xi=s.symbols('eta_H xi',real=True)
@lru_cache(maxsize=65536)
def expr(z):
 z=s.expand(s.sympify(z,locals={'eta_H':eta,'xi':xi}))
 assert z.free_symbols<={eta,xi}
 s.Poly(z,eta,xi)
 return z
def token(z):return str(expr(z))
# doubled dimension,ghost number,Grassmann parity,Lorentz-index parity
TYPES={'B':(2,0,0,1),'x':(2,0,0,0),'c':(2,1,1,0),'a':(2,-1,1,0),
       'Lambda':(4,0,0,0),'P':(3,0,1,0),'KP':(3,-1,0,0),
       'JB':(4,-1,1,1),'Jx':(4,-1,1,0),'JC':(4,-2,0,0),
       'Ja':(4,0,0,0),'JL':(2,-1,1,0),'d':(2,0,0,1)}
FILES={
 'BSF':('canonical_so10_bosonic_source_onejet_finite','primary_v2_tables.json.gz','replay_v3_tables.json.gz','validation_receipt.json','d162225d8a2c9b562a594ce1c4afc4464b2448f96ceb872fe61d067e85022ded'),
 'SVT':('canonical_so10_source_vector_finite_transport','primary_v2_tables.json.gz','replay_v2_tables.json.gz','validation_receipt_v2.json','7b84871bd217466526419e5ed2a12ce284014d91ed567b8d00c7b0c352c6ac9d'),
 'LSF':('canonical_so10_lower_source_vector_finite','primary_tables.json.gz','replay_tables.json.gz','validation_receipt_v2.json','62c5ed150391a88f9409b27acbdac7d9d95dfad4dc0d2b647675b996a2d12ccf'),
 'SCF':('canonical_so10_scalar_source_finite_comparison','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','429e1b2abb38cc3944341f99cdccbbbb3d2a498f0e7839b01b2b23028b828a14'),
 'GSF':('canonical_so10_ghost_source_finite_comparison','primary_tables.json.gz','replay_tables.json.gz','validation_receipt.json','475eef3e5dc25caa7a358bbb9c50f62b1e589d80564b36af9f20dec9c67330c1')}
HSC=CAL/'canonical_so10_complete_heat_scalar_response'
CHW=CAL/'canonical_so10_closed_heat_ward_normalization'
def embedded(h):
 v=h['old_three_projection_family']['previous_CHV_family']
 return {'BSF':v['relative_onejet_parents']['RHO'],
         'SVT':v['relative_vector_bosonic_sources']['SVT'],
         'LSF':v['relative_vector_bosonic_sources']['LSF'],
         'SCF':h['new_relative_scalar_source_coefficients'],
         'GSF':h['old_three_projection_family']['new_proper_ghost_source_coefficients']}
def parents(role):
 ans={}
 for tag,(fo,p,r,receipt,h) in FILES.items():
  assert digest(CAL/fo/receipt)==h
  d=packed(CAL/fo/(p if role=='primary' else r))
  if tag=='BSF':v=d['rho']
  elif tag in ['SVT','LSF']:v={part:{'B':m['B']} for part,m in d['finite_tensors'].items()}
  else:v=d['finite_coefficients']
  ans[tag]=v
 return ans
def begin(role):
 tick=time.perf_counter();t=threading.Timer(600,lambda:os._exit(124));t.daemon=True;t.start()
 assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]));peer='replay' if role=='primary' else 'primary'
   if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('JMF1_PEER_DENIED')
 sys.addaudithook(audit)
 return tick
def finish(role,out,tick):
 out.update({'elapsed_after_imports':time.perf_counter()-tick,'physical_scheme_adopted':False,
 'scientific_acceptance':'NOT_PERFORMED','authority':'34/39','new_loop_integrals':0,
 'full_chiral_Slavnov_QAP_measure_phase_background_massive_or_E5A5_qualified':False})
 raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'elapsed_after_imports':out['elapsed_after_imports'],
 'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest(),
 'packed_bytes':len(blob),'raw_bytes':len(raw)},sort_keys=True),flush=True)
