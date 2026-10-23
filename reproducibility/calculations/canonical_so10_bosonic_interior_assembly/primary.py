"""BIA1 coefficient maps, explicit family factors, direct full sum."""
from data import *
start=begin('primary');mp.mp.dps=100
A=packed(CAL/'canonical_so10_analytic_coupling_map/primary_tables.json.gz')
S4=packed(CAL/'canonical_so10_scalar_quartic_coupling_map/primary_tables.json.gz')
S3=packed(CAL/'canonical_so10_scalar_cubic_coupling_map/primary_amplitude_tables.json.gz')
MS=packed(CAL/'canonical_so10_mixed_scalar_coupling_map/primary_amplitude_tables.json.gz')
VS=packed(CAL/'canonical_so10_vss_coupling_map/primary_amplitude_v2_tables.json.gz')
O=packed(CAL/'canonical_so10_finite_threshold_controls/primary_tables.json.gz');cases={}
for key in ['1/2','3/4','1']:
 x=q(key);u=mp.log(x);av=A['cases'][key];families={n:[list(map(q,r)) for r in av['family_L_polynomials'][n]] for n in ['VVVV','VVV','ghostV','VVSS']}
 direct={n:list(map(q,av['direct_at_L_2_over7'][n])) for n in families}
 c=S4['coefficients'];ff=[1/x,1,x,u,x*u];ss=[1/x,1,x]
 families['SSSS']=[[mp.fsum(q(a)*b for a,b in zip(c['finite'][i],ff)),mp.fsum(q(a)*b for a,b in zip(c['slope'][i],ss)),mp.mpf(0)] for i in range(3)]
 direct['SSSS']=list(map(q,S4['cases'][key]['direct_L_2_over7']))
 row=S3['cases'][key];families['SSS']=[[q(row['finite_L0'][i]),q(row['scale_linear'][i]),mp.mpf(0)] for i in range(3)];direct['SSS']=list(map(q,row['direct_L_2_over7']))
 for name in ['VVS','ghostS']:
  row=MS['cases'][name][key];families[name]=[[x*q(row['finite_L0'][i]),x*q(row['L_coefficient'][i]),mp.mpf(0)] for i in range(3)];direct[name]=[x*q(v) for v in row['direct_L2over7']]
 row=VS['cases'][key];families['VSS']=[[x*q(v[1]),x*q(v[2]),mp.mpf(0)] for v in row['coefficients']];direct['VSS']=[x*q(v) for v in row['direct_L2over7']]
 bridge=[list(map(q,r)) for r in av['bridge_L_polynomial']]
 assert set(families)==set(FAMILIES)
 total=[[mp.fsum(families[n][i][k] for n in FAMILIES)+bridge[i][k] for k in range(3)] for i in range(3)]
 assert all(r[2]==0 for r in total)
 full_direct=[mp.fsum(direct[n][i] for n in FAMILIES)+bridge[i][0]+mp.mpf(2)/7*bridge[i][1] for i in range(3)]
 kin=[]
 for i,row in enumerate(total):
  l1=q(O['lambda1'][key][0][i]);k1=-x*l1/(48*mp.pi**2);k2=-x*row[0]/(768*mp.pi**4)
  kin.append({'lambda1':fmt(l1),'k1':fmt(k1),'k2':fmt(k2),'two_vs_tree':fmt(abs(k2)),'two_vs_one':fmt(abs(k2/k1)),'necessary_hierarchy':abs(k2)<1 and abs(k2)<abs(k1)})
 controls={'extra_SSSS_x':[fmt((x-1)*r[0]) for r in families['SSSS']],'missing_VSS_x':[fmt((1/x-1)*r[0]) for r in families['VSS']],'second_bridge':[fmt(r[0]) for r in bridge]}
 cases[key]={'families':{n:[list(map(fmt,r)) for r in families[n]] for n in FAMILIES},'bridge':[list(map(fmt,r)) for r in bridge],
  'lambda2_L_polynomial':[list(map(fmt,r)) for r in total],'direct_L2over7':list(map(fmt,full_direct)),'kinetic':kin,'controls':controls}
finish('primary',{'schema':'BIA1','cases':cases,'new_x':'3/4','HTB_multiplicity':1,'extra_FCI_or_parent_finite':False,'physical_C1_or_refit':False,'scientific_acceptance':'NOT_PERFORMED'},start)
