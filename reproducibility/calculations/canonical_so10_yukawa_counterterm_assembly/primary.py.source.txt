"""YCA1 measured matrix wavefunctions and bilinear pullback."""
from data import *
start=begin('primary')
f=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/primary_tables.json.gz')
h=packed(CAL/'canonical_so10_fermion_kinetic_mass_poles/primary_tables.json.gz')
g=read(CAL/'canonical_so10_gauge_yukawa_vertex_poles/validation_receipt_v2.json')
Y=[s.Matrix(3,3,lambda i,j:LOC[f'u{R}_{min(i,j)}{max(i,j)}']+s.I*LOC[f'v{R}_{min(i,j)}{max(i,j)}']) for R in ['10','126']]
family=list(map(dec,f['family_left']));internal=list(map(dec,f['internal_left']))
W=sum((s.trace(c)*a/16 for a,c in zip(family,internal)),s.zeros(3));Z=-W*s.sympify(f['loop_first_moment'])
assert f['inverse_propagator_loop_sign']=='+i'
models=[]
for r,y in enumerate(Y):
 k=s.expand(s.trace(y.H*y));metric=dec(h['scalar_metrics'][r]);support=list(range(306,326)) if r==0 else list(range(54,306))
 scalar_unit=metric[support[0],support[0]]*s.sympify(h['scalar_bar_derivative_pole'])
 zs=-k*scalar_unit
 fermion_image=(Z.T*y+y*Z)/2;scalar_image=zs*y/2
 # The proper pure-Yukawa vertex is the independently qualified YPP1 zero.
 p=read(CAL/'canonical_so10_yukawa_polarization_poles/validation_receipt_v2.json');assert p['pure_Yukawa_cubic_vertex_UV_pole']=='0'
 yp=-fermion_image-scalar_image
 gp=G**2*s.sympify(g['parameter_counterterms'][r]['parameter_pole_coefficient'])*y
 models.append({'R':['10','126'][r],'Y':enc(y),'trace':str(k),'fermion_field_image':enc(fermion_image),'scalar_field_image':enc(scalar_image),'Yukawa_pole':enc(yp),'gauge_pole':enc(gp),'full_pole':enc(yp+gp),'scalar_metric_unit':str(scalar_unit)})
finish('primary',{'method':'measured_matrix_wavefunctions_and_bare_bilinear_congruence','W':enc(W),'Z_F_Y':enc(Z),'models':models,'proper_Yukawa_vertex_UV_pole':'0','new_loop_integrals':0,'finite_scheme_or_flavor_adopted':False},start)
