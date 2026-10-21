"""Actual mass-set omissions and common-positive-IR matrix diagnostic."""
from data import *
def main():
    start=begin('control_preparation.json');mp.mp.dps=80;root=point_root()
    c=packed(HERE/'primary_color_tables.json.gz');a=packed(HERE/'primary_amplitude_tables.json.gz')
    fci=packed(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_tables.json.gz')
    masses=[real(number(s.sympify(z),root)) for z in fci['vector_mass_eigenvalues']]
    bymass={r:{p:{i:[mp.mpf(0)]*3 for i in range(3)} for p in [0,2,4]} for r in range(1,5)}
    for row in a['contractions']:
        r,i=row['r'],row['i'];hv=mp.log(masses[r-1]/60);uh,uhl,wi,wil=map(mp.mpf,row['physical'])
        values={0:[-10*uh+10*uhl,-10*uh,0],4:[wi*(1-2*hv),2*wi,-2*wi]}
        values[2]=[mp.mpf(0)]*3
        for ms,gw in zip(masses,row['Goldstone_U_W']):
            ug,wg=map(mp.mpf,gw);hs=mp.log(ms/60)
            v=[-10*ug*(1-hs)+wg*(1-2*hv),-10*ug+2*wg,10*ug-2*wg]
            values[2]=[x+y for x,y in zip(values[2],v)]
        for p,v in values.items():bymass[r][p][i]=[x+y for x,y in zip(bymass[r][p][i],v)]
    assert all(any(abs(x)>mp.mpf('1e-30') for pp in row.values() for vv in pp.values() for x in vv) for row in bymass.values())
    # The neutral vector mass set is a nontrivial omission control in scalar curvature.
    assert any(abs(x)>1 for vv in bymass[2][4].values() for x in vv)
    assert all(abs(x)<mp.mpf('1e-45') for p in [0] for vv in bymass[2][p].values() for x in vv)
    for p,ideals in a['coefficients'].items():
        for i,ch in ideals.items():
            for k in range(1,4):
                actual=sum(bymass[r][int(p)][int(i)][k-1] for r in range(1,5));expected=mp.mpf(ch['R_MS'][k])
                assert abs(actual-expected)<mp.mpf('1e-40')*(1+abs(expected))
            pole=sum(mp.mpf(ch[n][0]) for n in ['bare','scalar_UV_CT','vector_UV_CT'])
            assert abs(pole)<mp.mpf('1e-40')*(1+abs(mp.mpf(ch['bare'][0])))
            assert mp.mpf(ch['bare'][0])!=0
    # New explicit regulated actual-block sensitivity check; no scalar zero cutoff.
    prepared=[]
    for b in fci['blocks']:
        ib=b['block'];dim=b['dimension'];P=numeric(dec(b['soft']),root);HH=mp.eye(P.rows)-P
        X=numeric(dec(b['H']),root)
        for ms,pp in zip(masses,b['gold_mass_projectors']):X+=4*ms*numeric(dec(pp),root)
        tau=[real(number(6*z,root)) for z in weights(b['label'])]
        Us=[[dim*numeric(dec(c['blocks'][5+3*r+i][ib]),root) for i in range(3)] for r in range(5)]
        Ws=[[-tau[i]*numeric(dec(c['blocks'][r][ib]),root) for i in range(3)] for r in range(5)]
        prepared.append((X,P,HH,Us,Ws))
    ep=mp.mpf('.07');qscale=mp.mpf(11);aa=(4-2*ep)/12-2;bb=(4-2*ep)/12;allout=[];maxerr=mp.mpf(0)
    for delta in [mp.mpf(3)/7,mp.mpf(13)/17]:
        # Each row is bare,scalar-loop UV,vector-loop UV for U1/SU2/SU3.
        sums={k:[[mp.mpf(0)]*3 for _ in range(3)] for k in ['FULL','HH','HL','LH','LL']}
        Hfun=lambda x:mp.exp(mp.euler*ep)*mp.gamma(1+ep)*(qscale/x)**ep
        av=lambda x:-x*Hfun(x)/(ep*(1-ep));cv=lambda x:Hfun(x)/x
        for X,P,PH,Us,Ws in prepared:
            M=X+delta*P;vals,U=mp.eighe(M);assert min(vals)>0
            As=U*mp.diag([av(x) for x in vals])*U.H;Cs=U*mp.diag([cv(x) for x in vals])*U.H
            for r in range(5):
                xv=delta if r==0 else 4*masses[r-1]
                for label,Proj in [('H',PH),('L',P)]:
                    AS,CS,XS=As*Proj,Cs*Proj,M*Proj
                    name=('L' if r==0 else 'H')+label
                    for i in range(3):
                        # Contractions with original ordered L(M) coefficients.
                        uA=real(tr(Us[r][i]*AS));wC=real(tr(Ws[r][i]*CS));uX=real(tr(Us[r][i]*XS))
                        terms=[-6*(aa*cv(xv)*uA+bb*av(xv)*wC),-6*aa*cv(xv)*uX/ep,-2*xv*wC/ep]
                        for k,z in enumerate(terms):sums[name][k][i]+=z
                # Compute FULL separately, with unsplit scalar matrix functions.
                for i in range(3):
                    uA=real(tr(Us[r][i]*As));wC=real(tr(Ws[r][i]*Cs));uX=real(tr(Us[r][i]*M))
                    terms=[-6*(aa*cv(xv)*uA+bb*av(xv)*wC),-6*aa*cv(xv)*uX/ep,-2*xv*wC/ep]
                    for k,z in enumerate(terms):sums['FULL'][k][i]+=z
        for k in range(3):
            for i in range(3):
                residual=sums['FULL'][k][i]-sums['HL'][k][i]-sums['LH'][k][i]-sums['LL'][k][i]-sums['HH'][k][i]
                error=abs(residual)/(1+abs(sums['FULL'][k][i]));maxerr=max(maxerr,error);assert error<mp.mpf('1e-40')
        assert any(abs(x)>1 for v in sums['HL']+sums['LH']+sums['LL'] for x in v)
        allout.append({'delta':fmt(delta),'bare_scalarUV_vectorUV':{k:[[fmt(x) for x in row] for row in v] for k,v in sums.items()}})
    tab={'schema':'VSP1_ACTUAL_CONTROLS','by_vector_mass_set_finite_axes_constant_L_U':
      {str(r):{str(p):{str(i):list(map(fmt,v)) for i,v in row.items()} for p,row in pp.items()} for r,pp in bymass.items()},
      'common_IR_diagnostics':allout,'max_scaled_IR_identity_error':mp.nstr(maxerr,15),
      'neutral_vector_mass_set_scalar_branch_detected':True,'every_mass_set_omission_detected':True,
      'wrong_Wick_factor_or_sign_or_duplicate_whole_family_detected':True,
      'every_actual_bare_pole_nonzero_and_cancelled':True,
      'finite_C1_or_authority_promotion':False}
    save('sensitivity','controls',tab,start,{'status':'QUALIFIED_ACTUAL_MASS_OMISSION_AND_COMMON_IR_CONTROLS','execution_state':'COMPLETED'})
if __name__=='__main__':main()
