"""VSP1 complete massive matrix contractions and graph-local UV operations."""
from data import *
def kernels(role):
    e,jv,js=s.symbols('e jv js',real=True)
    if role=='primary':
        Hv=s.exp(e*jv);Hs=s.exp(e*js)
        bareU=s.series(6*(s.Rational(-5,3)-e/6)*Hv*Hs/(e*(1-e)),e,0,1).removeO().expand()
        bareW=s.series(6*(s.Rational(1,3)-e/6)*Hv*Hs/(e*(1-e)),e,0,1).removeO().expand()
        ctU=s.series(-6*(s.Rational(-5,3)-e/6)*Hv/e,e,0,1).removeO().expand()
        ctW=s.series(-2*Hs/e,e,0,1).removeO().expand()
        out={name:[z.coeff(e,-1),z.coeff(e,0)] for name,z in [('bareU',bareU),('bareW',bareW),('ctU',ctU),('ctW',ctW)]}
    else:
        # Direct A_{-1},A_0 and C_0,C_1 convolution, independently of series().
        A={-1:-1,0:-1-js};Cv={0:1,1:jv}
        def convolution(pref,aa,cc):
            return [s.expand(sum(v*a*c for p,v in pref.items() for q,a in aa.items() for r,c in cc.items() if p+q+r==k)) for k in [-1,0]]
        out={'bareU':convolution({0:10,1:1},A,Cv),
             'bareW':convolution({0:-2,1:1},{-1:-1,0:-1-jv},{0:1,1:js}),
             'ctU':convolution({0:-10,1:-1},{-1:-1},Cv),
             'ctW':convolution({0:2},{-1:-1},{0:1,1:js})}
    assert list(map(s.expand,[out['bareU'][0]+out['ctU'][0],out['bareW'][0]+out['ctW'][0]]))==[0,0]
    assert s.expand(out['bareU'][1]+out['ctU'][1])==-10-10*js
    assert s.expand(out['bareW'][1]+out['ctW'][1])==1+2*jv
    return out,jv,js
def functions(H,P,root,role):
    hn=numeric(H,root);pn=numeric(P,root);N=mp.eye(H.rows)-pn;M=hn+60*N
    if role=='primary':
        val,U=mp.eighe(M);assert min(val)>0
        inv=U*mp.diag([1/x for x in val])*U.H
        log=U*mp.diag([mp.log(x/60) for x in val])*U.H
    else:
        ch=mp.cholesky(M);assert max(abs(z) for z in M-ch*ch.H)<mp.mpf('1e-60')*(1+max(abs(z) for z in M))
        inv=M**-1;log=mp.logm(M/60)
    return hn*pn,hn*log*pn,inv*pn,inv*log*pn
