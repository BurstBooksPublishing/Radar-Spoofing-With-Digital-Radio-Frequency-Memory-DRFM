import math

# Parameters (example): highest signal frequency and desired jitter-limited SNR
f_in = 1.2e9      # highest input freq in Hz (1.2 GHz)
desired_snr_db = 60.0  # desired SNR due to jitter (dB)

# compute max RMS jitter sigma_j to meet desired SNR from eq (jitter_snr)
# SNR = -20*log10(2*pi*f_in*sigma_j)  => sigma_j = 10^(-SNR/20) / (2*pi*f_in)
sigma_j_max = 10**(-desired_snr_db/20.0) / (2.0*math.pi*f_in)
print(f"Max RMS jitter: {sigma_j_max*1e15:.2f} fs")

# Evaluate alias mapping for a range of sampling rates
candidate_fs = [1.0e9, 1.25e9, 2.0e9]  # Hz
for fs in candidate_fs:
    k = round(f_in / fs)
    f_alias = abs(f_in - k*fs)
    print(f"fs={fs/1e9:.3f} GHz -> k={k}, aliased f={f_alias/1e6:.2f} MHz")
# Comments: choose fs to avoid alias overlap and keep f_alias in desired IF band.