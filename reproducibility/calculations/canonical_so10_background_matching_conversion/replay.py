"""BMC1 bare Ward factors and independently solved inverse-coupling RG."""
from io_data import *
start=begin();guard('replay')
Zg,Zgi,zA0=s.symbols('Zg Zgi zA0',nonzero=True)
K=(Zg**-2/Zgi**-2)*zA0;zg2=(Zg/Zgi)**2/zA0
assert s.cancel(K*zg2-1)==0
assert s.cancel((Zgi/Zg)**2/zA0*K-1)!=0
# Independent recurrence solve for inverse of the renormalized kinetic series.
k1=-g*g*lam1/3;k2=-g*g*lam2/3;x1,x2=s.symbols('x1 x2')
prod=s.expand((1+ell*k1+ell**2*k2)*(1+ell*x1+ell**2*x2))
sol=s.solve([prod.coeff(ell,1),prod.coeff(ell,2)],[x1,x2]);za=1+ell*sol[x1]+ell**2*sol[x2]
c1=s.expand(sol[x1]/(4*g*g));c2=s.expand(sol[x2]/(16*g**4))
# Inverse coupling equation is additive, no geometric-square term.
kinetic_inverse=1/g**2-ell*lam1/3-ell**2*lam2/3
L1,L2=s.symbols('L1 L2')
left=-2*ell*b-2*ell**2*c*g*g-ell*(L1+ell*W)/3-ell**2*L2/3
right=-2*ell*bi-2*ell**2*ri*g*g
eq=s.expand(left-right);flow=s.solve([eq.coeff(ell,1),eq.coeff(ell,2)],[L1,L2])
l1=6*(bi-b)*tau-12*p0;l2=s.Symbol('lambda20')+flow[L2]*tau
poly=s.expand(c2.subs({lam1:l1,lam2:l2}))
gs=packed(CAL/'canonical_so10_two_loop_gauge_beta/replay_tables.json.gz')
mst=read(CAL/'canonical_so10_threshold_scheme_transport/replay_result.json')
sb=list(map(s.Rational,mst['scalar_beta']));tv=[sum(map(s.Rational,[row[i] for row in mst['vector_indices']])) for i in range(3)]
bp=s.Rational(gs['parent_b_one']);cp=s.Rational(gs['parent_c_two']);lb=list(map(s.Rational,gs['light_b_one']))
lc=[sum(s.Rational(z) for z in row) for row in gs['light_c_two_matrix']]
db=[x-bp for x in lb];dc=[x-cp for x in lc];jump=[2*(s.Rational(21,2)*v-3*t) for v,t in zip(tv,sb)]
assert jump==[6*x for x in db]
# Differentiate log of actual g^2 vector mass as log(g^2 m)-log(g^2 m0).
v_g=[s.expand(-s.Rational(21,2)*T*(2*bp*g*g)) for T in tv]
old=read(HERE/'old_RG_input_projection.json')['operands'];fullc=s.Rational(old['parent_B_two_loop_yukawa_independent'])
fullr=list(map(s.Rational,old['SM_B_row_sums_at_unified_coupling']));fulldc=[x-fullc for x in fullr]
save('replay',{'method':'bare_Ward_and_inverse_kinetic_recurrence_inverse_RG',
    'K':str(1+ell*k1+ell**2*k2),'g_i':str(s.series(g*s.sqrt(za),ell,0,3).removeO().expand()),
    'zeta_a_coefficient':str(c1),'zeta_a2_coefficient':str(c2),
    'inverse_alpha_a2_coefficient':str(s.expand((c1*c1-c2)/alpha)),
    'C0':str(-c1),'C1_formula_only':str(c2),
    'lambda1_tau_derivative':str(flow[L1]),'lambda2_tau_derivative':str(flow[L2]),
    'zeta_tau2':str(s.factor(poly.coeff(tau,2))),'zeta_tau1':str(s.factor(poly.coeff(tau,1))),
    'scalar_heavy_b':list(map(str,sb)),'vector_T':list(map(str,tv)),
    'one_loop_jump_mu':list(map(str,jump)),'GS_db':list(map(str,db)),'GS_dc':list(map(str,dc)),
    'old_full_dc':list(map(str,fulldc)),'full_minus_GS_dc':list(map(str,[x-y for x,y in zip(fulldc,dc)])),
    'explicit_g_component_W':list(map(str,v_g)),'full_W_calculated':False,'light_c_matrix':gs['light_c_two_matrix'],
    'bare_Ward_wrong_ratio_detected':True,'numerical_C1_calculated':False,'physical_demand_parsed':False,
    'complete_finite_inventory_proved':False},start)
