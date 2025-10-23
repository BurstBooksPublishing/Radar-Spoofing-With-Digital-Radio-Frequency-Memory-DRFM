import numpy as np
# x: complex baseband pulse samples (numpy array)
# fs: sampling rate (Hz)
# delay_s: desired delay (seconds)
# fd: Doppler shift (Hz)
# amp: amplitude scale factor

def drfm_replay(x, fs, delay_s, fd, amp=1.0):
    N = len(x)
    t = np.arange(N) / fs
    # apply Doppler (complex exponential) and amplitude
    x_dop = amp * x * np.exp(1j*2*np.pi*fd*t)
    # convert delay to integer + fractional sample shift
    int_delay = int(np.floor(delay_s * fs))
    frac_delay = delay_s * fs - int_delay
    # fractional delay via linear-phase FIR (simple, for demo)
    # use sinc or higher-order filter for production
    from scipy.signal import resample_poly
    # resample to implement fractional sample delay (demo approach)
    up = 100
    x_up = resample_poly(x_dop, up, 1)  # upsample
    shift = int(np.round(frac_delay * up))
    x_shifted = np.concatenate((np.zeros(int_delay + shift, dtype=complex),
                                x_up, np.zeros(1, dtype=complex)))
    # downsample back to original rate
    y = resample_poly(x_shifted, 1, up)
    return y[:N+int_delay+2]  # returned buffer with delay inserted

# Usage example (capture and playback loops omitted)