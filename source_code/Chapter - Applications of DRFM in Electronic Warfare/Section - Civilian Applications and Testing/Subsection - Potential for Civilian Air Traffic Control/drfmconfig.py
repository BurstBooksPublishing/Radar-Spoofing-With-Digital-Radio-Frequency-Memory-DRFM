# Configure DRFM to create one replica with delay and Doppler
# (This pseudocode assumes API calls provided by the DRFM vendor.)
drfm = DRFMConnection('192.168.0.10')            # connect to device
drfm.lock_to_radar()                              # lock LO and PRF
# Request parameters: delay in seconds, radial velocity in m/s, amplitude scale (linear)
params = {'delay': 5e-6, 'velocity': 60.0, 'amp_scale': 0.8}
# Compute Doppler shift for carrier frequency fc (Hz) and speed of light c
fc = drfm.get_carrier_frequency()
c = 299792458.0
# Doppler frequency (Hz) = 2*v / lambda
doppler = 2.0 * params['velocity'] * fc / c
drfm.set_replica(delay=params['delay'], doppler=doppler, amplitude=params['amp_scale'])
drfm.activate_simulation(duration=300)            # run for 5 minutes
# Monitor and log telemetry for validation
for t in range(0,300,10):
    log = drfm.get_status()
    print('#', t, 's', log['sync_error'], log['power_level'])
drfm.deactivate()