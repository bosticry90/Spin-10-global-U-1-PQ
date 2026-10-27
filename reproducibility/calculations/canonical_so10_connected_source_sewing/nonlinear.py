"""Exact nonlinear finite examples, with a direct connected Wick/log-Z route."""
from fractions import Fraction as F
from math import factorial
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'canonical_so10_nonminimal_source_products'))
import finite_algebra_v2 as A

def dfact(n):
    out=1
    for j in range(1,n+1,2):out*=j
    return out

def wick_log(vertices,k,m=None):
    # Keys: external amplitude mask, exterior mask, boson power,
    # explicit hbar power, number of ordinary cubic z vertices.
    def plus(P,Q):
        out=dict(P)
        for key,v in Q.items():out[key]=out.get(key,F(0))+v
        return {key:v for key,v in out.items() if v}
    def product(P,Q):
        out={}
        for (a,e,z,h,c),v in P.items():
            for (b,f,w,j,d),x in Q.items():
                if a&b or e&f or c+d>2:continue
                inversions=sum((f&((1<<i)-1)).bit_count() for i in range(4) if e&(1<<i))
                key=(a|b,e|f,z+w,h+j,c+d)
                out[key]=out.get(key,F(0))+(-1)**inversions*v*x
        return {key:v for key,v in out.items() if v}
    one={(0,0,0,0,0):F(1)};term=one;Z={}
    V={}
    for a,e,z,c,value in vertices:
        key=(a,e,z,-1,c);V[key]=V.get(key,F(0))-value
    # Exponential is finite in the selected amplitudes and cubic count.
    for n in range(6):
        for (a,e,z,h,c),v in term.items():
            if z%2 or (e&12) not in (0,12):continue
            hp=h+z//2;value=v*F(dfact(z-1),1)/k**(z//2)
            if e&12:
                assert m is not None
                hp+=1;value*=-1/m
            key=(a,e&3,0,hp,c);Z[key]=Z.get(key,F(0))+value
        term={key:v/F(n+1) for key,v in product(term,V).items()}
    assert not term,'Exponential truncation not exact in selected cubic/source domain'
    X=plus(Z,{(0,0,0,0,0):F(-1)});term=one;log={}
    for n in range(1,6):
        term=product(term,X)
        log=plus(log,{key:v*F((-1)**(n+1),n) for key,v in term.items()})
    assert not product(term,X),'Log truncation not exact in selected domain'
    exterior=3 if m is not None else 0
    # W=hbar log Z; its one-loop coefficient is hbar^0 in log Z.
    return sum(v for (a,e,z,h,c),v in log.items() if a==7 and e==exterior and h==0)

def inv(P,k):
    x=A.add(A.scale(P,1/k),A.atom(-1));term=A.atom();out={}
    for n in range(4):
        out=A.add(out,A.scale(term,F((-1)**n,1)/k));term=A.mul(term,x)
    assert not term
    return out

def value(P,mask=7,exterior=0):return P.get((mask,exterior,0),F(0))

