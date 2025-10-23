import numpy as np
from scipy.signal import chirp, correlate

# Parameters (example values)
fs = 1e6                # sampling rate (Hz)
T = 1e-3                # chirp duration (s)
f0, f1 = 1e5, 4e5       # chirp start/stop freq (Hz)
c = 3e8                 # speed of light

# Generate transmitted chirp
t = np.arange(0, T, 1/fs)
tx = chirp(t, f0=f0, f1=f1, t1=T, method='linear')

# Simulate received signal with delay dt and attenuation
dt_true = 2.3e-6        # true propagation delay (s)
atten = 0.5
delay_samples = int(np.round(dt_true * fs))
rx = np.concatenate((np.zeros(delay_samples), atten*tx))[:len(tx)]

# Measure delay by cross-correlation
corr = correlate(rx, tx, mode='full')
lags = np.arange(-len(tx)+1, len(tx))
lag_idx = np.argmax(np.abs(corr))
measured_delay = lags[lag_idx] / fs      # seconds
range_meas = (c * measured_delay) / 2     # meters

# Output results (in actual system, log and compare to spec)
print("# measured_delay (s):", measured_delay)
print("# range_meas (m):", range_meas)