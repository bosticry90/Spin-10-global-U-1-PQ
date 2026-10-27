from pathlib import Path
from hashlib import sha256
import json,gzip,time,threading,os,math
O=Path(__file__).resolve().parent;H=lambda p:sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_bytes());load=lambda p:json.loads(gzip.decompress(p.read_bytes()));tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
for p,h in read(O/'validation_preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
a,b=[load(O/(r+'_tables.json.gz')) for r in ['primary','replay']]
assert {k:v for k,v in a.items() if k!='role'}=={k:v for k,v in b.items() if k!='role'}
rows=[];fixed={1:0,2:0,3:0}
for z in a['outputs']:
 rr={}
 for prime,r in z['prime_logs'].items():
  rr[prime]={n:len(r[n]['entries']) for n in ['U','dV','H','F','dH','dF']}
  assert not r['second_variation_residual']['entries'] and not r['dF']['entries']
  for name,degree in [('H',1),('F',2),('dF',3)]:
   M=r[name];assert M['shape']==[328,math.comb(45,degree)] and M['ghost_degree']==degree
   assert len({(i,tuple(ww)) for i,ww,v in M['entries']})==len(M['entries']) and all(0<=i<328 and len(ww)==degree and ww==sorted(set(ww)) and all(0<=c<45 for c in ww) and v!='0' for i,ww,v in M['entries']);fixed[degree]+=328*math.comb(45,degree)
  rr[prime]['wrong_source_orientation_changed_positions']=r['wrong_source_orientation_changed_positions'];rr[prime]['omit_U_H_changed_positions']=r['omit_U_H_changed_positions'];rr[prime]['omit_U_F_changed_positions']=r['omit_U_F_changed_positions']
 rows.append({'probe':z['probe'],'prime_logs':rr})
out={'schema':'IFC1_SOURCE_DESCENT_VALIDATION','elapsed_after_imports':time.perf_counter()-tick,'component_cochain_and_odd_Leibniz_routes_agree':True,'fixed_H_F_dF_positions_including_zero_complements':fixed,'type_envelope':a['type_envelope'],'Lorentz_scalar_source_types':a['Lorentz_scalar_source_types'],'results':rows,'new_source_quantum_roots_independently_measured':False,'full_normalization_QAP_E5_A5_authority':False};print('RESULT '+json.dumps(out,sort_keys=True),flush=True);timer.cancel()
