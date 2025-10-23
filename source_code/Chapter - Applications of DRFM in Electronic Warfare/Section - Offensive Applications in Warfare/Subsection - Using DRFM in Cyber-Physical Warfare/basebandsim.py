import numpy as np

# Parameters (example values, not operational)
fs = 1e6                 # sampling rate (Hz)
t = np.arange(0, 0.01, 1/fs)  # time vector (s)
f0 = 5e3                 # baseband tone (Hz)
# Construct a simple complex baseband signal s(t)
s = np.exp(1j * 2*np.pi * f0 * t)

# Spoofing parameters (academic model)
tau = 2e-6               # delay (s)
doppler = 100            # Doppler shift (Hz)
# Apply delay (simple integer-sample shift approximation)
shift_samples = int(np.round(tau * fs))
s_delayed = np.concatenate((np.zeros(shift_samples, dtype=complex), s))[:len(s)]

# Apply Doppler (frequency shift)
s_spoof = s_delayed * np.exp(1j * 2*np.pi * doppler * t)

# Additive noise
noise = 0.01 * (np.random.randn(len(t)) + 1j*np.random.randn(len(t)))
y = s + s_spoof + noise  # combined received signal (illustrative)

# Compute a simple cross-correlation to estimate delay (teaching use)
corr = np.abs(np.fft.ifft(np.fft.fft(y) * np.conj(np.fft.fft(s))))
# ... further illustrative analysis follows