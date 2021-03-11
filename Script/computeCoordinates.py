"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    COMPUTE COORDINATES MODULE

    The following code computes the (x, y) coordinates from the generalized coordinates q
"""

import numpy as np 

def computeCoordinates(n, q, par):
    '''Computes cartesian coordinates from generalized coordinates'''

    x = np.zeros((n, len(q[:,0])))
    y = np.zeros((n, len(q[:,0])))

    if n == 1:

        x[0] = +par[n] * np.sin(q[:,0])
        y[0] = -par[n] * np.cos(q[:,0])

    elif n == 2:
        x[0] = +par[n] * np.sin(q[:,0])
        y[0] = -par[n] * np.cos(q[:,0])
        x[1] = +par[n+1] * np.sin(q[:,2]) + x[0]
        y[1] = -par[n+1] * np.cos(q[:,2]) + y[0]
    
    elif n == 3:
        x[0] = +par[n] * np.sin(q[:,0])
        y[0] = -par[n] * np.cos(q[:,0])
        x[1] = +par[n+1] * np.sin(q[:,2]) + x[0]
        y[1] = -par[n+1] * np.cos(q[:,2]) + y[0]
        x[2] = +par[n+2] * np.sin(q[:,4]) + x[1]
        y[2] = -par[n+2] * np.cos(q[:,4]) + y[1]

    return x.T, y.T

