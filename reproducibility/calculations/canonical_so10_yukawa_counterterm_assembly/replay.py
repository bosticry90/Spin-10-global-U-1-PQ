"""YCA1 component substitution into bare fields and coefficient equations."""
from data import *
start=begin('replay')
f=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/replay_tables.json.gz')
h=packed(CAL/'canonical_so10_fermion_kinetic_mass_poles/replay_v2_tables.json.gz')
gg=packed(CAL/'canonical_so10_gauge_yukawa_vertex_poles/replay_v2_tables.json.gz')
full=dec(f['full_left']);moment=s.sympify(f['loop_first_moment']);z=[[s.expand(-moment*full[16*i,16*j]) for j in range(3)] for i in range(3)]
t,c=s.symbols('formal_first_order unknown_entry');A=[[s.KroneckerDelta(i,j)+t*z[i][j]/2 for j in range(3)] for i in range(3)]
ci=dec(gg['fermion_Casimir_I_H'][0]);models=[]
for r,R in enumerate(['10','126']):
 y=[[LOC[f'u{R}_{min(i,j)}{max(i,j)}']+s.I*LOC[f'v{R}_{min(i,j)}{max(i,j)}'] for j in range(3)] for i in range(3)]
 k=s.expand(sum(s.conjugate(y[i][j])*y[i][j] for i in range(3) for j in range(3)))
 met=dec(h['scalar_metrics'][r]);unit=sum(met[i,i] for i in range(328))/sum(1 for i in range(328) if met[i,i]!=0)
 scalar_z=-k*unit*s.sympify(h['scalar_bar_derivative_pole']);ferm=s.zeros(3);sc=s.zeros(3);yp=s.zeros(3);gp=s.zeros(3)
 for i in range(3):
  for j in range(3):
   # Explicit two-leg pullback; solve its first-order bare coefficient,
   # rather than using a preassigned expression for the counterterm.
   pulled=sum(A[l][i]*y[l][m]*A[m][j] for l in range(3) for m in range(3))
   ferm[i,j]=s.diff(pulled,t).subs(t,0)
   sc[i,j]=s.diff((1+t*scalar_z/2)*y[i][j],t).subs(t,0)
   equation=s.expand(s.diff((1+t*scalar_z/2)*pulled+t*c,t).subs(t,0))
   yp[i,j]=s.solve(equation,c)[0]
   # GYV1's exact scalar image, contracted with the actual Casimir.
   gp[i,j]=-s.Rational(3,2)*G**2*(ci[0,0]+ci[0,0])*y[i][j]
 models.append({'R':R,'Y':enc(s.Matrix(y)),'trace':str(k),'fermion_field_image':enc(ferm),'scalar_field_image':enc(sc),'Yukawa_pole':enc(yp),'gauge_pole':enc(gp),'full_pole':enc(yp+gp),'scalar_metric_unit':str(unit)})
finish('replay',{'method':'explicit_family_index_bare_field_substitution_and_linear_coefficient_equations','W':enc(s.Matrix(z)/(-moment)),'Z_F_Y':enc(s.Matrix(z)),'models':models,'proper_Yukawa_vertex_UV_pole':'0','new_loop_integrals':0,'finite_scheme_or_flavor_adopted':False},start)
