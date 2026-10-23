"""CSB1 exact pairwise lower bound plus a saturating all-component witness."""
from data import *
def dual(A,B):
 assert len(A)==len(B)==3 and all(v>0 for v in B)
 bounds=[(abs(B[j]*A[i]-B[i]*A[j])/(B[i]+B[j]),i,j) for i in range(3) for j in range(i+1,3)]
 T,i,j=max(bounds);L=-(A[i]+A[j])/(B[i]+B[j]);res=[a+b*L for a,b in zip(A,B)]
 assert max(map(abs,res))==T
 return T,L,res,bounds
def main():
 start=begin('primary');mp.mp.dps=100;src=packed(CAL/'canonical_so10_bosonic_interior_assembly/primary_tables.json.gz');cases={}
 for key in ['1/2','3/4','1']:
  x=F(key);p=src['cases'][key]['lambda2_L_polynomial'];A=[-x*F(v[0]) for v in p];B=[-x*F(v[1]) for v in p];T,L,res,bounds=dual(A,B)
  lo=max((-TAU_HI-a)/b for a,b in zip(A,B));hi=min((TAU_HI-a)/b for a,b in zip(A,B));separate=[a+b*(-a/b) for a,b in zip(A,B)]
  omitted=[next(v for v,i,j in bounds if k not in [i,j]) for k in range(3)]
  cases[key]={'A':list(map(str,A)),'B':list(map(str,B)),'minimum_unscaled':str(T),'witness_L':str(L),'residuals_unscaled':list(map(str,res)),
   'pair_bounds':[{'pair':[i,j],'bound':str(v)} for v,i,j in bounds],'normalized_minimum':fmt(q(T)/(768*mp.pi**4)),
   'coarse_normalized_lower':str(T/TAU_HI),'coarse_normalized_upper':str(T/TAU_LO),'loose_tree_interval':[str(lo),str(hi)],'feasible_loose_tree':lo<=hi,
   'separate_scales_residuals':list(map(str,separate)),'omitted_constraint_minima':list(map(str,omitted)),
   'L0_normalized':list(map(lambda v:fmt(q(v)/(768*mp.pi**4)),A))}
 finish('primary',{'schema':'CSB1','cases':cases,'tau_lo':str(TAU_LO),'tau_hi':str(TAU_HI),'physical_scale_adopted':False,'RG_trajectory_or_full_theory_exclusion':False,'scientific_acceptance':'NOT_PERFORMED'},start)
if __name__=='__main__':main()
