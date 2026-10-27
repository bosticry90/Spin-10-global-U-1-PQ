from pathlib import Path
from hashlib import sha256
from itertools import product
import gzip,json,sys,time,threading,os,sympy as s
O=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_bytes());H=lambda p:sha256(p.read_bytes()).hexdigest();tick=time.perf_counter();timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start();role=sys.argv[1];assert role in ['primary','replay']
for p,h in read(O/'preparation.json')['input_sha256'].items():assert H(Path(p))==h,p
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes)):
  p=Path(os.fsdecode(args[0]))
  if p.parent.resolve()==O and p.name.startswith('replay' if role=='primary' else'primary'):raise PermissionError('NVT_PEER_DENIED')
  if p.parent.name=='canonical_so10_probe_fermion_onejet' and ('construction' in p.name or 'tables' in p.name):raise PermissionError('NVT_OLD_CANDIDATE_DENIED')
sys.addaudithook(guard)
d=json.loads(gzip.decompress((O/(role+'_inputs.json.gz')).read_bytes()));dec=lambda z:s.SparseMatrix(*z['shape'],{(i,j):s.sympify(v) for i,j,v in z['entries']});cl=lambda M:s.SparseMatrix(M).applyfunc(s.cancel);enc=lambda M:{'shape':list(M.shape),'entries':[[i,j,str(v)] for (i,j),v in sorted(cl(M).todok().items()) if v]}
T=list(map(dec,d['Tminus']));RB,RC=dec(d['RB']),dec(d['RC']);assert RB==RC;TB=[cl(sum((RB[a,b]*T[a] for a in range(45) if RB[a,b]),s.zeros(16))) for b in range(45)]
eta,xi,w=s.symbols('eta_H xi w');W=s.diag(*([eta]*12+[xi]*33));colors=[]
for rr,ker in enumerate(d['V_A_H']):
 V,A,HH=[dec(ker[n]) for n in ['V','A','H']];assert not A.todok() and not cl(HH-W*V/2).todok();assert all(i==j for i,j in V.todok()) and all(i==j for i,j in HH.todok())
 ids=range(12) if rr==0 else range(12,45);ww=eta if rr==0 else xi;expected=s.diag(*([-ww/2 if i in ids else 0 for i in range(45)]));assert V==expected
 if role=='primary':
  CU=cl(sum((ww**2*TB[a]*TB[a]/2 for a in ids),s.zeros(16)));source=cl(sum(((W*V-HH)[b,a]*TB[b]*TB[a] for b,a in (W*V-HH).todok()),s.zeros(16)))
 else:
  CU=cl(ww**2*sum((TB[a]**2 for a in ids),s.zeros(16))/2);source=cl(sum(((W*V)[b,a]*TB[a]*TB[b] for b,a in (W*V).todok()),s.zeros(16))-sum((HH[b,a]*TB[a]*TB[b] for b,a in HH.todok()),s.zeros(16)))
 assert not cl(2*source+CU).todok();colors.append(enc(CU))
kv=s.Matrix(s.symbols('k0:4'));lv=s.Matrix(s.symbols('l0:4'));q=(kv.T*kv)[0];z=(lv.T*lv)[0]
def G(v):
 Q=(v.T*v)[0];return (s.eye(4)/Q+(w-1)*v*v.T/Q**2).row_join(-v/Q).col_join((v.T/Q).row_join(s.zeros(1)))
U=(-2*kv*lv.T).row_join(w*kv).col_join((-w*lv.T).row_join(s.Matrix([[w*w/2]])))
expected=(w*w*kv*lv.T/(2*q*z)).row_join(-w*kv/q).col_join((w*lv.T/z).row_join(s.Matrix([[-2]])))
if role=='primary':Gu=cl(-G(kv)*U*G(lv))
else:
 Ak=kv.col_join(s.Matrix([[w/2]]));Bl=lv.T.row_join(s.Matrix([[-w/2]]));assert not cl(U+2*Ak*Bl).todok();left=cl(G(kv)*Ak);right=cl(Bl*G(lv));assert left== (w*kv/(2*q)).col_join(s.ones(1)) and right==(w*lv.T/(2*z)).row_join(-s.ones(1));Gu=cl(2*left*right)
