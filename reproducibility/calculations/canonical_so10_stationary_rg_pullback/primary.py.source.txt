"""SRG1 stationary parameter/Gram operator jets and their direct mass trace."""
from data import *
started=begin();guard('primary');mp.mp.dps=90;root=point_root()
fc=packed(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_tables.json.gz')
ht=packed(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_tables.json.gz')
sq=packed(CAL/'canonical_so10_scalar_quadratic_pullback/primary_tables.json.gz')
ut=read(CAL/'canonical_so10_uv_radial_tadpoles/primary_result.json')
M=dec(ht['raw_Hessian']);Mi=tidy(M.inv());zero(M*Mi-s.eye(3))
T={p:s.Matrix([red(s.sympify(z,locals={'w':w})/4) for z in ut[key]]) for p,key in zip(POWERS,['scalar_exact_reduced_w','mixed_fractional_exact','vector_fractional_exact'])}
d={p:tidy(Mi*T[p]) for p in POWERS};db=s.Matrix([20,25,0]);zero(d[2]-db/4)
vstat={p:tidy((db if p==2 else s.zeros(3,1))-d[p]) for p in POWERS}
# Source counterterm polynomial grading, including dimensionful coefficients.
contract=read(ROOT/'tools/two_loop_qft_compiler_v1/layer5_counterterm_contract.json')
degree={r['coefficient']:r['field_degree']-2 for r in contract['parent_operator_basis']['rows']}
def wt(n):return degree[n[:-3] if n.endswith(('_re','_im')) else n]
polys=packed(CAL/'canonical_so10_scalar_kernel_reconciliation/primary_tables.json.gz')['parameter_polynomials']
monomials=0
for name,raw in polys.items():
    P=s.sympify(raw);E=sum(wt(str(z))*z*s.diff(P,z) for z in P.free_symbols)
    assert s.expand(E-(wt(name)+2)*P)==0,name
    monomials+=sum(coef!=0 for _,coef in s.Poly(P,*sorted(P.free_symbols,key=str)).terms())
assert len(polys)==34 and monomials==342
result={p:mp.zeros(3,1) for p in POWERS};out=[];slots=0;mixed=0;goldchecks=0
for ib,(b,ds) in enumerate(zip(fc['blocks'],ht['radial_blocks'])):
    H=dec(b['H']);Pp=dec(b['physical']);Pg=dec(b['gauge']);N=dec(b['N0']);D=list(map(dec,ds['D']));m=H.rows;slots+=m*m
    jets=[]
    for k,p in enumerate(POWERS):
        Q=tidy(dec(b['P'][k])-sum((d[p][j]*D[j] for j in range(3)),s.zeros(m)))
        zero(Pg*Q*Pg);goldchecks+=m*m
        mixed+=len(tidy(Q*Pg).todok());jets.append(Q)
        if p==2:zero(Q+s.Rational(3,2)*dec(sq['blocks']['Hend'][ib]).subs(xi,1))
        for G in b['gold_mass_projectors']:assert red(s.trace(dec(G)*Q))==0
    hn,pn=numeric(H+60*N,root),numeric(Pp,root);inv=hn**-1
    beta=weights(b['label'])
    for p,Q in zip(POWERS,jets):
        qn=numeric(Q,root);tr=sum((pn*inv*qn)[j,j] for j in range(m));assert abs(mp.im(tr))<mp.mpf('1e-65')*(1+abs(tr))
        for a in range(3):result[p][a]+=mp.re(number(6*beta[a],root))*mp.re(tr)
    out.append({'block':ib,'stationary_pole_jets':list(map(enc,jets))})
assert slots==177 and mixed>0
dv=s.Matrix(ht['vector_Gram_radial_derivative_traces']);ranks=[8,1,12,12]
lams=list(map(s.Rational,fc['vector_mass_eigenvalues']));fj=list(map(s.Rational,fc['vector_fractional_jets']));tau=s.Matrix(fc['vector_indices'])
vf={}
for p in POWERS:
    frac=[red((fj[r] if p==2 else 0)-sum(d[p][j]*dv[r,j]/(ranks[r]*lams[r]) for j in range(3))) for r in range(4)]
    vf[str(p)]=list(map(str,frac))
    for a in range(3):result[p][a]+=mp.re(number(-21*sum(tau[r,a]*frac[r] for r in range(4)),root))
save('primary',{'method':'actual_stationary_operator_and_Gram_trace','stationary_operators':out,'stationary_vector_fractional_pole_jets':vf,
    'tadpole_CT':{str(p):list(map(str,T[p])) for p in POWERS},'stationary_VEV_pole':{str(p):list(map(str,vstat[p])) for p in POWERS},
    'W_coefficients':{'-2':['0']*3,**{str(p):list(map(fmt,result[p])) for p in POWERS}},
    'parameter_directions':34,'parameter_monomials':monomials,'matrix_slots':slots,'goldstone_compression_positions':goldchecks,
    'mixed_orbit_column_nonzero':mixed,'gauge2_endpoint_free_identity_checked':True,'finite_slope_read':False,
    'numerical_C1_calculated':False,'new_parameter_beta_obtained_from_finite_slope':False},started)
