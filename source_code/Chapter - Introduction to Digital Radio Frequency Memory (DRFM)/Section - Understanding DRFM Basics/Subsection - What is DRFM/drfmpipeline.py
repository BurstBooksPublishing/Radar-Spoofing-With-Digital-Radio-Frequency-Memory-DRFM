# capture samples from ADC (complex baseband samples)
buffer           = adc.read_block()                  # blocking read of N samples

# apply manipulation: delay, amplitude, phase
delayed          = apply_delay(buffer, delay_samples)      # insert or shift samples
phase_shifted    = delayed * np.exp(1j * phase_ramp)       # apply phase modulation
amplitude_scaled = gain * phase_shifted                    # control amplitude

# optionally generate multiple targets by copying and offsetting
composite        = sum([np.roll(amplitude_scaled, k * offset)
                        for k in targets])

# write to DAC for RF retransmission
dac.write_block(composite)                           # convert back to analog and upconvert