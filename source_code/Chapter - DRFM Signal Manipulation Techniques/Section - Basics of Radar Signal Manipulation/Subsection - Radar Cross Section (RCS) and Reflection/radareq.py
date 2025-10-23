# Simple radar equations: compute received power and delay for a fake range
import numpy as np

c = 3e8                 # speed of light (m/s)
Pt = 1000.0             # transmit power (W)
G = 30.0                # antenna gain (linear)
lambda_m = 0.03         # wavelength (m) -> 10 GHz ~ 0.03 m
sigma = 1.0             # RCS in m^2
R_true = 20000.0        # true range (m)
L = 1.5                 # system loss factor

# monostatic received power from Eq. (radar_eq)
Pr = (Pt * G * G * lambda_m**2 * sigma) / ((4*np.pi)**3 * R_true**4 * L)
print("# Received power (W):", Pr)

# convert RCS to dBsm
sigma_db = 10*np.log10(sigma)
print("# RCS (dBsm):", sigma_db)

# desired fake range and required extra delay
R_fake = 15000.0        # desired apparent range (m)
delta_R = R_fake - R_true
delta_t = 2.0 * delta_R / c   # round-trip delay change
print("# Required additional delay (s):", delta_t)