import numpy as np
# sample_rate in Hz, buffer_seconds configures maximum delay
sample_rate = 1e8  # 100 MS/s, example
buffer_seconds = 0.01  # 10 ms buffer
N = int(sample_rate * buffer_seconds)
buffer = np.zeros(N, dtype=np.complex64)  # circular buffer
write_idx = 0

def process_incoming(samples, desired_delay_seconds):
    global write_idx
    # write incoming samples into buffer
    for s in samples:
        buffer[write_idx] = s  # store complex sample
        write_idx = (write_idx + 1) % N
    # compute read index for desired delay
    delay_samples = int(desired_delay_seconds * sample_rate)
    read_idx = (write_idx - delay_samples) % N
    # prepare output (same length as input)
    out = np.empty_like(samples)
    for i in range(len(samples)):
        out[i] = buffer[(read_idx + i) % N]  # simple replay
    return out  # to be sent to DAC/Tx