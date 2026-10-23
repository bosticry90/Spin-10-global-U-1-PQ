"""HPR1 mutate qualified completed expressions, never the input coefficients."""
from data import *
start=begin('supplement_preparation.json');A=packed(HERE/'primary_tables.json.gz')
changed_scalar=0;changed_ghost=0;insensitive=[]
for sector in A['sectors']:
    for i,z in enumerate(sector['charge_components']):
        a=list(map(ex,z['scalar']));b=list(map(ex,z['ghost']))
        assert all(clean(x+y)==0 for x,y in zip(a,b))
        if a[0]==0:assert a==b==[0,0,0];insensitive.append([sector['mass_set'],i]);continue
        assert any(v!=0 for v in a) and any(v!=0 for v in b)
        changed_scalar+=1;changed_ghost+=1
assert changed_scalar==changed_ghost==8 and len(insensitive)==4
correct=ex(A['vector_pole_finite_positive_eps'][1]);wrong_D4=-s.Rational(21,2)*rho*j
assert clean(wrong_D4-correct)==rho
open_angular=1-2/(4-2*e)
extra_finite=clean(s.diff(open_angular,e).subs(e,0));assert extra_finite==-s.Rational(1,4)
ct=list(map(ex,A['overall_UV_minus_EFT_pole_CT']));loop=[-v for v in ct]
assert all(clean(x+y)==0 for x,y in zip(loop,ct)) and all(clean(x-y)!=0 for x,y in zip(loop,ct))
light=s.Matrix([[ex(z) for z in row] for row in A['light_c_matrix']])
missing_cross=[clean(s.Rational(3,2)*(sum(light[i,k] for k in range(3))-light[i,i])) for i in range(3)]
assert missing_cross[:2]==[s.Rational(27,20),s.Rational(9,20)] and missing_cross[2]==0
fci=json.loads((CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_result.json').read_bytes())
mp.mp.dps=80;extra=[mp.mpf(v) for v in fci['coefficients']['-2']['pole']]
assert all(abs(v)>100 for v in extra)
receipt={'schema':'HPR1_ADVERSARIAL','status':'QUALIFIED_HPR1_EXPLICIT_POLE_AND_FINITE_MUTATIONS',
 'execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
 'omit_scalar_partner_changed_charge_components':changed_scalar,'omit_ghost_partner_changed_charge_components':changed_ghost,
 'zero_projection_insensitive_components':insensitive,'premature_D4_wrong_minus_correct':str(clean(wrong_D4-correct)),
 'unprojected_open_angular_adds_finite_term':str(extra_finite),'wrong_CT_sign_residue':strs([clean(x-y) for x,y in zip(loop,ct)]),
 'omit_light_mixed_beta_CT_shift':strs(missing_cross),
 'duplicate_old_FCI_extra_gminus2_pole_coefficient':list(map(fmt,extra)),
 'same_bare_coordinate_repair_not_adopted':True,'finite_conditions_or_C1_E5_A5_qualified':False,
 'main_receipt_sha256':sha256((HERE/'validation_receipt.json').read_bytes()).hexdigest(),
 'elapsed_after_imports':time.perf_counter()-start}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
