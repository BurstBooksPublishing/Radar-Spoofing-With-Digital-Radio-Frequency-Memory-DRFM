\begin{lstlisting}[language=Python,caption={Naive peak detection with true and replayed echoes},label={lst:drfm_replay}]
import numpy as np

# generate pulse (rectangular) and echo; add noise and a replayed echo
fs   = 10e6                                  # sampling freq
t    = np.arange(0, 1e-3, 1/fs)
pulse = (np.abs(t - 1e-4) < 1e-6).astype(float)   # simple pulse

# true echo delayed by 200 us and attenuated
true_delay = int(200e-6 * fs)
echo       = np.zeros_like(t)
echo[true_delay:true_delay + len(pulse)] = 0.5 * pulse

# DRFM replay: capture pulse, retransmit with extra delay and scaling
replay_delay = int(260e-6 * fs)                  # pulled-off range
replay       = np.zeros_like(t)
replay[replay_delay:replay_delay + len(pulse)] = 0.6 * pulse

# composite received signal with noise
rx = echo + replay + 0.01 * np.random.randn(len(t))

# simple estimator: find peak index (naive range)
idx = np.argmax(np.convolve(rx, pulse[::-1], mode='same'))
print("Estimated range sample index:", idx)