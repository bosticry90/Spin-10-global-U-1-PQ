"""Coupled radial eigendecomposition and fixed-input one-loop scale logarithms."""
from pathlib import Path
from hashlib import sha256
import sys,json,time
import sympy as s
import mpmath as mp
import control as ctl
R=ctl.R;C=ctl.C;O=ctl.O;inp=ctl.inp;read=ctl.read;digest=ctl.digest
def main():
    start=time.perf_counter();prep=read(O/'assessment_preparation.json');writes=[]
    def readonly(event,args):
        if event=='open' and len(args)>1 and isinstance(args[1],str) and any(x in args[1] for x in 'wax+'):
            writes.append(str(args[0]));raise PermissionError('RADIAL_ASSESSMENT_WRITE_DENIED')
    sys.addaudithook(readonly)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    previous=read(C/'canonical_so10_singlet_tadpole/original_v2_result.json');radial=read(C/'canonical_so10_radial_bosonic_tadpoles/original_v2_result.json');H0=s.Matrix(read(C/'canonical_so10_higgs_neutral_valley/original_result.json')['singlet_Hessian_exact']);ix=[0,1,3];Hr=H0.extract(ix,ix);assert Hr[2,0]==Hr[2,1]==Hr[0,2]==Hr[1,2]==0
    metrics=[s.Integer(60),s.Rational(3,5),s.Rational(3,5)];co=inp.coefficients(0);slots=list(ctl.old.SLOTS);degrees=[inp.PHI,{n:inp.RESCALE.get(n,(0,0))[0] for n in inp.NAMES},inp.SDEG];probes=[]
    for precision in [100,140]:
        mp.mp.dps=precision;num=lambda x:mp.mpf(str(s.N(x,precision+8)));point=read(C/'canonical_so10_positive_higgs/POINT.json')['determinant_polynomial'];aa=mp.mpf(point['A']);bb=mp.mpf(point['B0'])+mp.mpf(point['B1'])*mp.sqrt(15);cc=mp.mpf(point['C0'])+mp.mpf(point['C1'])*mp.sqrt(15);w=(-bb+mp.sqrt(bb*bb-4*aa*cc))/(2*aa)
        root=[mp.sqrt(num(x)) for x in metrics];HR=mp.matrix([[num(x) for x in row] for row in Hr.tolist()]);HC=mp.matrix([[HR[i,j]/(root[i]*root[j]) for j in range(3)] for i in range(3)]);ev,U=mp.eigsy(HC);assert all(x>0 for x in ev)
        for j in range(3):
            pivot=max(range(3),key=lambda i:abs(U[i,j]))
            if U[pivot,j]<0:
                for i in range(3):U[i,j]=-U[i,j]
        coeff={n:ctl.old.number(x) for n,x in co.items()};coeff['mphi2']=60*(w+mp.mpf(1)/500);cs=[mp.re(coeff[n]) if not part or part=='re' else mp.im(coeff[n]) for slot in slots for n,_,part in [slot.partition(':')]];B=[mp.mpf(0)]*3
        def count(sec,n):return int(sec=='Phi') if n==0 else int(sec in ['Sigma','SigmaBar']) if n==1 else int(sec in ['S','SBar'])
        for b in previous['block_inputs']:
            m=len(b['metric']);gg=list(map(num,b['metric']));raw=[s.zeros(m) for _ in slots]
            for k,i,j,z in b['raw_H34_sparse']:raw[k][i,j]=s.sympify(z)
            mats=[mp.matrix([[ctl.old.number(A[i,j])/gg[i] for j in range(m)] for i in range(m)]) for A in raw];M=sum((z*A for z,A in zip(cs,mats)),mp.zeros(m))
            for n in range(3):
                D=mp.matrix([[sum(cs[k]*mats[k][i,j]*(degrees[n][slot.partition(':')[0]]-count(b['sectors'][i],n)-count(b['sectors'][j],n)) for k,slot in enumerate(slots)) for j in range(m)] for i in range(m)]);MD=M*D;B[n]+=b['dimension']*sum(MD[i,i] for i in range(m))/(root[n]*32*mp.pi**2)
        ts=mp.mpf(next(p for p in previous['probes'] if p['precision']==precision)['canonical_tadpole_with_loop_factor']);r=next(p for p in radial['probes'] if p['precision']==precision);cases=[('potential_scalar',r['potential_scalar_canonical_tadpoles'],None)]+[('bosonic_gstar_'+p['gstar']+'_xi_'+p['xi'],p['canonical_bosonic_total'],p) for p in r['diagnostic_couplings_not_physical_input_choices']];records=[]
        for label,pair,gauge in cases:
            T=mp.matrix(list(map(mp.mpf,pair))+[ts]);slope=B.copy()
            if gauge:
                gs=mp.mpf(gauge['gstar']);xi=mp.mpf(gauge['xi'])
                for n in range(2):slope[n]+=sum(3*gs**4*num(s.Rational(p['gamma']))*num(s.sympify(p['Gamma_derivative_trace'][n]))+xi*gs**2*num(s.Rational(p['gamma']))*num(s.sympify(p['orbit_potential_derivative_trace'][n])) for p in radial['gauge_spectral_coefficients'])/(root[n]*32*mp.pi**2)
            modes=[];projected=U.T*T
            for j in range(3):modes.append({'mass2':mp.nstr(ev[j],70),'mass2_over_omega2':mp.nstr(ev[j]/60,70),'canonical_eigenvector':[mp.nstr(U[i,j],70) for i in range(3)],'canonical_tadpole_projection':mp.nstr(projected[j],70),'tadpole_projection_over_omega3':mp.nstr(projected[j]/(60*mp.sqrt(60)),70),'raw_response_contribution':[mp.nstr(-U[i,j]*projected[j]/ev[j]/root[i],70) for i in range(3)]})
            grid=[]
            for ratio in [mp.mpf('.5'),mp.mpf(1),mp.mpf(2)]:
                TQ=T-2*mp.log(ratio)*mp.matrix(slope);dr=mp.lu_solve(HR,-mp.matrix([TQ[i]*root[i] for i in range(3)]));dc=-U*mp.matrix([(U.T*TQ)[j]/ev[j] for j in range(3)]);err=max(abs(dr[i]-dc[i]/root[i])/(1+abs(dr[i])) for i in range(3));assert err<mp.mpf('1e-60');grid.append({'Q_over_Q0':mp.nstr(ratio,20),'canonical_tadpoles':list(map(ctl.old.text,TQ)),'raw_linear_response':list(map(ctl.old.text,dr)),'spectral_raw_solve_relative_error':mp.nstr(err,30)})
            records.append({'case':label,'modes':modes,'explicit_log_slope_B_canonical':list(map(ctl.old.text,slope)),'reference_60I_raw_response':list(map(ctl.old.text,[-T[i]/(60*root[i]) for i in range(3)])),'scale_grid':grid})
        probes.append({'precision':precision,'scalar_explicit_log_slope_B_canonical':list(map(ctl.old.text,B)),'cases':records})
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    assert not writes and time.perf_counter()-start<900
    result={'schema':'RADIAL_CONTROL_SPECTRAL_SCALE_ASSESSMENT_V1','status':'COMPLETE_THREE_RADIAL_REFERENCE_DECOMPOSITION_AND_EXPLICIT_LOG_DIAGNOSTIC','raw_radial_Hessian':ctl.old.matrix_payload(Hr),'raw_radial_metrics':list(map(str,metrics)),'S_tree_decoupling_checked':True,'probes':probes,'complete_quantum_vacuum_or_RG_uncertainty_calculated':False,'fermion_terms_included':False,'scale_or_scheme_or_benchmark_adopted':False,'scientific_authority_changed':False,'write_attempts':writes,'whole_goal_complete':False}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True)
if __name__=='__main__':main()
