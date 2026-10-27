"""FYV1 Clifford reductions, Beta angular moments and Casimir transport."""
from data import *
start=begin('replay')
eps,m=s.symbols('epsilon m_IR',positive=True);d=4-2*eps
# Gaussian/Beta moments for bar rank4 inside d-dimensional loop space.
# E[rho^n]=B(2+n,d/2-2)/B(2,d/2-2); Gamma recurrence is its analytic form.
def moment(n):return s.prod(2+j for j in range(n))/s.prod(d/2+j for j in range(n))
a=moment(1);b=moment(2)
# Anticommuting chi reduces exchange F to -m_rank*K^2 and exchange L
# to -K^4. Mixed endpoints give opposite raw gamma signs, whose distinct
# action-derived phases make both scalar branches -i times the moment.
raw_actual={'E_F':-4*a,'E_L':-b,'L_F':-s.I*a,'L_L':-s.I*b,'R_F':-s.I*a,'R_L':-s.I*b}
raw_ref={'E_F':-d,'E_L':-1,'L_F':-s.I,'L_L':-s.I,'R_F':-s.I,'R_L':-s.I}
finite={}
for key in raw_actual:
 p=2 if key.endswith('_L') else 1
 schwinger=m**(-2*eps)*s.gamma(1+eps)*s.prod(d/2+j for j in range(p))/s.factorial(p+1)
 reg=s.factor(raw_actual[key]-raw_ref[key])*schwinger
 assert s.simplify(reg.subs(eps,0))==0
 finite[key]=s.simplify(s.diff(reg,eps).subs(eps,0))
# Explicit finite wrong contraction: premature actual Gbarbar*kbar=W*kbar/k2
# replaces the mixed longitudinal b by a. It has the same pole, different finite.
wrongreg=(-s.I*a+s.I)*s.gamma(1+eps)*(d/2)*(d/2+1)/6
wronglong=s.simplify(s.diff(wrongreg,eps).subs(eps,0))
G=packed(CAL/'canonical_so10_gauge_yukawa_vertex_poles/replay_v2_tables.json.gz');YCT=packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz');Bs=[dec(YCT[n]) for n in ['B10','B126']];CI,CH=map(dec,G['fermion_Casimir_I_H']);CSI,CSH=map(dec,G['scalar_Casimir_I_H']);CW=WM*CI+(WH-WM)*CH;I=s.eye(16);models=[]
for B in Bs:
 ci=(s.kronecker_product(CI.T,I)+s.kronecker_product(I,CI.T))*B;ch=(s.kronecker_product(CH.T,I)+s.kronecker_product(I,CH.T))*B
 ji=(B*CSI-ci)/2;jh=(B*CSH-ch)/2;jw=WM*ji+(WH-WM)*jh
 # Covariance supplies the two independently labelled endpoint structures.
 li=s.kronecker_product(CI.T,I)*B+ji;ri=s.kronecker_product(I,CI.T)*B+ji
 lw=s.kronecker_product(CW.T,I)*B+jw;rw=s.kronecker_product(I,CW.T)*B+jw
 E=(finite['E_F']*ji+finite['E_L']*(jw-ji)).applyfunc(s.expand)
 LL=(s.I*finite['L_F']*li+s.I*finite['L_L']*(lw-li)).applyfunc(s.expand)
 RR=(s.I*finite['R_F']*ri+s.I*finite['R_L']*(rw-ri)).applyfunc(s.expand)
 models.append({'exchange':enc(E),'scalar_left':enc(LL),'scalar_right':enc(RR),'total':enc((E+LL+RR).applyfunc(s.expand))})
# Independent formal two-state selector: every full-AC fermion numerator
# flips chirality. Scalar endpoints therefore carry the same polarization.
roles={f'{a}{b}{c}':(a==c and a!=b) for a in range(2) for b in range(2) for c in range(2)}
YPP=packed(CAL/'canonical_so10_yukawa_polarization_poles/replay_v2_tables.json.gz')
assert YPP.get('unconjugated_sums') is not None
for row in YPP['unconjugated_sums']:assert not s.SparseMatrix(dec(row)).todok()
finish('replay',{'method':'Clifford_Beta_moments_Schwinger_residue_and_scalar_Casimir_reconstruction','raw_finite_difference_units':{k:str(v) for k,v in finite.items()},'wrong_premature_width_collapse_longitudinal_unit':str(wronglong),
 'models':models,'pure_Yukawa_formal_roles':roles,'pure_Yukawa_finite_difference':'0_BY_CHECKED_CHIRAL_PATH_AND_BOUND_FULL_POLARIZATION','polarization_tensor_positions_reused':4*256**2,
 'full_internal_hat_gauge_and_scalar_current_vertices':True,'widths_symbolic':True,'general_family_extension':'Y_R tensor B_R_NO_TRACE_NO_EXTRA3','new_two_loop_integrals':0,'physical_scheme_or_finite_parameter_counterterm_adopted':False},start)
