from data_v3 import *
SECTORS=[('Phi',54),('Sigma',252),('phi',20),('S',2)]
def begin4(role):
 t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
 for p,h in read(HERE/'preparation_v4.json')['input_sha256'].items():assert digest(Path(p))==h,p
 def guard(event,args):
  if event=='open' and args and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0]));peer='orbit_replay_v4' if role=='primary' else 'orbit_primary_v4'
   if p.parent.resolve()==HERE and p.name.startswith(peer):raise PermissionError('DSW1_ORBIT_PEER_DENIED')
 sys.addaudithook(guard);return t
def finish4(role,out,t):
 out.update({'elapsed_after_imports':time.perf_counter()-t,'full_quantum_two_Q_QAP_E5A5_qualified':False,'authority':'34/39','scientific_acceptance':'NOT_PERFORMED'})
 raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
 with (HERE/('orbit_'+role+'_v4_tables.json.gz')).open('xb') as f:f.write(blob)
 print('RESULT '+json.dumps({'elapsed_after_imports':out['elapsed_after_imports'],'packed_sha256':sha256(blob).hexdigest(),'tables_sha256':sha256(raw).hexdigest()},sort_keys=True),flush=True)
def frozen_columns():
 old=packed(HERE/'primary_v2_tables.json.gz');return [fromrows(ps) for ps in old['source_columns']['GF_Xv']],[fromrows(ps) for ps in old['source_columns']['source_Ja']],old['pieces']['GF_Xv']
def contraction_witness(mats,grads):
 target=((f'JLp14',()),(f'Cp13',()),(f'Cp14',()));color=[p.get(target,0) for p in grads];W=tidy(sum((z*m for z,m in zip(color,mats) if z),s.SparseMatrix(54,54,{})));assert W.todok();(j,a),z=next(iter(sorted(W.todok().items())))
 return {'remaining_source':14,'ghost_pair':[13,14],'scalar_sector':'Phi','x_index':j,'z_or_h_index':a,'coefficient_without_gxi_g4log2_16pi2':str(z),'color_vector':list(map(str,color)),'complete_matrix':enc(W)}
