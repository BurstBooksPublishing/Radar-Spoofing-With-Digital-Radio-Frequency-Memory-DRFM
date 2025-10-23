# Capture: stream samples from ADC (blocking read)
samples = adc.read_block(n_samples)   # read n_samples from ADC

# Manipulate: apply time delay and phase rotation (example)
delayed = np.roll(samples, delay_samples)    # circular shift -> time delay
phase = np.exp(1j * phase_offset)            # complex phase rotation
manipulated = delayed * phase

# Replay: send modified samples to DAC (blocking write)
dac.write_block(manipulated)                 # output to RF chain