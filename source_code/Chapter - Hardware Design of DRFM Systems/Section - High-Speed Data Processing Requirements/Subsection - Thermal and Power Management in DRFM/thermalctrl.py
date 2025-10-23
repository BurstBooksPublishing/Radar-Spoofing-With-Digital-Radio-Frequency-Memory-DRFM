# Read sensors and control fans/DVFS (pseudocode)
def thermal_control_loop(sensor_iface, dvfs_iface, fan_iface):
    # target temperatures (degC)
    T_target = 70.0
    T_critical = 90.0
    # controller gains (tuned empirically)
    kp = 0.8
    ki = 0.02
    kd = 0.1
    integral = 0.0
    prev_err = 0.0
    while True:
        T_fpga = sensor_iface.read('FPGA_TEMP')    # die temp
        err = T_fpga - T_target
        integral += err * SAMPLE_PERIOD
        derivative = (err - prev_err) / SAMPLE_PERIOD
        fan_cmd = clamp(kp*err + ki*integral + kd*derivative, 0.0, 1.0)
        fan_iface.set_duty(fan_cmd)                # 0.0..1.0
        if T_fpga > T_critical:
            dvfs_iface.set_mode('SAFE')           # aggressive throttling
        elif T_fpga > T_target + 5:
            dvfs_iface.set_clock( dvfs_iface.get_clock() * 0.9 )
        prev_err = err
        sleep(SAMPLE_PERIOD)