"""Verify the complete literal single-mark source reduction and width witness."""
from importlib.util import module_from_spec, spec_from_file_location
import gzip
import json
import sys

import sympy as sp

from execute import ROOT, run_worker

CALC=ROOT/"calculations"
path=CALC/"canonical_so10_uncut_connected_marked_v1"/"connected_marked.py"
spec=spec_from_file_location("paired_marked_owner",path)
owner=module_from_spec(spec)
spec.loader.exec_module(owner)


def actual(phase):
    current=CALC/"canonical_so10_unprobed_compact_all_coupling_v1"
    with gzip.open(current/f"{phase}_full_current.json.gz","rt",encoding="utf-8") as stream:
        rows=json.load(stream)["current"]["complete_S_GF_source"]
    count=0
    cubic_driver=0
    pivot=[]
    for grade,word,cells in rows:
        ids=[i for i,_ in word]
        if not any(1151<=i<1196 for i in ids):
            continue
        if grade==2:
            assert len(ids)==4 and 553<=ids[0]<ids[1]<598<=ids[2]<643
            assert 1163<=ids[3]<1196 and all(not j for _,j in word)
            cubic_driver+=1
            continue
        assert grade==1 and len(ids)==3 and all(not j for _,j in word)
        assert 520<=ids[0]<553 and 553<=ids[1]<565 and 1163<=ids[2]<1196
        count+=1
        if ids[2]==1172 and ids[0]==525:
            pivot.append((ids,cells))
    assert count==334 and cubic_driver==3344
    assert pivot==[([525,553,1172],[[[0,0,5],-1,5]])]
    expected=(
        ("canonical_so10_augmented_metric_lift_v1/tensor_1.json.gz",
         "input_polynomial_Minkowski",[[[0,1,0,0],-1,2]],[[[0,0,0,0],1,1]]),
        ("canonical_so10_cartan_generator_residual_g1_v1/v2_fixed_ward_and_old_affine_endpoints.json.gz",
         "complete_K_epsilon_normal",[[[0,1,0,16],-1,2]],[[[0,0,0,0],-1,1]]),
    )
    for file,key,phase_width,phase_source in expected:
        with gzip.open(CALC/file,"rt",encoding="utf-8") as stream:
            phase_rows=json.load(stream)[key]
        assert [c for w,c in phase_rows if w==[[520,[]],[1286,[]]]]==[phase_width]
        assert [c for w,c in phase_rows if w==[[1253,[]],[1286,[]]]]==[phase_source]
    return [33,count,cubic_driver]


def width(phase):
    g,xi,P,Q,p=sp.symbols("g10 xi P Q p",nonzero=True)
    r=sp.sqrt(10)*g/5
    e=owner.Exterior()
    eta,C,j_a=e.variable("eta",1),e.variable("C",1),e.variable("ja",1)
    J=e.variable("JL",1)
    Lam,j_B=e.variable("L",0),e.variable("jB",0)
    if phase=="native":
        raw=e.scale(e.mul(Lam,C,J),-r)
        F=e.partial(raw,"JL")
        assert F==e.scale(e.mul(Lam,C),r)
    else:
        F=e.scale(e.mul(Lam,C),r)
        assert e.partial(e.mul(J,F),"JL")==F
    prefactor=sp.simplify(r*xi/2)
    phi_L=e.scale(e.mul(j_B),sp.I*p/P)
    phi_C=e.scale(e.mul(j_a),1/Q)
    rooted=e.scale(e.mul(eta,phi_L,phi_C),prefactor)
    assert rooted and rooted!=e.scale(rooted,-1)
    assert all("JL" not in word for word in rooted)
    return str(prefactor)


def evidence(phase):
    a=owner.mixed_root_control()
    b=owner.connected_source_control()
    assert [a[k] for k in ("shear_sign","width_shift_sign","retained_JC_shift_sign")]==[1,1,-1]
    assert a["full_J_omission_sensitive"] and all(b.values())
    def checks(folder):
        return json.loads((CALC/("canonical_so10_"+folder)/"result.json").read_bytes())["checks"]
    s=checks("e5_marked_mixed_master_feynman_v1")
    c=checks("e5_retained_marked_ghost_source_feynman_v1")
    assert s["shared_marked_boundary_magnitude"]=="3*sqrt(10)/8"
    assert c["complete_light_triangle_color"]=="3*sqrt(10)/8"
    assert c["ordinary_root_color_norms"]==[3,3]
    return True


def check(phase):
    return {"literal_broken_retained_rows":actual(phase),
            "three_ordered_mixed_terms":evidence(phase),
            "nonzero_width_tree_carrier":width(phase),
            "direct_shear_and_retained_log_controls":True}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
