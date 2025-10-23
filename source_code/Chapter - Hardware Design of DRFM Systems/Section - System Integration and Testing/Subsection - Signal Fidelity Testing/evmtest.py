import numpy as np
# Parameters
fs = 1e6                # sample rate (Hz)
T = 0.01                # duration (s)
Nbits = 12              # DAC/ADC resolution
t = np.arange(0, T, 1/fs)
# Generate baseband linear FM chirp
f0, f1 = 0e3, 200e3
phase = 2*np.pi*(f0*t + 0.5*(f1-f0)/T * t**2)
s = np.exp(1j*phase)    # ideal complex baseband
# Quantize (separate real/imag) to simulate finite resolution
maxval = 1.0
levels = 2**Nbits
q = lambda x: (np.round((x/maxval)*(levels/2-1)) / (levels/2-1)) * maxval
r = q(np.real(s)) + 1j*q(np.imag(s))
# Compute EVM (eq. \ref{eq:evm})
evm = np.sqrt(np.sum(np.abs(r - s)**2) / np.sum(np.abs(s)**2)) * 100
# Cross-correlation (normalized)
corr = np.abs(np.fft.ifft(np.fft.fft(s) * np.conj(np.fft.fft(r))))
corr /= np.sqrt(np.sum(np.abs(s)**2)*np.sum(np.abs(r)**2))
print("# EVM (percent):", evm)
print("# Peak normalized cross-corr:", np.max(corr))