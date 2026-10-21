"""VSSA1 exhaustive finite-domain and independent common-scale reconstruction."""
from data import *
from assemble import q,read_sources,FILES

def close(a,b):
    err=abs(a-b)/(1+abs(b));assert err<mp.mpf('1e-30'),(mp.nstr(a,25),mp.nstr(b,25),mp.nstr(err,12));return err

def main():
    start=begin('validation_preparation.json',300);mp.mp.dps=110
    for p,h in json.loads((HERE/'preparation.json').read_bytes())['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    A=packed(HERE/'primary_assembly_tables.json.gz');rs=read_sources()
    fci=packed(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_tables.json.gz');lam=[s.S.Zero]+list(map(s.sympify,fci['vector_mass_eigenvalues']))
    raw=packed(CAL/'canonical_so10_width_hard_projection/primary_tables.json.gz');Ps=list(map(dec,raw['projectors']))
    zero(sum(Ps,s.zeros(45))-s.eye(45));ranks=[]
    for i,P in enumerate(Ps):
        zero(P-P.T);zero(P*P-P);ranks.append(int(s.trace(P)))
        for Z in Ps[:i]:zero(P*Z)
    assert ranks==[12,8,1,12,12]
    T=packed(CAL/'canonical_so10_scalar_current_sm_kernel/primary_tables.json.gz');profiles=T['physical_probes']['profiles']
    assert len(profiles)==180 and len(T['basis'])==177 and T['physical_probes']['counts']==[290,5,8,1,12,12]
    rawcounts=[];fcounts=[];zeroraw=0;catalog=[]
    for r in range(5):
        nonzero=[];hasF=[];zerocharge=[]
        for row in [v for v in profiles if v['r']==r]:
            bits=[s.sympify(z)!=0 for k in ['q1_squared','q2_squared','qv_squared'] for z in row[k]]
            if s.sympify(row['raw'])==0:assert not any(bits);zeroraw+=1;continue
            nonzero.append(row)
            if any(bits):hasF.append(row)
            else:zerocharge.append((row['left'],row['right']))
        rawcounts.append(len(nonzero));fcounts.append(len(hasF))
        assert A['coverage'][r]['raw_nonzero']==len(nonzero) and A['coverage'][r]['F2_nonzero']==len(hasF)
        if r==2:assert set(zerocharge)=={('physical_positive','Gold_2'),('Gold_2','physical_positive')}
        else:assert not zerocharge
        if r in [3,4]:assert ('soft','soft') not in {(v['left'],v['right']) for v in nonzero}
        catalog.extend({'r':r,'left':v['left'],'right':v['right'],'F2':v in hasF} for v in nonzero)
    assert rawcounts==[5,16,8,11,15] and fcounts==[5,16,6,11,15] and zeroraw==125
    assert rs[0]['all_soft_graph_and_local_forests_equal_before_IR_removal'] and rs[0]['mixed_positive_soft_zero_by_current_projectors']
    assert rs[0]['exact_UV_arithmetic_no_float_atoms'] and rs[0]['all_five_vector_sector_primitive_inputs_available']
    assert rs[1]['profiles']==16 and rs[3]['profiles']==11 and rs[4]['profiles']==15
    assert all(v['scientific_acceptance']=='NOT_PERFORMED' and v['full_C1_or_E5_qualified'] is False for v in rs)
    assert [v['r'] for v in A['branch_receipts']]==list(range(5))
    assert len(set((v['folder'],v['receipt']) for v in A['branch_receipts']))==5
    # Prove the exact positive-mass scale transformation before any sums.
    LL=s.Symbol('L',real=True);gg=s.Symbol('g2',positive=True)
    for vv in lam[1:]:assert s.expand_log(LL+s.log(60/(vv*gg))-(LL-s.log(gg)+s.log(60/vv)),force=True).expand()==0
    error=mp.mpf(0);controls={};checks=[]
    for gs in ['0.5','1.0']:
        g2=mp.mpf(gs);rows=A['cases'][gs]['coefficients'];bad=[]
        for ideal in range(3):
            r0=rs[0]['coefficients']['Rprime_matched'][ideal]
            finite=q(r0[1])+q(r0[3])*mp.log(g2);slope=q(r0[2]);pole=s.sympify(r0[0]);blind=finite
            for r in range(1,5):
                own=rs[r]['cases'][gs]['coefficients'][ideal]
                delta=-mp.log(g2)+mp.log(mp.mpf(60))-mp.log(q(lam[r]))
                part=q(own[1])+q(own[2])*delta;finite+=part;slope+=q(own[2]);pole+=s.sympify(own[0]);blind+=q(own[1])
                component=A['cases'][gs]['components'][r]['components'][ideal]
                error=max(error,close(part,q(component['finite_at_L0'])),close(q(own[2]),q(component['L'])))
            assert not pole.has(s.Float) and str(red(pole))==rows[ideal][0]
            error=max(error,close(finite,q(rows[ideal][1])),close(slope,q(rows[ideal][2])))
            for Lv in [mp.mpf(0),mp.mpf(2)/7]:
                direct=q(r0[1])+q(r0[3])*mp.log(g2)+Lv*q(r0[2])
                for r in range(1,5):
                    own=rs[r]['cases'][gs]['coefficients'][ideal]
                    direct+=q(own[1])+q(own[2])*(Lv-mp.log(g2)+mp.log(60/q(lam[r])))
                error=max(error,close(direct,q(rows[ideal][1])+Lv*q(rows[ideal][2])))
            bad.append(mp.nstr(blind-finite,45));error=max(error,close(blind-finite,q(A['cases'][gs]['blind_own_scale_addition_finite_changes'][ideal])))
        controls[gs]={'blind_own_scale_finite_changes':bad,'omitted_r0_vector_finite_changes':rs[0]['controls']['omitted_vector_finite_changes']}
        checks.append({'g2':gs,'coefficients':rows})
    # Exact all-carrier UV identity,including the common EFT graph difference.
    soft=list(map(s.sympify,rs[0]['all_soft_common_EFT_poles']));inv=list(map(s.sympify,rs[0]['invariant_full_VSS_poles_before_common_EFT']))
    for gs in ['0.5','1.0']:
        assert [red(s.sympify(v[0])+w) for v,w in zip(A['cases'][gs]['coefficients'],soft)]==inv
    old=T['U1_quantum_light_vector_branch']['coefficients']['Rprime']
    duplicate_pole=s.sympify(old[0]);assert duplicate_pole!=0
    controls['duplicate_contained_full_U1_pole_change']=str(duplicate_pole)
    # The counterterm identity is exact bookkeeping,not an assumed zero parent.
    B,Cp,Cf,S,Cs=s.symbols('B Cp Cf S Cs')
    assert s.expand((B+Cp-S-Cs)-((B+Cf-S-Cs)+(Cp-Cf)))==0
    value={'schema':'VSSA1_VALIDATION','execution_state':'COMPLETED','status':'QUALIFIED_COMPLETE_COMMON_SCALE_VSS_PRIMITIVE',
      'elapsed_after_imports':time.perf_counter()-start,'vector_sectors':5,'vector_projector_ranks':ranks,'scalar_directions':328,'classes':35,'commutant_units':177,
      'type_slots':len(profiles),'raw_nonzero_profiles':sum(rawcounts),'F2_profiles':sum(fcounts),'zero_raw_profiles':zeroraw,'zerocharge_raw_profiles':2,
      'raw_profiles_per_sector':rawcounts,'F2_profiles_per_sector':fcounts,'coverage':catalog,'common_scale_cases':checks,
      'invariant_full_carrier_poles':list(map(str,inv)),'common_EFT_poles':list(map(str,soft)),
      'common_scale_comparison_error':mp.nstr(error,40),'controls':controls,'branch_receipts':A['branch_receipts'],
      'full_VSS_primitive_defined_by_branch_spectral_functions':True,'uniform_all_g_numerical_accuracy_proved':False,
      'full_parent_minus_family_counterterm_included':False,'overall_counterterm_adopted':False,'full_C1_or_E5_qualified':False,
      'physical_unification_test_performed':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED'}
    print('RESULT '+json.dumps(value,sort_keys=True),flush=True)
if __name__=='__main__':main()
