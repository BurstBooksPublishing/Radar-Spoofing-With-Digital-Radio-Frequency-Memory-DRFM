import numpy as np

# Parameters
fs = 1e9                # sample rate (Hz)
f_sig = 100e6           # input tone (Hz)
Nbits = 12              # ADC nominal bits
t_jitter = 200e-15      # rms jitter (s)
n = 100000              # samples

# Generate sine wave
t = np.arange(n)/fs
sig = 0.9*np.sin(2*np.pi*f_sig*t)  # 0.9 full scale

# Apply aperture jitter: random small time shifts -> phase error
t_err = np.random.normal(0, t_jitter, size=n)
sig_jittered = 0.9*np.sin(2*np.pi*f_sig*(t + t_err))

# Quantize
levels = 2**Nbits
q = np.round((sig_jittered + 1.0) * (levels/2 - 1))  # map to [0,levels)
sig_q = (q/(levels/2 - 1)) - 1.0                      # back to [-1,1]

# Compute SNRs
signal_power = np.mean(sig**2)
quant_noise_power = np.mean((sig - sig_q)**2)
jitter_noise_power = np.mean((sig - sig_jittered)**2)

print("Ideal quantization SNR (dB):", 6.02*Nbits + 1.76)
print("Measured quantization noise SNR (dB):", 10*np.log10(signal_power/quant_noise_power))
print("Jitter-limited SNR (dB) approx:", -20*np.log10(2*np.pi*f_sig*t_jitter))