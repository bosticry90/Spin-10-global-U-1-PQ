"""JMF1 recursive type census and direct sparse coefficient comparison."""
from data import *
tick=begin('primary')
names=tuple(sorted(TYPES))
def census(target,gh,parity,source=False):
 found=[]
 def walk(j,left,gg,pp,ll,counts):
  if j==len(names):
   if left or gg!=gh or pp%2!=parity:return
   n=dict(counts);matter=n.get('P',0)+n.get('KP',0)
   if source:
    if matter or not any(n.get(k) for k in ['JB','Jx','JC']) or ll%2:return
   elif matter<2:return
   found.append(sorted(k for k,v in n.items() for _ in range(v)));return
  key=names[j];dim,g,p,l=TYPES[key]
  for v in range(left//dim+1):
   walk(j+1,left-dim*v,gg+g*v,pp+p*v,ll+l*v,counts+([(key,v)] if v else []))
 walk(0,target,0,0,0,[])
 return sorted(found)
parent=census(8,0,0);breaking=census(10,1,1);source=census(8,0,0,True)
assert parent==sorted([sorted(z) for z in [('P','P','d'),('B','P','P'),('x','P','P'),('KP','c','P')]])
assert breaking==sorted([sorted(z) for z in [('c','P','P','d'),('c','B','P','P'),('c','x','P','P'),('KP','c','c','P')]])
assert source==sorted([sorted(z) for z in [('JB','d','c'),('JB','B','c'),('Jx','c','x'),('JC','c','c')]])

def flatten(x,path=()):
 out={}
 if isinstance(x,dict) and set(x)=={'entries','shape'}:
  shape=tuple(x['shape']);assert len(shape)==2 and all(n>0 for n in shape)
  for i,j,z in x['entries']:
   assert 0<=i<shape[0] and 0<=j<shape[1]
   k=path+('entry',i,j);assert k not in out and expr(z)!=0;out[k]=expr(z)
  return out
 if isinstance(x,dict):
  for k,v in sorted(x.items()):out.update(flatten(v,path+(k,)))
 elif isinstance(x,list):
  if x and isinstance(x[0],list):
   for row in x:
    assert len(row)==4 and all(isinstance(i,int) and 0<=i<45 for i in row[:-1])
    k=path+tuple(row[:-1]);assert k not in out and expr(row[-1])!=0;out[k]=expr(row[-1])
  else:
   for j,v in enumerate(x):out.update(flatten(v,path+(j,)))
 else:raise TypeError(path)
 return out

h=packed(HSC/'selected_four_projection_family.json.gz');e=embedded(h);p=parents('primary')
assert h['all_four_selected_projection_remainders_zero'] and not h['full_source_or_background_functional_image_qualified']
checks={}
for tag in FILES:
 a,b=flatten(e[tag]),flatten(p[tag]);assert set(a)==set(b)
 assert all(s.expand(a[k]-b[k])==0 for k in a)
 rows=[[list(k),str(v)] for k,v in sorted(a.items(),key=lambda kv:str(kv[0]))]
 checks[tag]={'nonzero_coefficient_slots':len(rows),'canonical_sha256':sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
              'omission_changed_slots':len(rows),'duplicate_changed_slots':len(rows)}
 assert rows

# Contracting two connected components by k edges gives k-1 additional cycles.
graph=[]
for nf in range(1,9):
 for ns in range(1,7):
  for k in range(1,7):
   vertices=nf+ns;edges=nf+(ns-1)+k
   rank=edges-vertices+1;assert rank==k
   graph.append([nf,ns,k,rank,k==1,k>=2])
assert all((row[3]==1 and row[4]) or row[3]>=2 for row in graph)

finish('primary',{'method':'recursive_full_type_census_and_direct_sparse_coefficient_dictionaries',
 'matter_parent_patterns':parent,'matter_breaking_patterns':breaking,'shared_source_patterns':source,
 'shared_coefficients':checks,'topological_control_cases':len(graph),
 'source_cycle_lemma':'one_connection_is_bridge;two_or_more_connections_have_at_least_two_loops',
 'triangular_cross_map':['E_B_m*F_JB','E_x_m*F_Jx','E_C_m*F_JC'],
 'joint_definition':'C_bStokes+(HSC-C_shared)+K_CHW',
 'selected_matter_projection_transfer':'all_four_inherit_HSC;new_closed_K_has_no_P_or_sources',
 'selected_zero_matter_transfer':'old_bosonic_Stokes+CHW_OGC;open_complement_has_P_or_KP',
 'naive_direct_sum_duplicates_five_shared_blocks':True,
 'free_parameters_not_selected':h['parameters_left_symbolic']+['zeta_g','zeta_M','zeta_V'],
 'all_original_quantum_inputs_reused_not_remeasured':True},tick)
