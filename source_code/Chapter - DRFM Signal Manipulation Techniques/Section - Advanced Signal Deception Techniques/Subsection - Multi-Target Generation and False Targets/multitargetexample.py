import numpy as np
# s: complex baseband pulse (1D numpy array), fs: sampling rate
# targets: list of tuples (delay_sec, amp, vel_m_s, phase_offset)
def synthesize_multi_targets(s, fs, targets, fc):
    N = len(s)
    # FFT of input pulse
    S = np.fft.fft(s)
    freqs = np.fft.fftfreq(N, d=1.0/fs)  # Hz
    out = np.zeros(N, dtype=complex)
    for delay_sec, amp, vel, phi0 in targets:
        # fractional delay as linear phase in freq domain
        phase_delay = np.exp(-1j * 2 * np.pi * freqs * delay_sec)
        # Doppler shift (approximate baseband multiplication)
        fD = 2 * vel / (3e8 / fc)  # Doppler frequency in Hz
        # Doppler as time-domain multiplication => freq shift via phase ramp per sample
        # Here we apply Doppler via frequency-domain shift (simple model)
        phase_doppler = np.exp(1j * 2 * np.pi * fD * np.arange(N)/fs)
        # Build delayed waveform in time domain
        s_del = np.fft.ifft(S * phase_delay)
        # Apply Doppler and amplitude and phase offset
        s_echo = amp * s_del * phase_doppler * np.exp(1j*phi0)
        out += s_echo
    return out
# Note: production systems use overlap-save, windowing, and higher-order interpolation.