def bosonic(seed):
    k,g,r1,r2,t1,t2,p,c=map(F,[seed+2,seed+1,seed+2,seed+3,seed+5,seed+7,seed+2,seed+3])
    v1,v2,w1,w2=map(F,[1,2,3,4])
    K=A.add(A.atom(k),A.atom(p,a=1));Ki=inv(K,k)
    R1=A.add(A.atom(r1),A.atom(v1,a=1));R2=A.add(A.atom(r2),A.atom(v2,a=1))
    T1=A.add(A.atom(t1),A.atom(w1,a=1));T2=A.add(A.atom(t2),A.atom(w2,a=1))
    pr=lambda *pp: __import__('functools').reduce(A.mul,pp,A.atom())
    yi=A.scale(pr(R1,Ki),-1);yj=A.scale(pr(R2,Ki),-1)
    yij=A.add(A.scale(pr(A.atom(c,a=1),Ki),-1),pr(A.add(pr(T1,R2),pr(T2,R1)),Ki,Ki),A.scale(pr(R1,R2,Ki,Ki,Ki),-g))
    terms=[A.scale(pr(T1,T2,Ki,Ki),F(1,2)),
      A.scale(pr(T1,Ki,Ki,yj),g/2),A.scale(pr(T2,Ki,Ki,yi),g/2),
      A.scale(pr(Ki,Ki,yi,yj),g*g/2),A.scale(pr(Ki,yij),-g/2)]
    chain=sum(value(x,1) for x in terms)
    # A separate implicit stationarity solve, in full three-direction algebra.
    H=A.add(K,A.atom(t1,a=2),A.atom(t2,a=4),A.atom(w1,a=3),A.atom(w2,a=5))
    B=A.add(A.atom(r1,a=2),A.atom(r2,a=4),A.atom(v1,a=3),A.atom(v2,a=5),A.atom(c,a=7))
    phi={}
    for step in range(4):phi=A.scale(pr(inv(H,k),A.add(B,A.scale(pr(phi,phi),g/2))),-1)
    assert not A.add(pr(H,phi),A.scale(pr(phi,phi),g/2),B)
    shifted=A.add(H,A.scale(phi,g));legendre=-value(A.scale(A.log_scalar(shifted,k),F(1,2)))
    vertices=[(0,0,3,1,g/6),(1,0,2,0,p/2),(2,0,1,0,r1),(4,0,1,0,r2),
      (2,0,2,0,t1/2),(4,0,2,0,t2/2),(3,0,1,0,v1),(5,0,1,0,v2),
      (3,0,2,0,w1/2),(5,0,2,0,w2/2),(7,0,1,0,c)]
    direct=wick_log(vertices,k)
    assert chain==legendre==direct,('NONLINEAR_BOSON_MISMATCH',seed,chain,legendre,direct)
    omissions=[value(x,1)!=0 for x in terms];assert all(omissions)
    contact_control=g*c/(2*k*k);assert contact_control
    return {'seed':seed,'W1_uab':str(direct),'five_terms_u':[str(value(x,1)) for x in terms],
      'all_omissions_sensitive':omissions,'source_pair_mean_contact':str(contact_control)}

def odd(seed):
    k,m,g,Y,p,q,c,r,t=map(F,[seed+2,seed+3,seed+1,seed+4,seed+2,seed+1,seed+3,1,2])
    # Original action, with theta1,theta2,f0,f1 in that exterior order.
    vertices=[(0,0,3,1,g/6),(0,12,1,0,Y),(1,0,2,0,p/2),(1,12,0,0,q),
      (2,5,0,0,F(1)),(4,10,0,0,F(1)),(3,5,0,0,r),(5,10,0,0,t),(7,3,1,0,c)]
    direct=wick_log(vertices,k,m)
    # Independent integrate-fermions-first expansion: Z(z) contains
    # M(z)+ab theta1 theta2(1+u(r+t))/hbar, then a scalar cubic Wick average.
    predicted=g*Y/(2*k*k*m*m)*(r+t-2*p/k-2*q/m)+c/k*(g/(2*k)-Y/m)
    assert direct==predicted,('ODD_CONNECTED_SIGN_OR_TADPOLE_MISMATCH',seed,direct,predicted)
    # Quadratic fluctuation Schur complement evaluated at the classical mean.
    K=A.add(A.atom(k),A.atom(p,a=1));M=A.add(A.atom(m),A.atom(q,a=1))
    Ki=inv(K,k);Mi=inv(M,m)
    pr=lambda *pp: __import__('functools').reduce(A.mul,pp,A.atom())
    f01=pr(A.atom(a=6,g=3),A.add(A.atom(),A.atom(r+t,a=1)),Mi,Mi)
    z=A.scale(pr(Ki,A.add(A.scale(f01,Y),A.atom(c,a=7,g=3))),-1)
    KP=A.add(K,A.scale(z,g));MP=A.add(M,A.scale(z,Y))
    gamma=A.add(A.scale(A.log_scalar(KP,k),F(1,2)),A.scale(A.log_scalar(MP,m),-1),
      A.scale(pr(f01,inv(KP,k),inv(MP,m)),-Y*Y))
    schur=-value(gamma,7,3);assert schur==direct
    assert c/k*(g/(2*k)-Y/m)!=0
    assert A.mul(A.atom(g=1),A.atom(g=2))==A.scale(A.mul(A.atom(g=2),A.atom(g=1)),-1)
    return {'seed':seed,'W1_uab_theta12':str(direct),'Schur_and_direct_Wick_agree':True,
      'source_pair_mean_contact':str(c/k*(g/(2*k)-Y/m)),'odd_exchange_sensitive':True,
      'proper_source_Hessian_zero_in_this_fixture':True}
