import numpy as np
from scipy.signal import chirp
import matplotlib.pyplot as plt

fs = 1e6              # sampling rate (Hz) - for simulation only
T = 1e-3              # duration (s)
t = np.arange(0, T, 1/fs)

# generate base chirp (start 100kHz -> 200kHz)
tx = chirp(t, f0=1e5, t1=T, f1=2e5, method='linear')

# simulate a delayed, attenuated echo
delay_sec = 5e-6      # equivalent to a short range target
attenuation = 0.3     # amplitude scaling (linear)
delay_samples = int(np.round(delay_sec * fs))
echo = np.zeros_like(tx)
echo[delay_samples:] = attenuation * tx[:-delay_samples]

rx = tx + echo        # received signal = direct + echo (simulation)

# plot a short time window to visualize
plt.plot(t[:200], rx[:200])
plt.title('Simulated received signal (tx + delayed echo)')
plt.xlabel('Time (s)')
plt.show()