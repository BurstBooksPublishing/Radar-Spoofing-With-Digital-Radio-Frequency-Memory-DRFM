import numpy as np
from scipy.signal import resample_poly, fftconvolve

# assume rx_wave is the sampled complex baseband received pulse
# fs: sampling rate, R: desired range (m), vr: radial velocity (m/s)
def simulate_echo(rx_wave, fs, R, vr, sigma_db=0.0):
    c = 3e8
    # compute delay in seconds
    tau = 2.0 * R / c
    # fractional delay in samples
    delay_samples = tau * fs
    int_delay = int(np.floor(delay_samples))
    frac = delay_samples - int_delay

    # fractional delay filter (simple linear interpolation kernel)
    # better filters should be used in practice (Lagrange, Farrow, etc.)
    n = np.arange(len(rx_wave))
    delayed = np.zeros_like(rx_wave)
    # integer delay via padding
    if int_delay < len(rx_wave):
        delayed[int_delay:] = rx_wave[:len(rx_wave)-int_delay]
    # fractional delay via linear interp (prototype)
    delayed = (1.0 - frac) * delayed + frac * np.roll(delayed, -1)

    # Doppler: apply complex exponential across duration
    fc = 1e9  # carrier frequency placeholder for Doppler calc (Hz)
    fd = 2.0 * vr * fc / c
    t = np.arange(len(delayed)) / fs
    delayed *= np.exp(1j * 2.0 * np.pi * fd * t)

    # amplitude scaling from RCS (simple dB scale)
    alpha = 10**(sigma_db/20.0)
    delayed *= alpha

    # optional additive noise
    noise = (np.random.randn(*delayed.shape) + 1j*np.random.randn(*delayed.shape)) * 1e-3
    return delayed + noise

# Example usage (not real-time safe); comments explain each step.