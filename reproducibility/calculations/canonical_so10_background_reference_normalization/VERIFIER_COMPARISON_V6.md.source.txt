# Pole diagnostic and complete comparison fix

V5's second failure is preserved. The isolated diagnostic records the actual
cause: SymPy returned an unevaluated Limit, not an expanded polynomial. V5
reduced a temporary difference but retained that unevaluated Limit as the next
integration input. Its Integral therefore also remained unevaluated. Reducing
the pole itself gives -M+u^2*z-u*z, whose integral is exactly -M-z/6. The
diagnostic is retained with full bound inputs and is not scientific acceptance.

V6 assigns that reduced pole before integration, compares exact reduced
differences and moves these cheap pole tests to the beginning. Original Gamma
formula, epsilon orientation, expected sign, contact coefficient, numerical
checks and all scientific conditions remain. Two failed verifiers, two failed
native executions and the successful nativeV3 outputs remain unchanged.
