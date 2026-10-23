"""BLH1 independent inverse-alpha subtraction then normalization to tree."""
from data import *
start=begin('replay');mp.mp.dps=105
fct=packed(CAL/'canonical_so10_finite_threshold_controls/replay_tables.json.gz')
fan=packed(CAL/'canonical_so10_finite_assembly_nielsen/replay_v2_tables.json.gz');rows=[]
for key in ['1/2','1']:
 x=q(key);tree=4*mp.pi/x
 for i in range(3):
  a=q(fct['lambda1'][key][0][i]);b=q(fan['finite_lambda2_fixed_xi'][key][i][0]);d1=-a/(12*mp.pi);d2=-b/(192*mp.pi**3);k1=d1/tree;k2=d2/tree
  rows.append({'x':key,'gauge':['U1','SU2','SU3'][i],'lambda1':fmt(a),'lambda2':fmt(b),'k1':fmt(k1),'k2':fmt(k2),'K_truncated':fmt((tree+d1+d2)/tree),'inverse_alpha_tree':fmt(tree),'inverse_alpha_shift1':fmt(d1),'inverse_alpha_shift2':fmt(d2),'two_vs_tree':fmt(abs(d2/tree)),'two_vs_one':fmt(abs(d2/d1)),'necessary_hierarchy':abs(d2)<tree and abs(d2)<abs(d1)})
finish('replay',{'schema':'BLH1','rows':rows,'L':'0','scope':'FIXED_REFERENCE_BOSONIC_SUBSET_ONLY','physical_refit_or_full_C1':False,'scientific_acceptance':'NOT_PERFORMED'},start)
