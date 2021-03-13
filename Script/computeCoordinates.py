"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    COMPUTE COORDINATES MODULE

    The following code computes the (x, y) coordinates from the generalized coordinates q
"""

# Python module
import numpy as np 


def computeCoordinates(n, q, par):
    '''Computes cartesian coordinates from generalized coordinates'''

    # Initialize (x, y) arrays to be multi dimensional arrays depending on the type of pendulum
    x = np.zeros((n, len(q[:,0])))
    y = np.zeros((n, len(q[:,0])))

    # If the system is the simple pendulum
    if n == 1:

        x[0] = +par[n] * np.sin(q[:,0])
        y[0] = -par[n] * np.cos(q[:,0])

    # If the system is the double pendulum
    elif n == 2:
        x[0] = +par[n] * np.sin(q[:,0])
        y[0] = -par[n] * np.cos(q[:,0])
        x[1] = +par[n+1] * np.sin(q[:,2]) + x[0]
        y[1] = -par[n+1] * np.cos(q[:,2]) + y[0]
    
    # If the system is the triple pendulum
    elif n == 3:
        x[0] = +par[n] * np.sin(q[:,0])
        y[0] = -par[n] * np.cos(q[:,0])
        x[1] = +par[n+1] * np.sin(q[:,2]) + x[0]
        y[1] = -par[n+1] * np.cos(q[:,2]) + y[0]
        x[2] = +par[n+2] * np.sin(q[:,4]) + x[1]
        y[2] = -par[n+2] * np.cos(q[:,4]) + y[1]

    return x.T, y.T

