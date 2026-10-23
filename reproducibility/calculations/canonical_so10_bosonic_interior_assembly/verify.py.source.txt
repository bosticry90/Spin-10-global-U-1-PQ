"""BIA1 complete family/full-sum regressions and actual hierarchy outcomes."""
from data import *
start=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();mp.mp.dps=100
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz');maximum=mp.mpf(0);comparisons=0;regressions=0
def compare(a,b,reg=False):
 global maximum,comparisons,regressions
 aa,bb=q(a),q(b);er=abs(aa-bb)/(1+abs(aa));maximum=max(maximum,er);assert er<mp.mpf('1e-28'),(a,b,str(er))
 if reg:regressions+=1
 else:comparisons+=1
assert set(A['cases'])==set(B['cases'])=={'1/2','3/4','1'}
for d in [A,B]:assert d['HTB_multiplicity']==1 and not d['extra_FCI_or_parent_finite'] and not d['physical_C1_or_refit']
for key in A['cases']:
 a,b=A['cases'][key],B['cases'][key]
 assert set(a['families'])==set(b['families'])==set(FAMILIES)
 for name in FAMILIES:
  for ra,rb in zip(a['families'][name],b['families'][name]):
   assert len(ra)==len(rb)==3
   for v,z in zip(ra,rb):compare(v,z)
 for name in ['bridge','lambda2_L_polynomial']:
  for ra,rb in zip(a[name],b[name]):
   for v,z in zip(ra,rb):compare(v,z)
 for v,z in zip(a['direct_L2over7'],b['direct_L2over7']):compare(v,z)
 for i,(ka,kb) in enumerate(zip(a['kinetic'],b['kinetic'])):
  for name in ['lambda1','k1','k2','two_vs_tree','two_vs_one']:compare(ka[name],kb[name])
  assert ka['necessary_hierarchy']==kb['necessary_hierarchy']==(abs(q(ka['k2']))<1 and abs(q(ka['k2']))<abs(q(ka['k1'])))
  row=a['lambda2_L_polynomial'][i];assert q(row[2])==0
  compare(a['direct_L2over7'][i],q(row[0])+q('2/7')*q(row[1]))
 for name,values in a['controls'].items():
  if name=='second_bridge' or key!='1':assert all(abs(q(v))>mp.mpf('1e-20') for v in values)
  else:assert all(q(v)==0 for v in values)
gp=packed(CAL/'canonical_so10_nine_family_uv_assembly/primary_tables.json.gz');fan=packed(CAL/'canonical_so10_finite_assembly_nielsen/primary_tables.json.gz')
blh=packed(CAL/'canonical_so10_bosonic_loop_hierarchy/primary_tables.json.gz')
for key in ['1/2','1']:
 a=A['cases'][key]
 for name in FAMILIES:
  for ra,rb in zip(a['families'][name],gp['finite_cases'][key]['family_L_polynomials'][name]):
   for v,z in zip(ra,rb):compare(v,z,True)
 for ra,rb in zip(a['lambda2_L_polynomial'],fan['finite_lambda2_fixed_xi'][key]):
  for v,z in zip(ra,rb):compare(v,z,True)
 for i,ka in enumerate(a['kinetic']):
  old=next(row for row in blh['rows'] if row['x']==key and row['gauge']==['U1','SU2','SU3'][i])
  for name in ['lambda1','k1','k2','two_vs_tree','two_vs_one']:compare(ka[name],old[name],True)
  assert ka['necessary_hierarchy']==old['necessary_hierarchy']
new=A['cases']['3/4'];outcomes=[row['necessary_hierarchy'] for row in new['kinetic']]
print('RESULT '+json.dumps({'status':'QUALIFIED_BOSONIC_INTERIOR_ASSEMBLY_AND_HIERARCHY_DIAGNOSTIC','elapsed_after_imports':time.perf_counter()-start,'new_coupling':'3/4','primitive_families':9,'heavy_bridge_multiplicity':1,'route_and_direct_comparisons':comparisons,'endpoint_regressions':regressions,'maximum_scaled_error':mp.nstr(maximum,35),'interior_hierarchy_passes':sum(outcomes),'interior_hierarchy_failures':3-sum(outcomes),'quadratic_L_coefficient_zero':True,'full_matter_physical_C1_or_refit':False,'uniform_all_x_numeric_error_bound':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39'},sort_keys=True),flush=True)
