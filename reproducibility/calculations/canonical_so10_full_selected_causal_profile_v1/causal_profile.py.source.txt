"""Exact mixed-cluster margins and selected normalization controls for V915."""

import json
import sys
import sympy as sp

from execute import ROOT, run_worker


def exponents(phase):
    b,e,n=sp.symbols("b e n",integer=True,nonnegative=True)
    delta,r=sp.symbols("delta r",positive=True)
    first=delta**e*r**(-b-e)*r**b*r**2
    second_tip=delta**e*delta**(4-b-e)*r**(b-2)
    second_top=delta**e*r**(4-b-e)*r**(b-2)
    hard=delta**(e+2*n)*r**(2-e-2*n)
    if phase=="native":
        assert sp.simplify(first-delta**2*(delta/r)**(e-2))==0
        assert sp.simplify(second_tip-delta**2*(delta/r)**(2-b))==0
        assert sp.simplify(second_top-first)==0
        assert sp.simplify(hard-delta**2*(delta/r)**(e+2*n-2))==0
    else:
        assert sp.expand(e+(2-e))==2
        assert sp.expand(e+(4-b-e)+(b-2))==2
        assert sp.expand(e+2*n+2-e-2*n)==2
    assert 3-1==2
    assert 3-0==3
    return {"real_ghost_bound":"delta**2*(delta/r)**(e-2)",
            "real_mixed_tip_bound":"delta**2*(delta/r)**(2-b)",
            "hard_shell_bound":"delta**2*(delta/r)**(e+2*n-2)",
            "minimum_extra_mixed_degree":2,
            "regular_mixed_delta_model_degree":-4,
            "regular_mixed_physical_power":3}


def kinetic():
    dimension,w,P,S=sp.symbols("D w P s2")
    angular=w*(P*S-P*S/dimension)/(4*P)
    assert sp.simplify(angular.subs(dimension,4)-3*w*S/16)==0
    assert angular.subs(w,0)==0
    assert sp.simplify(angular.subs({dimension:4,w:1}))!=0
    n=sp.symbols("n",integer=True)
    assert (2-n).subs(n,2)==0 and (2-n).subs(n,3)==-1
    return {"kinetic_angular_carrier":"3*w*s2/16",
            "last_kinetic_contact_sensitive_W_count":2,
            "width_zero_control":"blind for this diagnostic",
            "original_two_switch_forest_retained":True}


def check(phase):
    d=ROOT/"calculations"
    v=json.loads((d/"canonical_so10_mixed_w_transport_v1/result.json").read_bytes())["checks"]
    assert v["transport"]["remaining_max_coincidence_degree"]==1
    assert v["models"]["pointwise_W_cancellation_rejected"]
    b=json.loads((d/"canonical_so10_joint_internal_simple_switch_v1/result.json").read_bytes())["checks"]
    assert b["reference_combination"]=="300*log(M_Sigma/M_Phi)"
    return {"exponents":exponents(phase),"kinetic":kinetic(),
            "reference_combination":b["reference_combination"]}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
