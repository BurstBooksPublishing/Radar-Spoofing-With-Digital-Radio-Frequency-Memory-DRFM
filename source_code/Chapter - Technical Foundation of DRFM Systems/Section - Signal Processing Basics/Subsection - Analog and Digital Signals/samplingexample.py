import numpy as np
# synthesize analog sine (continuous approximation)
f0 = 10e6             # tone at 10 MHz
t_cont = np.linspace(0,1e-6,10000)  # dense time grid for 'analog'
x_cont = np.cos(2*np.pi*f0*t_cont)

# sample at fs and quantize to N bits
fs = 100e6            # sampling rate 100 MHz
t_samp = np.arange(0,1e-6,1/fs)
x_samp = np.cos(2*np.pi*f0*t_samp)  # ideal sampling
N_bits = 8
levels = 2**N_bits
# uniform quantization between -1 and 1
q = np.round((x_samp+1)*(levels/2-1))/ (levels/2-1) - 1
# q now holds quantized samples (simple model)
# further analysis could compute FFTs to inspect aliasing and quantization noise