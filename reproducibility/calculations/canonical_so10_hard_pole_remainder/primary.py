"""HPR1 positive-sector pole lifts, group-trace CTs and actual tangent minors."""
from data import *
start=begin();guard('primary')
gc=packed(CAL/'canonical_so10_ghost_counterterm_trace_closure/primary_tables.json.gz')['traces']
fc=packed(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_tables.json.gz')
H=1+e*j+e**2*(j*j+s.zeta(2))/2
def jet(v):
    reg=s.expand(e*v)
    return [clean(s.diff(reg,e,k).subs(e,0)/s.factorial(k)) for k in range(3)]
sectors=[]
for ir,(mass,S,C) in enumerate(zip(fc['vector_mass_eigenvalues'],gc['Goldstone_scalar_half_charge_traces'],gc['ghost_charge_traces']),1):
    jr=L-lg-s.log(ex(mass)/60);row=[]
    for sv,cv in zip(S,C):
        a=jet(-ex(sv)*H/(e*ex(mass)));b=jet(ex(cv)*H/(e*ex(mass)))
        row.append({'scalar':strs([v.subs(j,jr) for v in a]),'ghost':strs([v.subs(j,jr) for v in b]),'sum':strs([clean(x+y) for x,y in zip(a,b)])})
    sectors.append({'mass_set':ir,'mass_over_g2':mass,'charge_components':row})
D=s.Symbol('D',real=True)
heat_vector=12-D/2;heat_gold=-s.Rational(1,2);heat_ghost=s.Integer(1)
heat_total=clean((heat_vector+heat_gold+heat_ghost).subs(D,4-2*e))
vector_jet=jet(-rho*heat_total*H/e)
# Actual MS pole projection takes the UV angular residue at epsilon zero.
open_angular=1-2/(4-2*e);open_pole=clean(open_angular.subs(e,0))
open_forbidden_finite_lift=clean(s.diff(open_angular,e).subs(e,0))

rg=packed(CAL/'canonical_so10_two_loop_gauge_beta/primary_tables.json.gz')
CA,T,TC=map(s.sympify,[rg['parent_CA'],rg['parent_real_scalar_index'],rg['parent_Casimir_weighted_index']])
bp=-s.Rational(11,3)*CA+T/6;cp=-s.Rational(34,3)*CA**2+CA*T/3+2*TC
ca=list(map(s.sympify,rg['light_CA']));ti=list(map(s.sympify,rg['light_real_scalar_index']))
cross=s.Matrix([[s.sympify(v) for v in row] for row in rg['light_Casimir_cross_trace']])
cl=2*cross+s.diag(*[ca[i]*ti[i]/3-s.Rational(34,3)*ca[i]**2 for i in range(3)])
cr=[sum(cl[i,k] for k in range(3)) for i in range(3)]
ct=[clean(s.Rational(3,2)*(cp-c)) for c in cr]
u,b,c=s.symbols('u b c',real=True)
Zg=1+b*u/(2*e)+(3*b*b/(8*e*e)+c/(4*e))*u*u
ZA=s.series(Zg**(-2),u,0,3).removeO().expand()

ht=json.loads((CAL/'canonical_so10_higgs_stationary_tangent/primary_result.json').read_bytes());mp.mp.dps=70
A=[[mp.mpf(str(v)) for v in row] for row in ht['combined_one_loop_mass_response']]
diff=[[A[0][k]-A[i][k] for k in range(3)] for i in [1,2]]
minors={str(i)+str(k):diff[0][i]*diff[1][k]-diff[0][k]*diff[1][i] for i,k in [(0,1),(0,2),(1,2)]}
save('primary',{'schema':'HPR1_PRIMARY','peer_or_physical_target_read':False,'sectors':sectors,
 'heat_gauge_multiplet':str(heat_total),'vector_pole_finite_positive_eps':strs(vector_jet),
 'open_ghost_angular_pole':str(open_pole),'wrong_unprojected_angular_finite_lift':str(open_forbidden_finite_lift),
 'parent_b':str(bp),'parent_c':str(cp),'light_c_matrix':[[str(v) for v in cl.row(i)] for i in range(3)],
 'light_c_rows':strs(cr),'overall_UV_minus_EFT_pole_CT':strs(ct),'ZA_two':str(clean(ZA.coeff(u,2))),
 'stationary_Higgs_tangent_flags':{k:ht[k] for k in ['heavy_real','zero_real','Higgs_preserved_to_first_order_only','physical_reference_units_fixed','finite_reparameterization_or_counterterm_chosen']},
 'one_loop_tangent_response':[[fmt(v) for v in row] for row in A],'difference_response':[[fmt(v) for v in row] for row in diff],
 'difference_minors':{k:fmt(v) for k,v in minors.items()},'mphi2_tangent_over_reference_omega2':ht['mphi2_tangent_over_reference_omega2'],
 'finite_transport_sign':-1,'finite_conditions_or_C1_E5_A5_qualified':False},start)
