import numpy as np
from scipy.signal import correlate, find_peaks

# s: transmitted (template) pulse; r: received pulse stream (1D array)
# windowing and gating handled externally
def detect_replay(s, r, sr):
    # compute normalized cross-correlation
    corr = correlate(r, s.conj(), mode='valid')
    corr /= np.sqrt(np.sum(np.abs(s)**2) * np.convolve(np.abs(r)**2, np.ones(len(s)), 'valid'))
    # detect peaks above threshold
    peaks, props = find_peaks(np.abs(corr), height=0.6)  # threshold tuned for PD/PFA
    detections = []
    for p in peaks:
        # measure peak width and nearby secondary peaks
        neighborhood = np.abs(corr[max(0,p-50):p+50])
        # crude check: multiple closely spaced peaks imply replay/internal delays
        if np.sum(neighborhood > 0.2) > 3:
            detections.append({'index': p, 'amp': np.abs(corr[p])})
    return detections

# Example usage (comments): feed in gated pulse returns and check for detections.