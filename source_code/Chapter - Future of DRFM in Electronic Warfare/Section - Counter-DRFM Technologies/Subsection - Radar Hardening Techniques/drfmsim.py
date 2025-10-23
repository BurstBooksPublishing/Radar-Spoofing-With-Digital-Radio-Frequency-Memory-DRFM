import numpy as np
from scipy.signal import chirp, correlate
# parameters
fs = 1e6               # sampling rate
T = 1e-3               # pulse duration
t = np.arange(0, T, 1/fs)
# transmitted chirp
s = chirp(t, f0=1e4, f1=1e5, t1=T, method='linear')
# DRFM replay: scale, delay, quantize
delay_samples = int(60)  # replay latency in samples
a = 0.8                  # replay amplitude factor
# quantize to simulate finite bits
def quantize(x, bits=8):
    levels = 2**bits
    x_norm = (x - x.min()) / (x.max()-x.min())
    q = np.round(x_norm*(levels-1)) / (levels-1)
    return q*(x.max()-x.min()) + x.min()
replay = np.concatenate((np.zeros(delay_samples), a*quantize(s, bits=6)))
# received: true echo + replay + noise
r = np.concatenate((s, np.zeros(delay_samples))) + replay
r += 0.01*np.random.randn(len(r))
# correlation
corr = correlate(r, s, mode='full')
lag = np.argmax(np.abs(corr)) - (len(s)-1)
print("# Peak lag (samples):", lag)
# further analysis would check peak shape and side-lobe structure