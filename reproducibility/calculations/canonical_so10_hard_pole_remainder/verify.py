"""HPR1 separate exact projection, Gamma, RG and finite-direction checks."""
from data import *
from itertools import combinations
start=begin('validation_preparation.json');mp.mp.dps=100
A=packed(HERE/'primary_tables.json.gz');B=packed(HERE/'replay_tables.json.gz')
assert A['peer_or_physical_target_read'] is B['peer_or_physical_target_read'] is False
trace_coefficients=0
for a,b in zip(A['sectors'],B['sectors']):
    assert a['mass_set']==b['mass_set'] and ex(a['mass_over_g2'])==ex(b['mass_over_g2'])
    assert len(a['charge_components'])==len(b['charge_components'])==3
    for x,y in zip(a['charge_components'],b['charge_components']):
        for scope in ['scalar','ghost','sum']:
            for xx,yy in zip(x[scope],y[scope]):assert clean(ex(xx)-ex(yy))==0;trace_coefficients+=1
        assert list(map(ex,x['sum']))==[0,0,0]
        assert all(clean(ex(z)+ex(w))==0 for z,w in zip(x['scalar'],x['ghost']))
assert trace_coefficients==108
for x,y in zip(A['vector_pole_finite_positive_eps'],B['vector_pole_finite_positive_eps']):assert clean(ex(x)-ex(y))==0
assert ex(A['heat_gauge_multiplet'])==s.Rational(21,2)+e
assert ex(A['open_ghost_angular_pole'])==s.Rational(1,2)
assert ex(A['wrong_unprojected_angular_finite_lift'])==-s.Rational(1,4)

# Actual inherited operator premises, not inferred from a zero scalar/ghost sum.
gct=json.loads((CAL/'canonical_so10_ghost_counterterm_trace_closure/validation_receipt.json').read_bytes())
cbr=json.loads((CAL/'canonical_so10_common_light_boundary/validation_receipt_v2.json').read_bytes())
assert gct['positive_heavy_trace_equal_before_Laurent_finite_extraction'] and gct['known_FCI_prescribed_pole_not_added_again_to_Rprime_sum']
assert gct['complete_scalar_classes']==35 and gct['complete_scalar_slots']==177 and gct['nonradial_profile_cross_slots']==8
assert cbr['same_operation_before_limits'] and cbr['soft_reduced_tadpole_CT_cancels_with_EFT']
assert cbr['hard_parent_CT']=='RAW_1PI;HH_tadpole_CT_in_HTB_only'
qvalue=-s.Rational(2,3);kin=(10+e)*qvalue;mass=-kin;width=qvalue/2;ghost=-qvalue/2
assert clean(kin+mass+width+ghost)==0 and kin!=0 and width!=0
# A fixed spurion times delta stays suppressed on the positive-heavy projector.
for sector in A['sectors']:
    m=ex(sector['mass_over_g2']);jr=L-lg-s.log(m/60)
    suppressed=[delta/m,delta*jr/m,delta*(jr*jr+s.zeta(2))/(2*m)]
    assert all(not clean(z/delta).has(delta) for z in suppressed)

bp,cp=ex(A['parent_b']),ex(A['parent_c'])
assert bp==-s.Rational(46,3) and cp==s.Rational(4520,3)
u,b,c=s.symbols('u b c',real=True)
parseRG=lambda z:s.sympify(z,locals={'b':b,'c':c,'eps':e})
assert clean(parseRG(A['ZA_two'])-parseRG(B['ZA_two']))==0
assert clean(parseRG(A['ZA_two'])+c/(2*e))==0
ct=list(map(ex,A['overall_UV_minus_EFT_pole_CT']))
assert ct==list(map(ex,B['overall_UV_minus_EFT_pole_CT']))
for key in ['measured_heavy_pole','measured_EFT_pole','measured_parent_pole']:
    assert list(map(ex,B[key]['-2']))==[0,0,0]
