"""Check the actual linked retained/ordinary two-port and finite conversion."""
from collections import defaultdict
import gzip
import json
import sys

import sympy as sp

from execute import ROOT, run_worker

CALC=ROOT/"calculations"



def joined_kernels(rows):
    xi,eta=sp.symbols("xi eta_H")
    def coef(cells):
        return sp.expand(sum(sp.Rational(n,d)*xi**a*eta**b*(sp.I if m&16 else 1)
                  *sp.sqrt(sp.prod(x for k,x in enumerate((2,3,5,7)) if m&(1<<k)))
                  for (a,b,m),n,d in cells))
    L,A,B,V,U=(defaultdict(int) for _ in range(5))
    Q=sp.S.Zero
    for grade,word,cells in rows:
        ids=[i for i,_ in word]
        if grade==0 and len(ids)==3 and 508<=ids[0]<553<=ids[1]<598<=ids[2]<643:
            L[ids[0]-508,ids[2]-598,ids[1]-553]-=coef(cells)
        if grade!=1:
            continue
        if len(ids)==3 and 0<=ids[0]<180 and ids[0]%4==0 and 553<=ids[1]<598<=ids[2]<643:
            slot,=[i for i,(_,jets) in enumerate(word) if jets]
            key=ids[0]//4,ids[2]-598,ids[1]-553
            z=coef(cells)
            # Move the derivative on a to the other two slots.
            if slot==0:
                A[key]-=z
            if slot==1:
                B[key]-=z
            if slot==2:
                A[key]+=z
                B[key]+=z
        if len(ids)==3 and 0<=ids[0]<180 and ids[0]%4==0 and 553<=ids[1]<598 and ids[2]==691:
            V[ids[0]//4,ids[1]-553]-=coef(cells)
        if len(ids)==3 and 553<=ids[0]<598<=ids[1]<643 and ids[2]==1253:
            U[ids[1]-598,ids[0]-553]-=coef(cells)
        if len(ids)==4 and 553<=ids[0]<=ids[1]<598<=ids[2]<=ids[3]<643:
            for i in (0,1):
                for j in (2,3):
                    if ids[i]-553==ids[j]-598 and ids[1-i]==565 and ids[5-j]==610:
                        Q+=(-1)**(j-i-1)*coef(cells)
    T=sp.expand(sum(v*L[b,c,12] for (b,c),v in V.items()))
    H=sp.expand(sum((A[12,a,c]-B[12,a,c]/2)*L[12,c,a]
                    for a in range(45) for c in range(45)))
    J=sp.expand(sum(v*L[12,c,a] for (a,c),v in U.items()))
    def prod(M,N):
        return sum(M[b,12,c]*N[b,c,12] for b in range(45) for c in range(45))
    X=sp.expand(sp.I*(prod(B,L)-prod(L,A)-prod(A,L)))
    Y=sp.expand(sp.I*(prod(L,B)-prod(B,L)))
    assert sp.expand(Q)==-8*xi and X==8*xi and Y==J==0
    return [sp.expand(Q),T,H]


def literal(phase):
    result=CALC/"canonical_so10_mixed_Ward_positive_coupling"/"kernel_result.json"
    data=json.loads(result.read_bytes())
    non=data["nonzero"]
    assert [non[k] for k in ("Q","X","Y","T_JaLambda")]==[57,57,0,0]
    witnesses=data["witnesses"]
    values=[]
    for key in ("Q","T_JB_C","H_BL"):
        row=witnesses[key]
        assert row[:2]==[12,12]
        values.append(sp.sympify(row[2]))
    Q,T,H=values
    assert T==sp.I*Q and H==-T/2 and Q!=0

    path=CALC/"canonical_so10_unprobed_compact_all_coupling_v1"/f"{phase}_full_current.json.gz"
    with gzip.open(path,"rt",encoding="utf-8") as f:
        current=json.load(f)["current"]["complete_S_GF_source"]
    expected={
        ((48,(0,)),(520,())):[[[0,0,16],1,1]],
        ((520,()),(1253,())):[[[0,0,16],-1,1]],
        ((565,(0,)),(691,())):[[[0,0,0],-1,1]],
    }
    found={}
    for g,w,cells in current:
        key=tuple((i,tuple(d)) for i,d in w)
        if g==0 and key in expected:
            assert key not in found
            found[key]=cells
    assert found==expected
    g=sp.Symbol('g10')
    assert [g*v for v in joined_kernels(current)]==values
    return Q,T,H


def normalized(phase,T,H):
    p,z,b,mu=sp.symbols("p z b mu",positive=True)
    u,D=sp.symbols("u D",positive=True)
    k,delta=sp.symbols("kappa delta")
    alpha=2*b
    dimension_jet=-b*(sp.log(4*sp.pi)+1-sp.EulerGamma)
    if phase=="native":
        tau=b*sp.integrate(1-u/z,(u,0,z))
        jet=sp.diff(2*b*z*(1-4/D),D).subs(D,4)
    else:
        tau=b*z/2
        jet=2*b*z*4/16
    assert tau==jet==b*z/2
    tau_b=b*(1+sp.log(mu**2/z))
    scalar=sp.expand(tau_b-dimension_jet+(k-1-sp.log(16*sp.pi))*alpha/2)
    target=b*(1+sp.log(mu**2/z)+k-sp.EulerGamma-2*sp.log(2))
    assert sp.simplify(scalar-target)==0
    F_J=p*T*scalar/2
    F_L=sp.I*p*H*scalar
    if phase=="native":
        total=(-p)*F_J+(sp.I*p)*F_L
        assert sp.expand(total)==0
        assert F_J!=0 and F_L!=0
    else:
        # Fourier G_LambdaB(-p) and G_BLambda(p) each equal -p/z.
        phi_l=p/z
        phi_b=-sp.I*p/z
        rooted_jb=F_J/z
        rooted_ja=sp.simplify((phi_l*F_L*phi_b).subs(z,p*p))
        assert sp.simplify(rooted_ja+rooted_jb.subs(z,p*p))==0
        tree_J=sp.I*p/z
        tree_a=phi_b
        assert tree_J!=0 and tree_J+tree_a==0
    wrong=sp.expand(-p*(p*T*(scalar+b*delta)/2)+sp.I*p*F_L)
    assert wrong==-b*delta*p*p*T/2 and wrong!=0
    return True


def check(phase):
    Q,T,H=literal(phase)
    assert normalized(phase,T,H)
    return {"literal_nonzero_witness":[str(s) for s in (Q,T,H)],
            "signed_proper_and_connected_pair":True,
            "zero_shifted_massless_power_after_dimension_jet":True,
            "unmatched_finite_polynomial_is_visible":True}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
