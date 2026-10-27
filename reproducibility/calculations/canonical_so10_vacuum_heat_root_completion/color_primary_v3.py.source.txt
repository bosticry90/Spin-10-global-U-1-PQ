"""VHR1 actual literal GF and component field/dual transports."""
from color_data_v3 import *
t=begin3('primary');d=packed(CSW/'primary_inputs.json.gz');B,L,N,cubic=raw_rules(d['field_maps']);g=s.Symbol('g10');jets={j:defaultdict(lambda:s.S.Zero) for j in ['a','B','c']}
for row in d['GF']:
 w=row['word'];base=[n.split('__')[0] for n in w]
 if len(w)!=3:continue
 aa=[i for i,n in enumerate(base) if n.startswith(('bar','ub'))];cc=[i for i,n in enumerate(base) if n.startswith('C')];bb=[i for i,n in enumerate(base) if n.startswith('B')]
 if len(aa)!=1 or len(cc)!=1 or len(bb)!=1:continue
 a,c,b=aa[0],cc[0],bb[0];p=next(i for i,n in enumerate(w) if '__' in n);mu=int(w[p].split('__')[1]);r,nu=map(int,base[b][1:].split('_'));assert mu==nu
 if mu!=0:continue
 an=int(base[a][3:] if base[a].startswith('bar') else base[a][2:]);cn=int(base[c][1:]);z=co((-1 if c<a else 1)*s.sympify(row['coefficient'])/g);j='a' if p==a else 'B' if p==b else 'c';jets[j][r,an,cn]+=z
VV={k:co(jets['a'].get(k,0)-jets['B'].get(k,0)) for k in set(jets['a'])|set(jets['B'])};G=packed(GTT/'primary_tables.json.gz');Q=dec(G['C3_chart']);Qi=Q.inv();U=dec(G['raw_aux_map']);Ui=U.inv();CG=dec(G['raw_Gca']);assert not (Q*CG*Ui.T-s.eye(45)).applyfunc(co).todok()
def transport(raw,left,right):
 lr=defaultdict(list);rr=defaultdict(list);cr=defaultdict(list);out=defaultdict(lambda:s.S.Zero)
 for (a,r),z in left.todok().items():lr[r].append((a,z))
 for (r,a),z in right.todok().items():rr[r].append((a,z))
 for (r,a),z in Qi.todok().items():cr[r].append((a,z))
 for (r,a,c),z in raw.items():
  for b,x in lr[r]:
   for u,y in rr[a]:
    for v,w in cr[c]:out[b,u,v]+=x*y*w*z
 return clean(out)
bp=transport(B,Q,Qi);lp=transport(L,Ui,U);np=transport(N,Ui,U);vp=transport(VV,Qi.T,U);res={k:co(vp.get(k,0)-bp.get((k[1],k[0],k[2]),0)-lp.get(k,0)) for k in set(vp)|set(lp)|{(a,r,c) for r,a,c in bp}};res=clean(res)
finish3('primary',{'method':'literal_mu0_GF_and_actual_field_maps_component_intertwiner_transports','betaB':rows(bp),'betaL':rows(lp),'Nanti':rows(np),'Vold':rows(vp),'n3_color_residual':rows(res),'cubic_auxiliary_rows_retained':cubic,'scalar_review':scalar_review('primary',U)},t)
