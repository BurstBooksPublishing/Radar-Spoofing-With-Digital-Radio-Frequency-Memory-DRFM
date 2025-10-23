import numpy as np

# parameters (abstract, not hardware values)
fs = 1000.0                 # sample rate (arbitrary units)
pulse_len = 50              # samples per pulse
num_pulses = 200            # number of radar pulses
initial_delay = 100         # initial delay in samples
delay_rate = 0.5            # delay increment per pulse (samples/pulse)

# generate a single pulse waveform (envelope times carrier)
t = np.arange(pulse_len) / fs
pulse = np.exp(-((t-0.02)/0.005)**2) * np.cos(2*np.pi*50*t)  # illustrative pulse

# place real echo at a fixed delay
real_trace = np.zeros(int(initial_delay + num_pulses*delay_rate + pulse_len + 10))
real_pos = int(initial_delay)
real_trace[real_pos:real_pos+pulse_len] += pulse  # real echo

# create spoofed return that increases delay over pulses
spoof_trace = np.zeros_like(real_trace)
for n in range(num_pulses):
    d = int(initial_delay + n*delay_rate)  # integer sample delay (abstract)
    idx = d + int(n * 0)                   # stagger if desired
    spoof_trace[idx:idx+pulse_len] += pulse * (1.0 - n/num_pulses*0.5)  # fade amplitude slightly

# combined received trace (real + spoof)
received = real_trace + spoof_trace

# show where centroid moves (very simple metric)
centroids = []
for n in range(num_pulses):
    window_start = int(initial_delay + n*delay_rate - 20)
    window_end = window_start + 100
    w = received[window_start:window_end]
    if w.sum() > 0:
        centroids.append(window_start + np.argmax(w))
    else:
        centroids.append(None)
# centroids illustrates apparent peak movement over time