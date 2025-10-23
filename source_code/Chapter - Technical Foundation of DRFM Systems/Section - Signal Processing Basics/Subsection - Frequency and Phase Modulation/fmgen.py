import numpy as np

# parameters (comments are brief)
fs = 1e6           # sampling frequency in Hz
T = 1e-3           # pulse duration in seconds
B = 100e3          # chirp bandwidth in Hz
f0 = -B/2          # start freq in baseband
t = np.arange(0, T, 1/fs)

# generate complex baseband LFM: exp(j*(2*pi*f0*t + pi*K*t^2))
K = B / T
phase = 2*np.pi*f0*t + np.pi*K*t**2
s = np.exp(1j*phase)         # unit-amplitude complex baseband

# estimate instantaneous phase and frequency
phi = np.unwrap(np.angle(s))                 # unwrap reduces 2pi jumps
inst_freq = np.diff(phi) * (fs / (2*np.pi)) # Hz, length N-1

# simple manipulation: add linear phase ramp to simulate Doppler
doppler = 500.0                            # Hz
phase_shifted = phase + 2*np.pi*doppler*t
s_shifted = np.exp(1j*phase_shifted)