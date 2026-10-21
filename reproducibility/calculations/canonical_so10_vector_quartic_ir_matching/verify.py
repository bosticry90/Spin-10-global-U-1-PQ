"""Independent fundamental-plane/tree audit and entire Mellin partition."""
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
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
@lru_cache(None)
def clean(v):return s.cancel(s.expand(v))
def tidy(M):return s.SparseMatrix(M).applyfunc(clean)
def mat(x):return s.SparseMatrix(*x['shape'],{(i,j):s.sympify(v) for i,j,v in x['entries']})
def zero(M):assert not tidy(M).todok()
def parse(v):return s.sympify(v,locals=LOC)
def number(v):
    q=s.Rational(v);return mp.mpf(int(q.p))/int(q.q)
def near(a,b):assert abs(a-b)<mp.mpf('1e-40')*(1+abs(a)),(a,b)

def tree_and_operators(tab):
    B=packed(CAL/'canonical_so10_background_threshold_inputs/replay_tables.json.gz')
    P=list(map(mat,packed(CAL/'canonical_so10_width_hard_projection/replay_tables.json.gz')['projectors']))
    V=mat(tab['light_embedding']);zero(V.T*V-s.eye(12));zero(V*V.T-P[0])
    O=s.SparseMatrix(328,45,{(i,j):s.sympify(v) for i,j,v in B['orbit']});zero(O*V)
    pairs=list(combinations(range(10),2));H=[s.SparseMatrix(10,10,{(i,j):1/s.sqrt(2),(j,i):-1/s.sqrt(2)}) for i,j in pairs]
    f={}
    for i in range(45):
        for j in range(45):
            M=H[i]*H[j]-H[j]*H[i]
            for (a,b),v in M.todok().items():
                if a<b:f[i,j,pairs.index((a,b))]=clean(s.sqrt(2)*v)
    assert f=={(a,b,c):s.sympify(v) for a,b,c,v in B['f']}
    parents=[tidy(sum((V[a,i]*H[a] for a in range(45) if V[a,i]),s.zeros(10))) for i in range(12)]
    fh={}
    for i in range(12):
        for j in range(12):
            comm=tidy(parents[i]*parents[j]-parents[j]*parents[i])
            parent_vector=s.SparseMatrix(45,1,{(a,0):clean(s.sqrt(2)*comm[b,c]) for a,(b,c) in enumerate(pairs) if comm[b,c]})
            zero((s.eye(45)-P[0])*parent_vector)
            coeff=tidy(V.T*parent_vector)
            for (a,_),value in coeff.todok().items():fh[i,j,int(a)]=value
    assert fh=={(a,b,c):s.sympify(v) for a,b,c,v in tab['restricted_f']}
    Fe=[s.SparseMatrix(45,45,{(a,b):v for (a,b,k),v in f.items() if k==e}) for e in range(45)]
    adj=[s.SparseMatrix(45,45,{(out,b):v for (a,b,out),v in f.items() if a==h}) for h in range(45)]
    probes=[tidy(sum((V[a,i]*adj[a] for a in range(45) if V[a,i]),s.zeros(45))) for i in [0,1,4]]
    def K(M):return tidy(-sum((F*M*F for F in Fe),s.zeros(45)))
    def J(M):return tidy(sum((F*sum((v*M[a,b] for (a,b),v in F.todok().items()),s.Integer(0)) for F in Fe),s.zeros(45)))
    for r,Q in enumerate(P):zero(K(Q)-mat(tab['mass_operators'][r]))
    sensitive=[]
    for i,T in enumerate(probes):
        print('STAGE independent_operators_'+str(i),flush=True)
        for r,Q in enumerate(P):
            U=tidy(Q*T);S=tidy(Q*T*T);A=K(Q);Bop=tidy(J(U)+K(U));C=K(S)
            zero(Bop-mat(tab['first_curvature_operators'][i][r]));zero(C-mat(tab['second_curvature_operators'][i][r]))
            wrong=tidy(J(U)-K(U))
            if i>0 and r>0 and wrong!=Bop:
                trace_error=clean(s.trace(P[0]*T*(wrong-Bop)))
                if trace_error:sensitive.append({'group':i,'mass_slot':r,'wrong_antisymmetric_sign_trace_error':str(trace_error)})
            want=[clean(s.trace(P[0]*T*T*A)),clean(s.trace(P[0]*T*Bop)),clean(s.trace(P[0]*C))]
            assert want==list(map(s.sympify,tab['closure_traces'][i][r]))
    assert sensitive and any(x['group']==1 for x in sensitive) and any(x['group']==2 for x in sensitive)
    return sensitive