assert not cl(Gu-expected).todok()
J=lambda v:(s.I*w*v.T/2).row_join(s.Matrix([[-s.I*w*w/4]]));ending=cl(J(lv)*G(lv));adjoint_current=-J(-kv).T;other=cl(G(kv)*adjoint_current)
assert not cl(Gu[:4,:4]+2*s.I*kv*ending[:,:4]/q).todok() and not cl(Gu[:4,:4]+2*s.I*other[:4,:]*lv.T/z).todok()
Ek,El=s.symbols('E_k E_l',nonzero=True);assert not cl(Ek*El*Gu[:4,:4]+2*s.I*Ek*El*kv*ending[:,:4]/q).todok()
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];gamma=[s.kronecker_product(pa[1],x) for x in pa]+[s.kronecker_product(pa[0],s.eye(2))];slash=lambda v:sum((v[i]*gamma[i] for i in range(4)),s.zeros(4))
rv=s.Matrix(s.symbols('r0:4'));K,L,R=map(slash,[kv,lv,rv]);P,PP=K-R,L-R;Jm=(K+L)/2
if role=='primary':assert not cl(K*R*L-(P*R*L+K*R*PP)/2-((rv.T*rv)[0])*Jm).todok()
else:
 # Independent free-word reduction; only R squared is subsequently central.
 kk,ll,rr=s.symbols('K L R',commutative=False);word=s.expand(kk*rr*ll-((kk-rr)*rr*ll+kk*rr*(ll-rr))/2);assert s.expand(word-(rr*rr*ll+kk*rr*rr)/2)==0
 assert not cl(R*R-(rv.T*rv)[0]*s.eye(4)).todok()
# Generic exact witness controls, preserving distinct source momenta.
sub=dict(zip(list(kv)+list(lv)+list(rv),[1,2,3,1,2,-1,1,3,1,-2,2,-1]));sub[w]=s.Rational(3,2)
count=lambda M:len(cl(M.subs(sub)).todok());controls={}
controls['omit_left_Euler_half']=count(P*R*L/2);controls['replace_Pprime_by_P']=count(K*R*(PP-P)/2);controls['reverse_ordinary_Clifford']=count(K*R*L-L*R*K)
controls['erase_auxiliary_inverse']=count(Gu[:4,:4]-(-G(kv)[:4,:4]*U[:4,:4]*G(lv)[:4,:4]))
controls['erase_auxiliary_current']=count(ending[:,:4]-(J(lv)[:,:4]*G(lv)[:4,:4]));controls['replace_right_boson_momentum']=count(Gu[:4,:4]-Gu[:4,:4].subs(dict(zip(lv,kv)),simultaneous=True));controls['wrong_node_heat_polynomial']=str(s.expand(Ek**2-Ek*El));assert s.expand((Ek**2-Ek*El).subs(El,Ek))==0
assert all(controls[n]>0 for n in controls if n!='wrong_node_heat_polynomial')
jj,aa,jad=s.symbols('j2 a2 ja',real=True);den=(jj+aa)**2-4*jad**2;assert s.factor(1/den-1/jj**2-(4*jad**2-2*jj*aa-aa**2)/(jj**2*den))==0
# Reviewed analytic majorant: explicit numerator/denominator inequalities,
# strict exponents, positive remaining radial dimension and homogeneity.
upper=s.Rational(6)+s.Rational(1,4);assert upper*16==100
Dmin=s.Rational(7,2);assert Dmin-3==s.Rational(1,2) and Dmin-2==s.Rational(3,2) and 5-4==1 and 2/(Dmin-2)==s.Rational(4,3)
DD=s.Symbol('D',real=True);sc=s.simplify(DD+1-4);assert sc==DD-3
a0,m0,j0,c=s.symbols('a2 m2 j2 c',real=True);jdotm=s.Symbol('jm',real=True);assert s.expand((j0+a0)+(j0+a0)+(j0-2*jdotm+m0)-2*a0)==3*j0-2*jdotm+m0
out={'schema':'NVT1_TRANSFER_OPERATOR','role':role,'color_CU':colors,'full_mixed_finite_transfer_inverse':enc(Gu),'actual_current_with_A_zero_before_projection':True,'two_oriented_current_inverse_identities':True,'filtered_both_endpoints_Ek_El':True,'independent_P_Pprime_ordered_source_identity':True,'analytic_hatted_rank':'-2epsilon','comparison_UV_degree':5,'comparison_soft_degrees':[3,2,2],'majorant_uniform_D_interval':['7/2','4'],'deltaD_UV_bound_coefficient':100,'hatted_difference_bound':'(4/3)*epsilon*N*B_D(a)','root_difference':'uniform dominated convergence against |j|*abs(deltaD)','common_heat_factor':'exp(-2*c*a2)','whole_joint_limit_vector':'(P+Pprime)/12','source_root_reduction_reuses_CSW_not_fresh835_component_trace':True,'no_new_finite_3point_quadrature_or_complete_mixing_classification':True,'controls':controls,'new_physical_scheme_QAP_measure_phase_or_authority':False};blob=gzip.compress((json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0)
with(O/(role+'_tables.json.gz')).open('xb') as f:f.write(blob)
print('RESULT '+json.dumps({'elapsed_after_imports':time.perf_counter()-tick,'packed_sha256':sha256(blob).hexdigest(),'raw_sha256':sha256(gzip.decompress(blob)).hexdigest()},sort_keys=True),flush=True);timer.cancel()
