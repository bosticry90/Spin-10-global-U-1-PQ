# HPR1 V2 supplemental controller recovery

The observed adversarial worker COMPLETED successfully, returned the frozen
status QUALIFIED_HPR1_EXPLICIT_POLE_AND_FINITE_MUTATIONS, and passed all
its scientific assertions. The outer run_supplement.py then FAILED because
its copied expected status was QUALIFIED_HPR1_MUTATION_CONTROLS. The broad
name replacement ran before the longer literal replacement, so the latter
never matched. This is a controller metadata error, not a scientific failure.
Original source/copy, completed full worker capture and observed controller
traceback remain. No status is changed and no scientific gate is weakened.

Recovery authenticates every supplemental input and the original completed
capture, rechecks the launch/resource observations and exact status returned
by that frozen worker, and saves its existing RESULT dictionary unchanged.
No scientific or adversarial calculation is rerun. A separate metadata
recovery receipt records the failed controller and successful native result.
