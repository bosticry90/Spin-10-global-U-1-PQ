"""S3A1 original-row axis restoration and independent mass inverse slope."""
from data import *
start=begin();mp.mp.dps=110
save('primary',{'schema':'S3A1_COMPLETE_SSS_PRIMITIVE','working_digits':110,'cases':{gs:aggregate('primary',q(gs)) for gs in ['1/2','1']},
 'independent_slope':inverse_slope('primary'),'remaining_overall_pole':[0,0,0],'finite_function':'C(g10^2)+L*(A+B/g10^2); L=log(Q2/60)',
 'no_universal_g2_prefactor':True,'SSS_amplitude_complete_pending_validation':True},start)
