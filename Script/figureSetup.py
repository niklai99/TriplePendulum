"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    FIGURE SETUP MODULE

    The following code deals with the graphic setup of the figures 
"""

# Python modules
import numpy as np
import matplotlib.pyplot as plt


def staticFigure(n, q, par):
    '''Static plot figure configuration'''

    # Create the figure
    fig = plt.figure(figsize=(14, 6))
    # Set the figure axes grid
    gs = fig.add_gridspec(9, 33)
    
    # Create the axes:
    # ax1 holds the pendulum trajectory
    # ax2 holds the theta trend
    # ax3 holds the omega trend
    ax1 = fig.add_subplot(gs[:, 20:])
    ax2 = fig.add_subplot(gs[0:4, 0:17])
    ax3 = fig.add_subplot(gs[5:9, 0:17])

    # ax1 title and labels
    ax1.set_title('Pendulum Trajectory')
    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    # ax2 title and labels
    ax2.set_title('\u03B8 trend over time')
    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    # ax3 title and labels
    ax3.set_title('\u03C9 trend over time')
    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')

    # Unpack time parameters
    t0 = par[-3]
    tf = par[-2]


    # If the system is the simple pendulum
    if n == 1:

        # Unpack the length of the rope
        l1 = par[n]

        # Compute the total length
        l = l1

        # Compute the maximum and minimum of the theta trend
        tMin = np.amin(q[:,0])
        tMax = np.amax(q[:,0])

        # Compute the maximum and minimum of the omega trend
        oMin = np.amin(q[:,1])
        oMax = np.amax(q[:,1])


    # If the system is the double pendulum
    elif n == 2: 

        # Unpack the length of the ropes
        l1 = par[n]
        l2 = par[n+1]

        # Compute the total length
        l = l1 + l2

        # Compute the maximum and minimum of the theta trend
        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        tMin = np.minimum(t1Min, t2Min)

        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        tMax = np.maximum(t1Max, t2Max)

        # Compute the maximum and minimum of the omega trend
        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        oMin = np.minimum(o1Min, o2Min)

        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        oMax = np.maximum(o1Max, o2Max)


    # If the system is the triple pendulum
    elif n == 3: 
        
        # Unpack the length of the ropes
        l1 = par[n]
        l2 = par[n+1]
        l3 = par[n+2]

        # Compute the total length
        l = l1 + l2 + l3

        # Compute the maximum and minimum of the theta trend
        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        t3Min = np.amin(q[:,4])
        tMin = np.amin([t1Min, t2Min, t3Min])
    
        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        t3Max = np.amax(q[:,4])
        tMax = np.amax([t1Max, t2Max, t3Max])

        # Compute the maximum and minimum of the omega trend
        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        o3Min = np.amin(q[:,4])
        oMin = np.amin([o1Min, o2Min, o3Min])
    
        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        o3Max = np.amax(q[:,4])
        oMax = np.amax([o1Max, o2Max, o3Max])


    # Compute the half span of theta and omega trends
    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    # Set ax1 plot range
    ax1.set_xlim(-(l + l/5), l + l/5)
    ax1.set_ylim(-(l + l/5), l + l/5)

    # Set ax2 plot range
    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin - varT/2, tMax + varT)

    # Set ax3 plot range
    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin - varO/2, oMax + varO)

    return fig, ax1, ax2, ax3


def animatedFigure(n, q, par):
    '''Animated plot figure configuration'''

    # Create the figure
    fig = plt.figure(figsize=(16, 6))
    # Set the figure axes grid
    gs = fig.add_gridspec(9, 35)

    # Create the axes:
    # ax1 holds the pendulum trajectory
    # ax2 holds the theta trend
    # ax3 holds the omega trend
    # ax4 holds the kinetic energy bar
    # ax5 holds the potential energy bar
    ax1 = fig.add_subplot(gs[:, 20:-2])
    ax2 = fig.add_subplot(gs[0:4, 0:17])
    ax3 = fig.add_subplot(gs[5:9, 0:17])
    ax4 = fig.add_subplot(gs[:, -2:-1])
    ax5 = fig.add_subplot(gs[:, -1:])

    # ax1 title and labels
    ax1.set_title('Pendulum Trajectory')
    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    # ax2 title and labels
    ax2.set_title('\u03B8 trend over time')
    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    # ax3 title and labels
    ax3.set_title('\u03C9 trend over time')
    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')

    # ax4 title and labels
    ax4.set_title(r'E$_k$')
    ax4.axes.xaxis.set_ticks([])
    ax4.axes.yaxis.set_ticks([])
    ax4.yaxis.set_label_position("right")

    # ax5 title and labels
    ax5.set_title(r'E$_p$')
    ax5.axes.xaxis.set_ticks([])
    ax5.axes.yaxis.set_ticks([])
    ax5.yaxis.set_label_position("right")

    # Unpack time parameters
    t0 = par[-3]
    tf = par[-2]

    # If the system is the simple pendulum
    if n == 1:
        
        # Unpack the length of the rope
        l1 = par[n]

        # Compute the total length
        l = l1

        # Compute the maximum and minimum of the theta trend
        tMin = np.amin(q[:,0])
        tMax = np.amax(q[:,0])

        # Compute the maximum and minimum of the omega trend
        oMin = np.amin(q[:,1])
        oMax = np.amax(q[:,1])


    # If the system is the double pendulum
    elif n == 2: 
        
        # Unpack the length of the ropes
        l1 = par[n]
        l2 = par[n+1]

        # Compute the total length
        l = l1 + l2

        # Compute the maximum and minimum of the theta trend
        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        tMin = np.minimum(t1Min, t2Min)

        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        tMax = np.maximum(t1Max, t2Max)

        # Compute the maximum and minimum of the omega trend
        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        oMin = np.minimum(o1Min, o2Min)

        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        oMax = np.maximum(o1Max, o2Max)

    
    # If the system is the triple pendulum
    elif n == 3: 

        # Unpack the length of the ropes
        l1 = par[n]
        l2 = par[n+1]
        l3 = par[n+2]

        # Compute the total length
        l = l1 + l2 + l3

        # Compute the maximum and minimum of the theta trend
        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        t3Min = np.amin(q[:,4])
        tMin = np.amin([t1Min, t2Min, t3Min])
    
        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        t3Max = np.amax(q[:,4])
        tMax = np.amax([t1Max, t2Max, t3Max])

        # Compute the maximum and minimum of the omega trend
        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        o3Min = np.amin(q[:,4])
        oMin = np.amin([o1Min, o2Min, o3Min])
    
        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        o3Max = np.amax(q[:,4])
        oMax = np.amax([o1Max, o2Max, o3Max])


    # Compute the half span of theta and omega trends
    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    # Set ax1 plot range
    ax1.set_xlim(-(l + l/5), l + l/5)
    ax1.set_ylim(-(l + l/5), l + l/5)

    # Set ax2 plot range
    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin - varT/2, tMax + varT)

    # Set ax3 plot range
    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin - varO/2, oMax + varO)

    # Set ax4 plot range
    ax4.set_xlim(0, 1)
    ax4.set_ylim(-1, 1)

    # Set ax5 plot range
    ax5.set_xlim(0, 1)
    ax5.set_ylim(-1, 1)

    return fig, ax1, ax2, ax3, ax4, ax5


def addLegend(n, ax1, ax2, ax3):
    '''Adds the plot legend depending on the type of system'''

    ax1.legend(loc = 'upper right', ncol = 1)
    ax2.legend(loc = 'upper right', ncol = n)
    ax3.legend(loc = 'upper right', ncol = n)
    return
