import numpy as np
# parameters
fs = 1e6               # sampling rate (Hz)
t = np.arange(0, 1e-3, 1/fs)  # time vector for a pulse
fc = 0.0               # baseband (fc already removed)
# base pulse (Gaussian-shaped envelope)
pulse = np.exp(-((t-0.5e-3)/(0.1e-3))**2) * np.exp(1j*0)  # analytic baseband
# false target definitions: (delay_seconds, amplitude, phase_radians)
targets = [(30e-6, 0.8, 0.0), (80e-6, 0.4, np.pi/4), (150e-6, 1.2, -np.pi/6)]
out = np.zeros_like(pulse, dtype=complex)
for delay, amp, ph in targets:
    # fractional sample delay via linear interpolation (simple example)
    shift_samples = delay * fs
    idx = np.arange(len(pulse)) - shift_samples
    # clamp indices for interpolation
    idx_floor = np.floor(idx).astype(int)
    frac = idx - idx_floor
    idx_floor = np.clip(idx_floor, 0, len(pulse)-2)
    # linear interp
    delayed = (1-frac)*pulse[idx_floor] + frac*pulse[idx_floor+1]
    # apply amplitude and phase
    out += amp * delayed * np.exp(1j*ph)
# 'out' now contains the composite deceptive waveform