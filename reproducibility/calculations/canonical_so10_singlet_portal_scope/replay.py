"""SPS1 Fraction contraction of the independently generated M05 matrices."""
from data import *
start=begin('replay')
d=read(ROOT/'tools/two_loop_qft_compiler_v1/uvp_m05_independent_scalar_replay_uncompared.json')
payload=dict(d);expected=payload.pop('artifact_sha256');assert sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()==expected
names=d['inventory']['quartic_input_directions'];assert len(names)==26 and d['projection_rank']==26 and d['projection_residual']=='0'
full={};restricted={}
for portal in PORTALS:
 B=d['coefficient_tables'][portal];assert len(B)==26 and all(len(row)==26 for row in B)
 coeff={}
 for i,row in enumerate(B):
  for j,c in enumerate(row):
   pair=tuple(sorted((names[i],names[j])));coeff[pair]=coeff.get(pair,F(0))+F(c)
 coeff={k:v for k,v in coeff.items() if v};full[portal]=coeff
 restricted[portal]={k:v for k,v in coeff.items() if not set(k)&set(PORTALS)}
oldbase=read(CAL/'canonical_so10_scalar_benchmark/STAGE1_POINT.json')['free_coefficients']
oldover=read(CAL/'canonical_so10_positive_higgs/POINT.json')['changed_free_coefficients']
old={n:F(oldover.get(n,oldbase.get(n))) for n in names if not n.endswith(('_re','_im'))}
for n in names:
 if n.endswith(('_re','_im')):
  key=n[:-3]+':'+n[-2:];old[n]=F(oldover.get(key,oldbase[key]))
# All couplings active on the restricted support are real rational components.
# Recover them independently from the two printed real/imaginary components.
raw=read(CAL/'canonical_so10_finite_radial_control/primary_result.json')['physical_parameters']
active=sorted(set(v for terms in restricted.values() for pair in terms for v in pair));finite={}
for n in active:
 if n.startswith('z4_'):
  text=raw['z4'].replace(' ','');real,imag=text.split('-',2)[1:];assert imag.count('*I')==1
  finite[n]=-F(real) if n.endswith('_re') else -F(imag.replace('*I',''))
 elif n=='zK_re':finite[n]=F(raw['zK'])
 elif n=='zK_im':finite[n]=F(0)
 else:finite[n]=F(raw[n])
points={label:{p:str(2*sum((v*values[a]*values[b] for (a,b),v in rows.items()),F(0))) for p,rows in restricted.items()} for label,values in [('old',old),('finite',finite)]}
assert not set(active)&set(CHANGED)
encode=lambda coeff:{'*'.join(k):str(v) for k,v in sorted(coeff.items())}
finish('replay',{'method':'uncompared_M05_Fraction_bilinear_contraction','names':names,'full_pole_terms':{p:encode(c) for p,c in full.items()},
 'zero_portal_pole_terms':{p:encode(c) for p,c in restricted.items()},'active_restricted_names':active,'point_beta_I':points,
 'independent_of_changed_quartics_and_eta':True,'beta_I_equals_two_parameter_pole':True,'new_loop_integrals':0,'matrix_positions_read':2*26*26},start)
