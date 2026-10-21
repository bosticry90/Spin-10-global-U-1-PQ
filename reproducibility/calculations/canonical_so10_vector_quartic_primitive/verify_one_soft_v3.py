"""Independent open-density kernel and its measured inverse-IR closure."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
import gzip,json,os,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
def pack(p):return json.loads(gzip.decompress(p.read_bytes()))
def mat(x):return s.SparseMatrix(*x['shape'],{(i,j):s.sympify(v) for i,j,v in x['entries']})
@lru_cache(None)
def clean(v):return s.cancel(s.expand(v))
def tidy(M):return s.SparseMatrix(M).applyfunc(clean)
def zero(M):assert not tidy(M).todok()

def main():
    start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
    B=pack(CAL/'canonical_so10_background_threshold_inputs/primary_tables.json.gz')
    P=list(map(mat,pack(CAL/'canonical_so10_width_hard_projection/primary_tables.json.gz')['projectors']))
    f={(a,b,c):s.sympify(v) for a,b,c,v in B['f']};Fe=[s.SparseMatrix(45,45,{(a,b):v for (a,b,k),v in f.items() if k==e}) for e in range(45)]
    K=[tidy(-sum((F*Q*F for F in Fe),s.zeros(45))) for Q in P]
    # Independent density differentiation: all six slot choices, both source
    # orderings, the fixed1/4 density, then the internal Lorentz sum.
    pairings=list(combinations(range(4),2));pol=[s.zeros(45) for _ in range(5)]
    fused={}
    for F in Fe:
        for (a,b),u in F.todok().items():
            for (c,e),v in F.todok().items():fused[a,b,c,e]=fused.get((a,b,c,e),0)+u*v
    fused={key:clean(v) for key,v in fused.items() if clean(v)}
    for r,Q in enumerate(P):
        print('STAGE open_density_'+str(r),flush=True)
        slots=[s.zeros(45) for _ in range(6)];qd=Q.todok()
        for colors,value in fused.items():
            for k,(i,j) in enumerate(pairings):
                rem=[x for x in range(4) if x not in [i,j]]
                p=qd.get((colors[rem[0]],colors[rem[1]]),0)
                if p:slots[k][colors[i],colors[j]]+=value*p
        slots=list(map(tidy,slots))
        for N in [4,6]:
            result=s.zeros(45)
            for k,((i,j),S) in enumerate(zip(pairings,slots)):
                # Lorentz labels of slots are(mu,nu,mu,nu). External values0
                # pin both labels for a cross choice; a repeated label leaves
                # the other internal label summed over D components.
                factor=N if i%2==j%2 else 1
                result+=s.Rational(1,4)*factor*(S+S.T)
            zero(result-(N-1)*K[r])
    pairs=list(combinations(range(10),2))
    def vec(entries):return s.SparseMatrix(45,1,{(pairs.index(pair),0):v for pair,v in entries})
    Y=vec([((2*j,2*j+1),s.Integer(v)/s.sqrt(30)) for j,v in enumerate([-2,-2,-2,3,3])])
    weak=[vec([((6,7),1/s.sqrt(2)),((8,9),-1/s.sqrt(2))]),
          vec([((6,9),-1/s.sqrt(2)),((7,8),1/s.sqrt(2))]),
          vec([((6,8),1/s.sqrt(2)),((7,9),1/s.sqrt(2))])]
    Qy=tidy(Y*Y.T);Qw=tidy(sum((v*v.T for v in weak),s.zeros(45)));Qc=tidy(P[0]-Qy-Qw)
    ideals=[Qy,Qw,Qc];ranks=[1,3,8];kis=[]
    G=s.SparseMatrix(45,45,{(a,b):s.sympify(v) for a,b,v in B['Gram']})
    zero(sum(ideals,s.zeros(45))-P[0])
    for i,Q in enumerate(ideals):
        zero(Q*Q-Q);zero(Q-Q.T);zero(G*Q);assert s.trace(Q)==ranks[i]
        for U in ideals[:i]:zero(Q*U)
        row=[]
        for r,Kr in enumerate(K):
            kval=clean(s.trace(Q*Kr)/ranks[i]);zero(Q*Kr*Q-kval*Q);row.append(kval)
            for j,U in enumerate(ideals):
                if j!=i:zero(Q*Kr*U)
        kis.append(row)
    # The Schur scalar agrees with the independent mass-resolved charge index.
    measured=pack(HERE/'primary_v2_tables.json.gz')
    for i,row in enumerate(kis):assert row==list(map(s.sympify,measured['color'][i]['indices']))
    k=[s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)]
    e,z,ld=s.symbols('eps z ld',real=True);hs=s.symbols('h1:5',real=True)
    tau=[0,2,3];pole=[];closed=[]
    loc={str(v):v for v in [e,z,ld,*hs]}
    for i in range(3):
        masspole=clean(-3*sum(k[r-1]*kis[i][r] for r in range(1,5)));pole.append(str(masspole))
        # Actual independently opened (D-1) mass kernel closed on the light
        # vector propagator. Only inverse-d terms are selected here.
        expression=0
        for r in range(1,5):
            expression+=(10+e)*(3-2*e)*(-tau[i]*kis[i][r])*k[r-1]*(-1/e-1-2*z+ld+hs[r-1])
        p=s.expand(expression).coeff(e,-1);fin=s.expand(expression).coeff(e,0)
        expected=measured['amplitudes'][i]['IR_decomposition']
        assert clean(p-s.sympify(expected['-1']['inverse_d'],locals=loc))==0
        assert clean(fin-s.sympify(expected['0']['inverse_d'],locals=loc))==0
        if i>0:
            assert p!=0 and fin!=0
            premature=30*sum((-tau[i]*kis[i][r])*k[r-1]*(-1/e-1-2*z+ld+hs[r-1]) for r in range(1,5))
            assert clean(s.expand(premature).coeff(e,0)-fin)!=0
            missingC=s.expand(sum((10+e)*(3-2*e)*(-tau[i]*kis[i][r])*k[r-1]*(-1/e-1-z+hs[r-1]) for r in range(1,5))).coeff(e,0)
            assert clean(missingC-fin)!=0 and p/2!=p
        closed.append({'group':['U1','SU2','SU3'][i],'pole_inverse_d':str(p),'finite_inverse_d':str(fin)})
    value={'schema':'C1_VECTOR_QUARTIC_ONE_SOFT_SUPPLEMENT_V3','execution_state':'COMPLETED',
      'all_five_45x45_open_kernels_from_six_density_slots_agree':True,
      'actual_light_ideal_ranks':ranks,'mass_resolved_open_kernel_scalars':[[str(v) for v in row] for row in kis],
      'hard_graph_mass_poles_in_ell60g4_units':pole,'inverse_d_closure':closed,
      'full_inverse_d_pole_and_finite_terms_equal_actual_one_soft_closure':True,
      'wrong_half_D4_and_missing_C_epsilon_controls_sensitive_in_nonabelian_factors':True,
      'hypercharge_closure_control':'INSENSITIVE_ZERO_LIGHT_CHARGE',
      'd0_IR_logs_UV_forests_or_common_matching_closed':False,
      'physical_gauge_masses_or_counterterms_adopted':False,
      'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(value,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