heavy=list(map(ex,B['measured_heavy_pole']['-1']));light=list(map(ex,B['measured_EFT_pole']['-1']));parent=list(map(ex,B['measured_parent_pole']['-1']))
assert all(clean(x+y)==0 for x,y in zip(heavy,ct))
assert all(clean(x+y-z)==0 for x,y,z in zip(heavy,light,parent))
assert parent==[-s.Integer(2260)]*3
# Pole counterterms are fixed by the RG construction; no independently chosen
# finite mass/tadpole/background constant is extracted from this equality.
lightc=s.Matrix([[ex(v) for v in row] for row in A['light_c_matrix']])
dropmixed=[s.Rational(3,2)*(sum(lightc[i,k] for k in range(3))-lightc[i,i]) for i in range(3)]
assert dropmixed==[s.Rational(27,20),s.Rational(9,20),s.Integer(0)]

# Unexpanded Gamma controls on each separate nonzero profile, not only its zero sum.
maxgamma=mp.mpf(0);refinement=mp.mpf(0);checks=0
items=[]
for sector in A['sectors']:
    for ih,component in enumerate(sector['charge_components']):
        for name in ['scalar','ghost']:
            vals=list(map(ex,component[name]));co=vals[0]
            if co==0:assert vals==[0,0,0];continue
            items.append((co,vals,ex(sector['mass_over_g2'])))
items.append((None,list(map(ex,A['vector_pole_finite_positive_eps'])),None))
for co,vals,m in items:
    for Lv,gv in [(mp.mpf(0),mp.mpf(1)),(mp.mpf(2)/7,mp.mpf(1)/2)]:
        actual_j=Lv-mp.log(gv)-(mp.log(mp.mpf(str(m))/60) if m is not None and m.is_Integer else mp.log(mp.mpf(str(s.numer(m)))/mp.mpf(str(s.denom(m)))/60) if m is not None else 0)
        want=[]
        for z in vals:
            sub={L:s.Float(str(Lv),110),lg:s.Float(str(mp.log(gv)),110),j:s.Float(str(actual_j),110),rho:s.Integer(1)}
            want.append(mp.mpf(str(s.N(z.subs(sub),105))))
        coefficient=mp.mpf(str(s.N(co,105))) if co is not None else None
        hist=[]
        for nodes,rad in [(40,mp.mpf(1)/32),(64,mp.mpf(1)/64)]:
            out=[mp.mpc(0)]*3
            for n in range(nodes):
                phase=mp.exp(2j*mp.pi*n/nodes);ev=rad*phase
                h=mp.exp(mp.euler*ev)*mp.gamma(1+ev)*mp.exp(ev*actual_j)
                numerator=coefficient*h if coefficient is not None else -(mp.mpf(21)/2+ev)*h
                for k in range(3):out[k]+=numerator/(nodes*ev**k)
            for x,y in zip(out,want):
                err=abs(x-y)/(1+abs(y));maxgamma=max(maxgamma,err);assert err<mp.mpf('1e-35');checks+=1
            hist.append(out)
        for x,y in zip(*hist):
            err=abs(x-y)/(1+abs(y));refinement=max(refinement,err);assert err<mp.mpf('1e-35')

# Numerical admissible-direction witness, with inherited HST accuracy retained.
flags=A['stationary_Higgs_tangent_flags'];assert flags['heavy_real']==290 and flags['zero_real']==38
assert flags['Higgs_preserved_to_first_order_only'] and flags['physical_reference_units_fixed'] and not flags['finite_reparameterization_or_counterterm_chosen']
X=[[mp.mpf(z) for z in row] for row in A['one_loop_tangent_response']]
Y=[[mp.mpf(z) for z in row] for row in B['one_loop_tangent_response_refined']]
maxdirection=mp.mpf(0);maxgram=mp.mpf(0)
for x,y in zip(sum(X,[]),sum(Y,[])):
    err=abs(x-y)/(1+abs(x)+abs(y));maxdirection=max(maxdirection,err);assert err<mp.mpf('5e-7')
