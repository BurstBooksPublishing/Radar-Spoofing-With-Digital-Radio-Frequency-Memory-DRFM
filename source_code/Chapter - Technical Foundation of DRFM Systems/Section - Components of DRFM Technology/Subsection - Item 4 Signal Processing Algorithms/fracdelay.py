import numpy as np

def frac_delay_interp(x, D, L=32):
    """
    x: 1D complex numpy array of samples
    D: desired delay in samples (float)
    L: half-length of windowed-sinc filter (int)
    """
    N = len(x)
    M = 2*L+1
    n = np.arange(-L, L+1)
    # fractional offset
    d = D - np.floor(D)
    # ideal sinc shifted by fractional part
    h = np.sinc(n - d)
    # apply window (e.g., Hamming)
    h *= np.hamming(M)
    # normalize
    h /= np.sum(h)
    # convolve (simple, not optimized)
    y = np.convolve(x, h, mode='full')
    # align to produce delayed output (integer part handled by slicing)
    int_delay = int(np.floor(D))
    start = L + int_delay
    end = start + N
    return y[start:end]  # returns same length as x