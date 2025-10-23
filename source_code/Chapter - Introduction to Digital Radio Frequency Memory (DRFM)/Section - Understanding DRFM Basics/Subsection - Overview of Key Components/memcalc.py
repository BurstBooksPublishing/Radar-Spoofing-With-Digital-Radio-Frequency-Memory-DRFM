# Simple memory calc: sample rate fs (Hz), capture duration T (s), bits per sample b
def compute_memory_requirements(fs, T, b):
    # nsamples and memory in bytes
    nsamples = int(fs * T)
    nbytes = nsamples * (b // 8)  # integer bytes per sample
    return nsamples, nbytes

# Example: 200 MS/s, 0.1 s capture, 16-bit samples
fs = 200e6
T = 0.1
b = 16
# prints sample count and memory in MB
print(compute_memory_requirements(fs, T, b))  # quick estimate