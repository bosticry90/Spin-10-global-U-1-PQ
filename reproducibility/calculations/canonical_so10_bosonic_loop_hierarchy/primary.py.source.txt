"""BLH1 direct canonical-kinetic orders; no inversion/resummation."""
from data import *
start=begin('primary');mp.mp.dps=95
fct=packed(CAL/'canonical_so10_finite_threshold_controls/primary_tables.json.gz')
fan=packed(CAL/'canonical_so10_finite_assembly_nielsen/primary_tables.json.gz')
ell=1/(16*mp.pi**2);rows=[]
for key in ['1/2','1']:
 x=q(key)
 for i in range(3):
  a=q(fct['lambda1'][key][0][i]);b=q(fan['finite_lambda2_fixed_xi'][key][i][0]);k1=-ell*x*a/3;k2=-ell**2*x*b/3;tree=4*mp.pi/x
  assert k1!=0
  rows.append({'x':key,'gauge':['U1','SU2','SU3'][i],'lambda1':fmt(a),'lambda2':fmt(b),'k1':fmt(k1),'k2':fmt(k2),'K_truncated':fmt(1+k1+k2),'inverse_alpha_tree':fmt(tree),'inverse_alpha_shift1':fmt(tree*k1),'inverse_alpha_shift2':fmt(tree*k2),'two_vs_tree':fmt(abs(k2)),'two_vs_one':fmt(abs(k2/k1)),'necessary_hierarchy':abs(k2)<1 and abs(k2)<abs(k1),'missing_external_x_control':fmt(k2/x-k2),'missing_loop_factor_control':fmt(k2/ell-k2)})
finish('primary',{'schema':'BLH1','rows':rows,'L':'0','scope':'FIXED_REFERENCE_BOSONIC_SUBSET_ONLY','physical_refit_or_full_C1':False,'scientific_acceptance':'NOT_PERFORMED'},start)
