# capture_buffer: ring buffer of complex baseband samples
# schedule_queue: retransmit events with time offsets
# NOTE: comments are brief for clarity
import numpy as np

def apply_fractional_delay(x, frac_delay):
    # simple sinc interpolation; replace with polyphase for real system
    n = np.arange(len(x))
    h = np.sinc(n - frac_delay) * np.hamming(len(x))
    return np.convolve(x, h, mode='same')

def apply_doppler(x, delta_f, fs):
    t = np.arange(len(x)) / fs
    return x * np.exp(1j * 2 * np.pi * delta_f * t)  # apply phase ramp

def drfm_process(capture_buffer, fs):
    while True:
        pulse = capture_buffer.get_next_pulse()  # blocking read
        # compute spoof profile (delay, doppler, amplitude envelope)
        delay_sec = compute_desired_delay(pulse)   # mission-specific
        doppler_hz = compute_desired_doppler(pulse)
        amp_env = compute_amplitude_envelope(pulse)
        frac_delay_samples = delay_sec * fs
        # apply fractional delay and doppler
        delayed = apply_fractional_delay(pulse, frac_delay_samples)
        shifted = apply_doppler(delayed, doppler_hz, fs)
        output = amp_env * shifted
        schedule_queue.enqueue_transmit(output, when=delay_sec)  # timing critical