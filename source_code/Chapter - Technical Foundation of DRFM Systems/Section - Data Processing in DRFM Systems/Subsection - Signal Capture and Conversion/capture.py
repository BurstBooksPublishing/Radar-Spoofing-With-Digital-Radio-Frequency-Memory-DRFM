# Initialize ADC and DMA (pseudo-API)
adc = ADCDevice(rate=200e6, bits=14)      # 200 MS/s, 14-bit ADC
dma = DMAController(adc)                  # attach DMA to ADC
buffer = dma.allocate_buffer(size=2**20)  # circular buffer (1M samples)

# Capture loop (simplified)
while True:
    idx, length = dma.get_filled_region()    # get filled region in buffer
    samples = buffer.read(idx, length)       # raw integer samples
    # Convert to floating point voltage, apply I/Q demod if ADC is real
    volt = adc.to_voltage(samples)           # convert counts to volts
    # Digital downconversion to complex baseband (centered at f0)
    t = np.arange(len(volt)) / adc.rate
    lo = np.exp(-2j * np.pi * f0 * t)        # complex LO (vectorized)
    complex_baseband = volt * lo             # mix to baseband
    decimated = decimate(complex_baseband, q=8)  # reduce sample rate
    process(decimated)                       # hand off to DSP routines
    dma.release_region(idx, length)          # free buffer region