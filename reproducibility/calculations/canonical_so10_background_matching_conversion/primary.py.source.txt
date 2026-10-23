"""BMC1 non-Abelian kinetic normalization and direct g_i RG differentiation."""
from io_data import *
start=begin();guard('primary')
K=1-ell*g*g*lam1/3-ell**2*g*g*lam2/3
z=s.series(1/K,ell,0,3).removeO().expand();gi=s.series(g/s.sqrt(K),ell,0,3).removeO().expand()
q,comm=s.symbols('q comm',real=True);scale=s.Symbol('scale',positive=True)
assert s.expand((scale*q+g/scale*scale**2*comm)**2-scale**2*(q+g*comm)**2)==0
wrong=s.expand((scale*q+g*scale**2*comm)**2-scale**2*(q+g*comm)**2)
assert wrong.coeff(q*comm)!=0
# All coefficients remain symbolic; no physical finite amplitude substituted.
converted=s.expand(z.subs(ell,a/(4*g*g)))
z1=converted.coeff(a,1);z2=converted.coeff(a,2)
inverse=s.series(1/(alpha*converted),a,0,3).removeO().expand()
assert s.simplify(inverse.coeff(a,2)+lam2/(48*alpha*g*g))==0
L1,L2=s.symbols('L1 L2')
beta=s.diff(gi,g)*(ell*b*g**3+ell**2*c*g**5)+s.diff(gi,lam1)*(L1+ell*W)+s.diff(gi,lam2)*L2
rhs=ell*bi*gi**3+ell**2*ri*gi**5
res=s.series(beta-rhs,ell,0,3).removeO().expand()
v1=s.solve(res.coeff(ell,1),L1)[0];v2=s.solve(res.coeff(ell,2).subs(L1,v1),L2)[0]
assert s.simplify(v1-6*(bi-b))==0 and s.simplify(v2-6*g*g*(ri-c)+W)==0
lam1tau=6*(bi-b)*tau-12*p0;lam2tau=s.Symbol('lambda20')+(6*g*g*(ri-c)-W)*tau
poly=s.expand(z2.subs({lam1:lam1tau,lam2:lam2tau}))
gs=packed(CAL/'canonical_so10_two_loop_gauge_beta/primary_tables.json.gz')
mst=read(CAL/'canonical_so10_threshold_scheme_transport/primary_result.json')
sb=list(map(s.Rational,mst['scalar_beta']));tv=[sum(s.Rational(row[i]) for row in mst['vector_indices']) for i in range(3)]
bp=s.Rational(gs['parent_b_one']);cp=s.Rational(gs['parent_c_two']);lb=list(map(s.Rational,gs['light_b_one']));lc=list(map(s.Rational,gs['light_c_two_equal_g_row_sum']))
db=[x-bp for x in lb];dc=[x-cp for x in lc];jump=[-6*x+21*y for x,y in zip(sb,tv)]
assert jump==[6*x for x in db]
gpiece=[s.expand(bp*g**3*s.diff(-s.Rational(21,2)*v*s.log(g*g),g)) for v in tv]
old=read(HERE/'old_RG_input_projection.json')['operands'];fullc=s.Rational(old['parent_B_two_loop_yukawa_independent']);fullr=list(map(s.Rational,old['SM_B_row_sums_at_unified_coupling']))
fulldc=[x-fullc for x in fullr];fulldb=[s.Rational(x['delta_b']) for x in old['rg_log_kernel']]
assert db==fulldb and all(x!=y for x,y in zip(dc,fulldc))
save('primary',{'method':'nonabelian_rescaling_and_direct_g_RG','K':str(K),'g_i':str(gi),'zeta_a_coefficient':str(z1),'zeta_a2_coefficient':str(z2),
    'inverse_alpha_a2_coefficient':str(inverse.coeff(a,2)),'C0':str(-z1),'C1_formula_only':str(z2),
    'lambda1_tau_derivative':str(v1),'lambda2_tau_derivative':str(v2),'zeta_tau2':str(s.factor(poly.coeff(tau,2))),
    'zeta_tau1':str(s.factor(poly.coeff(tau,1))),'scalar_heavy_b':list(map(str,sb)),'vector_T':list(map(str,tv)),
    'one_loop_jump_mu':list(map(str,jump)),'GS_db':list(map(str,db)),'GS_dc':list(map(str,dc)),
    'old_full_dc':list(map(str,fulldc)),'full_minus_GS_dc':list(map(str,[x-y for x,y in zip(fulldc,dc)])),
    'explicit_g_component_W':list(map(str,gpiece)),'full_W_calculated':False,
    'light_c_matrix':gs['light_c_two_matrix'],'nonabelian_unrescaled_g_control':True,
    'numerical_C1_calculated':False,'physical_demand_parsed':False,'complete_finite_inventory_proved':False},start)
