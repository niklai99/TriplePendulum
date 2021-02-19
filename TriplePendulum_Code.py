import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import collections

import numpy as np

from sympy import symbols
from sympy.physics import mechanics
from sympy import Dummy, lambdify

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
    u = mechanics.dynamicsymbols('u:{0}'.format(n))

    # mass and length of each 
    m = symbols('m:{0}'.format(n))
    l = symbols('l:{0}'.format(n))

    # gravity and time symbols
    g, t = symbols('g,t')
    
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
    forces = []
    kinetic_odes = []

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
        particles.append(Pai)

        # Set forces on every single mass point
        forces.append((Pi, m[i] * g * K.x))

        # Compute kinematic ODEs
        kinetic_odes.append(q[i].diff(t) - u[i])

        P = Pi

    # Generate equations of motion using Khane's Method
    KM = mechanics.KanesMethod(K, q_ind=q, u_ind=u, kd_eqs=kinetic_odes)
    fr, fr_star = KM.kanes_equations(particles, forces)
    

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

    # Define symbols and dictionary for unknown parameters
    unknowns = [Dummy() for i in q + u]
    unknown_dict = dict(zip(q + u, unknowns))

    # Create dictionary for solved parameters 
    kds = KM.kindiffdict()

    # Substitute unknown symbols for qdot terms
    mm_sym = KM.mass_matrix_full.subs(kds).subs(unknown_dict)
    fo_sym = KM.forcing_full.subs(kds).subs(unknown_dict)

    # Create functions for numerical calculation by merging fixed parameters and unknown parameters
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

    fig = plt.figure( figsize=(6, 6) )
    ax = fig.add_subplot(1, 1, 1)

    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    ax.set(xlim=(-1, 1), ylim=(-1, 1))

    def column(matrix, i):
        return [row[i] for row in matrix]

    if x.shape[1] == 2:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
    elif x.shape[1] == 3:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
        ax.plot( column(x, 2), column(y, 2), color='#ff8404' )
    elif x.shape[1] == 4:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
        ax.plot( column(x, 2), column(y, 2), color='#ff8404' )
        ax.plot( column(x, 3), column(y, 3), color='#00C415' )
    elif x.shape[1] == 5:
        ax.plot( column(x, 1), column(y, 1), color='#047fff' )
        ax.plot( column(x, 2), column(y, 2), color='#ff8404' )
        ax.plot( column(x, 3), column(y, 3), color='#00C415' )
        ax.plot( column(x, 4), column(y, 4), color='#ff047f' )
    else:
        for i in range(x.shape[1] - 1):
            ax.plot(column(x, i+1), column(y, i+1))

    plt.show()

    return fig




def animate_pendulum(n, times, initial_positions, initial_velocities, lengths, masses):
    """Make the pendulum animation"""

    p = integrate_pendulum(n, times, initial_positions, initial_velocities, lengths, masses)
    x, y = get_xy_coords(p)
    
    fig = plt.figure( figsize=(6, 6) )
    ax = fig.add_subplot(1, 1, 1)

    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])

    ax.set(xlim=(-1, 1), ylim=(-1, 1))

    line, = ax.plot([], [], 'o-', lw=2)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data(x[i], y[i])
        return line,

    anim = animation.FuncAnimation(fig, animate, frames=len(times),
                                   interval=1000 * times.max() / len(times),
                                   blit=True, init_func=init)
    plt.close(fig)
    return anim




def animate_pendulums(n, times, initial_positions, initial_velocities, lengths, masses, n_pendulums=1, perturbation=0, track_length=15):
    oversample = 3
    track_length *= oversample
    
    t = np.linspace(0, 10, oversample * 200)
    p = [integrate_pendulum(n=n, times=times, 
                            initial_positions=initial_positions + i * perturbation / n_pendulums, 
                            initial_velocities=initial_velocities, lengths=lengths, masses=masses)
         for i in range(n_pendulums)]

    positions = np.array([get_xy_coords(pi) for pi in p])
    positions = positions.transpose(0, 2, 3, 1)
    # positions is a 4D array: (npendulums, len(t), n+1, xy)
    
    fig = plt.figure( figsize=(6, 6) )
    ax = fig.add_subplot(1, 1, 1)

    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])

    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    
    track_segments = np.zeros((n_pendulums, 0, 2))
    tracks = collections.LineCollection(track_segments, cmap='gist_rainbow')
    tracks.set_array(np.linspace(0, 1, n_pendulums))
    ax.add_collection(tracks)
    
    points, = plt.plot([], [], 'ok')
    
    pendulum_segments = np.zeros((n_pendulums, 0, 2))
    pendulums = collections.LineCollection(pendulum_segments, colors='black')
    ax.add_collection(pendulums)

    def init():
        pendulums.set_segments(np.zeros((n_pendulums, 0, 2)))
        tracks.set_segments(np.zeros((n_pendulums, 0, 2)))
        points.set_data([], [])
        return pendulums, tracks, points

    def animate(i):
        i = i * oversample
        pendulums.set_segments(positions[:, i])
        sl = slice(max(0, i - track_length), i)
        tracks.set_segments(positions[:, sl, -1])
        x, y = positions[:, i].reshape(-1, 2).T
        points.set_data(x, y)
        return pendulums, tracks, points

    interval = 1000 * oversample * t.max() / len(t)
    anim = animation.FuncAnimation(fig, animate, frames=len(times) // oversample,
                                   interval=interval,
                                   blit=True, init_func=init)
    plt.close(fig)
    return anim