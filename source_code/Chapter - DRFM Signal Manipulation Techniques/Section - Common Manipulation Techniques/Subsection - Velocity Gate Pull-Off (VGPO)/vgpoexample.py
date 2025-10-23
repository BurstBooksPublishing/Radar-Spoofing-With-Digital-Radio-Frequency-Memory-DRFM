import numpy as np

# inputs (example values)
fs = 10e6            # sampling rate (Hz)
delta_f = 500.0      # desired Doppler offset (Hz)
samples = np.array(...)  # complex baseband samples captured by DRFM

# compute phase increment per sample
n = np.arange(len(samples))
phase_ramp = np.exp(1j * 2 * np.pi * delta_f * n / fs)

# apply ramp (preserve amplitude envelope)
shifted = samples * phase_ramp

# optionally apply smooth windowing at pulse edges to avoid spectral leakage
# (use a cosine taper or similar)
# output shifted can be DAC'ed with appropriate timing