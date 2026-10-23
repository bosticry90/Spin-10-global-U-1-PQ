"""CSB1 exact simultaneous interval feasibility, independent of the dual code."""
from data import *
def interval(A,B,t):return max((-t-a)/b for a,b in zip(A,B)),min((t-a)/b for a,b in zip(A,B))
def solve(A,B):
 assert len(A)==len(B)==3 and all(v>0 for v in B)
 # Cross the affine lower and upper endpoint lines; no pairwise abs bound.
 candidates={F(0)}
 for i in range(3):
  for j in range(3):
   c0=-A[i]/B[i]+A[j]/B[j];c1=-1/B[i]-1/B[j];t=-c0/c1
   if t>=0:candidates.add(t)
 for t in sorted(candidates):
  lo,hi=interval(A,B,t)
  if lo<=hi:return t,(lo+hi)/2,[lo,hi],len(candidates)
 raise AssertionError('NO_FINITE_INTERVAL_EXTENSION')
def main():
 start=begin('replay');mp.mp.dps=110;src=packed(CAL/'canonical_so10_bosonic_interior_assembly/replay_tables.json.gz');cases={}
 for key in ['1/2','3/4','1']:
  x=F(key);p=src['cases'][key]['lambda2_L_polynomial'];A=[-x*F(v[0]) for v in p];B=[-x*F(v[1]) for v in p];T,L,optimal,n=solve(A,B)
  assert max(abs(a+b*L) for a,b in zip(A,B))==T
  lo,hi=interval(A,B,TAU_HI)
  cases[key]={'A':list(map(str,A)),'B':list(map(str,B)),'minimum_unscaled':str(T),'witness_L':str(L),'optimal_interval':list(map(str,optimal)),
   'normalized_minimum':fmt(q(T)/(768*mp.pi**4)),'coarse_normalized_lower':str(T/TAU_HI),'coarse_normalized_upper':str(T/TAU_LO),
   'loose_tree_interval':[str(lo),str(hi)],'feasible_loose_tree':lo<=hi,'candidate_count':n,
   'L0_normalized':[fmt(q(a)/(768*mp.pi**4)) for a in A]}
 finish('replay',{'schema':'CSB1','cases':cases,'tau_lo':str(TAU_LO),'tau_hi':str(TAU_HI),'physical_scale_adopted':False,'RG_trajectory_or_full_theory_exclusion':False,'scientific_acceptance':'NOT_PERFORMED'},start)
if __name__=='__main__':main()
