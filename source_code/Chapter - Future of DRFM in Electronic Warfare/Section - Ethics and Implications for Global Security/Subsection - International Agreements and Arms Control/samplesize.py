import math
from scipy.stats import norm

# Desired detection and false-alarm probabilities (set by treaty)
P_d = 0.9   # target probability of detection
P_fa = 1e-3 # acceptable false-alarm probability

# Per-sample standardized effect size (must be measured/calibrated)
d = 0.1     # small effect size for high-fidelity DRFM

# Compute minimum N from equation (use absolute because Q^{-1} negative)
Nd = ( (norm.isf(P_fa) - norm.isf(P_d)) / d )**2
N_required = math.ceil(Nd)
print("# of independent pulses required:", N_required)
# Inspector notes: ensure independence and stationarity assumptions hold.