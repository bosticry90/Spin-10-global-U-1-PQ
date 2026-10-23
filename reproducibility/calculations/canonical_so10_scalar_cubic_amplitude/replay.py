"""S3A1 canonical-unit grouping and source-reconstructed inverse slope."""
from data import *
start=begin();mp.mp.dps=140
save('replay',{'schema':'S3A1_COMPLETE_SSS_PRIMITIVE','working_digits':140,'cases':{gs:aggregate('replay',q(gs)) for gs in ['1/2','1']},
 'independent_slope':inverse_slope('replay'),'remaining_overall_pole':[0,0,0],'finite_function':'C(g10^2)+L*(A+B/g10^2); L=log(Q2/60)',
 'no_universal_g2_prefactor':True,'SSS_amplitude_complete_pending_validation':True},start)
