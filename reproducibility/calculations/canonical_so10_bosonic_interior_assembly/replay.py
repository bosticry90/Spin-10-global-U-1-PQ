"""BIA1 replay inputs, pointwise polynomial extraction and grouped sums."""
from data import *
start=begin('replay');mp.mp.dps=110
A=packed(CAL/'canonical_so10_analytic_coupling_map/replay_tables.json.gz')
S4=packed(CAL/'canonical_so10_scalar_quartic_coupling_map/replay_tables.json.gz')
S3=packed(CAL/'canonical_so10_scalar_cubic_coupling_map/replay_amplitude_tables.json.gz')
MS=packed(CAL/'canonical_so10_mixed_scalar_coupling_map/replay_amplitude_tables.json.gz')
VS=packed(CAL/'canonical_so10_vss_coupling_map/replay_amplitude_v2_tables.json.gz')
O=packed(CAL/'canonical_so10_finite_threshold_controls/replay_tables.json.gz');cases={}
sectors=[['SSSS','SSS'],['VVSS','VSS','VVS','ghostS'],['VVVV','VVV','ghostV']]
for key in ['1/2','3/4','1']:
 x=q(key);av=A['cases'][key]
 def value(ll):
  out={n:[mp.fsum(q(v)*ll**k for k,v in enumerate(row)) for row in av['family_L_polynomials'][n]] for n in ['VVVV','VVV','ghostV','VVSS']}
  for name,data in [('SSSS',S4['cases'][key]),('SSS',S3['cases'][key])]:out[name]=[q(a)+ll*q(b) for a,b in zip(data['finite_L0'],data['scale_linear'])]
  for name in ['VVS','ghostS']:
   row=MS['cases'][name][key];out[name]=[x*(q(a)+ll*q(b)) for a,b in zip(row['finite_L0'],row['L_coefficient'])]
  out['VSS']=[x*(q(row[1])+ll*q(row[2])) for row in VS['cases'][key]['coefficients']]
  return out
 vals={ll:value(q(ll)) for ll in ['-1','0','1']};fam={n:[[vals['0'][n][i],(vals['1'][n][i]-vals['-1'][n][i])/2,(vals['1'][n][i]+vals['-1'][n][i])/2-vals['0'][n][i]] for i in range(3)] for n in FAMILIES}
 bridge=[list(map(q,r)) for r in av['bridge_L_polynomial']]
 total=[[mp.fsum(mp.fsum(fam[n][i][k] for n in group) for group in sectors)+bridge[i][k] for k in range(3)] for i in range(3)]
 for row in total:assert abs(row[2])<mp.mpf('1e-35')*(1+abs(row[0]));row[2]=mp.mpf(0)
 direct={n:list(map(q,av['direct_at_L_2_over7'][n])) for n in ['VVVV','VVV','ghostV','VVSS']}
 direct.update({'SSSS':list(map(q,S4['cases'][key]['direct_L_2_over7'])),'SSS':list(map(q,S3['cases'][key]['direct_L_2_over7']))})
 for n in ['VVS','ghostS']:direct[n]=[x*q(v) for v in MS['cases'][n][key]['direct_L2over7']]
 direct['VSS']=[x*q(v) for v in VS['cases'][key]['direct_L2over7']]
 full_direct=[mp.fsum(mp.fsum(direct[n][i] for n in group) for group in sectors)+bridge[i][0]+q('2/7')*bridge[i][1] for i in range(3)]
 kin=[];tree=4*mp.pi/x
 for i,row in enumerate(total):
  l1=q(O['lambda1'][key][0][i]);d1=-l1/(12*mp.pi);d2=-row[0]/(192*mp.pi**3);k1=d1/tree;k2=d2/tree
  kin.append({'lambda1':fmt(l1),'k1':fmt(k1),'k2':fmt(k2),'two_vs_tree':fmt(abs(d2/tree)),'two_vs_one':fmt(abs(d2/d1)),'necessary_hierarchy':abs(d2)<tree and abs(d2)<abs(d1)})
 cases[key]={'families':{n:[list(map(fmt,r)) for r in fam[n]] for n in FAMILIES},'bridge':[list(map(fmt,r)) for r in bridge],
  'lambda2_L_polynomial':[list(map(fmt,r)) for r in total],'direct_L2over7':list(map(fmt,full_direct)),'kinetic':kin}
finish('replay',{'schema':'BIA1','cases':cases,'new_x':'3/4','HTB_multiplicity':1,'extra_FCI_or_parent_finite':False,'physical_C1_or_refit':False,'scientific_acceptance':'NOT_PERFORMED'},start)