def main():
    start=begin('amplitude_preparation.json');role=sys.argv[1];assert role in ['primary','replay'];mp.mp.dps=80
    root=point_root() if role=='primary' else None
    if root is None:
        a,b,c=[mp.mpf(str(s.N(z,100))) for z in QUAD];root=-2*c/(b+mp.sqrt(b*b-4*a*c))
    assert mp.mpf('.00530')<root<mp.mpf('.00531')
    color=packed(HERE/(role+'_color_tables.json.gz'));fci=packed(CAL/'canonical_so10_finite_counterterm_insertion'/f'{role}_v3_tables.json.gz')
    masses=list(map(s.sympify,fci['vector_mass_eigenvalues']));K,jv,js=kernels(role)
    powers=[0,2,4];names=['bare','scalar_UV_CT','vector_UV_CT','R_MS']
    sums={p:{i:{name:[mp.mpf(0)]*4 for name in names} for i in range(3)} for p in powers}
    goldonly={i:[mp.mpf(0)]*4 for i in range(3)};closed_D_error={i:mp.mpf(0) for i in range(3)};rows=[]
    def add(p,i,k,wgt,jvvec,jsvec,isgold=False):
        # axes pole,finite constant,L=log(Q^2/60),Ulog=log(g^2)
        for kn,nm in [('bare'+k,'bare'),('ct'+k,'scalar_UV_CT' if k=='U' else 'vector_UV_CT')]:
            pole,fin=K[kn];v=[mp.mpf(str(pole))*wgt]
            c=mp.mpf(str(fin.subs({jv:0,js:0})));a=mp.mpf(str(fin.coeff(jv)));b=mp.mpf(str(fin.coeff(js)))
            v += [c*wgt+a*jvvec[0]+b*jsvec[0],a*jvvec[1]+b*jsvec[1],a*jvvec[2]+b*jsvec[2]]
            sums[p][i][nm]=[x+y for x,y in zip(sums[p][i][nm],v)]
            sums[p][i]['R_MS']=[x+y for x,y in zip(sums[p][i]['R_MS'],v)]
            if isgold:goldonly[i]=[x+y for x,y in zip(goldonly[i],v)]
    print('STAGE actual35blocks_matrix_functions',flush=True)
    counts={'physical':0,'gauge':0,'soft':0};noncommuting=0
    for ib,b in enumerate(fci['blocks']):
        H,P=dec(b['H']),dec(b['physical']);dim=b['dimension'];tau=[6*z for z in weights(b['label'])]
        for k in counts:counts[k]+=int(red(dim*s.trace(dec(b[k]))))
        Hp,Hlog,Inv,Invlog=functions(H,P,root,role)
        for r,lam in enumerate(masses,1):
            A=dec(color['blocks'][r][ib]);an=numeric(A,root);lv=real(number(lam,root));hv=mp.log(lv/60)
            if tidy(A*H-H*A).todok():noncommuting+=1
            for i in range(3):
                B=dec(color['blocks'][5+3*r+i][ib]);un=dim*numeric(B,root);wn=-real(number(tau[i],root))*an
                uh=real(tr(un*Hp))/lv;uhl=real(tr(un*Hlog))/lv
                wi=lv*real(tr(wn*Inv));wil=lv*real(tr(wn*Invlog))
                jvu=[-hv*uh,uh,-uh];jsu=[-uhl,uh,0]
                jvw=[-hv*wi,wi,-wi];jsw=[-wil,wi,0]
                add(0,i,'U',uh,jvu,jsu);add(4,i,'W',wi,jvw,jsw);closed_D_error[i]+=wi
                gold=[]
                for ls,pg in zip(masses,b['gold_mass_projectors']):
                    pp=numeric(dec(pg),root);ms=real(number(ls,root));hs=mp.log(ms/60)
                    ug=ms*real(tr(un*pp))/lv;wg=lv*real(tr(wn*pp))/ms
                    add(2,i,'U',ug,[-hv*ug,ug,-ug],[-hs*ug,ug,-ug],True)
                    add(2,i,'W',wg,[-hv*wg,wg,-wg],[-hs*wg,wg,-wg],True);closed_D_error[i]+=wg
                    gold.append([fmt(ug),fmt(wg)])
                rows.append({'block':ib,'r':r,'i':i,'physical':[fmt(x) for x in [uh,uhl,wi,wil]],'Goldstone_U_W':gold})
        if ib in [7,17,27,34]:print('STAGE block_'+str(ib),flush=True)
    assert counts=={'physical':290,'gauge':33,'soft':5}
    assert noncommuting>0
    for p in powers:
        for i in range(3):assert abs(sums[p][i]['R_MS'][0])<mp.mpf('1e-60')*(1+sum(abs(x[0]) for x in sums[p][i].values()))
    tab={'schema':'VSP1_AMPLITUDE','axes':['pole','finite_constant','L','Ulog'],
      'coupling_powers':powers,'ideals':['U1','SU2','SU3'],
      'coefficients':{str(p):{str(i):{nm:list(map(fmt,v)) for nm,v in row.items()} for i,row in sums[p].items()} for p in powers},
      'contractions':rows,'counts':counts,'noncommuting_mass_operator_pairs':noncommuting,
      'kernels':{nm:list(map(str,v)) for nm,v in K.items()},
      'Goldstone_R_only':{str(i):list(map(fmt,v)) for i,v in goldonly.items()},
      'wrong_D_in_closed_UV_changes_finite':{str(i):fmt(v) for i,v in closed_D_error.items()},
      'normalization':'Lambda2=-12 Gamma2_F2/(ell^2 g10^2); g^0,g^2,g^4 coefficients; L=log(Qscale^2/60),Ulog=log(g10^2)',
      'finite_C1_qualified':False,'finite_normalizations_adopted':[]}
    save(role,'amplitude',tab,start,{'counts':counts})
if __name__=='__main__':main()
