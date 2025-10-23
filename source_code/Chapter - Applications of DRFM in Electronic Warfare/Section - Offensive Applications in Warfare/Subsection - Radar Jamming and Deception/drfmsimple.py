import numpy as np

# x: captured complex baseband samples (numpy array)
# fs: sampling rate in Hz
# echoes: list of dicts with keys 'delay_s','amp','freq_offset','phase'
def synthesize_echoes(x, fs, echoes):
    N = len(x)
    t = np.arange(N) / fs
    y = np.zeros(N, dtype=np.complex64)
    for e in echoes:
        # integer and fractional delay in samples
        d = e['delay_s'] * fs
        d_int = int(np.floor(d))
        frac = d - d_int
        # simple linear interpolation fractional delay (placeholder)
        x_del = np.roll(x, d_int)  # coarse shift
        if frac != 0:
            x_del[:-1] = (1-frac)*x_del[:-1] + frac*x_del[1:]  # crude fractional delay
        # apply amplitude, frequency shift, and phase
        y += e['amp'] * x_del * np.exp(1j*(2*np.pi*e['freq_offset']*t + e.get('phase',0.0)))
    return y

# Example usage (comments show intent)
# captured = ... # acquire samples from ADC
# echoes = [{'delay_s':1e-6,'amp':0.8,'freq_offset':100.0,'phase':0.0},
#           {'delay_s':2.5e-6,'amp':0.5,'freq_offset':-50.0,'phase':0.2}]
# out = synthesize_echoes(captured, 1e6, echoes)
# send out through DAC and RF upconverter