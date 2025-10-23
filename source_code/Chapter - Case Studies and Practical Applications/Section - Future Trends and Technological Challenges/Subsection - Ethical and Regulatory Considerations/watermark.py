import numpy as np

# s: received signal, w: known watermark template (low-power)
# compute normalized cross-correlation to test presence of watermark
def detect_watermark(s, w, threshold=5.0):
    # brief comments: compute FFT-based cross-correlation for speed
    S = np.fft.rfft(s)
    W = np.fft.rfft(w, n=s.size)
    corr = np.fft.irfft(S * np.conj(W), n=s.size)
    metric = np.max(np.abs(corr)) / np.std(corr)  # signal-to-noise metric
    return metric > threshold, metric

# usage (pseudo): authorized auditors only should run this on captured replay