def exact_partition(tab,old):
    controls=[]
    for i,row in enumerate(tab['polynomials']):
        direct={q:0 for q in ['-2','-1','0']}
        for r in range(1,5):
            for t in range(1,5):
                k=[None,s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)]
                X=s.sympify(old['color'][i]['X'][r][t]);Z=s.sympify(old['color'][i]['Z'][r][t]);j=2*z-hs[r-1]-hs[t-1]
                direct['-2']-=12*Z;direct['-1']+=-30*X*k[t]/k[r]-12*Z*j
                direct['0']+=X*k[t]/k[r]*(-13-30*j)-12*Z*(j*j/2+zz)
        for q in direct:
            full=parse(old['amplitudes'][i]['Laurent'][q]);mixed=parse(row['mixed_closure'][q]);eft=parse(row['EFT_pure_light'][q]);hard=parse(row['hard_bare_remainder'][q])
            assert clean(full-mixed-eft-hard)==0 and clean(direct[q]-hard)==0
            assert not ({d,ld}&hard.free_symbols)
        # Directly construct omitted pieces with exact ratio slots.
        kk=[d,s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)]
        Bmiss=0;Cmiss=0
        for r in range(1,5):
            b=s.sympify(tab['closure_traces'][i][r][1]);c=s.sympify(tab['closure_traces'][i][r][2]);j=2*z-ld-hs[r-1]
            Bmiss+=24*b*(j*j/2+zz)
            Cmiss+=c*d/kk[r]*(-13-30*j)
        if i>0:assert clean(Bmiss)!=0
        assert clean(Cmiss)!=0
        assert clean(parse(row['full']['0'])-parse(row['mixed_closure']['0'])/2-parse(row['EFT_pure_light']['0'])-parse(row['hard_bare_remainder']['0']))!=0
        if i>0:assert parse(row['EFT_pure_light']['-2'])!=0
        controls.append({'group':row['group'],'omitted_first_curvature_constant_zeta2_coefficient':str(s.expand(Bmiss).coeff(zz)),
           'omitted_second_curvature_retains_d_log_terms':True,'half_mixed_closure_detected':True,
           'pure_light_double_pole':row['EFT_pure_light']['-2']})
    return controls

def mellin_partition(tab,old):
    mp.mp.dps=80;heavy=[mp.mpf(1)/200,mp.mpf(1)/40,mp.mpf(5)/12,mp.mpf(253)/600];errors=[]
    for dd in [mp.mpf('0.001'),mp.mpf('0.0001')]:
        k=[dd,*heavy];lg=list(map(mp.log,k))
        for i,row in enumerate(tab['polynomials']):
            X=[[number(v) for v in line] for line in old['color'][i]['X']];Z=[[number(v) for v in line] for line in old['color'][i]['Z']]
            traces=[[number(v) for v in line] for line in tab['closure_traces'][i]]
            ex=number(tab['EFT_color'][i]['X']);ez=number(tab['EFT_color'][i]['Z'])
            def pieces(e):
                E=[mp.exp(mp.euler*e)*mp.gamma(1+e)*mp.exp(-e*v) for v in lg]
                kap=30-17*e-2*e*e;full=mp.mpf(0);mixed=mp.mpf(0);hard=mp.mpf(0)
                for r in range(5):
                    for t in range(5):
                        v=E[r]*E[t]*(kap*e/(e-1)*X[r][t]*k[t]/k[r]-12*Z[r][t]);full+=v
                        if r>0 and t>0:hard+=v
                for r in range(1,5):
                    a,b,c=traces[r];mixed+=E[0]*E[r]*(kap*e/(e-1)*(a*k[r]/dd+c*dd/k[r])+24*b)
                eft=E[0]*E[0]*(kap*e/(e-1)*ex-12*ez)
                return full,mixed,eft,hard
            for e in [mp.mpf('1.25'),mp.mpf('0.1')]:
                full,mix,eft,hard=pieces(e);near(hard,full-mix-eft);errors.append(abs(hard-full+mix+eft)/(1+abs(hard)))
            def diff(e):
                full,mix,eft,hard=pieces(e);return full-mix-eft
            sub={z:0,zz:s.pi**2/6,**{h:s.log(v) for h,v in zip(hs,[s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)])}}
            for order,q in [(0,'-2'),(1,'-1'),(2,'0')]:
                got=mp.diff(diff,0,order)/mp.factorial(order)
                want=mp.mpf(str(s.N(parse(row['hard_bare_remainder'][q]).subs(sub),85)))
                near(got,want);errors.append(abs(got-want)/(1+abs(want)))
    return mp.nstr(max(errors),12)

def main():
    start=time.perf_counter();timer=threading.Timer(240,lambda:os._exit(124));timer.daemon=True;timer.start()
    a=packed(HERE/'primary_tables.json.gz');b=packed(HERE/'replay_tables.json.gz');assert a==b
    old=packed(CAL/'canonical_so10_vector_quartic_primitive/primary_v2_tables.json.gz')
    for role in ['primary','replay']:
        r=json.loads((HERE/(role+'_result.json')).read_bytes());raw=gzip.decompress((HERE/(role+'_tables.json.gz')).read_bytes())
        assert sha256(raw).hexdigest()==r['tables_sha256']
    signs=tree_and_operators(a);controls=exact_partition(a,old)
    print('STAGE independent_entire_Mellin_partition',flush=True);error=mellin_partition(a,old)
    result={'schema':'C1_VECTOR_QUARTIC_IR_MATCHING_VALIDATION_V1','execution_state':'COMPLETED',
      'status':'QUALIFIED_ACTUAL_QUARTIC_MIXED_AND_ALL_LIGHT_IR_SUBTRACTION_WITH_BARE_HARD_REMAINDER',
      'scientific_acceptance':'NOT_PERFORMED','scientific_authority':'34/39_UNCHANGED',
      'all35_full_open_operators_and_zero_complements_checked':True,'all144_tree_brackets_and_metric_orbit_maps_checked':True,
      'whole_mass_assignment_IR_partition_before_Laurent_and_IR_limits':True,
      'hard_double_poles':[row['hard_bare_remainder']['-2'] for row in a['polynomials']],
      'max_scaled_Mellin_partition_error':error,'wrong_antisymmetric_sign_controls':signs,
      'other_negative_controls':controls,'UV_forests_or_complete_finite_C1_qualified':False,
      'finite_scheme_or_physical_mass_adopted':False,'full_EFT_or_E5_promoted':False,
      'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
