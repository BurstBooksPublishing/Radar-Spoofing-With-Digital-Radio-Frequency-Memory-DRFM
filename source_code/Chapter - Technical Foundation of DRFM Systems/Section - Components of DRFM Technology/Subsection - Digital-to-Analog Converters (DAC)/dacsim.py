import numpy as np
# Parameters
fs = 100e6        # DAC sample rate (Hz)
f0 = 10e6         # tone frequency (Hz)
N = 12            # DAC bits
Vfs = 1.0         # full scale (Vpp)
t = np.arange(0, 1e-4, 1/(10*fs))  # high-rate time vector for plotting

# Generate ideal continuous tone, then sample & quantize
ts = 1/fs
n = np.arange(0, int(1e-4*fs))
samples = 0.5*Vfs*np.sin(2*np.pi*f0*n*ts)               # sampled waveform
qstep = Vfs/(2**N)                                     # quantization step
quant = qstep*np.round(samples/qstep)                  # quantized codes

# Zero-order-hold reconstruction: hold each sample for Ts
recon = np.repeat(quant, 10)                           # simple upsample by 10 (ZOH)
t_recon = np.arange(len(recon))*(ts/10)

# FFT to inspect spectrum (brief)
spec = np.fft.fftshift(np.fft.fft(recon*np.hanning(len(recon))))
freq = np.fft.fftshift(np.fft.fftfreq(len(recon), ts/10))
# (Plotting omitted; comments show intent)
# # Plot time-domain and spectrum to observe quantization spurs and sinc envelope