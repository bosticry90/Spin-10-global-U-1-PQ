"""VHR1 historical source rules and independent per-ghost matrix transports."""
from color_data_v4 import *
t=begin3('replay');d=packed(CSW/'replay_inputs.json.gz');B,L,N,cubic=raw_rules(d['field_maps']);G=packed(GTT/'replay_tables.json.gz');Q=dec(G['C3_chart']);Qi=Q.inv();U=dec(G['raw_aux_map']);Ui=U.inv();a={(r,b,c):s.sympify(z) for r,b,c,z in G['raw_jets']['a']};b={(r,b,c):s.sympify(z) for r,b,c,z in G['raw_jets']['B']};VV={k:co(a.get(k,0)-b.get(k,0)) for k in set(a)|set(b)}
def slices(raw):
 out=[s.SparseMatrix(45,45,{}) for c in range(45)]
 for (r,a,c),z in raw.items():out[c][r,a]=z
 return out
BS,LS,NS,VS=map(slices,[B,L,N,VV]);bp={};lp={};np={};vp={};res={}
for c in range(45):
 def combo(mm):return sum((Qi[k,c]*mm[k] for k in range(45) if Qi[k,c]),s.SparseMatrix(45,45,{}))
 BB=(Q*combo(BS)*Qi).applyfunc(co);LL=(Ui*combo(LS)*U).applyfunc(co);NN=(Ui*combo(NS)*U).applyfunc(co);VVV=(Qi.T*combo(VS)*U).applyfunc(co);dd=(VVV-BB.T-LL).applyfunc(co)
 for mat,out in [(BB,bp),(LL,lp),(NN,np),(VVV,vp),(dd,res)]:
  for (r,a),z in mat.todok().items():out[r,a,c]=z
finish3('replay',{'method':'historical_source_only_field_rules_and_per_ghost_matrix_products','betaB':rows(bp),'betaL':rows(lp),'Nanti':rows(np),'Vold':rows(vp),'n3_color_residual':rows(res),'cubic_auxiliary_rows_retained':cubic,'scalar_review':scalar_review('replay',U)},t)
