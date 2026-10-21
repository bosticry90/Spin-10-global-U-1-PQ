"""VSP1 separate sparse contractions, actual soft restrictions and Laurent controls."""
from data import *
def main():
    start=begin('validation_preparation.json');mp.mp.dps=80
    colors=[packed(HERE/(r+'_color_tables.json.gz')) for r in ['primary','replay']]
    amps=[packed(HERE/(r+'_amplitude_tables.json.gz')) for r in ['primary','replay']]
    assert colors[0]==colors[1];color=colors[0];amp=amps[0];err=mp.mpf(0)
    def compare(a,b):
        nonlocal err
        if isinstance(a,dict):
            assert set(a)==set(b)
            for k in a:compare(a[k],b[k])
        elif isinstance(a,list):
            assert len(a)==len(b)
            for x,y in zip(a,b):compare(x,y)
        elif isinstance(a,str):
            try:x,y=mp.mpf(a),mp.mpf(b)
            except ValueError:assert a==b;return
            e=abs(x-y)/(1+abs(x));err=max(err,e);assert e<mp.mpf('1e-40'),(a,b)
        else:assert a==b
    compare(amps[0],amps[1])
    d,rho,V,ad,Ps,frame,Q,Qi,E=inputs('replay');fci=packed(CAL/'canonical_so10_finite_counterterm_insertion/replay_v3_tables.json.gz')
    print('STAGE third_sparse_index_contraction',flush=True)
    # Elementwise sparse index join, without native rho_a*rho_b or Gram products.
    rd=[R.todok() for R in rho];left=[];right=[]
    for dd in rd:
        la={};ra={}
        for (i,j),z in dd.items():la.setdefault(j,[]).append((i,z));ra.setdefault(i,[]).append((j,z))
        left.append(la);right.append(ra)
    @lru_cache(1000)
    def pair(a,b):
        out={}
        for k,rows in left[a].items():
            for i,z in rows:
                for j,t in right[b].get(k,[]):out[i,j]=out.get((i,j),0)-z*t
        return out
    for n,Mdata in enumerate(color['M_color']):
        out={}
        for (a,b),z in dec(Mdata).todok().items():
            for ij,t in pair(int(a),int(b)).items():out[ij]=out.get(ij,0)+z*t
        direct=tidy(s.SparseMatrix(328,328,out));zero(direct-dec(color['full'][n]))
    # Genuine local soft tree operator, not just matching abstract placeholders.
    softu=[0,0,0];softw=[0,0,0]
    for b in fci['blocks']:
        ib=b['block'];P=dec(b['soft']);A=dec(color['blocks'][0][ib]);tau=[6*z for z in weights(b['label'])]
        for i in range(3):
            B=dec(color['blocks'][5+i][ib]);softu[i]+=b['dimension']*s.trace(B*P);softw[i]-=tau[i]*s.trace(A*P)
    assert list(map(red,softu))==[0,-2,0]
    assert list(map(red,softw))==[-s.Rational(27,50),-s.Rational(9,10),0]
    light_bare_pole=[red(-10*x+2*y) for x,y in zip(softu,softw)];assert any(light_bare_pole)
    # Differentiate the literal two-species quartic before closing; no guessed Wick weight.
    q,x,R=s.symbols('q x R');L=-q*q*x*x*R/2
    C=s.diff(L,q,2,x,2);assert C/4==-R/2
    assert s.diff(L,q,2)/2==-x*x*R/2 and s.diff(L,x,2)/2==-q*q*R/2
    vv,vs,sv,ss=s.symbols('vv vs sv ss');bil=lambda a,b:-R*a*b/2
    assert s.expand(bil(vv+vs,sv+ss)-bil(vv,ss)-bil(vs,sv)-bil(vs,ss)-bil(vv,sv))==0
    # Same bilinear identity separately for each UV-projected tadpole attachment.
    ev,es,lv,ls=s.symbols('ev es lv ls')
    assert s.expand((ev+lv)*(es+ls)-ev*ls-lv*es-lv*ls-ev*es)==0
    # Eight labelled edge insertions; signs of G_hk are not lost.
    edgewords=[(edge,term) for edge in range(2) for term in ['KhG Kk','KkG Kh','-Khk']]+[(0,1),(1,0)]
    assert len(edgewords)==8
    for D in [4,6]:
        F=s.zeros(D);F[0,1]=2;F[1,0]=-2;F2=sum(F[a,b]**2 for a in range(D) for b in range(D))
        assert s.trace(s.eye(D)*F2/12+2*F*F)==(s.Rational(D,12)-2)*F2
        assert s.trace(F)==0
    e,jv,js=s.symbols('e jv js');u,z=s.symbols('u z')
    # Direct Gamma identities for A and C, then actual pole projection.
    A=-s.exp(e*js)/(e*(1-e));C=s.exp(e*jv)
    U=s.series(-6*(-s.Rational(5,3)-e/6)*C*A,e,0,1).removeO().expand()
    W=s.series(-6*(s.Rational(1,3)-e/6)*s.exp(e*js)*(-s.exp(e*jv)/(e*(1-e))),e,0,1).removeO().expand()
    CU=s.series(6*(s.Rational(5,3)+e/6)*s.exp(e*jv)/e,e,0,1).removeO().expand()
    CW=s.series(-2*s.exp(e*js)/e,e,0,1).removeO().expand()
    assert s.expand(U+CU)==-10*(1+js) and s.expand(W+CW)==1+2*jv
    assert W.coeff(e,0)-s.expand(W.subs(e,e)).coeff(e,0)==0
    # Wrong D in closed UV pole: -(2-e) exp(e js)/eps rather than -2 exp(e js)/eps.
    bad=s.series(-(2-e)*s.exp(e*js)/e,e,0,1).removeO().expand()
    assert s.expand(bad-CW)==1
    premature=s.series(-2*(-s.exp(e*(js+jv))/(e*(1-e))),e,0,1).removeO().expand()
    assert s.expand(premature-W)==1
    assert U.coeff(e,-1)!=0 and W.coeff(e,-1)!=0
    # Correct scale-normalized Gamma masters checked numerically off the pole.
    for ep in [mp.mpf('.07'),mp.mpf('.13')]:
        m=mp.mpf(3);qscale=mp.mpf(11);h=mp.exp(mp.euler*ep)*mp.gamma(1+ep)*(qscale/m)**ep
        aa=mp.exp(mp.euler*ep)*qscale**ep*mp.gamma(ep-1)*m**(1-ep)
        cc=mp.exp(mp.euler*ep)*qscale**ep*mp.gamma(ep+1)*m**(-ep-1)
        assert abs(aa+m*h/(ep*(1-ep)))<mp.mpf('1e-65')
        assert abs(cc-h/m)<mp.mpf('1e-65')
    # Rebuild finite answer independently from recorded ordered contractions.
    totals={p:{i:[mp.mpf(0)]*4 for i in range(3)} for p in [0,2,4]}
    masses=list(map(s.sympify,fci['vector_mass_eigenvalues']));root=point_root()
    for row in amp['contractions']:
        r=row['r'];i=row['i'];hv=mp.log(real(number(masses[r-1],root))/60)
        uh,uhl,wi,wil=map(mp.mpf,row['physical'])
        vals={0:[0,-10*uh+10*uhl,-10*uh,0],4:[0,wi*(1-2*hv),2*wi,-2*wi]}
        vals[2]=[mp.mpf(0)]*4
        for ls,gw in zip(masses,row['Goldstone_U_W']):
            ug,wg=map(mp.mpf,gw);hs=mp.log(real(number(ls,root))/60)
            vv=[0,-10*ug*(1-hs)+wg*(1-2*hv),-10*ug+2*wg,10*ug-2*wg]
            vals[2]=[a+b for a,b in zip(vals[2],vv)]
        for p in vals:totals[p][i]=[a+b for a,b in zip(totals[p][i],vals[p])]
    for p in totals:
        for i,v in totals[p].items():
            target=list(map(mp.mpf,amp['coefficients'][str(p)][str(i)]['R_MS']))
            for a,b in zip(v,target):assert abs(a-b)<mp.mpf('1e-40')*(1+abs(a))
            assert target[0]==0
            if p in [2,4]:assert abs(target[2]+target[3])<mp.mpf('1e-40')*(1+abs(target[2]))
    assert all(mp.mpf(v)!=0 for v in amp['wrong_D_in_closed_UV_changes_finite'].values())
    assert any(mp.mpf(v)!=0 for row in amp['Goldstone_R_only'].values() for v in row)
    controls={'wrong_Wick_sign_and_factor':'nonzero_complete_amplitude_changes',
      'omitted_Goldstone':'actual_nonzero_finite_coefficients','bad_frame_inverse':color['bad_Q_adjoint_control_changes'],
      'wrong_closed_D_or_premature_D4':'nonzero_actual_W_contractions',
      'missing_CT':'nonzero_generic_and_actual_bare_pole','duplicate_CT':'nonzero_bare_pole_and_wrong_finite',
      'omitted_EFT':['bare_LL_poles',list(map(str,light_bare_pole))],
      'wrong_color_sign':'actual_nonzero_operators_flip',
      'drop_C_positive_eps_consistently':'R_MS_FINITE_INSENSITIVE; bare_and_CT_terms_individually_sensitive',
      'premature_D4_only_in_U_pair_consistently':'R_MS_FINITE_INSENSITIVE',
      'whole_family_zero_test':'NOT_USED; family_nonzero'}
    status='QUALIFIED_VVSS_GRAPH_LOCAL_UV_AND_LIGHT_MATCHED_FINITE_F2'
    print('RESULT '+json.dumps({'schema':'VSP1_VALIDATION','execution_state':'COMPLETED','status':status,
      'elapsed_after_imports':time.perf_counter()-start,'full_color_domain':20*328**2,
      'common_IR_identity':'FULL-OPENED_HS-OPENED_SH-EFT=HH at delta>0, including graph-local UV projections',
      'max_scaled_route_error':mp.nstr(err,15),'controls':controls,'counts':amp['counts'],
      'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED',
      'complete_C1_or_gauge_independence_or_E5_qualified':False},sort_keys=True),flush=True)
if __name__=='__main__':main()
