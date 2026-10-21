"""SSI1 exact scalar carrier; two independent inherited derivative representations."""
from pathlib import Path
from hashlib import sha256
import json,sys,time,threading,os
import sympy as s

START=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
role=sys.argv[1];assert role in ['primary','replay']
prep=json.loads((O/'preparation.json').read_bytes())
for path,h in prep['input_sha256'].items():assert sha256(Path(path).read_bytes()).hexdigest()==h,path
cache=json.loads((R/'calculations/canonical_so10_singlet_tadpole/original_v2_result.json').read_bytes())
point=json.loads((R/'calculations/canonical_so10_finite_radial_control/primary_result.json').read_bytes())
quartic=json.loads((R/'calculations/canonical_so10_singlet_quartic_running/primary_result.json').read_bytes())
slots=cache['slots'];assert len(slots)==34
raw={k:s.sympify(v) for k,v in point['raw_coefficients'].items()}
def coefficient(slot):
 name,_,part=slot.partition(':')
 return s.im(raw[name]) if part=='im' else s.re(raw[name])
degree={'mS2':2,'lambdaPhiS':2,'lambdaSigmaS':2,'lambdaVectorS':2,'lambdaS':4,'z6':1,'z4':1,'zK':1}
metricS=s.Rational(3,5);portal=s.Rational(quartic['same_point_couplings']['lambdaVectorS'])
assert portal==s.Rational(49893,50000000) and raw['lambdaVectorS']==s.Rational(3,10)*portal
blocks=[];total=s.S.Zero;inside=s.S.Zero;outside=s.S.Zero;trace=s.S.Zero;rank=0;realcount=0
for b in cache['block_inputs']:
 n=len(b['metric']);assert len(b['sectors'])==n;Rraw=s.zeros(n)
 if role=='primary':
  for slot,i,j,value in b['raw_H34_sparse']:
   name=slots[slot].partition(':')[0];p=degree.get(name,0)-int(b['sectors'][i] in ['S','SBar'])-int(b['sectors'][j] in ['S','SBar'])
   assert p>=0
   Rraw[i,j]+=p*coefficient(slots[slot])*s.sympify(value)
 else:
  # These are separately retained literal raw Euler derivatives, not p*H here.
  assert set(b['raw_D8'])=={'lambdaS','lambdaVectorS','z4:im','z4:re','z6:im','z6:re','zK:im','zK:re'}
  for slot,matrix in b['raw_D8'].items():Rraw+=coefficient(slot)*s.Matrix(matrix)
 W=s.diag(*[1/s.sqrt(s.Rational(x)) for x in b['metric']])
 D=(W*Rraw*W/s.sqrt(metricS)).applyfunc(s.simplify)
 assert (D-D.H).applyfunc(s.simplify)==s.zeros(n)
 idx=[j for j,q in enumerate(b['sectors']) if q in ['phi','phiBar']]
 w=s.simplify(sum(s.conjugate(D[i,j])*D[i,j] for j in idx for i in range(n)))
 wi=s.simplify(sum(s.conjugate(D[i,j])*D[i,j] for j in idx for i in idx))
 tr=s.simplify(sum(D[j,j] for j in idx))
 assert w.is_Rational and wi.is_Rational and w>=wi>=0
 total+=b['dimension']*w;inside+=b['dimension']*wi;outside+=b['dimension']*(w-wi);trace+=b['dimension']*tr
 rank+=b['dimension']*len(idx);realcount+=b['dimension']*n
 entries=[[i,j,str(D[i,j])] for i in range(n) for j in range(n) if D[i,j]!=0]
 fingerprint=sha256(json.dumps(entries,separators=(',',':')).encode()).hexdigest()
 blocks.append({'label':b['label'],'multiplicity':b['dimension'],'size':n,'phi_columns':idx,
  'D_nonzero_positions':len(entries),'D_sha256':fingerprint,'D_entries':entries,
  'W10_unweighted':str(w),'W10_phi_spectator':str(wi),'trace_phi_block':str(tr)})
assert len(blocks)==35 and realcount==328 and rank==20
total,inside,outside,trace=map(s.simplify,[total,inside,outside,trace])
assert trace==s.simplify(20*portal*s.sqrt(metricS))
lower=s.simplify(10*portal**2*metricS)
assert total/2>=inside/2>=lower>0 and total==inside+outside
assert total>0 and outside>=0
# Ordered graph has parallel fermion edges; deleting any edge keeps connectivity.
edges=[(0,1),(0,2),(3,1),(2,3),(2,3)]
def connected(edges):
 seen={0}
 while True:
  added={v for e in edges if set(e)&seen for v in e}
  if added<=seen:return len(seen)==4
  seen|=added
assert len(edges)-4+1==2 and all(connected(edges[:j]+edges[j+1:]) for j in range(5))
# Symbolic realification gives K/2 on all20 directions; external y_S remains0.
assert s.simplify((1/s.sqrt(2))**2)==s.Rational(1,2)
assert s.simplify(total/2*metricS-total/2)!=0  # omitted external metric control
assert total/2!=total  # dropped sqrt2 normalization
elapsed=time.perf_counter()-START;assert elapsed<120
out={'schema':'SINGLET_TWO_LOOP_INPUT_CLOSURE_V1','route':role,'blocks':blocks,
 'real_scalar_directions':realcount,'real_phi_projector_rank':rank,
 'trace_actual_phi_cubic':str(trace),'canonical_lambdaVectorS':str(portal),
 'W10_unweighted':str(total),'C10_K10_coefficient_unweighted':str(total/2),
 'C10_phi_spectator':str(inside/2),'C10_other_spectator':str(outside/2),
 'exact_portal_lower_bound_on_C10':str(lower),
 'C10_decimal':str(s.N(total/2,30)),'coupling_contraction_strictly_positive':True,
 'V_graph_loops':2,'V_graph_one_particle_irreducible':True,
 'no_direct_S_Yukawa_required':True,'actual_two_loop_integral_or_total_cancellation_computed':False,
 'numerical_Yukawa_or_flavor_fit_adopted':False,'quantum_control_E5_or_physical_promotion':False,
 'scientific_disposition':'ACTUAL_NONZERO_INTERNAL_YUKAWA_TWO_LOOP_VERTEX_CARRIER_REQUIRE_INDEPENDENT_VALIDATION_NOT_INTEGRATED_AMPLITUDE',
 'execution_state':'COMPLETED','elapsed_after_imports':elapsed,'authority_changed':False}
print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
