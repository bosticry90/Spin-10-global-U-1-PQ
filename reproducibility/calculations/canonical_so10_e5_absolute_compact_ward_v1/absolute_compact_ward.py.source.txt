"""Authenticate literal vacuum source support and absolute envelope controls."""
from collections import Counter
import gzip
import json
import sys

import sympy as sp

from execute import ROOT, run_worker

CURRENT = ROOT / "calculations" / "canonical_so10_unprobed_compact_all_coupling_v1"


def census(phase):
    with gzip.open(CURRENT/f"{phase}_full_current.json.gz","rt",encoding="utf-8") as stream:
        current=json.load(stream)["current"]["complete_S_GF_source"]
    ports=Counter()
    ghost=Counter()
    for grade,word,_ in current:
        ids=[i for i,_ in word]
        ordinary=[i for i in ids if i<643]
        sources=[i for i in ids if 643<=i<1286]
        Ja=[i for i in sources if 1241<=i<1286]
        if Ja:
            assert sources==Ja and len(Ja)==1
            assert all(not jets for _,jets in word)
            if grade==0:
                assert ordinary==[Ja[0]-733]
            else:
                assert grade==1 and len(ordinary)==2
                assert 553<=ordinary[0]<565 and 610<=ordinary[1]<643
            ports[grade]+=1
        if not sources and len(ordinary)==2:
            c,a=ordinary
            if 553<=c<598 and 598<=a<643:
                ghost[grade,c<565,a<610]+=1
    assert ports=={0:45,1:334}
    assert ghost=={(0,True,True):48,(0,False,False):132,(1,True,True):288}
    return [ports[0],ports[1]],[ghost[0,True,True],ghost[0,False,False],ghost[1,True,True]]


def exclusion(phase):
    a,b,c,d,u,v=sp.symbols("a b c d u v")
    R=sp.diag(a,b)
    B=sp.diag(c,d)
    N=sp.Matrix([[0,u],[0,0]])
    other=sp.Matrix([[0,0],[v,0]])
    if phase=="native":
        assert N*R*N==sp.zeros(2)
        assert sp.trace(R*N*B)==0
    else:
        s=sp.Symbol("s")
        assert sp.det(R+s*N)==sp.det(R)
        assert sp.det(B+s*N)==sp.det(B)
        assert sp.trace((R*B*N).T)==0
    assert sp.trace(N*other)==u*v
    return True


def envelopes(phase):
    x,j,J,A,M,v,s,e=sp.symbols("x j J A M v s e",nonzero=True)
    P=M*x*x/2+J*x+A*A/2
    F=x*x/2+J*J+A*A
    V=x*x/2+A
    x0=-(J+j)/M
    x1=-x0/M
    w0=(P+j*x).subs(x,x0)
    w1=F.subs(x,x0)
    if phase=="native":
        direct=P+e*F+j*x
        st=-(J+j)/(M+e)
        assert sp.simplify(direct.subs(x,st).diff(e).subs(e,0)-w1)==0
        derivative=(P+s*V+j*x).diff(x)
        y=sp.solve(derivative,x)[0].diff(s).subs(s,0)
    else:
        st=x0+e*x1
        direct=sp.expand((P+e*F+j*x).subs(x,st)).coeff(e)
        assert sp.simplify(direct-w1)==0
        y=-V.diff(x).subs(x,x0)/M
    response=F.diff(x).subs(x,x0)*y
    assert sp.expand(response-V.diff(x).subs(x,x0)*x1)==0
    assert response!=0
    assert sp.simplify(w0.diff(j)-x0)==0
    assert sp.simplify(w1.diff(j)-x1)==0
    assert sp.simplify(w1.diff(J)-(F.diff(J).subs(x,x0)+x1))==0
    assert sp.simplify(w1.diff(A)-2*A)==0
    assert sp.simplify((w1-J*J-A*A).diff(j)-w1.diff(j))==0
    assert sp.expand(w1.diff(J)-(w1-J*J).diff(J))==2*J
    assert sp.expand(w1.diff(A)-(w1-A*A).diff(A))==2*A
    # Even affine external dual: shift v with a nontrivial linear tangent.
    r=v+s*x
    parent=P+e*F
    lhs=(r*parent.diff(x)).subs(x,st)+j*v
    rhs=-s*j*st
    assert sp.series(lhs-rhs,e,0,2).removeO().expand()==0
    return True


def slope(phase):
    u=sp.Symbol("u")
    M=sp.Symbol("M",positive=True)
    if phase=="native":
        value=-sp.integrate(u*(1-u)*(1-2*u)**2,(u,0,1))/M
    else:
        # Independent moments of the symmetric beta density u(1-u).
        moments=[sp.Rational(1,(n+2)*(n+3)) for n in range(3)]
        value=-(moments[0]-4*moments[1]+4*moments[2])/M
    assert value==-1/(30*M)
    return str(value)


def check(phase):
    ports,ghost=census(phase)
    return {"literal_source_ports":ports,"pure_mean_zero_ghost_blocks":ghost,
            "zero_mean_source_cycle_exclusion":exclusion(phase),
            "reference_form_factor_slope":slope(phase),
            "absolute_envelope_controls":envelopes(phase)}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
