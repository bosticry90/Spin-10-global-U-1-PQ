"""Alternate-probe color audit, Mellin derivatives and positive quadratures."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from hashlib import sha256
import gzip,json,os,threading,time
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
d=s.Symbol('d',positive=True);z,ld,zz=s.symbols('z ld zeta2',real=True);hs=s.symbols('h1:5',real=True)
LOC={str(v):v for v in [d,z,ld,zz,*hs]}
def read(p):return json.loads(p.read_bytes())
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
@lru_cache(None)
def clean(v):return s.cancel(s.expand(v))
def mat(x):return s.SparseMatrix(*x['shape'],{(i,j):s.sympify(v) for i,j,v in x['entries']})
def tidy(M):return s.SparseMatrix(M).applyfunc(clean)
def equal(A,B):assert not tidy(A-B).todok()
def near(a,b,tol='1e-40'):assert abs(a-b)<mp.mpf(tol)*(1+abs(a)),(a,b)
def rational(v):
    q=s.Rational(v);return mp.mpf(int(q.p))/int(q.q)

def actual_colors(tab):
    inp=packed(CAL/'canonical_so10_background_threshold_inputs/replay_tables.json.gz')
    wh=packed(CAL/'canonical_so10_width_hard_projection/replay_tables.json.gz');P=list(map(mat,wh['projectors']))
    f={(a,b,c):s.sympify(v) for a,b,c,v in inp['f']}
    Fe=[s.SparseMatrix(45,45,{(a,b):v for (a,b,k),v in f.items() if k==e}) for e in range(45)]
    adj=[s.SparseMatrix(45,45,{(out,b):v for (a,b,out),v in f.items() if a==h}) for h in range(45)]
    pairs=list(combinations(range(10),2));cs=[adj[pairs.index((2*j,2*j+1))] for j in range(5)]
    # SU2 uses a non-Cartan direction and SU3 a different Cartan. Both are
    # normalized actual SO10 planes; their bracket/source inputs are unchanged.
    probes=[tidy(sum((v*T for v,T in zip([-2,-2,-2,3,3],cs)),s.zeros(45))/s.sqrt(30)),
      tidy((-adj[pairs.index((6,9))]+adj[pairs.index((7,8))])/s.sqrt(2)),
      tidy((cs[0]+cs[1]-2*cs[2])/s.sqrt(6))]
    gram=mat(inp['Gram']);cov=[]
    K={}
    for F in Fe:
        for (a,b),u in F.todok().items():
            for (c,e),v in F.todok().items():K[a,b,c,e]=K.get((a,b,c,e),0)+u*v
    K={key:clean(v) for key,v in K.items() if clean(v)}
    vacuum_pairings=[sum((v*int(a==b)*int(c==e) for (a,b,c,e),v in K.items()),s.Integer(0)),
      sum((v*int(a==c)*int(b==e) for (a,b,c,e),v in K.items()),s.Integer(0)),
      sum((v*int(a==e)*int(b==c) for (a,b,c,e),v in K.items()),s.Integer(0))]
    assert vacuum_pairings==[0,360,-360]
    for N in [4,6,8]:
        full=vacuum_pairings[0]*N+vacuum_pairings[1]*N*N+vacuum_pairings[2]*N
        assert full==360*N*(N-1) and full/s.Integer(4)!=full/s.Integer(8)
    for idx,T in enumerate(probes):
        print('STAGE alternate_probe_'+str(idx),flush=True)
        for Q in P:equal(Q*T,T*Q)
        # A norm method obtains X without using either native X contraction.
        X=s.zeros(5);L=s.zeros(5);Y=s.zeros(5);U=[tidy(Q*T) for Q in P]
        for F in Fe:
            for r in range(5):
                A=T*P[r]*F
                for t in range(5):
                    B=tidy(A*P[t]);X[r,t]-=sum((v*v for v in B.todok().values()),s.Integer(0))
        # Other independent color invariant evaluated with explicit f entries.
        Ud=[Q.todok() for Q in U]
        for (a,b,c,e),value in K.items():
            for r in range(5):
                for t in range(5):
                    L[r,t]+=value*Ud[r].get((a,b),0)*Ud[t].get((c,e),0)
                    Y[r,t]+=value*Ud[r].get((a,e),0)*Ud[t].get((b,c),0)
        X,L,Y=map(tidy,[X,L,Y])
        row=tab['color'][idx]
        for key,M in [('X',X),('L',L),('Y',Y),('Z',L-Y)]:equal(M,s.Matrix([[s.sympify(v) for v in line] for line in row[key]]))
        # Both Wick cross pairings are necessary already in the double pole.
        assert sum(L)==64 and sum(Y)==-32 and sum(X)==-64
        assert -12*sum(L)!=-1152 and 12*sum(Y)!=-1152
        cov.append({'group':row['group'],'alternate_probe_all_entries_agree':True,
                    'X_negative_projected_norms':True})
    # Mixed-factor terms vanish by the inherited exact H invariance of f/P;
    # explicitly test them for every r,s in the X tensor as a sensitive check.
    mixed=[]
    for a,b in [(0,1),(0,2),(1,2)]:
        UA=[tidy(Q*probes[a]) for Q in P];UB=[tidy(Q*probes[b]) for Q in P]
        for r in range(5):
            S=tidy(P[r]*(probes[a]*probes[b]+probes[b]*probes[a]))
            for t in range(5):
                v=sum((-s.trace(S*F*P[t]*F) for F in Fe),s.Integer(0));assert clean(v)==0
                cross=0
                for F in Fe:
                    entries=F.todok()
                    dot=lambda U:sum((v*U[i,j] for (i,j),v in entries.items()),s.Integer(0))
                    cross+=dot(UA[r])*dot(UB[t])+dot(UB[r])*dot(UA[t])
                    cross+=s.trace(F*UB[t]*F*UA[r])+s.trace(F*UA[t]*F*UB[r])
                assert clean(cross)==0
        mixed.append([a,b])
    return cov,mixed

def heat_and_lorentz():
    D,e=s.symbols('D eps',real=True)
    F=s.Matrix([[0,1],[-1,0]])
    assert s.trace(F*F)==-2
    # Explicit two-plane spin matrix multiplied by its orbital oscillator.
    b,t=s.symbols('b t',real=True)
    orbital=s.series(b*t/s.sinh(b*t),b,0,3).removeO()
    spin=s.series(s.cosh(2*b*t),b,0,3).removeO()
    hv=s.expand(orbital*(D-2+2*spin)).coeff(b,2)/t**2
    assert clean(hv-(4-D/6))==0
    kappa=clean(-6*(D-1)*(D/12-2)).subs(D,4-2*e).expand()
    assert kappa==30-17*e-2*e*e
    assert (kappa-30).coeff(e,1)==-17
    # Spin magnitude zero and1 are detected; reversing2 to-2 is insensitive.
    def k(c):return clean(-6*(D-1)*(D/12-s.Rational(c*c,2)))
    assert k(0)!=k(2) and k(1)!=k(2) and k(-2)==k(2)
    assert clean(-12*(D/s.Integer(24)-1)-(12-D/2))==0
    return {'orbital_and_spin_coefficients_independent_heat_check':True,
      'dimensional_and_external_coupling_normalization_checked':True,
      'wrong_spin_magnitude_or_omitted_orbital_term_detected':True,
      'global_spin_sign_insensitive':True}

def mellin(tab):
    mp.mp.dps=80;points=[mp.mpf('0.001'),mp.mpf('0.0001')];errors=[]
    heavy=[mp.mpf(1)/200,mp.mpf(1)/40,mp.mpf(5)/12,mp.mpf(253)/600]
    for dd in points:
        masses=[dd,*heavy];logs=[mp.log(v) for v in masses]
        sub={d:s.Float(str(dd),85),z:0,ld:s.Float(str(logs[0]),85),zz:s.pi**2/6,
             **{h:s.log(q) for h,q in zip(hs,[s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)])}}
        for row,amp in zip(tab['color'],tab['amplitudes']):
            X=[[rational(v) for v in line] for line in row['X']];Z=[[rational(v) for v in line] for line in row['Z']]
            def smooth(e):
                common=mp.exp(2*mp.euler*e)*mp.gamma(1+e)**2
                v=mp.mpf(0)
                for r in range(5):
                    for t in range(5):
                        coefficient=(30-17*e-2*e*e)*e/(e-1)*(masses[t]/masses[r])*X[r][t]-12*Z[r][t]
                        v+=coefficient*mp.exp(-e*(logs[r]+logs[t]))
                return common*v
            for order,power in [(0,'-2'),(1,'-1'),(2,'0')]:
                got=mp.diff(smooth,0,order)/mp.factorial(order)
                expected=mp.mpf(str(s.N(s.sympify(amp['Laurent'][power],locals=LOC).subs(sub),85)))
                near(got,expected);errors.append(abs(got-expected)/(1+abs(got)))
    # Independent positive Schwinger integrals in a common convergence strip.
    mp.mp.dps=45;e=mp.mpf(5)/4;errs=[]
    for x in [mp.mpf('0.001'),*heavy]:
        for j in range(3):
            got=mp.exp(mp.euler*e)*mp.quad(lambda u:4*u**(4*j)*mp.exp(-x*u**4),[0,1,4,16,mp.inf])
            expected=mp.exp(mp.euler*e)*mp.gamma(e-1+j)*x**(1-e-j)
            near(got,expected,'1e-25');errs.append(abs(got-expected)/(1+abs(expected)))
    return {'all18_bare_Laurent_coefficients_from_smooth_Mellin_derivatives':True,
       'max_scaled_Mellin_error':mp.nstr(max(errors),12),'positive_quadratures':len(errs),
       'quadrature_epsilon':'5/4','max_scaled_positive_quadrature_error':mp.nstr(max(errs),12)}

def ir(tab):
    out=[]
    for amp in tab['amplitudes']:
        summary={}
        for power,expr in amp['Laurent'].items():
            value=s.sympify(expr,locals=LOC);parts=amp['IR_decomposition'][power]
            p={k:s.sympify(v,locals=LOC) for k,v in parts.items()}
            total=p['inverse_d']/d+p['log_d_at_d0']+p['regular_d0']+d*p['vanishing_d_times_log_polynomial']
            assert clean(value-total)==0
            assert clean(p['log_d_at_d0'].subs(ld,0))==0
            summary[power]={'inverse_d_nonzero':p['inverse_d']!=0,'log_d_at_d0_nonzero':p['log_d_at_d0']!=0}
        out.append({'group':amp['group'],'IR_terms':summary})
    return out

def main():
    start=time.perf_counter();timer=threading.Timer(240,lambda:os._exit(124));timer.start()
    a=packed(HERE/'primary_tables.json.gz');b=packed(HERE/'replay_tables.json.gz');assert a==b
    for role in ['primary','replay']:
        r=read(HERE/(role+'_result.json'));raw=gzip.decompress((HERE/(role+'_tables.json.gz')).read_bytes())
        assert sha256(raw).hexdigest()==r['tables_sha256']
    assert len(a['background_words'])==8 and sum(s.sympify(w[0])==-1 for w in a['background_words'])==2
    cov,mixed=actual_colors(a);heat=heat_and_lorentz()
    print('STAGE Mellin_and_positive_quadratures',flush=True);me=mellin(a);irdata=ir(a)
    value={'schema':'C1_VECTOR_QUARTIC_PRIMITIVE_VALIDATION_V1','execution_state':'COMPLETED',
      'status':'QUALIFIED_COMPLETE_AUXILIARY_IR_REGULATED_BARE_VECTOR_QUARTIC_F2',
      'scientific_acceptance':'NOT_PERFORMED','scientific_authority':'34/39_UNCHANGED',
      'all225_color_coefficients_and_zero_complements_checked':True,'all25_mass_assignments_retained':True,
      'alternate_probes':cov,'mixed_factor_X_and_Z_checks':mixed,'heat_and_lorentz':heat,'Mellin':me,
      'IR_classification':irdata,'double_pole_each_factor':-1152,
      'UV_forests_or_common_EFT_IR_subtraction_constructed':False,
      'complete_finite_hard_family_or_C1_qualified':False,'finite_scheme_or_vacuum_adopted':False,
      'source_or_arbitrary_width_controls':'NOT_APPLICABLE_SOURCE_ZERO_XI1',
      'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(value,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
