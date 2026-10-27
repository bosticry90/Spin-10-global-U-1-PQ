"""FYV1 explicit actual/reference projected gamma chains and finite residues."""
from data import *
from itertools import product
start=begin('primary')
def zero(M):assert not s.SparseMatrix(M).applyfunc(s.expand).todok()
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
g4=[s.kronecker_product(pa[1],a) for a in pa]+[s.kronecker_product(pa[0],s.eye(2))]
gs=[s.kronecker_product(g,pa[2]) for g in g4]+[s.kronecker_product(s.eye(4),a) for a in pa[:2]]
chi=s.prod(g4);U=s.kronecker_product(chi,s.Matrix([0,1]));chis=[s.prod(gs[:4]),s.I*s.prod(gs)];k=s.symbols('k0:6');D=s.Symbol('d');h=s.Symbol('h')
def avg(a):
 out=0
 for powers,c in s.Poly(s.expand(a),*k).terms():
  if any(v%2 for v in powers):continue
  n=sum(powers)//2;out+=c*s.prod(s.factorial2(v-1) for v in powers)/s.prod(D+2*j for j in range(n))
 return s.factor(out)
def extract(M,pp):
 projected=U.H*M*U;p4=(s.eye(4)+(1 if pp==0 else -1)*chi)/2;out=s.factor(s.trace(p4*projected)/2);zero(projected-out*p4);return out
phase=[s.S.One,s.S.One,s.I,s.I,-s.I,-s.I];keys=['E_F','E_L','L_F','L_L','R_F','R_L'];samples={key:[] for key in keys};actual=None;conjugate={key:[] for key in keys}
for nh in range(3):
 for kind in range(2):
  ng=4 if kind==0 else 4+nh;cc=chis[kind];P=(s.eye(8)+cc)/2;Q=s.eye(8)-P;ss=sum((k[j]*gs[j] for j in range(ng)),s.zeros(8));K2=sum(v*v for v in k[:ng]);GK=ss*cc
  mats=[sum((g*cc*ss*P*ss*g*cc for g in gs[:ng]),s.zeros(8)),GK*ss*P*ss*GK,GK*ss*P,GK*ss*P*K2,P*ss*GK,P*ss*GK*K2]
  units=[s.factor(ph*extract(mat.applyfunc(avg),0)) for ph,mat in zip(phase,mats)]
  anti=[sum((g*cc*ss*Q*ss*g*cc for g in gs[:ng]),s.zeros(8)),GK*ss*Q*ss*GK,GK*ss*Q,GK*ss*Q*K2,Q*ss*GK,Q*ss*GK*K2]
  antiunits=[s.factor(ph*extract(mat.applyfunc(avg),1)) for ph,mat in zip(phase,anti)]
  if kind==0:
   if actual is None:actual=dict(zip(keys,units))
   else:assert actual==dict(zip(keys,units))
  else:
   for key,v,av in zip(keys,units,antiunits):samples[key].append(v);conjugate[key].append(av)
ref={key:s.factor(s.interpolate(list(enumerate(vals)),h)) for key,vals in samples.items()}
anti={key:s.factor(s.interpolate(list(enumerate(vals)),h)) for key,vals in conjugate.items()}
eps,m=s.symbols('epsilon m_IR',positive=True);dim=4-2*eps
def radial_regular(power):return m**(-2*eps)*s.gamma(power+dim/2)*s.gamma(1+eps)/(s.gamma(dim/2)*s.gamma(power+2))
finite={};deltas={};radial=[]
for key in keys:
 power=2 if key.endswith('_L') else 1;rr=radial_regular(power);radial.append(str(s.simplify(rr.subs(eps,0))))
 diff=(actual[key]-ref[key].subs(h,-2*eps)).subs(D,dim);reg=diff*rr
 assert s.simplify(reg.subs(eps,0))==0
 finite[key]=s.simplify(s.diff(reg,eps).subs(eps,0));deltas[key]=str(s.factor(diff))
# Projector routing for the pure-Yukawa triangle is checked with both chi.
paths={}
for kind,cc in enumerate(chis):
 Ps=[(s.eye(8)+cc)/2,(s.eye(8)-cc)/2]
 for j in range(4 if kind==0 else 6):
  for a,b,c in product(range(2),repeat=3):
   mat=U.H*Ps[a]*gs[j]*Ps[b]*gs[j]*Ps[c]*U;want=(s.eye(4)+(1 if a==0 else -1)*chi)/2 if a==c and a!=b else s.zeros(4);zero(mat-want)
   paths[f'{kind}_{j}_{a}{b}{c}']=bool(want!=s.zeros(4))
YPP=packed(CAL/'canonical_so10_yukawa_polarization_poles/primary_tables.json.gz')
for row in YPP['unconjugated_sums']:zero(dec(row))
G=packed(CAL/'canonical_so10_gauge_yukawa_vertex_poles/primary_tables.json.gz');YCT=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');Bs=[dec(YCT[n]) for n in ['B10','B126']];CI,CH=map(dec,G['fermion_Casimir_I_H']);CW=WM*CI+(WH-WM)*CH;I=s.eye(16)
models=[]
for rr,B in enumerate(Bs):
 ji=dec(G['models'][rr]['J_I']);jh=dec(G['models'][rr]['J_H']);jw=WM*ji+(WH-WM)*jh
 li=s.kronecker_product(CI.T,I)*B+ji;lw=s.kronecker_product(CW.T,I)*B+jw;ri=s.kronecker_product(I,CI.T)*B+ji;rw=s.kronecker_product(I,CW.T)*B+jw
 E=(finite['E_F']*ji+finite['E_L']*(jw-ji)).applyfunc(s.expand)
 LL=(s.I*finite['L_F']*li+s.I*finite['L_L']*(lw-li)).applyfunc(s.expand)
 RR=(s.I*finite['R_F']*ri+s.I*finite['R_L']*(rw-ri)).applyfunc(s.expand)
 models.append({'exchange':enc(E),'scalar_left':enc(LL),'scalar_right':enc(RR),'total':enc((E+LL+RR).applyfunc(s.expand))})
finish('primary',{'method':'projected_gamma8_hat_rank_polynomial_and_retained_radial_Gamma_limits','actual_raw_angular':{k:str(v) for k,v in actual.items()},'reference_raw_angular_polynomial':{k:str(v) for k,v in ref.items()},'reference_conjugate_raw_polynomial':{k:str(v) for k,v in anti.items()},
 'raw_finite_difference_units':{k:str(v) for k,v in finite.items()},'evanescent_angular_differences':deltas,'radial_residues':radial,'models':models,
 'pure_Yukawa_paths':paths,'pure_Yukawa_finite_difference':'0_BY_CHECKED_CHIRAL_PATH_AND_BOUND_FULL_POLARIZATION','polarization_tensor_positions_reused':4*256**2,
 'full_internal_hat_gauge_and_scalar_current_vertices':True,'widths_symbolic':True,'general_family_extension':'Y_R tensor B_R_NO_TRACE_NO_EXTRA3','new_two_loop_integrals':0,'physical_scheme_or_finite_parameter_counterterm_adopted':False},start)
