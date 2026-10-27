# Native V2: read the supplied constant source chart in its actual encoding

Native V1 failed at JP.decode(data['source_action']) before constructing
any source-product output. That field is the older270-coordinate constant
source chart with integer words and symbolic coefficient strings, not the
643-pair differential-polynomial encoding of QG. Its complete FAILED
capture, source/copy, preparation and controller failure remain unchanged.

V2 checks source linearity directly in that integer chart: indices0..134
are JL,Ja,JC in three45-coordinate blocks; indices135..269 are C,a,Lambda.
This is exactly the already frozen UMH general_v2.py conversion, separately
used by its original verifier. The QG jet decoder is unchanged. No jet is
discarded from QG, no coefficient or source is reinterpreted as a default.
Fresh base-source validation concerns this supplied nonminimal/ghost
chart; full classical source linearity remains the explicit CSW premise.

All prospective mathematical assertions, controls,300s/180s resource limits,
inputs and authority ceilings remain. No original result or receipt exists.
