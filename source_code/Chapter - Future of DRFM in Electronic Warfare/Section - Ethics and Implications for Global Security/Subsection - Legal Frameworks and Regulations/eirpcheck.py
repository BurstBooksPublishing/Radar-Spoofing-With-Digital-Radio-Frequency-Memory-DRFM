# Compute EIRP and check against a regulatory limit; also check occupied bandwidth.
# All values in dB/dBm or Hz as indicated.
P_tx_dbm = 10.0            # transmitter power in dBm (example)
G_tx_dbi = 12.0            # transmit antenna gain in dBi (example)
loss_dB = 2.0              # system losses in dB
eirp_dbm = P_tx_dbm + G_tx_dbi - loss_dB  # follows eq: EIRP = P_tx + G - L

EIRP_limit_dbm = 36.0      # example regulatory EIRP limit for this band
occupied_bw_hz = 5e6       # measured occupied bandwidth in Hz
bandwidth_limit_hz = 6e6   # regulatory bandwidth allocation

# Compliance checks
eirp_ok = eirp_dbm <= EIRP_limit_dbm
bw_ok = occupied_bw_hz <= bandwidth_limit_hz

print(f"EIRP = {eirp_dbm:.1f} dBm -> {'OK' if eirp_ok else 'EXCEEDS LIMIT'}")
print(f"Occupied BW = {occupied_bw_hz/1e6:.2f} MHz -> {'OK' if bw_ok else 'EXCEEDS LIMIT'}")
# If non-compliant, raise flag and require mitigation before operation.
if not (eirp_ok and bw_ok):
    raise SystemExit("Regulatory non-compliance detected: abort deployment.")