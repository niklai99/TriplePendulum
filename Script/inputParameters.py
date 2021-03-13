"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    INPUT PARAMETERS MODULE

    The following code deals with getting key parameters of the system from the user
"""

# Python module
import numpy as np


def inputParameters(n):
    '''Reads parameters from keyboard and returns the list of parameters'''

    # Initialize the array p to hold masses and lengths
    p = np.zeros(2*n)
    # Initialize the array q to hold initial conditions
    q0 = np.zeros(2*n)
    # Initialize the array simTime to hold information time
    simTime = np.zeros(3)


    # Fill the p array with masses
    for i in range(n):    
        p[i] = float(input('\nInsert mass for point %1.0f: ' % (i+1)))

    # Fill the p array with lengths
    for j in range(n):
        p[j+n] = float(input('\nInsert length for rope %1.0f: ' % (j+1)))
    
    # Fill the q0 array with initial angles
    for k in range(n):
        q0[2*k] = np.radians(float(input('\nInsert initial angle of point %1.0f (in deg): ' % (k+1))))

    # Fill the q0 array with initial velocities
    for l in range(n):
        q0[2*l + 1] = np.radians(float(input('\nInsert initial angular velocity of point %1.0f (in deg/s): ' % (l+1))))

    # Fill the simTime array with the starting time, ending time and the number of iterations to perform
    simTime[0] = int(input("\nInsert starting time: "))
    simTime[1] = int(input("\nInsert ending time: "))
    simTime[2] = int(input('\nInsert number of iterations: '))

    # Create the parameters list
    par = [*p, q0, *simTime]

    return par