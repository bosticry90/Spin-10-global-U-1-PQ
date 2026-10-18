"""Finite SM-component anomaly traces and Spin10 ordinary-orbit identifications."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import product
from math import gcd
from functools import reduce
import sys,json,time
import sympy as s
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def main():
    start=time.perf_counter();prep=read(O/'preparation.json');writes=[]
    def readonly(event,args):
        if event=='open' and len(args)>1 and isinstance(args[1],str) and any(z in args[1] for z in 'wax+'):
            writes.append(str(args[0]));raise PermissionError('PQ_SCREEN_WRITE_DENIED')
    sys.addaudithook(readonly)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    fields=[('16F',1,1),('Phi54',0,0),('Sigma126',2,2),('phi10',-2,2),('S',-4,0)];gen=3
    # All entries are left-handed Weyl fields; right-handed physical names must be conjugated.
    matter=[('Q',3,2,[F(2,3),F(-1,3)],F(1,2),F(1,2)),('uc',3,1,[F(-2,3)],F(1,2),F(1,2)),('dc',3,1,[F(1,3)],F(1,2),F(-3,2)),('L',1,2,[F(0),F(-1)],F(0),F(-3,2)),('ec',1,1,[F(1)],F(0),F(1,2)),('nc',1,1,[F(0)],F(0),F(5,2))]
    rows=[]
    for name,color,weak,charges,T,cartan in matter:
        assert len(charges)==weak;qphys=1-F(2,5)*cartan
        rows.append({'name':name,'color_dimension':color,'weak_dimension':weak,'electric_charges':list(map(str,charges)),'color_Dynkin_index':str(T),'C_charge':str(cartan),'PQ_charge':'1','horizontal_PQ_charge':str(qphys),'color_trace':str(weak*T),'electric_trace':str(color*sum(q*q for q in charges))})
    N=2*gen*sum(F(z['color_trace']) for z in rows);E=2*gen*sum(F(z['electric_trace']) for z in rows);NC=2*gen*sum(F(z['C_charge'])*F(z['color_trace']) for z in rows);EC=2*gen*sum(F(z['C_charge'])*F(z['electric_trace']) for z in rows)
    NP=2*gen*sum(F(z['horizontal_PQ_charge'])*F(z['color_trace']) for z in rows);EP=2*gen*sum(F(z['horizontal_PQ_charge'])*F(z['electric_trace']) for z in rows);assert NC==EC==0 and NP==N and EP==E
    weights=[tuple(F(z,2) for z in signs) for signs in product([1,-1],repeat=5) if signs.count(-1)%2==0];assert len(weights)==16 and all(int(2*sum(w))%4==1 for w in weights)
    kernel=[(k,t) for k in range(4) for t in range(4) if all((k*c+t*q)%4==0 for _,q,c in fields)];assert kernel==[(0,0),(1,3),(2,2),(3,1)]
    assert all((q-c)%4==0 for _,q,c in fields)
    # alpha/(2pi)=n/4: necessary by the nonzero neutral S, sufficient by center action.
    period_turns=F(1,4);assert -4*period_turns==-1 and all((F(q)*period_turns-F(c,4)).denominator==1 for _,q,c in fields)
    assert N.denominator==1 and N>0;NN=int(N);H=sorted({(NN*k//4)%NN for k in range(4)});assert NN%4==0
    cosets=[];unseen=set(range(NN))
    while unseen:
        representative=min(unseen);coset=sorted({(representative+h)%NN for h in H});cosets.append(coset);unseen-=set(coset)
    naive=int(N/reduce(gcd,[2,4]));dw=len(cosets);assert NN*period_turns==dw
    geo=read(C/'canonical_so10_higgs_light_eft_boundary/original_result.json')['geometry'];F2=F(geo['horizontal_norm_squared']);assert geo['projection_coefficient']=='2/5' and F2==F(48,5)
    f2=F2/(N*N);period2=F2/16;assert period2==dw*dw*f2
    for scale in [2,3]:assert F2*scale*scale/(N*scale)**2==f2 and N*scale*period_turns/scale==dw
    wrong_right_sign=2*gen*(F(1)-F(1,2)-F(1,2));assert wrong_right_sign!=N
    assert N/2!=N and N/gen!=N and naive!=dw and F(16)/(N*N)!=f2
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    assert not writes and time.perf_counter()-start<900
    result={'schema':'PQ_ORDINARY_ORBIT_ANOMALY_SCREEN_V1','status':'COMPLETE_UV_ANOMALIES_AND_CONDITIONAL_ORDINARY_ORBIT_COUNT_ONLY','left_Weyl_generations':gen,'field_charges_and_center_characters':[{'field':n,'PQ_charge':q,'Spin10_center_exponent_mod4':c} for n,q,c in fields],'matter_rows':rows,'N_color':str(N),'E_electromagnetic':str(E),'E_over_N':str(E/N),'compensating_C_color_anomaly':str(NC),'compensating_C_electromagnetic_anomaly':str(EC),'horizontal_N_color':str(NP),'horizontal_E_electromagnetic':str(EP),'chiral_spinor_weights':[[str(z) for z in w] for w in weights],'ordinary_field_action_kernel_center_times_PQ_quarters':kernel,'ordinary_vacuum_period_in_2pi_PQ_turns':str(period_turns),'anomaly_ZN_gauge_identifications':H,'anomaly_cosets':cosets,'scalar_gcd_only_naive_wall_count':naive,'conditional_domain_wall_number':dw,'inherited_horizontal_length_squared':str(F2),'reference_anomaly_normalization_squared':str(f2),'reference_anomaly_normalization_squared_over_omega_squared':str(f2/60),'physical_orbit_period_scale_squared':str(period2),'physical_orbit_period_scale_squared_over_omega_squared':str(period2/60),'conditions':['only declared ordinary fields and Spin10 gauge transformations','nonzero S and Sigma VEVs','ordinary PQ orbit; no extra S-charged gauge identification','standard QCD potential after realistic nonzero quark masses; no other explicit PQ breaking'],'full_global_bundle_or_defect_classification_proved':False,'physical_axion_mass_or_relic_density_predicted':False,'reference_normalization_is_full_EW_quantum_decay_constant':False,'gauge_anomaly_cancellation_or_full_E5_proved':False,'flavor_fit_resumed':False,'new_benchmark_cosmology_or_global_completion_adopted':False,'scientific_authority_changed':False,'old_spectrum_or_loop_recomputed':False,'whole_goal_complete':False,'write_attempts':writes,'input_sha256':prep['input_sha256'],'state_sha256':prep['state_sha256']}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True)
if __name__=='__main__':main()
