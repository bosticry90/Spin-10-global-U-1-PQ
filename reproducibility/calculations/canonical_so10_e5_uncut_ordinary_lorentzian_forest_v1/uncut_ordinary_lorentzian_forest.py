"""Check sensitive incidence, literal derivative, and forced-root controls."""
import gzip
from itertools import combinations, product
import json
import sys

import sympy as sp

from execute import ROOT, run_worker

CALC=ROOT/"calculations"


def rank(rows,phase):
    matrix=sp.Matrix(rows)
    if phase=="native":
        return matrix.rank()
    for n in range(min(matrix.shape),0,-1):
        for rr in combinations(range(matrix.rows),n):
            for cc in combinations(range(matrix.cols),n):
                if matrix.extract(rr,cc).det():
                    return n
    return 0


def margins(forms,phase):
    out={}
    for n in range(1,len(forms)+1):
        for ids in combinations(range(len(forms)),n):
            out[ids]=4*rank([forms[k] for k in ids],phase)
    return out


def graph(phase):
    forms=((1,0,0),(0,1,0),(0,0,1),(1,-1,0),(0,1,-1),(-1,0,1))
    raw=margins(forms,phase)
    ports=((0,1,3),(1,2,4),(2,0,5))
    assert raw[tuple(range(6))]-12==0
    count=0
    for selected in product(*ports):
        weight=[2-selected.count(k) for k in range(6)]
        assert all(r>sum(weight[k] for k in subset) for subset,r in raw.items())
        count+=1
    # Two trivalent trees joined through the two-port, before and after fusion.
    fused=((1,0,0),(0,1,0),(0,0,1),(-1,-1,-1),(1,1,0))
    before=margins(fused+((1,1,0),),phase)
    after=margins(fused,phase)
    m0=min(v-2*len(k) for k,v in before.items())
    m1=min(v-2*len(k) for k,v in after.items())
    assert (m0,m1)==(0,2)
    # A signed edge weight is permitted in the same prefix criterion.
    signed=[2,2,2,2,-1]
    assert all(v>sum(signed[k] for k in ids) for ids,v in after.items())
    return [count,len(raw),raw[tuple(range(6))]-12],[m0,m1]


def literal(phase):
    folder=CALC/"canonical_so10_physical_current_input_recovery_g1_v1"
    name="native_v2_action.json.gz" if phase=="native" else "replay_v4_action.json.gz"
    with gzip.open(folder/name,"rt",encoding="utf-8") as f:
        rows=json.load(f)["S1_gauge"]
    match=[c for w,c in rows if w==[[0,[]],[4,[1]],[9,[]]]]
    assert match==[[[[1,0,0,5],1,4]]]
    return str(sp.sqrt(10)/4)


def root(phase):
    p,M,V,e=sp.symbols("P M V epsilon",nonzero=True)
    expr=V*p/((p+sp.I*e)*(p-M+sp.I*e))
    assert expr.subs(p,0)==0
    assert sp.simplify(expr.subs(e,0)).subs(p,0)==-V/M
    a,b,c=sp.symbols("a b c")
    R=sp.Matrix([[0,a,b],[-a,0,c],[-b,-c,0]])
    v=sp.Matrix(sp.symbols("x:3"))
    if phase=="native":
        assert sp.expand(v.dot(R*v))==0
    else:
        assert (R+R.T)==sp.zeros(3)
        assert sp.expand((v.T*R*v)[0]+(v.T*R.T.T*v)[0])==0
    assert sp.expand((sp.Matrix([1,0,0]).T*R*v)[0])!=0
    return True


def gaps():
    n=sp.symbols("n0:6")
    w=sp.symbols("w0:6")
    r=sp.symbols("r0:6")
    greedy=sum(n[j]*(w[j]-2*(r[j]-(r[j-1] if j else 0))) for j in range(6))
    gaps=sum((n[j]-(n[j+1] if j<5 else 0))*(sum(w[:j+1])-2*r[j]) for j in range(6))
    assert sp.expand(greedy-gaps)==0
    return True


def check(phase):
    triangle,tree=graph(phase)
    return {"literal_cubic_pivot":literal(phase),
            "cut_triangle_signed_assignments":triangle,
            "tied_tree_margin_before_and_after":tree,
            "radial_and_forced_point_controls":root(phase),
            "weighted_gap_identity":gaps()}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
