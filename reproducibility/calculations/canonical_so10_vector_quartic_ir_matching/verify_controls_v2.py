"""Explicit mutants of the new light map and hard finite polynomial."""
from pathlib import Path
import gzip,json,os,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def mat(x):return s.SparseMatrix(*x['shape'],{(i,j):s.sympify(v) for i,j,v in x['entries']})
def clean(x):return s.cancel(s.expand(x))
def main():
    start=time.perf_counter();timer=threading.Timer(120,lambda:os._exit(124));timer.daemon=True;timer.start()
    t=packed(HERE/'primary_tables.json.gz');old=packed(CAL/'canonical_so10_vector_quartic_primitive/primary_v2_tables.json.gz')
    V=mat(t['light_embedding']);bad=V.copy();bad[:,1]=2*V[:,1]
    kinetic=(bad.T*bad-s.eye(12)).applyfunc(clean);assert kinetic[1,1]==3 and any(kinetic)
    assert any((bad*bad.T-V*V.T).applyfunc(clean))
    k=[None,s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)]
    d=s.Symbol('d',positive=True);z,ld,zz=s.symbols('z ld zeta2',real=True);hs=s.symbols('h1:5',real=True)
    loc={str(v):v for v in [d,z,ld,zz,*hs]};mutants=[]
    for i,row in enumerate(t['polynomials']):
        xs=sum((s.sympify(old['color'][i]['X'][r][q])*k[q]/k[r] for r in range(1,5) for q in range(1,5)),s.Integer(0))
        dimensional=clean(-17*xs);assert dimensional!=0
        finite=s.sympify(row['hard_bare_remainder']['0'],locals=loc)
        zeta=s.expand(finite).coeff(zz);assert zeta!=0 and zeta==s.sympify(row['hard_bare_remainder']['-2'])
        omission=s.sympify(row['full']['0'],locals=loc)-finite
        assert clean(omission)!=0
        # Reverse the actual antisymmetric curvature-kernel trace.
        traces=[s.sympify(t['closure_traces'][i][r][1]) for r in range(1,5)]
        residuals=[clean(-2*v) for v in traces]
        if i>0:assert any(residuals)
        else:assert all(v==0 for v in residuals)
        mutants.append({'group':row['group'],'premature_D4_hard_finite_residual':str(dimensional),
          'missing_B_epsilon_zeta2_residual':str(zeta),'reversed_trace_residuals':list(map(str,residuals)),
          'omitted_light_assignments_full_UV_residual_nonzero':True,
          'omitted_light_assignments_final_hard_test':'INSENSITIVE_REQUIRES_FULL_UV_AND_PARTNERS'})
    value={'schema':'C1_VECTOR_QUARTIC_IR_CONTROLS_V2','execution_state':'COMPLETED',
      'unnormalized_frame_kinetic_defect':'3','actual_hard_remainder_mutants':mutants,
      'native_and_completed_V1_validation_reused':True,'new_loop_calculations':False,
      'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(value,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
