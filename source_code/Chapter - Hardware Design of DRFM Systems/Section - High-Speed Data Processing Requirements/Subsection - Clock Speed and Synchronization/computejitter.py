import math

def max_rms_jitter(f_hz, snr_db):
    # Compute allowable t_j,rms from SNR_jitter ~ -20*log10(2*pi*f*tj)
    # Rearranged: tj = 10^(-SNR/20) / (2*pi*f)
    factor = 10**(-snr_db/20.0)
    tj = factor / (2.0 * math.pi * f_hz)
    return tj  # seconds

# Example: allowable jitter for 60 dB SNR at 100 MHz
f = 100e6
snr = 60.0
tj_seconds = max_rms_jitter(f, snr)
print("Max RMS jitter: {:.3e} s".format(tj_seconds))  # ~2.65e-12 s = 2.65 ps