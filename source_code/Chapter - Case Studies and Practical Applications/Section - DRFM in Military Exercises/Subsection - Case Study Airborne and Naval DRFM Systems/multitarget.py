import numpy as np

fs = 1e6          # sample rate (conceptual)
t = np.arange(0, 1e-3, 1/fs)   # time vector (1 ms)
pulse = np.where((t>=0.0001) & (t<0.00012), 1.0, 0.0)  # simple pulse

# delays in seconds (conceptual, not platform specs)
delay1 = 2e-6
delay2 = 5e-6

def delay_signal(sig, d, fs):
    # integer-sample shift (simple illustration)
    shift = int(np.round(d * fs))
    return np.concatenate((np.zeros(shift), sig))[:len(sig)]

replica1 = delay_signal(pulse, delay1, fs) * 0.8  # attenuated replica
replica2 = delay_signal(pulse, delay2, fs) * 0.5  # second replica

composite = pulse + replica1 + replica2  # multi-target composite
# downstream: apply windowing, quantization model, etc. (omitted)