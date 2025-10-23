import numpy as np
# Parameters
fs = 1e6              # sampling rate (Hz)
t = np.arange(0,0.01,1/fs)  # time vector
f0 = 100e3            # input tone (Hz)
A = 0.8               # amplitude (full-scale = 1.0)
Nbits = 8             # quantizer bits

# Continuous-time tone (simulated at same sample grid for demo)
x = A * np.sin(2*np.pi*f0*t)

# Downsample / alias demo (alias happens if fs_alias < 2*f0)
fs_alias = 150e3
decim = int(fs/fs_alias)
x_alias = x[::decim]  # simple decimation (no anti-aliasing)

# Uniform quantization
Vpp = 2.0             # assume full-scale -1..+1 => Vpp=2
Delta = Vpp/(2**Nbits)
xq = np.round(x/Delta) * Delta  # quantized samples

# Compute quantization noise power and SNR
q = x - xq
P_signal = np.mean(x**2)
P_noise = np.mean(q**2)
SNR_db = 10*np.log10(P_signal/P_noise)
print("# SNR (quantization limited) = %.2f dB" % SNR_db)

# Small output: show alias frequency index for decimated sequence
# (compute FFT and find peak)
Xf = np.fft.fft(x_alias * np.hanning(len(x_alias)))
f_axis = np.fft.fftfreq(len(Xf), d=1/fs_alias)
peak = np.argmax(np.abs(Xf))
print("# Aliased peak at %.1f Hz" % np.abs(f_axis[peak]))