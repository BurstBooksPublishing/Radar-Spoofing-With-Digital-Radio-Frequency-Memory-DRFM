import numpy as np
from scipy.signal import resample

# s: complex baseband waveform array
# fs: sampling frequency (Hz)
# fd: desired Doppler shift (Hz)  (use 0 for time-scaling mode)
# alpha: time-scaling factor (resampling), alpha<1 compresses (faster)

def apply_doppler(s, fs, fd=0.0, alpha=None):
    t = np.arange(len(s)) / fs
    if fd != 0.0:
        # Multiply by complex exponential to impose Doppler (preserve range)
        s_shifted = s * np.exp(1j*2*np.pi*fd*t)
        return s_shifted
    elif alpha is not None:
        # Time-scale by resampling: new length = len(s)*alpha
        new_len = int(np.round(len(s) * alpha))
        s_resampled = resample(s, new_len)  # changes both range and spectrum
        return s_resampled
    else:
        return s  # no change