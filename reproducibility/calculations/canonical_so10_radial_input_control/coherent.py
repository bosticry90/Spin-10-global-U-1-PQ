"""Complete the selected real SM module and its normalized coherent pair channel."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import sys,json,time
import sympy as s
import mpmath as mp
import control as ctl
R=ctl.R;C=ctl.C;O=ctl.O;g=ctl.g;d=ctl.d;inp=ctl.inp
read=ctl.read;digest=ctl.digest
def main():
    start=time.perf_counter();prep=read(O/'coherent_preparation.json');writes=[]
    def readonly(event,args):
        if event=='open' and len(args)>1 and isinstance(args[1],str) and any(x in args[1] for x in 'wax+'):
            writes.append(str(args[0]));raise PermissionError('COHERENT_CHANNEL_WRITE_DENIED')
    sys.addaudithook(readonly)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    old=read(O/'original_result.json')['scattering_witness'];u=g.state(old['raw_u']);w=g.state(old['raw_w']);K=s.Rational(old['K_direct_exact']);nu=s.Rational(g.inner(u,u))
    neutral=read(C/'canonical_so10_higgs_charge_sector/original_result.json')['actual_neutral_generators'];Ts=[s.Matrix(10,10,list(map(s.Rational,row))) for row in neutral['color']]+[s.Matrix(10,10,list(map(s.Rational,neutral['Q'])))];basis=[]
    def extend(a):
        for b in basis:a=g.plus(a,g.times(b,-g.inner(b,a)/g.inner(b,b)))
        if g.inner(a,a):basis.append(a);return True
        return False
    extend(w);index=0
    while index<len(basis):
        assert len(basis)<=6,'INCOMPLETE_UNEXPECTED_MODULE_DIMENSION'
        for T in Ts:extend(d.action(T,basis[index]))
        index+=1
    assert len(basis)==6
    G=d.gram(basis);assert G==s.diag(*[G[i,i] for i in range(6)]) and all(G[i,i]>0 for i in range(6))
    rho=[]
    for T in Ts:
        assert d.action(T,u)==g.ZERO
        A=s.Matrix(6,6,lambda i,j:s.Rational(g.inner(basis[i],d.action(T,basis[j])))/G[i,i]);rho.append(A)
        assert A.T*G+G*A==s.zeros(6)
        assert all(d.action(T,basis[j])==g.combine(basis,[F(z) for z in A[:,j]]) for j in range(6))
    positions=[(i,j) for i in range(6) for j in range(i,6)];columns=[]
    for i,j in positions:
        E=s.zeros(6);E[i,j]=1;E[j,i]=1;columns.append(s.Matrix.vstack(*(s.Matrix(36,1,list(A.T*E+E*A)) for A in rho)))
    equations=s.Matrix.hstack(*columns);kernel=equations.nullspace();assert len(kernel)==1
    assert equations*s.Matrix([G[i,j] for i,j in positions])==s.zeros(equations.rows,1)
    second=basis[1];nw=s.Rational(g.inner(second,second));co=inp.coefficients(0);forms=[u[1],second[1],g.plus(u,second)[1],g.plus(u,g.times(second,-F(1)))[1]];qv=list(map(ctl.qvalues,forms));cross=[s.Rational(2*(p[2]+p[3]-2*p[0]-2*p[1]))/(nu*nw) for p in zip(*qv)];K2=sum(co[n]*z for n,z in zip(['lambdaSigma1','lambdaSigma2','lambdaSigma3','lambdaSigma4'],cross));assert s.expand(K2-K)==0
    allT=[d.J(i,j) for i in range(10) for j in range(i+1,10)];images=[d.action(T,u) for T in allT];crosscurrents=[[str(g.inner(b,im)) for b in basis] for im in images]
    assert all(F(x)==0 for row in crosscurrents for x in row)
    assert all(g.inner(u,im)==0 for im in images) and all(g.inner(b,d.action(T,b))==0 for b in basis for T in allT)
    # Six orthonormal identical-pair states: the coherent vector has norm1.
    amplitudes=s.ones(6,1)/s.sqrt(6);assert (amplitudes.T*amplitudes)[0]==1
    contact=s.simplify(sum(amplitudes)*K/2);assert s.simplify(contact-s.sqrt(6)*K/2)==0
    exact_fail=bool(6*K*K>s.Rational(352,7)**2);probes=[]
    for precision in [100,140]:
        mp.mp.dps=precision;k=mp.mpf(K.p)/K.q;a=mp.sqrt(6)*abs(k)/(32*mp.pi);probes.append({'precision':precision,'a0_absolute':mp.nstr(a,70),'ratio_to_half':mp.nstr(2*a,70)})
    print('STAGE complete_real6_module_unique_invariant_bilinear_second_literal_derivative_and270_currents',flush=True)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    assert not writes and time.perf_counter()-start<900
    result={'schema':'COHERENT_SCALAR_PERTURBATIVITY_CHANNEL_V1','status':'COMPLETE_DIRECT_FIXED_INPUT_HIGH_ENERGY_CHANNEL','module_dimension':6,'basis':list(map(d.serial,basis)),'metric':ctl.old.matrix_payload(G),'SM_generators':[list(map(str,T)) for T in Ts],'module_actions':[ctl.old.matrix_payload(A) for A in rho],'invariant_symmetric_bilinear_dimension':len(kernel),'second_direction_quartic_by_invariant':list(map(str,cross)),'second_direct_K_exact':str(s.expand(K2)),'K_exact':str(K),'all270_cross_currents':crosscurrents,'all_identical_state_currents_zero':True,'normalized_coherent_contact_magnitude':str(abs(contact)),'exact_squared_rational_failure_certificate':exact_fail,'probes':probes,'tree_fixed_input_perturbative_unitarity_screen':'FAIL_SELECTED_COHERENT_CHANNEL' if exact_fail else 'INCONCLUSIVE','full_finite_energy_or_RG_unitarity_proved':False,'nonperturbative_inconsistency_or_full_model_exclusion_proved':False,'finite_scheme_or_benchmark_adopted':False,'scientific_authority_changed':False,'write_attempts':writes,'whole_goal_complete':False}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-start}),flush=True)
if __name__=='__main__':main()
