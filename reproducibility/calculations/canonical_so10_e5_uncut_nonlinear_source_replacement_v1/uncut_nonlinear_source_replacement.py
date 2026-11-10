"""Check the actual repeated direct uncut replacement on both action routes."""
from importlib.util import module_from_spec, spec_from_file_location
import sys

import sympy as sp

from execute import ROOT, run_worker

path=ROOT/"calculations"/"canonical_so10_e5_compact_cubic_ghost_replacement_v2"/"compact_cubic_ghost_replacement.py"
spec=spec_from_file_location("compact_source_owner",path)
owner=module_from_spec(spec)
spec.loader.exec_module(owner)


def rooted(phase,canonical):
    th,x,y,z,r,xi,p,q,B=sp.symbols("theta x y z r xi p q B",nonzero=True)
    # The full odd trace has the two transposed species with the negative sign.
    if phase=="native":
        full=-2*canonical*xi**2
        normalized=-full*((1+th*r)**2-1)*B/4
        mixed=-full*((1+(x+y)*r)**2-1)*B/4
    else:
        original=canonical*xi**2/2
        normalized=original*((1+th*r)**2-1)*B
        mixed=original*((1+(x+y)*r)**2-1)*B
    quad=sp.expand(normalized).coeff(th,2)
    both=mixed.diff(x,y)
    assert quad==4*xi**2*r**2*B
    assert both==8*xi**2*r**2*B
    # Both ordinary mixed roots are retained, with opposite momenta.
    roots=(p/z)*(-q/z)
    assert sp.simplify((normalized*roots).diff(th,2)/2-quad*roots)==0
    assert quad*roots!=0
    assert normalized.diff(th).subs(th,0)!=0
    return [4,8]


def check(phase):
    found=owner.check(phase)
    assert found["literal_shift_counts"]==[138,276,648]
    canonical=int(found["canonical_one_species_square"])
    assert canonical==8
    return {"literal_transport_data":found["literal_shift_counts"],
            "canonical_quadratic_trace_factor":canonical,
            "uncut_same_label_and_mixed_log_residues":rooted(phase,canonical),
            "absolute_rooted_repeated_coefficient":True}


if __name__=="__main__":
    run_worker(check,sys.argv[1])
