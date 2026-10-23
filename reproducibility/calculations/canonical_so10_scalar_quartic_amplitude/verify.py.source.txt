"""S4A1 compare all form values, full model sums and independent inverse slope."""
from data import *
start=begin('validation_preparation.json');mp.mp.dps=110
a=packed(HERE/'primary_tables.json.gz');b=packed(HERE/'replay_tables.json.gz')
assert a['working_digits']==110 and b['working_digits']==140 and a['mode_counts']==b['mode_counts']==[290,5,8,1,12,12]
assert a['remaining_overall_pole']==b['remaining_overall_pole']==[0,0,0]
assert a['original_Cfull']==b['original_Cfull'] and a['Csoft']==b['Csoft'] and a['Chard']==b['Chard']
maxdiff=mp.mpf(0);comparisons=0
def compare(x,y):
    global maxdiff,comparisons
    if isinstance(x,dict):
        assert set(x)==set(y)
        for k in x:compare(x[k],y[k])
    elif isinstance(x,list):
        assert len(x)==len(y)
        for u,v in zip(x,y):compare(u,v)
    elif isinstance(x,bool):assert x==y
    else:
        u,v=mp.mpf(x),mp.mpf(y);e=abs(u-v)/(1+abs(u)+abs(v));maxdiff=max(maxdiff,e);comparisons+=1
        assert e<mp.mpf('1e-55'),(x,y,e)
compare(a['cases'],b['cases'])
frame,cov,polys,coeff,charges,fci,blocks,counts=input_data('primary');root=root_value('primary');pair,parts=pair_function(polys,coeff,root,'primary')
inverse_error=mp.mpf(0);recon_error=mp.mpf(0);controls=[]
for gs,case in a['cases'].items():
    g2=mp.mpf('.5') if gs=='1/2' else mp.mpf(1);Ms=[];Rs=[]
    for bb in blocks:
        M=numeric(bb['H'],root)+g2*numeric(bb['G'],root);P=numeric(bb['P'][1],root)
        R=mp.inverse(M+P)-P;Ms.append(M);Rs.append(R)
        inverse_error=max(inverse_error,norm(M*R+P-mp.eye(M.rows)))
    mv=form_values(Ms,cov,root)
    for h in range(3):
        B=form_values([number(charges[h][i],root)*R for i,R in enumerate(Rs)],cov,root)
        slope=-pair(mv,B)/4;reported=mp.mpf(case['scale_linear'][h])
        assert abs(slope-reported)/(1+abs(slope))<mp.mpf('1e-55')
        contrib=case['coupling_contributions'][h]
        for j,name in enumerate(['finite_L0','scale_linear']):
            e=abs(mp.fsum(mp.mpf(v[j]) for v in contrib.values())-mp.mpf(case[name][h]))/(1+abs(mp.mpf(case[name][h])))
            recon_error=max(recon_error,e);assert e<mp.mpf('1e-55')
        hist=case['matching_histories'][h]
        for row in hist:
            C=mp.mpf(case['finite_L0'][h]);R=mp.mpf(row['predicted_suppressed_remainder']);matched=mp.mpf(row['full_minus_opened_soft_and_EFT'])
            assert abs(matched-C-R)/(1+abs(C)+abs(R))<mp.mpf('1e-55')
        controls.append(case['negative_controls'][h])
assert inverse_error<mp.mpf('1e-80')
assert any(abs(mp.mpf(v['omit_tadpole_constant_change']))>mp.mpf('1e-40') for v in controls)
assert any(abs(mp.mpf(v['extra_g2_prefactor_change']))>mp.mpf('1e-40') for v in controls)
assert any(abs(mp.mpf(v['omit_compact_offdiagonals_change']))>mp.mpf('1e-40') for v in controls)
assert any(v['deleted_light_soft_sensitive'] for v in controls)
receipt={'schema':'S4A1_VALIDATION','status':'QUALIFIED_COMPLETE_SCALAR_QUARTIC_MATCHED_PRIMITIVE',
 'execution_state':'COMPLETED','scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
 'amplitude_primitive_inventory':8,'real_scalar_fields':328,'SM_classes':35,'complete_mode_counts':counts,
 'diagnostics':{gs:{k:c[k] for k in ['finite_L0','scale_linear','soft_coefficients','negative_controls']} for gs,c in a['cases'].items()},
 'numeric_comparisons':comparisons,'max_serialized_scaled_error':mp.nstr(maxdiff,35),
 'max_independent_inverse_residual':mp.nstr(inverse_error,35),'max_parent_contribution_sum_error':mp.nstr(recon_error,35),
 'original_Cfull_retained_for_parent_minus_family':True,'regulated_full_soft_EFT_identity_retained':True,
 'remaining_overall_pole':[0,0,0],'finite_function_scale_form':'C(g10^2)+L*S(g10^2), L=log(Q2/60), no universal g10^2 prefactor',
 'uniform_all_g_numeric_bound':False,'SSS_complete':False,'full_C1_E5_A5_or_physical_matching_qualified':False,
 'shared_error_limits':['qualified action/quartic functional and kernel','frame/vacuum/projectors/reference prescription','symbolic and numerical software','AI authorship'],
 'elapsed_after_imports':time.perf_counter()-start}
print('RESULT '+json.dumps(receipt,sort_keys=True),flush=True)
