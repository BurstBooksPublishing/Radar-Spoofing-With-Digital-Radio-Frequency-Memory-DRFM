import numpy as np

# Monte Carlo parameters
N_trials = 10000            # number of simulated approaches
p_spoof = 0.02              # probability a spoof affects this sensor per approach
p_detect_hardening = 0.6    # chance that hardened sensor detects spoof
redirect_if_undetected = 0.9# probability asset redirects if spoof not detected

# simulate outcomes
rng = np.random.default_rng(seed=42)
affected = rng.random(N_trials) < p_spoof
detected = rng.random(N_trials) < p_detect_hardening
redirects = affected & (~detected) & (rng.random(N_trials) < redirect_if_undetected)

# estimate per-approach humanitarian incident probability
incident_prob = redirects.mean()
print(f"Estimated incident probability per approach: {incident_prob:.4f}")