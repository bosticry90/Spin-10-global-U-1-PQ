"""G2P1 exact simultaneous pole test against the separately derived RG target."""
from data import *
start=begin('validation_preparation.json');mp.mp.dps=150
a=packed(HERE/'primary_tables.json.gz');b=packed(HERE/'replay_tables.json.gz');rg=receipt('canonical_so10_two_loop_gauge_beta')
assert rg['status']=='QUALIFIED_INDEPENDENT_TWO_LOOP_GAUGE_SCALAR_PARENT_AND_LIGHT_RG_COMPARATOR'
for key in ['quartic','pole_assembly','quartic_forest_weight','original_forest_ownership']:assert a[key]==b[key],key
P=a['pole_assembly'];assert len(P['families'])==len(P['EFT_families'])==9
assert a['RG_comparator_answer_read'] is b['RG_comparator_answer_read'] is False
assert all(clean(expr(v))==0 for name in ['heavy_sum','EFT_sum','parent_sum'] for v in P[name]['-2'])
assert all(clean(expr(v))==0 for v in P['finite_L_squared_coefficient_inside_g2'])
for i in range(3):
    assert clean(expr(P['heavy_sum']['-1'][i])-expr(rg['parent_minus_light_Lambda_simple_pole'][i]))==0
    assert clean(expr(P['EFT_sum']['-1'][i])-expr(rg['light_Lambda_simple_pole'][i]))==0
    assert clean(expr(P['parent_sum']['-1'][i])-expr(rg['parent_Lambda_simple_pole']))==0
    for name in ['heavy_sum','EFT_sum','parent_sum']:assert not expr(P[name]['-1'][i]).has(J,z,d,*hs)
counts=0;maxerror=mp.mpf(0)
for gs,case in a['finite_cases'].items():
    other=b['finite_cases'][gs];assert set(case)==set(other)
    for field in ['family_L_polynomials','known_graph_local_finite_L0','known_graph_local_scale_linear','raw_quadratic_sum','direct_at_L_2_over7']:
        def compare(x,y):
            global counts,maxerror
            if isinstance(x,dict):
                assert set(x)==set(y)
                for k in x:compare(x[k],y[k])
            elif isinstance(x,list):
                assert len(x)==len(y)
                for p,r in zip(x,y):compare(p,r)
            else:
                p,r=q(x),q(y);err=abs(p-r)/(1+abs(p)+abs(r));maxerror=max(maxerror,err);counts+=1;assert err<mp.mpf('1e-28')
        compare(case[field],other[field])
    assert all(q(v)==0 for v in case['raw_quadratic_sum'])
    for h in range(3):
        C,S,D=map(q,[case['known_graph_local_finite_L0'][h],case['known_graph_local_scale_linear'][h],case['direct_at_L_2_over7'][h]])
        assert abs(D-C-mp.mpf(2)/7*S)<mp.mpf('1e-28')*(1+abs(C)+abs(S))
    assert case['finite_physical_C1'] is False
# Controls compare actual nonzero remainders; zeros remain labelled insensitive.
controls={}
missing=[expr(v['omitted_light_insertion']['-2']) for v in a['quartic']];assert missing[0]==0 and missing[1]!=0 and missing[2]!=0
controls['omit_light_internal_quartic']={'double_pole_residual':vec([-v for v in missing]),'U1_insensitive':True}
tripled=[2*expr(v['CT_heavy_projection']['-2']) for v in a['quartic']];assert all(v!=0 for v in tripled)
controls['triple_full_quartic_real_trace']={'double_pole_residual':vec(tripled)}
controls['drop_VVS']={'simple_pole_residual':vec([-expr(v) for v in P['families']['VVS']['-1']]),'U1_insensitive':True}
assert any(expr(v)!=0 for v in controls['drop_VVS']['simple_pole_residual'])
controls['omit_quartic_light_EFT']={'double_pole_residual':vec([-expr(v) for v in P['EFT_families']['VVVV']['-2']]),'U1_insensitive':True}
assert any(expr(v)!=0 for v in controls['omit_quartic_light_EFT']['double_pole_residual'])
controls['delete_VVV_quadratic_scale']={'finite_L_squared_residual':vec([expr(v['family']['0']).expand().coeff(J,2) for v in a['quartic']])}
assert all(expr(v)!=0 for v in controls['delete_VVV_quadratic_scale']['finite_L_squared_residual'])
controls['omit_each_finite_family']={}
for name,line in a['finite_cases']['1/2']['family_L_polynomials'].items():
    change=[-q(v[0]) for v in line];assert max(abs(v) for v in change)>mp.mpf('1e-12');controls['omit_each_finite_family'][name]=list(map(fmt,change))
