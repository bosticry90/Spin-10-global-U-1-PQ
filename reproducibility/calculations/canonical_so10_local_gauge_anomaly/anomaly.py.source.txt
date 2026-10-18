"""Local representation anomaly screen: chiral weights and left-SM charge sums."""
from pathlib import Path
from hashlib import sha256
from itertools import product
from fractions import Fraction as F
import json,sys,time
import sympy as s
R=Path(__file__).resolve().parents[2];C=R/'calculations';O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def main():
    started=time.perf_counter();prep=read(O/'preparation.json');writes=[]
    def readonly(event,args):
        if event=='open' and len(args)>1 and isinstance(args[1],str) and any(z in args[1] for z in 'wax+'):
            writes.append(str(args[0]));raise PermissionError('LOCAL_ANOMALY_WRITE_DENIED')
    sys.addaudithook(readonly)
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    old=read(C/'canonical_so10_pq_anomaly_screen/original_result.json');weights=[tuple(s.Rational(z,2) for z in signs) for signs in product([1,-1],repeat=5) if signs.count(-1)%2==0];assert [[str(z) for z in w] for w in weights]==old['chiral_spinor_weights'];x=s.symbols('x0:5');dot=lambda w:sum(a*b for a,b in zip(w,x));cubic=s.Poly(s.expand(sum(dot(w)**3 for w in weights)),*x);linear=s.expand(sum(dot(w) for w in weights));assert cubic.as_expr()==linear==0
    monomials=[a for a in product(range(4),repeat=5) if sum(a)==3];assert len(monomials)==35 and all(cubic.coeff_monomial(a)==0 for a in monomials)
    moment5=sum(sum(w)**5 for w in weights);assert moment5==60 and sum(sum(w)**5 for w in weights+[tuple(-z for z in w) for w in weights])==0
    quadratic=[[sum(w[i]*w[j] for w in weights) for j in range(5)] for i in range(5)];assert quadratic==s.diag(*([4]*5)).tolist()
    # Columns: name, color dimension, weak dimension, left hypercharge, cubic color index.
    matter=[('Q',3,2,s.Rational(1,6),1),('uc',3,1,-s.Rational(2,3),-1),('dc',3,1,s.Rational(1,3),-1),('L',1,2,-s.Rational(1,2),0),('ec',1,1,s.Integer(1),0),('nc',1,1,s.Integer(0),0)]
    def screen(rows):
        return {'SU3_cubic':sum(w*a for _,c,w,y,a in rows),'SU3_squared_Y':sum(w*y/2 for _,c,w,y,a in rows if c==3),'SU2_squared_Y':sum(c*y/2 for _,c,w,y,a in rows if w==2),'Y_cubic':sum(c*w*y**3 for _,c,w,y,a in rows),'Y_gravity':sum(c*w*y for _,c,w,y,a in rows)}
    sm=screen(matter);assert all(z==0 for z in sm.values());bad=screen([z for z in matter if z[0]!='uc']);assert bad['Y_cubic']==s.Rational(8,9) and bad['SU3_cubic']==1
    gen=3;assert old['left_Weyl_generations']==gen;nc=2*gen*sum(s.Rational(w,2) for _,c,w,y,a in matter if c==3);nw=2*gen*sum(s.Rational(c,2) for _,c,w,y,a in matter if w==2);ny=2*gen*sum(c*w*y*y for _,c,w,y,a in matter);grav=gen*sum(c*w for _,c,w,_,_ in matter);ne=2*gen*sum(c*sum((y+t)**2 for t in [s.Rational(1,2),-s.Rational(1,2)]) if w==2 else c*y*y for _,c,w,y,a in matter)
    assert nc==nw==12 and ny==20 and s.Rational(3,5)*ny==12 and ne==32 and grav==48 and str(nc)==old['N_color'] and str(ne)==old['E_electromagnetic']
    missing=s.expand(sum(dot(w)**3 for w in weights[1:]));assert missing==-dot(weights[0])**3 or s.expand(missing+dot(weights[0])**3)==0;assert missing!=0
    for n,h in prep['input_sha256'].items():assert digest(R/n)==h,n
    assert not writes and time.perf_counter()-started<900
    out={'schema':'LOCAL_SPIN10_FERMION_ANOMALY_SCREEN_V1','status':'COMPLETE_CARTAN_POLARIZATION_AND_SM_LOCAL_REPRESENTATION_SCREEN_ONLY','chiral_generations':gen,'left_Weyl_components_per_generation':16,'weights':[[str(z) for z in w] for w in weights],'Cartan_linear_polynomial':str(linear),'Cartan_cubic_polynomial':str(cubic.as_expr()),'degree_three_slots_checked':len(monomials),'Cartan_quadratic_trace':[[str(z) for z in row] for row in quadratic],'chiral_C_fifth_moment_one_generation':str(moment5),'full_tensor_argument':'compact skew normal form to Cartan, Spin10 lift, trace conjugation invariance and real polarization','SM_left_fields':[{'name':n,'color':c,'weak':w,'Y':str(y),'cubic_color_index':a} for n,c,w,y,a in matter],'SM_gauge_coefficients_per_generation':{k:str(v) for k,v in sm.items()},'omit_uc_control':{k:str(v) for k,v in bad.items()},'PQ_mixed_N_color':str(nc),'PQ_mixed_N_weak':str(nw),'PQ_mixed_N_hypercharge_unnormalized':str(ny),'PQ_mixed_N_hypercharge_GUT_normalized':str(s.Rational(3,5)*ny),'PQ_electromagnetic_E':str(ne),'PQ_linear_and_cubic_traces':str(grav),'local_Spin10_gauge_trace_screen_passed':True,'global_anomaly_or_full_regulated_measure_proved':False,'full_E5_or_quantum_restoration_qualified':False,'physical_matter_determinant_or_triangle_loop_computed':False,'numerical_feasibility_study_launched':False,'new_benchmark_domain_scheme_or_global_completion_adopted':False,'flavor_fit_resumed':False,'scientific_authority_changed':False,'whole_goal_complete':False,'write_attempts':writes,'input_sha256':prep['input_sha256'],'state_sha256':prep['state_sha256']}
    print('RESULT '+json.dumps(out,sort_keys=True,separators=(',',':')),flush=True);print('METRICS '+json.dumps({'total_seconds':time.perf_counter()-started}),flush=True)
if __name__=='__main__':main()
