"""VHR1 support-matrix powers, independently supplied roots and Gamma weights."""
from data import *
t=begin('replay');M=roots('replay');types=sorted({x for a,b,_ in G for x in [a,b]});X=defaultdict(list)
for a,k,gt in G:
 for kk,b,vt,degree in V:
  if k==kk:X[a,b].append((degree,(gt+'/'+vt,)))
power={(a,a):[(ZERO,())] for a in types};words=[]
for n in range(5):
 for a,b,root,degree in M:
  for d,path in power.get((b,a),[]):
   if plus(d,degree)==TARGET:words.append({'root':root,'n':n,'path':list(path),'sign':(-1)**n,'heat_lengths':[2*n,2*n+2]})
 nxt=defaultdict(list)
 for (a,k),rows in power.items():
  for b in types:
   for da,wa in rows:
    for db,wb in X.get((k,b),[]):
     dd=plus(da,db)
     if allowed(dd):nxt[a,b].append((dd,wa+wb))
 power=nxt
assert not power,'EXTERNAL_LABEL_BOUND_MUST_EMPTY_N5'
words.sort(key=lambda x:(x['n'],x['root'],x['path']));eps=s.Symbol('eps',positive=True);rad={str(n):str(s.expand_log(s.limit(s.gamma(eps)*((2*n)**(-eps)-(2*n+2)**(-eps)),eps,0),force=True)) for n in sorted({w['n'] for w in words})}
finish('replay',{'method':'free_noncommutative_support_matrix_powers_and_Gamma_radial_limit','words':words,'all_actual_roots':[list(x) for x in M],'target_degree':list(TARGET),'n_bound_from_external_labels':4,'radial_weights':rad,'nonzero_roots':sorted({w['root'] for w in words})},t)
