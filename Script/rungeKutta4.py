import numpy as np 


def rk4(f, q0, t0, tf, n):
    '''Runge-Kutta 4'''

    t = np.linspace(t0, tf, n+1)
    h = t[1]-t[0]
    q = np.array((n+1)*[q0])
    
    for i in range(n):
        k1 = h * f(q[i], t[i])
        k2 = h * f(q[i] + 0.5 * k1, t[i] + 0.5*h)
        k3 = h * f(q[i] + 0.5 * k2, t[i] + 0.5*h)
        k4 = h * f(q[i] + k3, t[i] + h)
        q[i+1] = q[i] + (k1 + 2*(k2 + k3) + k4) / 6

    return q, t