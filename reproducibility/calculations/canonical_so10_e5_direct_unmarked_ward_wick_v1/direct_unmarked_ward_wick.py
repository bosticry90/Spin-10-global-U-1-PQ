"""Exact phase, anisotropic subtraction, and literal Ward operand controls."""
import json
import sys

import sympy as sp

from execute import ROOT, run_worker

CALC=ROOT/"calculations"


def result(owner):
    p=CALC/("canonical_so10_"+owner)/"result.json"
    return json.loads(p.read_bytes())["checks"]


def bound_operands(phase):
    chart=result("connected_master_source_chart_v1")
    pairs=chart["phase_pairs"]
    assert [i for i,*_ in pairs]==list(range(643))
    counts=[]
    for sign in (1,-1):
        selected=[row for row in pairs if row[-1]==sign]
        counts.append(len(selected))
        for _,l,r,s in selected:
            if phase=="native":
                assert sp.I**(l+r)==-s
            else:
                assert (l+r-(2 if s==1 else 0))%4==0
                jphase=-sp.I**(-l)
                assert sp.expand(s*jphase*sp.I**(-r))==1
    assert counts==[553,90]
    a=result("uncut_connected_ward_v1")["actual_drivers"]
    assert a["own_coordinate_derivative_rows"]==0
    e=result("uncut_connected_geometric_v3")
    rows=[e["field"]["ordinary_affine_rows"],e["field"]["ordinary_homogeneous_rows"],
          e["action"]["J_free_g3_rows"]]
    assert rows==[48,7800,48960]
    assert e["action"]["whole_source_grade_counts"]=={"g0":48,"g1":1152,"g2":11264,"g3":48960}
    assert e["reference"]["Phi12_shape_slope_times_mass_squared"]=="-1/30"
    assert e["reference"]["reference_omission_detected"]
    return counts,rows


def cutoff(phase):
    D,s,t=sp.symbols("D s t",positive=True)
    tau,jet,alpha,delta,k=sp.symbols("tau jet alpha delta k")
    if phase=="native":
        moment=1/D
    else:
        half=sp.Rational(1,2)
        moment=sp.gammasimp(sp.gamma(3*half)*sp.gamma(D*half)/
                            (sp.gamma(half)*sp.gamma((D+2)*half)))
    density=s/(1+(s*s-1)*t)**2
    d=density.diff(s).subs(s,1).subs(t,moment)
    log=(sp.log(1+(s*s-1)*t)/2).diff(s).subs(s,1).subs(t,moment)
    assert sp.simplify(d.diff(D).subs(D,4)-log.subs(D,4))==0
    assert log.subs(D,4)==sp.Rational(1,4)
    old=tau-jet+k*alpha/2
    new=(tau-delta)-(jet-delta)+k*alpha/2
    assert sp.expand(old-new)==0
    assert sp.expand((tau-delta)-jet+k*alpha/2-old)==-delta
    return "1/4"


def normals(phase):
    t,u,m,q,r=sp.symbols("t u m q r")
    hard=u*t-(1-t)
    assert hard.diff(t)==u+1 and hard.subs({t:sp.Rational(1,2),u:1})==0
    v=sp.Matrix([1,1,0,0])
    tip=sp.zeros(4,1)
    E=sp.diag(1,-1,-1,-1)
    direction=E*v
    polynomial=lambda a:(a.T*E*a)[0]-m
    assert polynomial(v+q*direction).diff(q).subs(q,0)==4
    assert polynomial(tip+r*tip).diff(r)==0
    return True


def check(phase):
    phases,rows=bound_operands(phase)
    return {"fixed_chart_phase_products":phases,
            "even_affine_and_source_rows":rows,
            "normalized_ellipsoid_mixed_derivative":cutoff(phase),
            "first_dimension_jet_matches_anisotropic_finite_part":True,
            "common_shell_metric_and_reference_controls":normals(phase)}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
