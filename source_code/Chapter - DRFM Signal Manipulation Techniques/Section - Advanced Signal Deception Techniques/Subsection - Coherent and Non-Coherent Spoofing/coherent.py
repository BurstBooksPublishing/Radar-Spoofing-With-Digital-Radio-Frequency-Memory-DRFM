# generate complex chirp and apply coherent delay + phase offset
import numpy as np
fs = 2e6  # sampling rate
t = np.arange(0,1e-3,1/fs)
f0 = 50e3
k = 1e6  # chirp rate
# complex baseband chirp
s = np.exp(1j*(2*np.pi*(f0*t + 0.5*k*t**2)))
# simulate DRFM replay: delay and phase continuity
delay_samples = int(40e-6 * fs)
phase_offset = np.pi/6
# roll preserves sample-by-sample complex phase (coherent replay)
r_replay = np.roll(s, delay_samples) * np.exp(1j*phase_offset)
# short-hand visualization comment: compute cross-correlation peak
corr = np.abs(np.fft.ifft(np.fft.fft(r_replay) * np.conj(np.fft.fft(s))))
# In hardware: ADC/DAC quantization, sample rate conversion and LO phase locks are required.