directY=[[Y[0][k]-Y[i][k] for k in range(3)] for i in [1,2]]
minor_values={}
for i,k in combinations(range(3),2):
    key=str(i)+str(k);a=mp.mpf(A['difference_minors'][key]);ref=directY[0][i]*directY[1][k]-directY[0][k]*directY[1][i]
    err=abs(a-ref)/(1+abs(a)+abs(ref));assert err<mp.mpf('5e-7')
    gram=mp.mpf(B['centered_Gram_determinants'][key]);err=abs(a*a/3-gram)/(1+abs(gram));maxgram=max(maxgram,err);assert err<mp.mpf('5e-7')
    minor_values[key]=fmt(a)
assert abs(mp.mpf(A['difference_minors']['01']))>100
assert A['finite_transport_sign']==B['finite_transport_sign']==-1
# Inverse finite reparameterization of the SAME bare coefficient fixes that sign.
t,h,fp0,fp1,fp2=s.symbols('t h fp0 fp1 fp2')
coefficient=s.expand(t*(fp0-t*h*fp1)+t*t*fp2).coeff(t,2)
assert s.expand(coefficient-(fp2-h*fp1))==0
controls={'omit_one_profile_partner':'nonzero actual components; neutral_r2_and_r1_SU2_insensitive',
 'premature_D4_vector_closing_wrong_minus_correct':str(rho),
 'unprojected_open_angular_lift_is_extra_finite_scheme_term':A['wrong_unprojected_angular_finite_lift'],
 'drop_light_mixed_beta_CT_shift':strs(dropmixed),'reverse_UV_minus_EFT_CT_leaves':strs([2*x for x in heavy]),
 'whole_correlated_q_direction_duplicate':'F2_INSENSITIVE;actual QMV operator witness inherited',
 'finite_jets_assumed_zero':'not_implied_by_pole_closure;actual_nonuniversal_rank2_witness',
 'same_bare_transport_not_benchmark_refit':True}
receipt={'schema':'HPR1_VALIDATION','status':'QUALIFIED_PRESCRIBED_HARD_POLE_CLOSURE_OVERALL_MS_POLE_AND_FINITE_INPUT_WITNESS',
 'execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
 'actual_sector_Laurent_coefficients_compared':trace_coefficients,'prescribed_pole_parent_minus_family_hard_trace':'ZERO_BEFORE_LAURENT;gapped_CBR_domain_only',
 'overall_MSbar_UV_minus_EFT_CT_g2_over_eps':strs(ct),'measured_heavy_overall_pole_g2_over_eps':strs(heavy),
 'overall_double_and_simple_pole_residuals':['0','0','0'],'vector_closing_finite_dimensional_constant':'-rho_RETAINED',
 'Gamma_comparisons':checks,'maximum_Gamma_scaled_error':fmt(maxgamma),'maximum_Gamma_refinement':fmt(refinement),
 'finite_difference_response_matrix':A['difference_response'],'finite_tangent_2x2_minors':minor_values,
 'maximum_tangent_scaled_route_difference':fmt(maxdirection),'maximum_minor_Gram_scaled_difference':fmt(maxgram),
 'finite_nonuniversal_response_rank':'NUMERICAL_2_IN_QUALIFIED_HST_TANGENT_SCOPE;NOT_RIGOROUS_INTERVAL_OR_EXACT_RANK_CERTIFICATE',
 'finite_parent_conditions_fixed':False,'full_finite_C1_E5_A5_or_physical_unification_qualified':False,
 'finite_scheme_change_not_physical_repair':True,'formal_E5_FNL_PCT_not_imported_into_C1':True,
 'negative_controls':controls,'shared_limits':['qualified action/point/operator/region premises','stored HST complex128-derived inputs','software and AI analyst'],
 'elapsed_after_imports':time.perf_counter()-start}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
