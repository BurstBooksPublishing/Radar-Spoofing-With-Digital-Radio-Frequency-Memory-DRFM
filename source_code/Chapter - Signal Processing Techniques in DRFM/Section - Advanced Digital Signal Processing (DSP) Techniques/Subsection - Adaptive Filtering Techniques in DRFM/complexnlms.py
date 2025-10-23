import numpy as np

def nlms_complex(x, d, M=64, mu=0.1, delta=1e-6):
    # x: input array (complex), d: desired array (complex)
    N = len(x)
    w = np.zeros(M, dtype=np.complex64)  # filter coeffs
    y = np.zeros(N, dtype=np.complex64)
    e = np.zeros(N, dtype=np.complex64)
    xbuf = np.zeros(M, dtype=np.complex64)
    for n in range(N):
        # shift-in new sample
        xbuf[1:] = xbuf[:-1]
        xbuf[0] = x[n]
        xn = xbuf  # current input vector
        y[n] = np.vdot(w, xn)  # output (conj of vdot handles complex)
        e[n] = d[n] - y[n]     # error
        norm = np.vdot(xn, xn).real + delta
        w += (mu / norm) * xn * np.conj(e[n])  # NLMS update
    return y, e, w

# Example usage: simulate chirp desired plus narrowband jammer on x