import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

fs = 1.0e6              # sample rate (Hz)
nyq = fs/2.0
# FIR: linear-phase lowpass via windowed sinc
cutoff = 100e3          # passband edge
numtaps = 101           # FIR order + 1 (odd => symmetric linear phase)
b_fir = signal.firwin(numtaps, cutoff/nyq, window='hamming')
w, h_fir = signal.freqz(b_fir, [1.0], worN=2048, fs=fs)

# IIR: Butterworth lowpass (4th order)
b_iir, a_iir = signal.butter(4, cutoff/nyq, btype='low', analog=False)
w, h_iir = signal.freqz(b_iir, a_iir, worN=2048, fs=fs)

# Plot magnitude and phase (omitted here in headless environments)
# plt.semilogy(w, np.abs(h_fir), label='FIR')
# plt.semilogy(w, np.abs(h_iir), label='IIR')
# plt.legend(); plt.show()