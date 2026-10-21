# Explicit contour dictionary for the independent BCR1 check

This makes section3's fixed contour dictionary explicit; it does not change the
native formula or its scope. The final verifier is prepared after both native
routes and before its first execution. The earlier verifier versions have not
been executed and are not failed verifications.

For one actual physical color, use eta=(+---), P=p0^2-pvec^2 and u=eta*p.
The frozen physical Hessian is
K_M=[[-P eta+u u^t, i u],[-i u^t,w]]. Its ordered odd block is
[[0,-P],[P,0]]. These are recovered directly from the frozen canonical Hessian
and its actual inverse frame, rather than inferred from the desired Euclidean
formula. For p=(i q0,qvec), put S_B=diag(-i,1,1,1), S_Lambda=i and S_x=S_C=S_a=1.
Then K_E=-S^(-t) K_M S^(-1) has the zero-sigma form of equation(5), and
G_E=-S G_M S^t. The scalar block becomes q^2+Mref_squared; the odd block has
off-diagonals -q^2,+q^2. The wrong auxiliary contour fails these same equations.

The constant contour Jacobian is A independent and cancels only in the allowed
relative normalization at A=0. The loop-density phase is inherited from MLB1;
it is not derived by assuming a positive full mixed Hessian. The two-point
Phi contribution is therefore reported first in the stripped Euclidean Gaussian
convention and then with the project's -hbar/i*hbar Wick dictionary. No global
phase choice for finite large backgrounds or physical measure positivity follows.
