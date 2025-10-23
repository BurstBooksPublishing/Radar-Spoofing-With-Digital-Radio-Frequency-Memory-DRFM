# sig_rx: received complex baseband vector (samples)
# sig_ref: expected echo template (watermarked)
# tf_map: time-frequency representation function (STFT)
import numpy as np

# basic correlation (coarse verification)
corr = np.vdot(sig_ref, sig_rx)  # complex inner product
mag = np.abs(corr)

# adaptive threshold based on noise estimate
noise_est = np.median(np.abs(sig_rx))  # simple noise proxy
threshold = 5 * noise_est  # adjustable factor

if mag < threshold:
    # possible spoof or weak return
    # compute time-frequency consistency
    S_rx = tf_map(sig_rx)
    S_ref = tf_map(sig_ref)
    # compare energy distribution (normalized)
    dist = np.linalg.norm(np.abs(S_rx)/np.sum(np.abs(S_rx)) -
                          np.abs(S_ref)/np.sum(np.abs(S_ref)))
    if dist > 0.2:
        print("High likelihood of spoofing")  # detection flag
    else:
        print("Ambiguous; escalate to challenge-response")
else:
    print("Echo authenticated (correlation pass)")