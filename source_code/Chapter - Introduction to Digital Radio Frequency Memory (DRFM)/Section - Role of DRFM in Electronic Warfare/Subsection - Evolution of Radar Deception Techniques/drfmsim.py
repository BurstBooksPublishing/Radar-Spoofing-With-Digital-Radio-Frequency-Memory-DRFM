import numpy as np

# sample_rate in Hz, s is complex baseband samples
def fractional_delay(s, delay_seconds, sample_rate):
    # linear interpolation fractional delay (simple example)
    n = np.arange(len(s))
    t = n / sample_rate
    t_shift = t - delay_seconds
    idx = np.floor(t_shift * sample_rate).astype(int)
    frac = (t_shift * sample_rate) - idx
    # boundary handling (zeros outside)
    out = np.zeros_like(s, dtype=complex)
    valid = (idx >= 0) & (idx+1 < len(s))
    out[valid] = (1-frac[valid])*s[idx[valid]] + frac[valid]*s[idx[valid]+1]
    return out

# usage: apply delay and Doppler (phase ramp)
# s: intercepted samples, delay: seconds, fd: Doppler Hz, sample_rate: Hz
def replay_spoof(s, delay, fd, sample_rate, amplitude=1.0):
    y = fractional_delay(s, delay, sample_rate)
    n = np.arange(len(y))
    phase_ramp = np.exp(1j*2*np.pi*fd*(n/sample_rate))
    return amplitude * y * phase_ramp

# brief example
# s = received_complex_samples
# spoofed = replay_spoof(s, delay=1e-6, fd=100.0, sample_rate=1e6)