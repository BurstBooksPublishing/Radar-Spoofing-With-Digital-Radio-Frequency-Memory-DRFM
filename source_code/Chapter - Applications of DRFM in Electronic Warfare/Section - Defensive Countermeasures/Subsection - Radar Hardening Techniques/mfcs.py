# r: received samples, s: transmitted template (complex)
# compute matched-filter output (discrete)
import numpy as np
z = np.vdot(s, r)  # matched filter (conjugate inner product)
energy = np.abs(z)**2
# simple energy threshold check
if energy < energy_threshold:
    # likely weak or decorrelated return
    raise_alarm("low_correlation")
# quick cyclostationary proxy: conjugate product at lag P (PRI)
P = pulse_interval_samples
sc = np.mean(r[:-P] * np.conj(r[P:]))  # cyclic autocorr proxy
if np.abs(sc) < cs_threshold:
    raise_alarm("weak_cyclostationarity")
# proceed with track update otherwise