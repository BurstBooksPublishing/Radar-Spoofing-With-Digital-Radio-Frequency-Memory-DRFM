import numpy as np

# params
fs = 1e9               # sample rate (Hz)
delay_samps = 120      # integer delay (samples)
phase_rad = 0.5        # phase offset (radians)

def synth_replica(rx_samples):
    # apply circular delay (simple model)
    delayed = np.roll(rx_samples, delay_samps)
    # apply phase rotation (complex baseband assumed)
    rotated = delayed * np.exp(1j * phase_rad)
    # amplitude shaping (window) to avoid abrupt transients
    window = np.hanning(len(rotated))
    return rotated * window

# Example usage: rx is a complex numpy array of samples
# tx = synth_replica(rx)   # send to DAC path