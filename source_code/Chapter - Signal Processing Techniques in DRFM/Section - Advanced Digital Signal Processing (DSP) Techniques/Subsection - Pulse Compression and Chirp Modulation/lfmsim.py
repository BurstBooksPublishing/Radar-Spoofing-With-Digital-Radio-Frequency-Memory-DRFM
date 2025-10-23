import numpy as np
from scipy.signal import fftconvolve
# parameters (simulation-scale values)
fs = 2000.0         # sampling rate in Hz (simulation choice)
T  = 0.1            # pulse duration in seconds
B  = 200.0          # bandwidth in Hz
f0 = 300.0          # center frequency in Hz
t = np.arange(-T/2, T/2, 1/fs)
k = B / T           # chirp rate

# transmit LFM (baseband complex)
s = np.exp(1j*(2*np.pi*f0*t + np.pi*k*t**2))

# simulate one-way delay and add white noise
tau = 0.02                              # delay in seconds (simulated)
delay_samples = int(round(tau*fs))
r = np.roll(s, delay_samples) + 0.01*(np.random.randn(len(s))+1j*np.random.randn(len(s)))

# matched filter is time-reversed conjugate
h = np.conjugate(s[::-1])
y = fftconvolve(r, h, mode='full')     # compressed output (complex)

# output index of peak gives estimated delay (simulation)
peak_idx = np.argmax(np.abs(y))
estimated_delay = (peak_idx - len(s) + 1) / fs
# print or plot in actual analysis code (omitted here)