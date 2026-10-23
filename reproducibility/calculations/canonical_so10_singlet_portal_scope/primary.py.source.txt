"""SPS1 symbolic specialization of the authenticated complete pole formula."""
from data import *
import sympy as s
start=begin('primary')
table=json.loads(gzip.decompress((CAL/'canonical_so10_scalar_kernel_reconciliation/primary_tables.json.gz').read_bytes()))
names=read(ROOT/'tools/two_loop_qft_compiler_v1/uvp_m05_complete_scalar_v4v4.json')['inventory']['input_quartic_directions']
env={n:s.Symbol(n,real=True) for n in names};zero={env[n]:0 for n in PORTALS}
full={n:s.Poly(s.sympify(table['parameter_polynomials'][n],locals=env),*env.values()) for n in PORTALS}
restricted={n:s.Poly(s.expand(p.as_expr().subs(zero)),*env.values()) for n,p in full.items()}
def terms(p):
 out={}
 for powers,c in p.terms():
  if c:
   key='*'.join(sorted(n for n,k in zip(names,powers) for _ in range(k)));out[key]=str(c)
 return dict(sorted(out.items()))
old=read(CAL/'canonical_so10_scalar_benchmark/STAGE1_POINT.json')['free_coefficients']
old.update(read(CAL/'canonical_so10_positive_higgs/POINT.json')['changed_free_coefficients'])
finite=read(CAL/'canonical_so10_finite_radial_control/primary_result.json')['physical_parameters']
points={}
for label,values in [('old',old),('finite',finite)]:
 sub={}
 for n,z in env.items():
  if n.endswith(('_re','_im')):
   base=n[:-3];part=n[-2:]
   v=s.Rational(values[base+':'+part]) if label=='old' else (s.re if part=='re' else s.im)(s.sympify(values[base]))
  else:v=s.Rational(values[n])
  sub[z]=v
 assert all(sub[env[n]]==0 for n in PORTALS)
 points[label]={n:str(s.factor(2*p.as_expr().subs(sub))) for n,p in restricted.items()}
active=sorted(set().union(*(set(map(str,p.as_expr().free_symbols)) for p in restricted.values())))
assert not set(CHANGED)&set(active)
finish('primary',{'method':'qualified_global_symbolic_poles','names':names,'full_pole_terms':{n:terms(p) for n,p in full.items()},
 'zero_portal_pole_terms':{n:terms(p) for n,p in restricted.items()},'active_restricted_names':active,'point_beta_I':points,
 'independent_of_changed_quartics_and_eta':True,'beta_I_equals_two_parameter_pole':True,'new_loop_integrals':0},start)
