"""Measured radial input sizes and a directly polarized pure-Sigma contact witness."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from functools import lru_cache
import sys,json,time,platform
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
sys.path.insert(0,str(C/'canonical_so10_singlet_tadpole'));import tadpole_v2 as old
sys.path.insert(0,str(C/'canonical_so10_scalar_reconstruction'));import certify_sigma_quartics as qs
inp=old.inp;g=inp.g;d=inp.d
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def exact_atom(data,k):
    a,b=data['algebra']['atoms'][k];theta=s.sqrt(2)+s.sqrt(3)+s.sqrt(5)
    base=lambda c:sum(s.Rational(z)*theta**i for i,z in enumerate(c))
    return base(a),base(b)
def evaluator(data,w):
    theta=mp.sqrt(2)+mp.sqrt(3)+mp.sqrt(5)
    def rat(z):a=F(z);return mp.mpf(a.numerator)/a.denominator
    def base(co):
        out=mp.mpf(0)
        for z in reversed(co):out=out*theta+rat(z)
        return out
    @lru_cache(None)
    def ev(k):a,b=data['algebra']['atoms'][k];return base(a)+w*base(b)
    return ev
def qvalues(form):
    paired=[qs.paired_tensor(form,k) for k in range(3)]
    return [sum(a*a+b*b for a,b in p.values()) for p in paired]+[qs.cross_contraction(paired[1],3,1)]
def main():
    start=time.perf_counter();prep=read(O/'preparation.json');writes=[]
    def readonly(event,args):
        if event=='open' and len(args)>1 and isinstance(args[1],str) and any(x in args[1] for x in 'wax+'):
            writes.append(str(args[0]));raise PermissionError('RADIAL_INPUT_CONTROL_WRITE_DENIED')
    sys.addaudithook(readonly)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    full=read(C/'canonical_so10_higgs_exact_light_ct_map/original_result.json');subset=read(C/'canonical_so10_higgs_counterterm_subsets/original_result.json');case=next(a for a in subset['cases'] if a['label']=='S0_target9')
    radial=read(C/'canonical_so10_radial_bosonic_tadpoles/original_v2_result.json');singlet=read(C/'canonical_so10_singlet_tadpole/original_v2_result.json');co=inp.coefficients(0);metrics=[s.Integer(60),s.Rational(3,5),s.Rational(3,5)]
    probes=[]
    for digits in [100,140]:
        mp.mp.dps=digits;point=read(C/'canonical_so10_positive_higgs/POINT.json')['determinant_polynomial'];aa=mp.mpf(point['A']);bb=mp.mpf(point['B0'])+mp.mpf(point['B1'])*mp.sqrt(15);cc=mp.mpf(point['C0'])+mp.mpf(point['C1'])*mp.sqrt(15);w=(-bb+mp.sqrt(bb*bb-4*aa*cc))/(2*aa)
        ev=evaluator(full,w);subev=evaluator(subset,w);A=mp.matrix([[ev(k) for k in row] for row in full['exact']['potential_plus_lightmass_map_exact']]);L=mp.matrix([[subev(k) for k in row] for row in case['particular_inverse_exact']]);N=ev(full['exact']['q_norm_exact']);assert N>0
        source=next(p for p in radial['probes'] if p['precision']==digits);TS=mp.mpf(next(p for p in singlet['probes'] if p['precision']==digits)['canonical_tadpole_with_loop_factor'])
        cases=[('potential_scalar',source['potential_scalar_canonical_tadpoles'])]+[('bosonic_gstar_'+p['gstar']+'_xi_'+p['xi'],p['canonical_bosonic_total']) for p in source['diagnostic_couplings_not_physical_input_choices']]
        values=[]
        phys={n:s.simplify(z/(s.sqrt(s.Rational(3,160))**inp.RESCALE.get(n,(0,0))[0]*s.sqrt(s.Rational(3,10))**inp.RESCALE.get(n,(0,0))[1])) for n,z in co.items()};phys['mphi2']=60*(s.Float(str(w),digits)+s.Rational(1,500))
        def physical(name):n,_,part=name.partition(':');z=phys[n];return old.number(s.re(z) if not part or part=='re' else s.im(z))
        for label,pair in cases:
            tc=list(map(mp.mpf,pair))+[TS];raw=mp.matrix([tc[i]*mp.sqrt(old.number(metrics[i])) for i in range(3)]);y=mp.matrix([-x for x in raw]+[mp.mpf(0)]*6)
            dm=mp.matrix([mp.mpf(0)]*34)
            for n,z,den in zip(['mPhi2','mSigma2','mS2'],raw,[120,mp.mpf(6)/5,mp.mpf(3)/5]):dm[full['potential_counterterm_names'].index(n)]=-z/den
            ds=L*y;df=mp.matrix([mp.mpf(0)]*34)
            for n,z in zip(case['parameter_names'],ds):df[full['potential_counterterm_names'].index(n)]=z
            got=A*df;err=max(abs(got[i]-y[i])/(1+abs(y[i])) for i in range(9));assert err<mp.mpf('1e-60')
            direct=A*dm;assert max(abs(direct[i]-y[i])/(1+abs(y[i])) for i in range(3))<mp.mpf('1e-60')
            rows=[]
            for n,z in zip(case['parameter_names'],ds):
                p=physical(n);rows.append({'parameter':n,'frozen_value':old.text(p),'conditional_S0_increment':old.text(z),'absolute_relative_increment':old.text(abs(z/p)) if p else None})
            values.append({'case':label,'target9_increment':list(map(old.text,y)),'pure_mass_increments':{n:old.text(dm[full['potential_counterterm_names'].index(n)]) for n in ['mPhi2','mSigma2','mS2']},'pure_mass_mixed_increment':list(map(old.text,list(direct)[3:9])),'pure_mass_direct_canonical_Higgs_mass2':old.text(direct[9]/N),'S0_parameters':rows,'S0_target_relative_residual':old.text(err),'S0_direct_canonical_Higgs_mass2':old.text(got[9]/N)})
        probes.append({'precision':digits,'cases':values})
    print('STAGE measured_tadpole_input_maps_and_frozen_parameter_size_comparison',flush=True)
    reps=old.rational_representatives();candidates=[];slots=list(old.SLOTS)
    for b in singlet['block_inputs']:
        if len(b['sectors'])!=1 or b['sectors'][0] not in ['Sigma','SigmaBar']:continue
        mass=s.S.Zero;K=s.S.Zero;Gs=s.Rational(b['metric'][0])
        for k,i,j,z in b['raw_H34_sparse']:
            n,_,part=slots[k].partition(':');coef=s.re(co[n]) if not part or part=='re' else s.im(co[n]);mass+=coef*s.sympify(z)/Gs
            q=inp.RESCALE.get(n,(0,0))[0]-2;K+=coef*q*(q-1)*s.sympify(z)/(Gs*metrics[1])
        mass,K=s.expand(mass),s.expand(K)
        if mass>0:candidates.append({'label':b['label'],'mass2_exact':str(mass),'K_exact':str(K)})
    assert candidates
    assert all(s.sympify(a['K_exact']).is_Rational for a in candidates)
    chosen=sorted(candidates,key=lambda a:(-abs(s.Rational(a['K_exact'])),tuple(a['label'])))[0];label=tuple(chosen['label']);sector,_,obj=reps[label][0];rep=old.realified_representative(sector,obj)
    ar,ai=old.state(rep.real),old.state(rep.imag);wr=ar if g.inner(ar,ar) else ai;v=d.vacuum();u=(g.ZERO[0],v[1],g.ZERO[2],g.Z);nu=s.Rational(g.inner(u,u));nw=s.Rational(g.inner(wr,wr));assert nu==metrics[1] and nw>0 and g.inner(u,wr)==0
    qnames=['lambdaSigma1','lambdaSigma2','lambdaSigma3','lambdaSigma4'];forms=[u[1],wr[1],g.plus(u,wr)[1],g.plus(u,g.times(wr,-F(1)))[1]];qv=list(map(qvalues,forms));cross=[s.Rational(2*(p[2]+p[3]-2*p[0]-2*p[1]))/(nu*nw) for p in zip(*qv)];Kdirect=s.expand(sum(co[n]*z for n,z in zip(qnames,cross)))
    assert s.expand(Kdirect-s.sympify(chosen['K_exact']))==0,'FIRST_FAILURE_LITERAL_PARENT_QUARTIC_DISAGREEMENT'
    currents=[]
    for i in range(10):
        for j in range(i+1,10):
            T=d.J(i,j);tu=d.action(T,u);tw=d.action(T,wr);currents.append([str(g.inner(wr,tu)),str(g.inner(u,tu)),str(g.inner(wr,tw))])
    nogauge=all(s.Rational(z)==0 for row in currents for z in row)
    fail_exact=bool(abs(Kdirect)>s.Rational(352,7));bound=abs(old.number(Kdirect))/(32*mp.pi)
    assert Kdirect!=0 and nu*nw!=1
    lam=s.symbols('lam',real=True);h=s.symbols('h',real=True);vertex=s.diff(lam*h**4/4,h,4);assert vertex==6*lam and s.expand(vertex/2-3*lam)==0
    # Orthonormal symmetric two-particle basis for an O(N) reference.
    ON=[]
    for n in [1,2,4]:
        pairs=[(i,j) for i in range(n) for j in range(i,n)];Q=s.Matrix(len(pairs),len(pairs),lambda a,b:2*(int(pairs[a][0]==pairs[a][1])*int(pairs[b][0]==pairs[b][1])+int(pairs[a][0]==pairs[b][0])*int(pairs[a][1]==pairs[b][1])+int(pairs[a][0]==pairs[b][1])*int(pairs[a][1]==pairs[b][0]))/s.sqrt((1+int(pairs[a][0]==pairs[a][1]))*(1+int(pairs[b][0]==pairs[b][1]))))
        assert max(Q.eigenvals())==n+2;ON.append({'N':n,'largest_normalized_contact_eigenvalue_per_lambda':str(max(Q.eigenvals()))})
    Hs=s.Matrix(read(C/'canonical_so10_higgs_neutral_valley/original_result.json')['singlet_Hessian_exact'])[:2,:2];assert Hs[0,0]>0 and s.simplify(Hs.det())>0
    witness={'selected':chosen,'inventory':candidates,'raw_u':d.serial(u),'raw_w':d.serial(wr),'u_metric':str(nu),'w_metric':str(nw),'direct_quartic_raw_samples':[[str(z) for z in row] for row in qv],'canonical_quartic_by_invariant':list(map(str,cross)),'K_direct_exact':str(Kdirect),'all45_currents':currents,'tree_vector_exchange_absent_for_selected_states':nogauge,'a0_entry_absolute':old.text(bound),'exact_rational_sufficient_failure':fail_exact,'fixed_coupling_contact_criterion':'FAIL_SELECTED_ENTRY' if fail_exact else 'INCONCLUSIVE_NO_SELECTED_ENTRY_FAILURE','full_finite_energy_or_RG_unitarity_proved':False,'ON_reference':ON,'wrong_fourth_derivative_factor_K_error':str(Kdirect/2),'wrong_identical_pair_factor_error':old.text(bound),'wrong_kinetic_factor_K_error':str(s.expand(Kdirect*(nu*nw-1)))}
    print('STAGE direct_parent_quartic_normalized_scattering_and_all45_gauge_currents',flush=True)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    assert not writes and time.perf_counter()-start<900
    result={'schema':'RADIAL_INPUT_AND_CONTACT_CONTROL_V1','status':'COMPLETE_MEASURED_INPUT_MAP_AND_DIRECT_CONTACT_SCREEN','input_probes':probes,'scattering_witness':witness,'unknown_mixed_loop_targets_assumed_zero':False,'finite_condition_or_scheme_or_benchmark_adopted':False,'full_model_exclusion_proved':False,'physical_Higgs_matching_complete':False,'scientific_authority_changed':False,'input_sha256':prep['input_sha256'],'state_sha256':prep['state_sha256'],'write_attempts':writes,'whole_goal_complete':False}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start,'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},sort_keys=True),flush=True)
if __name__=='__main__':main()
