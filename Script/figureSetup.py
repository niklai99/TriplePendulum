"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    FIGURE SETUP MODULE

    The following code deals with the graphic setup of the figures 
"""

import numpy as np
import matplotlib.pyplot as plt


def staticFigure(n, q, par):
    '''Static plot figure configuration'''

    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(9, 33)
    
    ax1 = fig.add_subplot(gs[:, 20:])
    ax2 = fig.add_subplot(gs[0:4, 0:17])
    ax3 = fig.add_subplot(gs[5:9, 0:17])


    ax1.set_title('Pendulum Trajectory')
    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    ax2.set_title('\u03B8 trend over time')
    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    ax3.set_title('\u03C9 trend over time')
    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')


    t0 = par[-3]
    tf = par[-2]

    if n == 1:

        l1 = par[n]

        l = l1

        tMin = np.amin(q[:,0])
        tMax = np.amax(q[:,0])

        oMin = np.amin(q[:,1])
        oMax = np.amax(q[:,1])


    elif n == 2: 

        l1 = par[n]
        l2 = par[n+1]

        l = l1 + l2

        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        tMin = np.minimum(t1Min, t2Min)

        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        tMax = np.maximum(t1Max, t2Max)

        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        oMin = np.minimum(o1Min, o2Min)

        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        oMax = np.maximum(o1Max, o2Max)


    elif n == 3: 

        l1 = par[n]
        l2 = par[n+1]
        l3 = par[n+2]

        l = l1 + l2 + l3
    
        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        t3Min = np.amin(q[:,4])
        tMin = np.amin([t1Min, t2Min, t3Min])
    
        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        t3Max = np.amax(q[:,4])
        tMax = np.amax([t1Max, t2Max, t3Max])
    
        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        o3Min = np.amin(q[:,4])
        oMin = np.amin([o1Min, o2Min, o3Min])
    
        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        o3Max = np.amax(q[:,4])
        oMax = np.amax([o1Max, o2Max, o3Max])


    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    ax1.set_xlim(-(l + l/5), l + l/5)
    ax1.set_ylim(-(l + l/5), l + l/5)

    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin - varT/2, tMax + varT)

    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin - varO/2, oMax + varO)

    return fig, ax1, ax2, ax3


def animatedFigure(n, q, par):
    '''Static plot figure configuration'''

    fig = plt.figure(figsize=(16, 6))
    gs = fig.add_gridspec(9, 35)

    ax1 = fig.add_subplot(gs[:, 20:-2])
    ax2 = fig.add_subplot(gs[0:4, 0:17])
    ax3 = fig.add_subplot(gs[5:9, 0:17])
    ax4 = fig.add_subplot(gs[:, -2:-1])
    ax5 = fig.add_subplot(gs[:, -1:])


    ax1.set_title('Pendulum Trajectory')
    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    ax2.set_title('\u03B8 trend over time')
    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    ax3.set_title('\u03C9 trend over time')
    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')

    ax4.set_title(r'E$_k$')
    ax4.axes.xaxis.set_ticks([])
    ax4.axes.yaxis.set_ticks([])
    ax4.yaxis.set_label_position("right")

    ax5.set_title(r'E$_p$')
    ax5.axes.xaxis.set_ticks([])
    ax5.axes.yaxis.set_ticks([])
    ax5.yaxis.set_label_position("right")


    t0 = par[-3]
    tf = par[-2]

    if n == 1:

        l1 = par[n]

        l = l1

        tMin = np.amin(q[:,0])
        tMax = np.amax(q[:,0])

        oMin = np.amin(q[:,1])
        oMax = np.amax(q[:,1])

    elif n == 2: 

        l1 = par[n]
        l2 = par[n+1]

        l = l1 + l2

        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        tMin = np.minimum(t1Min, t2Min)

        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        tMax = np.maximum(t1Max, t2Max)

        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        oMin = np.minimum(o1Min, o2Min)

        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        oMax = np.maximum(o1Max, o2Max)

    
    elif n == 3: 

        l1 = par[n]
        l2 = par[n+1]
        l3 = par[n+2]

        l = l1 + l2 + l3
    
        t1Min = np.amin(q[:,0])
        t2Min = np.amin(q[:,2])
        t3Min = np.amin(q[:,4])
        tMin = np.amin([t1Min, t2Min, t3Min])
    
        t1Max = np.amax(q[:,0])
        t2Max = np.amax(q[:,2])
        t3Max = np.amax(q[:,4])
        tMax = np.amax([t1Max, t2Max, t3Max])
    
        o1Min = np.amin(q[:,1])
        o2Min = np.amin(q[:,3])
        o3Min = np.amin(q[:,4])
        oMin = np.amin([o1Min, o2Min, o3Min])
    
        o1Max = np.amax(q[:,1])
        o2Max = np.amax(q[:,3])
        o3Max = np.amax(q[:,4])
        oMax = np.amax([o1Max, o2Max, o3Max])


    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    ax1.set_xlim(-(l + l/5), l + l/5)
    ax1.set_ylim(-(l + l/5), l + l/5)

    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin - varT/2, tMax + varT)

    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin - varO/2, oMax + varO)

    ax4.set_xlim(left = 0, right = 1)
    ax4.set_ylim(bottom = -1, top = 1)

    ax5.set_xlim(left = 0, right = 1)
    ax5.set_ylim(bottom = -1, top = 1)

    return fig, ax1, ax2, ax3, ax4, ax5


