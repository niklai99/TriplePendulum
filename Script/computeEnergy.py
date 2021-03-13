"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    COMPUTE ENERGY MODULE

    The following code computes the kinetic, potential and total energy of the system
"""

# Python module
import numpy as np


def simplePendulumEnergy(q, par):
    '''Computes and returns total energy of the simple pendulum system'''

    # Unpack the relevant parameters
    m1 = par[0]
    l1 = par[1]

    # Unpack theta and omega from the generalized coordinates array q
    t1, o1 = q.T

    # Initialize arrays for the three energies
    E = np.zeros(len(t1))
    U = np.zeros(len(t1))
    T = np.zeros(len(t1))

    # Fill the energy arrays 
    for i in range(len(t1)):
        E[i] = 0.5 * m1 * l1**2 * o1[i]**2
        U[i] = - m1 * 9.81 * l1*np.cos(t1[i])
        T[i] = E[i] + U[i]

    return E, U, T


def doublePendulumEnergy(q, par):
    '''Computes and returns total energy of the double pendulum system'''

    # Unpack the relevant parameters
    m1 = par[0]
    m2 = par[1]
    l1 = par[2]
    l2 = par[3]

    # Unpack theta and omega from the generalized coordinates array q
    t1, o1, t2, o2 = q.T

    # Initialize arrays for the three energies
    E = np.zeros(len(t1))
    U = np.zeros(len(t1))
    T = np.zeros(len(t1))

    # Fill the energy arrays
    for i in range(len(t1)):
        E[i] = 0.5 * (m1+m2) * l1**2 * o1[i]**2 + 0.5 * m2 * l2**2 * o2[i]**2 + m2 * l1 * l2 * o1[i]*o2[i]*np.cos(t1[i]-t2[i])
        U[i] = - m1 * 9.81 * l1*np.cos(t1[i]) - m2 * 9.81 * (l1*np.cos(t1[i]) + l2*np.cos(t2[i]))
        T[i] = E[i] + U[i]

    return E, U, T


def triplePendulumEnergy(q, par):
    '''Computes and returns total energy of the triple pendulum system'''

    # Unpack the relevant parameters
    m1 = par[0]
    m2 = par[1]
    m3 = par[2]
    l1 = par[3]
    l2 = par[4]
    l3 = par[5]

    # Unpack theta and omega from the generalized coordinates array q
    t1, o1, t2, o2, t3, o3 = q.T

    # Initialize arrays for the three energies
    E = np.zeros(len(t1))
    U = np.zeros(len(t1))
    T  = np.zeros(len(t1))

    # Fill the energy arrays
    for i in range(len(t1)):
        E[i] = 0.5 * (m1+m2+m3) * l1**2 * o1[i]**2 + 0.5 * (m2+m3) * l2**2 * o2[i]**2 + 0.5 * m3 * l3**2 * o3[i]**2 + (m2+m3)*l1*l2*o1[i]*o2[i]*np.cos(t1[i]-t2[i]) +  m3*l1*l3*o1[i]*o3[i]*np.cos(t1[i]-t3[i]) + m3*l2*l3*o2[i]*o3[i]*np.cos(t2[i]-t3[i])
        U[i] = - 9.81 * ( l1*(m1+m2+m3)*np.cos(t1[i]) + l2*(m2+m3)*np.cos(t2[i]) +  l3*m3*np.cos(t3[i]) )
        T[i] = E[i] + U[i]

    return E, U, T