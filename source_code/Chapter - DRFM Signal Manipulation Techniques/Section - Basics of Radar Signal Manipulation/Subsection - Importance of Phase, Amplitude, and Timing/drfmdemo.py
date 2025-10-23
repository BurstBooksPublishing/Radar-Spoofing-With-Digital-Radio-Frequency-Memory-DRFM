import numpy as np
c = 3e8
fs = 20e6                   # sample rate
T = 1e-6                    # pulse duration
t = np.arange(0, T, 1/fs)
f0 = 5e6                    # baseband center
k = 1e12                    # chirp rate (rad/s^2) simplified
# generate complex chirp
s = np.exp(1j*(2*np.pi*(f0*t + 0.5*(k/(2*np.pi))*t**2)))
# apply amplitude envelope (simulate RCS)
amp = np.hanning(len(t))
s = amp * s
# apply time delay tau (in samples)
tau = 5e-9                  # 5 ns delay
delay_samps = int(round(tau * fs))
s_delayed = np.concatenate((np.zeros(delay_samps, dtype=complex), s)) 
# apply per-pulse phase ramp for fake velocity
# assume single pulse example: global phase offset simulating Doppler
phase_offset = np.deg2rad(30)  # 30 degree offset
s_delayed *= np.exp(1j*phase_offset)
# matched filter correlation (example)
mf = np.conj(s[::-1])        # simple matched filter
corr = np.abs(np.convolve(s_delayed, mf))  # correlation magnitude
# (plotting or further analysis would follow)