qir=packed(CAL/'canonical_so10_vector_quartic_ir_matching/primary_tables.json.gz');qus=packed(CAL/'canonical_so10_vector_quartic_uv_subgraphs/primary_tables.json.gz')
closed=[];remaining=[];positive=[]
for i,row in enumerate(qus['insertions']):
    M=sum(expr(v['mass_CT_trace']) for v in row['traces']['full'])/3;M=common(M.subs(d,0));assert M!=0
    closed.append(str(-20*M));remaining.append(str(-3*M))
    # Lose ONLY the remaining B-loop epsilon-positive term of the CT.
    lost=common(-12*sum((-expr(v['curvature_loop_trace']))*((z-hs[v['external_mass_slot']-1])**2+zz) for v in row['traces']['full']))
    assert lost!=0;positive.append(str(lost))
controls['keep_D_inside_closed_subgraph_pole']={'finite_residual':closed}
controls['premature_D4_remaining_mass_trace']={'finite_residual':remaining}
controls['drop_remaining_B_positive_epsilon']={'finite_residual_J_polynomial':positive}
ownership=a['original_forest_ownership'];assert ownership['Cparent_minus_sum_original_Cfamily_evaluated'] is False
assert ownership['SSS']['cuts']==4806 and ownership['SSS']['original_soft_closings']==234
v3=packed(CAL/'canonical_so10_three_vector_sunset/primary_v2_tables.json.gz');assert v3['mandatory_hard_forest_correction_sha256']=='019db039094fadc591f6841c715beb9816f32a0f225ce2356eff0c8d064bb509'
receipt={'schema':'G2P1_VALIDATION','status':'QUALIFIED_SIMULTANEOUS_NINE_FAMILY_ORIGINAL_FOREST_POLE_AND_COMMON_SCALE_ASSEMBLY',
 'execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED','primitive_inputs':9,
 'heavy_original_forest_combination_pole':P['heavy_sum'],'actual_light_EFT_pole':P['EFT_sum'],'parent_completed_projection_pole':P['parent_sum'],
 'independent_RG_target_matched_exactly':True,'finite_quadratic_scale_coefficient':P['finite_L_squared_coefficient_inside_g2'],
 'known_graph_local_finite_diagnostics':{g:{k:v for k,v in c.items() if k!='family_L_polynomials'} for g,c in a['finite_cases'].items()},
 'finite_numeric_comparisons':counts,'finite_max_scaled_assembly_error':mp.nstr(maxerror,35),'finite_input_precision_limit':'VSS retained common values35digits; scoped comparison1e-28; not C1 acceptance',
 'negative_controls':controls,'original_forest_ownership_preserved':True,'quartic_marked_cycle_completeness_within_declared_slice':True,
 'Cparent_minus_original_families_finite_trace_evaluated':False,'finite_physical_jets_or_full_C1_E5_A5_or_unification_qualified':False,
 'shared_error_limits':['actual model/reference/action/operator inputs','upstream qualified loops/subtraction','symbolic/numeric software','AI authorship'],
 'elapsed_after_imports':time.perf_counter()-start}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
