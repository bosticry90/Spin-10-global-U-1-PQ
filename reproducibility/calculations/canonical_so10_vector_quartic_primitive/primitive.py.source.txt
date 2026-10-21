"""Actual VVVV color contractions and entire auxiliary-IR bare amplitude."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
PAIRS=list(combinations(range(10),2));d=s.Symbol('d',positive=True)
z,ld,zz=s.symbols('z ld zeta2',real=True);hs=s.symbols('h1:5',real=True)
ks=[d,s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)];ls=[ld,*hs]
eps=s.Symbol('eps',real=True)
@lru_cache(None)
def clean(v):return s.cancel(s.expand(v))
def tidy(M):return s.SparseMatrix(M).applyfunc(clean)
def zero(M):assert not tidy(M).todok()
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def matrix(x):return s.SparseMatrix(*x['shape'],{(i,j):s.sympify(v) for i,j,v in x['entries']})
def enc(M):return [[str(clean(M[i,j])) for j in range(M.cols)] for i in range(M.rows)]

def tensors(role):
    p=packed(CAL/'canonical_so10_width_hard_projection'/f'{role}_tables.json.gz');P=list(map(matrix,p['projectors']))
    data=packed(CAL/'canonical_so10_background_threshold_inputs'/f'{role}_tables.json.gz')
    supplied={(a,b,e):s.sympify(v) for a,b,e,v in data['f']}
    if role=='primary':f=supplied
    else:
        hh=[s.SparseMatrix(10,10,{(i,j):1/s.sqrt(2),(j,i):-1/s.sqrt(2)}) for i,j in PAIRS];f={}
        for a in range(45):
            for b in range(45):
                C=hh[a]*hh[b]-hh[b]*hh[a]
                for (i,j),v in C.todok().items():
                    if i<j:f[a,b,PAIRS.index((i,j))]=clean(s.sqrt(2)*v)
        assert f==supplied
    Fe=[s.SparseMatrix(45,45,{(a,b):v for (a,b,k),v in f.items() if k==e}) for e in range(45)]
    ad=[s.SparseMatrix(45,45,{(out,b):v for (h,b,out),v in f.items() if h==a}) for a in range(45)]
    cart=[ad[PAIRS.index((2*j,2*j+1))] for j in range(5)]
    T=[tidy(sum((v*A for v,A in zip([-2,-2,-2,3,3],cart)),s.zeros(45))/s.sqrt(30)),
       tidy((cart[3]-cart[4])/s.sqrt(2)),tidy((cart[0]-cart[1])/s.sqrt(2))]
    expected=[[0,s.Rational(14,5),0,5,s.Rational(1,5)],[2,0,0,3,3],[3,1,0,2,2]]
    G=matrix(data['Gram'])
    planevecs=[[-2/s.sqrt(30)]*3+[3/s.sqrt(30)]*2,[0,0,0,1/s.sqrt(2),-1/s.sqrt(2)],
               [1/s.sqrt(2),-1/s.sqrt(2),0,0,0]]
    for idx,(h,coeff) in enumerate(zip(T,planevecs)):
        a=s.SparseMatrix(45,1,{(PAIRS.index((2*j,2*j+1)),0):v for j,v in enumerate(coeff) if v})
        zero(G*a);assert clean((a.T*a)[0])==1
        zero(h+h.T)
        for r,Q in enumerate(P):zero(Q*h-h*Q);assert clean(-s.trace(Q*h*h))==expected[idx][r]
    assert len(data['background_words']['VVVV'])==8
    # Fuse the second copy of f once for the entry-contraction route.
    K={}
    if role=='replay':
        for F in Fe:
            for (a,b),u in F.todok().items():
                for (c,e),v in F.todok().items():K[a,b,c,e]=K.get((a,b,c,e),0)+u*v
        K={key:clean(v) for key,v in K.items() if clean(v)}
    output=[]
    for group,h in enumerate(T):
        print('STAGE color_'+role+'_'+str(group),flush=True)
        S=[tidy(Q*h*h) for Q in P];U=[tidy(Q*h) for Q in P]
        X=s.zeros(5);L=s.zeros(5);Y=s.zeros(5)
        if role=='primary':
            for F in Fe:
                dots=[sum((v*U[r][a,b] for (a,b),v in F.todok().items()),s.Integer(0)) for r in range(5)]
                for r in range(5):
                    for t in range(5):
                        X[r,t]-=s.trace(S[r]*F*P[t]*F)
                        L[r,t]+=dots[r]*dots[t]
                        Y[r,t]-=s.trace(F*U[t]*F*U[r])
        else:
            pd=[Q.todok() for Q in P];sd=[Q.todok() for Q in S];ud=[Q.todok() for Q in U]
            for (a,b,c,e),value in K.items():
                for r in range(5):
                    for t in range(5):
                        X[r,t]+=value*sd[r].get((a,c),0)*pd[t].get((b,e),0)
                        L[r,t]+=value*ud[r].get((a,b),0)*ud[t].get((c,e),0)
                        Y[r,t]+=value*ud[r].get((a,e),0)*ud[t].get((b,c),0)
        X,L,Y=map(tidy,[X,L,Y]);zero(L-L.T);zero(Y-Y.T)
        assert clean(sum(X))==-64 and clean(sum(L))==64 and clean(sum(Y))==-32
        output.append({'group':['U1','SU2','SU3'][group],'indices':list(map(str,expected[group])),
                       'X':enc(X),'L':enc(L),'Y':enc(Y),'Z':enc(tidy(L-Y))})
    return output,data['background_words']['VVVV']

def lorentz(role):
    D=s.Symbol('D');
    if role=='primary':return clean(-6*(D-1)*(D/s.Integer(12)-2)).subs(D,4-2*eps)
    values=[]
    for N in [4,6,8]:
        F=s.zeros(N);F[0,1]=1;F[1,0]=-1;F2=2
        C=s.eye(N)*s.Rational(F2,12)+2*F*F
        p2=2*sum(C[i,i] for i in range(N))*N
        p3=-2*sum(C[i,j]*int(i==j) for i in range(N) for j in range(N))
        bb1=4*sum(F[i,j]*F[i,j] for i in range(N) for j in range(N))/F2
        bb3=4*sum(F[i,j]*F[j,i] for i in range(N) for j in range(N))/F2
        assert bb1==4 and bb3==-4
        values.append((N,clean(-12*s.Rational(1,4)*(p2+p3)/F2)))
    # At most two independent Lorentz index traces: polynomial degree<=2.
    return s.expand(s.interpolate(values,D).subs(D,4-2*eps))

def amplitudes(rows,role):
    kappa=s.expand(lorentz(role));assert kappa==30-17*eps-2*eps**2
    result=[]
    for row in rows:
        X=s.Matrix([[s.sympify(v) for v in r] for r in row['X']]);Z=s.Matrix([[s.sympify(v) for v in r] for r in row['Z']])
        p2=p1=f0=0
        for r in range(5):
            for t in range(5):
                j=z-ls[r];jt=z-ls[t];ratio=ks[t]/ks[r]
                if role=='primary':
                    p2-=12*Z[r,t];p1+=-30*X[r,t]*ratio-12*Z[r,t]*(j+jt)
                    f0+=X[r,t]*ratio*(-13-30*(j+jt))-12*Z[r,t]*((j+jt)**2/2+zz)
                else:
                    # Independent Laurent convolution of the regulated propagators.
                    A={-1:-ks[t],0:-ks[t]*(1+jt)}
                    C={0:1/ks[r],1:j/ks[r]}
                    B={-1:1,0:j,1:j*j/2+zz/2};Bt={-1:1,0:jt,1:jt*jt/2+zz/2}
                    poly={-2:0,-1:0,0:0}
                    for a,u in C.items():
                        for b,v in A.items():
                            for c in [0,1,2]:
                                q=a+b+c
                                if q in poly:poly[q]+=X[r,t]*u*v*kappa.coeff(eps,c)
                    for a,u in B.items():
                        for b,v in Bt.items():
                            if a+b in poly:poly[a+b]-=12*Z[r,t]*u*v
                    p2+=poly[-2];p1+=poly[-1];f0+=poly[0]
        pol={str(k):s.expand(v) for k,v in [(-2,p2),(-1,p1),(0,f0)]}
        assert pol['-2']==-1152
        ir={}
        for power,value in pol.items():
            parts={str(k):s.expand(value).coeff(d,k) for k in [-1,0,1]}
            assert s.expand(value-sum(d**k*parts[str(k)] for k in [-1,0,1]))==0
            ir[power]={'inverse_d':str(parts['-1']),
              'log_d_at_d0':str(s.expand(parts['0']-parts['0'].subs(ld,0))),
              'regular_d0':str(parts['0'].subs(ld,0)),
              'vanishing_d_times_log_polynomial':str(parts['1'])}
        result.append({'group':row['group'],'Laurent':{k:str(v) for k,v in pol.items()},'IR_decomposition':ir})
    return result

def controls(rows,amps):
    # Absolute external normalization fixed by the one-loop determinant heat factors.
    D=4-2*eps;tau=s.Symbol('tau')
    assert clean(-12*tau/24+tau/2)==0
    assert clean(-12*tau*(D/24-1)-tau*(10+eps))==0
    assert clean(-12*(-tau/12)-tau)==0
    # Omitting O(eps) in B*B loses a nonzero universal finite zeta2 term.
    zeta_term=[s.expand(s.sympify(a['Laurent']['0'],locals={'d':d,'z':z,'ld':ld,'zeta2':zz,**{str(x):x for x in hs}})).coeff(zz) for a in amps]
    assert zeta_term==[-1152]*3
    # D4 instead of the dimensional multiplier changes finite AC by17 sumX*ratio.
    ev=[]
    for row in rows:
        X=s.Matrix([[s.sympify(v) for v in r] for r in row['X']])
        err=s.expand(17*sum(X[r,t]*ks[t]/ks[r] for r in range(5) for t in range(5)))
        assert err!=0;ev.append(str(err))
    return {'external_g2_stripping_checked_against_three_one_loop_kernels':True,
      'missing_B_epsilon_zeta2_term':list(map(str,zeta_term)),
      'D4_vs_dimensional_finite_AC_difference':ev,
      'global_T_or_gyromagnetic_sign':'INSENSITIVE_EVEN_BACKGROUND_ORDER',
      'renormalized_or_matched_F2_claimed':False}

def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=time.perf_counter()
    timer=threading.Timer(180,lambda:os._exit(124));timer.start()
    rows,words=tensors(role);amp=amplitudes(rows,role);c=controls(rows,amp)
    payload={'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_TABLES_V1','color':rows,'amplitudes':amp,
      'background_words':words,'log_dictionary':{'ld':'log(d)','h1':'log(1/200)','h2':'log(1/40)',
      'h3':'log(5/12)','h4':'log(253/600)','zeta2':'pi**2/6','z':'log(Q**2/60)-log(g10**2)'},
      'normalization':'Lambda2=-12 Gamma2_Fphys2/(ell**2*g10**2); output Lambda2/g10**2',
      'positive_aux_IR_mass':'delta=60*g10**2*d; d>0; background_derivatives_first',
      'UV_subdivergences_subtracted':False,'IR_limit_or_scheme_adopted':False,'controls':c}
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as out:out.write(compressed)
    result={'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_NATIVE_V1','execution_state':'COMPLETED','route':role,
      'color_coefficients':225,'all_ordered_mass_pairs':25,'background_words':len(words),
      'table_bytes':len(raw),'packed_bytes':len(compressed),'tables_sha256':sha256(raw).hexdigest(),
      'packed_sha256':sha256(compressed).hexdigest(),'double_poles':[-1152]*3,
      'full_C1_or_finite_hard_family_qualified':False,'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
