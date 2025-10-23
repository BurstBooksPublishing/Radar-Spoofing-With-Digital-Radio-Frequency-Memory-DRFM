import numpy as np
# parameters
Fs = 1e6            # sampling rate (Hz)
N = 4096            # FFT length
t = np.arange(N)/Fs
# create a test pulse (Gaussian-modulated sinusoid)
f0 = 100e3
x = np.exp(-((t-0.0015)/0.0002)**2) * np.cos(2*np.pi*f0*t)
# FFT
X = np.fft.fft(x)
k = np.fft.fftfreq(N, d=1/Fs)
# apply a time delay tau by multiplying by exp(-j*2*pi*f*tau)
tau = 3.2e-6  # desired delay in seconds
phase_ramp = np.exp(-1j*2*np.pi*k*tau)
X_delayed = X * phase_ramp
# inverse FFT -> delayed time-domain signal
x_delayed = np.real(np.fft.ifft(X_delayed))
# x_delayed now contains the pulse delayed by approximately tau