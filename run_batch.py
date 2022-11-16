import numpy as np
import os

from values import r_vals, L_vals, num_repeats

for r in r_vals:
    for L in L_vals:
        for n in range(num_repeats):
            os.system(f"python run_clifford_expand.py {r} {L} {n}")