import numpy as np
# capture: complex baseband buffer (samples captured from ADC)
rx_buffer = capture_samples()      # comment: hardware-specific capture
fs = 1e6                           # sample rate in Hz (example)
t = np.arange(len(rx_buffer)) / fs

# apply delay (circular buffer shift) and Doppler shift
delay_samples = int(0.0005 * fs)   # 0.5 ms delay -> range shift
buffer_shifted = np.roll(rx_buffer, delay_samples)

f_d = 200.0                        # Doppler shift in Hz (example)
doppler = np.exp(1j * 2 * np.pi * f_d * t)
spoof_buffer = buffer_shifted * doppler

# amplitude shaping to simulate RCS change
spoof_buffer *= 0.8                # scale amplitude

# transmit: send to DAC and RF front end
transmit_samples(spoof_buffer)     # comment: handles timing and RF upconvert