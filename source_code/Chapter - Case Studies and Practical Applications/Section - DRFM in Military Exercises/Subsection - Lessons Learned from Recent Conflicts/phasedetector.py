# load coherent pulse returns (complex samples)
# x[n] is complex sample for pulse n
window = 32                          # number of pulses for stat window
phase_diff = []                      # collect inter-pulse phase deltas
amp_var = []                         # amplitude variance window

for n in range(1, len(x)):
    # compute inter-pulse phase difference (unwrap)
    dphi = np.angle(x[n] * np.conj(x[n-1]))
    phase_diff.append(dphi)
    # rolling amplitude variance (magnitude)
    amp_var.append(np.var(np.abs(x[max(0,n-window):n+1])))

# simple thresholds (set by ROC analysis in practice)
phase_anomaly = np.mean(np.abs(phase_diff)) > 0.5  # radian threshold
amp_anomaly = np.mean(amp_var) > 0.1               # normalized units

# flag if both anomalies present
if phase_anomaly and amp_anomaly:
    alert("Possible DRFM replay or manipulation detected")