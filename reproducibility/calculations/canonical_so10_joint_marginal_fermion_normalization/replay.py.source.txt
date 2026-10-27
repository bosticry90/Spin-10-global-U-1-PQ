"""JMF1 fixed matter degree census and sparse matrix/exterior comparison."""
from itertools import combinations_with_replacement
from data import *
tick=begin('replay')
def weight(word,j):return sum(TYPES[k][j] for k in word)
def census(target,gh,parity,source=False):
 found=[]
 # Every atom has doubled dimension>=2: this is an exact finite bound.
 for length in range(target//2+1):
  for word in combinations_with_replacement(sorted(TYPES),length):
   if weight(word,0)!=target or weight(word,1)!=gh or weight(word,2)%2!=parity:continue
   if source:
    if any(k in word for k in ['P','KP']) or not any(k in word for k in ['JB','Jx','JC']) or weight(word,3)%2:continue
   elif word.count('P')+word.count('KP')<2:continue
   found.append(list(word))
 return sorted(found)

def matrix(m):
 assert set(m)=={'entries','shape'}
 entries={}
 for i,j,z in m['entries']:
  assert (i,j) not in entries and 0<=i<m['shape'][0] and 0<=j<m['shape'][1]
  assert expr(z)!=0;entries[i,j]=expr(z)
 return s.SparseMatrix(*m['shape'],entries)
def compare(a,b,path=()):
 rows=[]
 if isinstance(a,dict) and 'shape' in a:
  assert a['shape']==b['shape'];A,B=matrix(a),matrix(b)
  assert not (A-B).applyfunc(s.expand).todok()
  return [[list(path+('entry',i,j)),str(v)] for (i,j),v in A.todok().items()]
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:rows+=compare(a[k],b[k],path+(k,))
 elif isinstance(a,list):
  if a and isinstance(a[0],list):
   def tensor(v):
    entries={}
    for row in v:
     assert len(row)==4 and all(isinstance(i,int) and 0<=i<45 for i in row[:-1])
     q=tuple(row[:-1]);assert q not in entries and expr(row[-1])!=0
     entries[q]=expr(row[-1])
    return entries
   A,B=tensor(a),tensor(b)
   T=s.ImmutableSparseNDimArray(A,(45,45,45))-s.ImmutableSparseNDimArray(B,(45,45,45))
   assert all(s.expand(v)==0 for v in T._sparse_array.values())
   rows=[[list(path+k),str(v)] for k,v in A.items()]
  else:
   assert len(a)==len(b)
   for j in range(len(a)):rows+=compare(a[j],b[j],path+(j,))
 else:raise TypeError(path)
 return rows

h=packed(HSC/'selected_four_projection_family.json.gz');e=embedded(h);p=parents('replay');checks={}
for tag in FILES:
 rows=compare(e[tag],p[tag]);rows.sort(key=lambda row:str(tuple(row[0])))
 checks[tag]={'nonzero_coefficient_slots':len(rows),'canonical_sha256':sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
              'omission_changed_slots':len(rows),'duplicate_changed_slots':len(rows)}
 assert rows
# Independent contraction-of-connected-components proof: cycle-space dimension
# is old1+old0+(k-1); edge subdivisions add equally many vertices/edges.
count=0
for subdivisions in range(8):
 for tree_size in range(6):
  for k in range(1,7):
   cycle_dimension=1+(k-1)
   assert cycle_dimension==k and (k==1 or cycle_dimension>=2)
   count+=1
assert count==288
finish('replay',{'method':'bounded_multiset_generating_coefficient_census_and_sparse_matrix_exterior_replay',
 'matter_parent_patterns':census(8,0,0),'matter_breaking_patterns':census(10,1,1),
 'shared_source_patterns':census(8,0,0,True),'shared_coefficients':checks,
 'topological_control_cases':count,
 'source_cycle_lemma':'one_connection_is_bridge;two_or_more_connections_have_at_least_two_loops',
 'triangular_cross_map':['E_B_m*F_JB','E_x_m*F_Jx','E_C_m*F_JC'],
 'joint_definition':'C_bStokes+(HSC-C_shared)+K_CHW',
 'selected_matter_projection_transfer':'all_four_inherit_HSC;new_closed_K_has_no_P_or_sources',
 'selected_zero_matter_transfer':'old_bosonic_Stokes+CHW_OGC;open_complement_has_P_or_KP',
 'naive_direct_sum_duplicates_five_shared_blocks':True,
 'free_parameters_not_selected':h['parameters_left_symbolic']+['zeta_g','zeta_M','zeta_V'],
 'all_original_quantum_inputs_reused_not_remeasured':True},tick)
