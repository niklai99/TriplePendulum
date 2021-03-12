import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import collections

import numpy as np

from sympy import *
import sympy as sp
from sympy import symbols
from sympy.physics import mechanics
from sympy import Dummy, lambdify
from sympy import Derivative

def integrate_pendulum(n, times, initial_positions=135, initial_velocities=0, lengths=None, masses=1):

    #-------------------------------------------------
    # PENDULUM MODEL
    
    # Generalized coordinates and velocities
    # (angular positions & velocities of each mass) 
    q = mechanics.dynamicsymbols('q:{0}'.format(n))
    u = mechanics.dynamicsymbols('q:{0}'.format(n), 1)

    # mass and length of each 
    m = symbols('m:{0}'.format(n))
    l = symbols('l:{0}'.format(n))

    # gravity and time symbols
    g, t = symbols('g t')
    
    #--------------------------------------------------
    # INTEGRATION MODEL

    # Create reference frame
    # The reference frame will have the x axis pointing down, y axis pointing right and z axis pointing inwards the screen
    K = mechanics.ReferenceFrame('K')

    # Create point (which stores the position, velocity and acceleration)
    P = mechanics.Point('P')

    # Set to zero the velocity of the point in the reference frame K
    P.set_vel(K, 0)

    # Create lists to hold particles, forces and kinetic ODEs for each pendulum's segment
    particles = []

    # Run through all the segments:
    for i in range(n):
        # Create a reference frame following the i^th mass
        # We call the new frames "Ki" (i=1...n)
        # The new frames follow the position of the i^th mass and are rotated around the z axis
        Ki = K.orientnew('K' + str(i), 'Axis', [q[i], K.z])

        # Set the angular velocity of the frame Ki with respect to the frame K 
        Ki.set_ang_vel(K, u[i] * K.z)

        # Create a point in this reference frame
        Pi = P.locatenew('P' + str(i), l[i] * Ki.x)

        # Set the velocity of this point in K based on the velocity of P in Ki
        Pi.v2pt_theory(P, K, Ki)

        # Create a new particle of mass m[i] at this point
        Pai = mechanics.Particle('Pa' + str(i), Pi, m[i])

        # Potential energies
        for j in range(i+1):
            Pai.potential_energy += -1 * m[i] * g * ( l[j] * sp.cos(q[j]) )

        particles.append(Pai)


        P = Pi

    # Generate equations of motion using Lagrange's Method
    L = mechanics.Lagrangian(K, *particles)
    LM = mechanics.LagrangesMethod(L, q)
    eq = LM.form_lagranges_equations()

        #-----------------------------------------------------
    # NUMERICAL INTEGRATION

    # Initial positions and velocities GIVEN IN DEGREES (here converted to radiants)
    y0 = np.deg2rad(np.concatenate([np.broadcast_to(initial_positions, n),
                                    np.broadcast_to(initial_velocities, n)]))

    # Create an array of lengths and masses (given as parameter to the function)
    if lengths is None:
        lengths = np.ones(n) / n

    lengths = np.broadcast_to(lengths, n)
    masses = np.broadcast_to(masses, n)

    # Set fixed parameters: gravitational constant, lengths, and masses
    parameters = [g] + list(l) + list(m)
    parameter_vals = [9.81] + list(lengths) + list(masses)

    dq = []
    for i in range(n):
        dq.append(q[i].diff(t))

    d = dict(zip(dq, u))

    unknowns = [Dummy() for i in q + u]
    unknown_dict = dict(zip(q + u, unknowns))

    mm_sym = LM.mass_matrix_full.subs(d).subs(unknown_dict)
    fo_sym = LM.forcing_full.subs(d).subs(unknown_dict)
    mm_func = lambdify(unknowns + parameters, mm_sym)
    fo_func = lambdify(unknowns + parameters, fo_sym)

    # Function which computes the derivatives of parameters
    # Needed for integrating the ODEs 
    def gradient(y, t, args):
        vals = np.concatenate((y, args))
        sol = np.linalg.solve(mm_func(*vals), fo_func(*vals))
        return np.array(sol).T[0]

    