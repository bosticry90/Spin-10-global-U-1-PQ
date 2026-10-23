"""HPR1 original traces/poles, inverse bare RG and centered finite directions."""
from data import *
start=begin();guard('replay')
gc=packed(CAL/'canonical_so10_ghost_counterterm_trace_closure/replay_tables.json.gz')['traces']
fc=packed(CAL/'canonical_so10_finite_counterterm_insertion/replay_v3_tables.json.gz')
sectors=[]
for ir in range(4):
    mass=ex(fc['vector_mass_eigenvalues'][ir]);jr=L-lg-s.log(mass/60);rows=[]
    for S,C in zip(gc['Goldstone_scalar_half_charge_traces'][ir],gc['ghost_charge_traces'][ir]):
        # First three coefficients of exp(gamma eps)Gamma(1+eps) exp(j eps).
        factors=[s.Integer(1),jr,(jr*jr+s.pi**2/6)/2]
        a=[clean(-ex(S)*z/mass) for z in factors];b0=[clean(ex(C)*z/mass) for z in factors]
        rows.append({'scalar':strs(a),'ghost':strs(b0),'sum':strs([clean(v+w) for v,w in zip(a,b0)])})
    sectors.append({'mass_set':ir+1,'mass_over_g2':str(mass),'charge_components':rows})
u,b,c,a1,a22,a21=s.symbols('u b c a1 a22 a21',real=True)
Z=1+a1*u/e+a22*u*u/e**2+a21*u*u/e
# d[mu^-2eps Z/g^2]/dlogmu=0, beta/g=-eps+b*u+c*u^2.
eq=s.expand(-2*e*Z+(-2*Z+2*u*s.diff(Z,u))*(-e+b*u+c*u*u))
solution=s.solve([eq.coeff(u,1),s.expand(e*eq.coeff(u,2)).coeff(e,0),s.expand(e*eq.coeff(u,2)).coeff(e,1)],[a1,a22,a21],dict=True)
assert len(solution)==1
ZA2=clean((a22/e**2+a21/e).subs(solution[0]))
rg=packed(CAL/'canonical_so10_two_loop_gauge_beta/replay_tables.json.gz')
cp=ex(rg['parent_c_two']);cl=list(map(ex,rg['light_c_two_equal_g_row_sum']))
ct=[clean(s.Rational(3,2)*(cp-v)) for v in cl]
measured=packed(CAL/'canonical_so10_nine_family_uv_assembly/replay_tables.json.gz')['pole_assembly']
ht=json.loads((CAL/'canonical_so10_higgs_stationary_tangent/replay_result.json').read_bytes());mp.mp.dps=70
A=[[mp.mpf(str(ht['scalar_response_refined'][i][k]))+mp.mpf(str(ht['vector_threshold_response'][i][k])) for k in range(3)] for i in range(3)]
mean=[sum(A[i][k] for i in range(3))/3 for k in range(3)]
C=[[A[i][k]-mean[k] for k in range(3)] for i in range(3)]
grams={}
for i,k in [(0,1),(0,2),(1,2)]:
    xx=sum(row[i]**2 for row in C);yy=sum(row[k]**2 for row in C);xy=sum(row[i]*row[k] for row in C)
    grams[str(i)+str(k)]=xx*yy-xy*xy
save('replay',{'schema':'HPR1_REPLAY','peer_or_physical_target_read':False,'sectors':sectors,
 'vector_pole_finite_positive_eps':strs([-21*rho/2,-rho*(1+21*j/2),-rho*(j+21*(j*j+s.pi**2/6)/4)]),
 'ZA_two':str(ZA2),'overall_UV_minus_EFT_pole_CT':strs(ct),'measured_heavy_pole':measured['heavy_sum'],
 'measured_EFT_pole':measured['EFT_sum'],'measured_parent_pole':measured['parent_sum'],
 'one_loop_tangent_response_refined':[[fmt(v) for v in row] for row in A],
 'centered_Gram_determinants':{k:fmt(v) for k,v in grams.items()},
 'finite_transport_sign':-1,'finite_conditions_or_C1_E5_A5_qualified':False},start)
