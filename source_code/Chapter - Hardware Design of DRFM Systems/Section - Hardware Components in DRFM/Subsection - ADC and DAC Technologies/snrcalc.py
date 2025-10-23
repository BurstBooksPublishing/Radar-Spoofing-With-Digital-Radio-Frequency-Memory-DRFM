import numpy as np

# Parameters
Vfs = 1.0            # Full-scale amplitude (V)
N = 12               # ADC bits
fin = 1e9            # input frequency (Hz)
tj = 100e-15         # aperture jitter (s)

# Quantization noise
Delta = Vfs / (2**N)
sigma_q2 = Delta**2 / 12
SNR_quant = 6.02*N + 1.76  # dB, ideal

# Jitter-limited SNR (dB)
SNR_jitter = -20*np.log10(2*np.pi*fin*tj)

print("Ideal SNR (bits): {:.2f} dB".format(SNR_quant))
print("Jitter-limited SNR: {:.2f} dB".format(SNR_jitter))