from pathlib import Path
from hashlib import sha256
from collections import defaultdict,Counter
from functools import lru_cache
import json,gzip,os,sys,time,threading
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations';PK=ROOT/'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1'
read=lambda p:json.loads(p.read_bytes());packed=lambda p:json.loads(gzip.decompress(p.read_bytes()));digest=lambda p:sha256(p.read_bytes()).hexdigest()
TARGET=(2,1,3,1,1,1);ZERO=(0,0,0,0,0,0)
G=[('B','B','BB'),('B','L','BL'),('L','B','LB'),('C','a','Ca'),('a','C','aC'),('F','F','FF'),('X','X','XX')]
V=[('B','F','gP_BF',(1,0,1,0,0,0)),('F','B','gP_FB',(1,0,1,0,0,0)),('X','F','YP_XF',(1,0,0,1,0,0)),('F','X','YP_FX',(1,0,0,1,0,0)),('a','B','gC_aB',(0,1,1,0,0,0)),('B','a','gC_Ba',(0,1,1,0,0,0)),('a','L','xiC_aL',(0,1,0,0,1,0)),('L','a','xiC_La',(0,1,0,0,1,0)),('a','X','GF_CaX_v',(0,1,2,0,1,1)),('X','a','GF_XaC_v',(0,1,2,0,1,1)),('L','X','GF_LX_v',(0,0,1,0,1,1)),('X','L','GF_XL_v',(0,0,1,0,1,1))]
plus=lambda a,b:tuple(x+y for x,y in zip(a,b))
allowed=lambda a:all(x<=y for x,y in zip(a,TARGET))
def begin(role):
 t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def audit(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]));peer='replay' if role=='primary' else 'primary'
   if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('VHR1_PEER_DENIED')
   if p.parent.name=='canonical_so10_ghost_vertex_order_reconciliation' and p.suffix=='.gz':raise PermissionError('VHR1_COEFFICIENT_TARGET_DENIED')
 sys.addaudithook(audit);return t
def roots(role):
 d=packed(CAL/'canonical_so10_cutoff_source_ward_operator'/(role+'_v3_tables.json.gz'));r=[]
 for out,inn,label,g,der in d['model']['roots']:
  r.append((out,inn,'M_'+out+inn+'_'+label+('_d' if der else ''),(int(label=='P'),int(label=='C'),g,0,0,0)))
 return r
def finish(role,d,t):
 d.update({'elapsed_after_imports':time.perf_counter()-t,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39','coefficient_groups_calculated':False,'complete_regulated_identity_qualified':False,'physical_scheme_adopted':False})
 raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'elapsed_after_imports':d['elapsed_after_imports'],'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
def gf_audit():
 d=packed(CAL/'canonical_so10_cutoff_source_ward_operator/primary_inputs.json.gz');g,xi=s.symbols('g10 xi');counts=Counter()
 def kind(n):
  if n.startswith('x_'):return 'X'
  if n.startswith(('bar','ub')):return 'a'
  if n.startswith('C'):return 'C'
  if n[0] in 'Lb' and n[1:].isdigit():return 'L'
  if n.startswith('B'):return 'B'
  return 'other'
 for row in d['GF']:
  w=row['word'];k=sorted(map(kind,w))
  if k not in [['C','X','a'],['L','X']]:continue
  assert not any('__' in z for z in w);co=s.sympify(row['coefficient']);powers=s.Poly(co,g,xi).monoms();expect=(2,1) if len(w)==3 else (1,1);assert powers==[expect]
  counts['GF_CaX_v' if len(w)==3 else 'GF_LX_v']+=1
 assert counts['GF_CaX_v'] and counts['GF_LX_v'];return dict(counts)
