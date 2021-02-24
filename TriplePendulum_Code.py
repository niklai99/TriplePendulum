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

from scipy.integrate import odeint

from IPython.display import HTML



# n -> number of segments
# times -> time instants for the integration of the system
# initial_positions -> initial positions of all (or each, if list) segments IN DEGREES
# initial_velocities -> initial velocities of all (or each, if list) segments IN DEGREES
# lenghts -> lenght of each segment
# masses -> mass of each point
def integrate_pendulum(n, times, initial_positions=135, initial_velocities=0, lengths=None, masses=1):
    """Integrate the equations of motion of a pendulum made of n segments"""

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

    # ODE integration
    return odeint(gradient, y0, times, args=(parameter_vals,))



def get_xy_coords(p, lengths=None):
    """Get (x, y) coordinates from generalized coordinates"""

    # Make the coordinates a 2D array
    p = np.atleast_2d(p)

    # Compute the number of segments from the shape of the coordinates
    n = p.shape[1] // 2

    if lengths is None:
        lengths = np.ones(n) / n

    # Make some zero values to fill all the non-used entries in the following arrays
    zeros = np.zeros(p.shape[0])[:, None]

    # "hstack" stacks arrays in sequence horizontally (column wise)
    # which means we get arrays of x and y coordinates
    # each array of size n
    x = np.hstack([zeros, lengths * np.sin(p[:, :n])])
    y = np.hstack([zeros, -1 * lengths * np.cos(p[:, :n])])

    # we return the cumulative sum of entries in axis 1 -> zeros + projected position of each mass point
    return np.cumsum(x, 1), np.cumsum(y, 1)



def make_plot(x, y):
    """Make the plot of trajectories"""

    # Make figure and axes
    fig = plt.figure( figsize=(6, 6) )
    ax = fig.add_subplot(1, 1, 1)

    # Make ticks invisible
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])

    # Set axis labels
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    # Set axis limits
    ax.set(xlim=(-1, 1), ylim=(-1, 1))

    # Function which selects columns of a matrix
    def column(matrix, i):
        return [row[i] for row in matrix]

    # Here we make some special cases plots with customized line colors
    # if n = 1
    if x.shape[1] == 2:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
    # if n = 2
    elif x.shape[1] == 3:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
        ax.plot( column(x, 2), column(y, 2), color='#ff8404' )
    # if n = 3
    elif x.shape[1] == 4:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
        ax.plot( column(x, 2), column(y, 2), color='#ff8404' )
        ax.plot( column(x, 3), column(y, 3), color='#00C415' )
    # if n = 4
    elif x.shape[1] == 5:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
        ax.plot( column(x, 2), column(y, 2), color='#ff8404' )
        ax.plot( column(x, 3), column(y, 3), color='#00C415' )
        ax.plot( column(x, 4), column(y, 4), color='#ff047f' )
    # if n is greater than 4
    else:
        for i in range(x.shape[1] - 1):
            ax.plot(column(x, i+1), column(y, i+1))

    plt.show()

    return fig



def animate_pendulums(n, times, initial_positions, initial_velocities, lengths, masses, n_pendulums=1, perturbation=0, track_length=15):
    """Make the animation of 'n_pendulums' pendulums"""

    const = 3
    track_length *= const
    
    # Store the coordinates of motions of all pendulums
    p = [integrate_pendulum(n=n, times=times, 
                            initial_positions=initial_positions + i * perturbation / n_pendulums, 
                            initial_velocities=initial_velocities, lengths=lengths, masses=masses)
         for i in range(n_pendulums)]

    # Store the (x, y) coordinates of all pendulums
    positions = np.array([get_xy_coords(pi) for pi in p])

    # Transpose the array (change ordering!)
    positions = positions.transpose(0, 2, 3, 1)
    # positions is a 4D array: (npendulums, len(t), n+1, xy)
    
    # Make figure and axes
    fig = plt.figure( figsize=(6, 6) )
    ax = fig.add_subplot(1, 1, 1)

    # Make ticks invisible
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])

    # Set axis limits
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    
    # Make tracks
    track_segments = np.zeros((n_pendulums, 0, 2))
    tracks = collections.LineCollection(track_segments, cmap='gist_rainbow')
    tracks.set_array(np.linspace(0, 1, n_pendulums))
    ax.add_collection(tracks)
    
    # Make mass points
    points, = plt.plot([], [], 'ok')
    
    # Make pendulum segments
    pendulum_segments = np.zeros((n_pendulums, 0, 2))
    pendulums = collections.LineCollection(pendulum_segments, colors='black')
    ax.add_collection(pendulums)

    # Initial config of the animation
    def init():
        # Set everything to zero
        pendulums.set_segments(np.zeros((n_pendulums, 0, 2)))
        tracks.set_segments(np.zeros((n_pendulums, 0, 2)))
        points.set_data([], [])
        return pendulums, tracks, points

    # Animation
    def animate(i):
        i = i * const

        # Set segments position by indexing to the (x, y) coordinates
        pendulums.set_segments(positions[:, i])

        # Animate the tracks by "going back in time" by a value of 'track_lenght'
        sl = slice(max(0, i - track_length), i)
        tracks.set_segments(positions[:, sl, -1])

        # Extract explicitly the (x, y) coordinates to set mass point positions
        x, y = positions[:, i].reshape(-1, 2).T
        points.set_data(x, y)

        return pendulums, tracks, points

    # Set the time interval of the animation
    interval = 1000 * const * times.max() / len(times)

    # Make the animation
    anim = animation.FuncAnimation(fig, animate, frames=len(times) // const,interval=interval, blit=True, init_func=init)
    
    plt.close(fig)
    return anim