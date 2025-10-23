import numpy as np
from scipy.signal import remez, lfilter, chirp
# generate a test chirp pulse
fs = 1e6            # sampling rate 1 MHz
t = np.arange(0,0.002,1/fs)     # 2 ms pulse
s = chirp(t, f0=1e4, f1=1.5e5, t1=t[-1], method='linear')
# add white Gaussian noise
snr_db = 0
sigma = np.sqrt(np.mean(s**2) / (10**(snr_db/10)))
x = s + sigma * np.random.randn(len(s))
# design an FIR lowpass (keep chirp band, suppress high-frequency noise)
bands = [0, 2e5, 2.2e5, fs/2]    # pass up to 200 kHz, stop above 220 kHz
desired = [1, 0]
numtaps = 129
h = remez(numtaps, bands, desired, fs=fs)  # equiripple design
y = lfilter(h, 1.0, x)  # apply filter (note: introduces group delay)
# y now has improved SNR with preserved chirp energy (check in frequency/time dom)