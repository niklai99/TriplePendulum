"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    RUNGE-KUTTA 4 MODULE

    The following code is a simple implementation of the Runge-Kutta 4 iterative method
"""

import numpy as np 


def RungeKutta4(f, par):
    '''Runge-Kutta 4'''

    q0 = par[-4]
    t0 = par[-3]
    tf = par[-2]
    n  = par[-1]

    t = np.linspace(int(t0), int(tf), int(n)+1)
    h = t[1]-t[0]
    q = np.array((int(n)+1)*[q0])
    
    for i in range(int(n)):
        k1 = h * f(q[i], t[i], par)
        k2 = h * f(q[i] + 0.5 * k1, t[i] + 0.5*h, par)
        k3 = h * f(q[i] + 0.5 * k2, t[i] + 0.5*h, par)
        k4 = h * f(q[i] + k3, t[i] + h, par)
        q[i+1] = q[i] + (k1 + 2*(k2 + k3) + k4) / 6

    return q, t