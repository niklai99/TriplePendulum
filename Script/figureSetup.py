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


def figureSetup(t1, o1, par):
    '''Plot figure configuration'''

    l1 = par[1]
    t0 = par[3]
    tf = par[4]

    t1Min = np.amin(t1)
    t1Max = np.amax(t1)

    o1Min = np.amin(o1)
    o1Max = np.amax(o1)

    varT = (t1Max - t1Min) / 2
    varO = (o1Max - o1Min) / 2

    fig1 = plt.figure(figsize=(16, 6))
    gs = fig1.add_gridspec(9, 35)

    ax1 = fig1.add_subplot(gs[:, 20:-2])
    ax2 = fig1.add_subplot(gs[0:4, 0:17])
    ax3 = fig1.add_subplot(gs[5:9, 0:17])
    ax4 = fig1.add_subplot(gs[:, -2:-1])
    ax5 = fig1.add_subplot(gs[:, -1:])

    ax1.set_xlim(-(l1 + l1/5), l1 + l1/5)
    ax1.set_ylim(-(l1 + l1/5), l1 + l1/5)

    ax2.set_xlim(t0, tf)
    ax2.set_ylim(t1Min - varT, t1Max + varT)

    ax3.set_xlim(t0, tf)
    ax3.set_ylim(o1Min - varO, o1Max + varO)

    ax1.set_title('Pendulum Trajectory')
    ax2.set_title('\u03B8 trend over time')
    ax3.set_title('\u03C9 trend over time')
    ax4.set_title(r'E$_k$')
    ax5.set_title(r'E$_p$')

    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')

    ax4.axes.xaxis.set_ticks([])
    ax4.axes.yaxis.set_ticks([])
    ax4.yaxis.set_label_position("right")
    #ax4.set_ylabel('kinetic energy', rotation = 270, labelpad = 15)

    ax5.axes.xaxis.set_ticks([])
    ax5.axes.yaxis.set_ticks([])
    ax5.yaxis.set_label_position("right")
    #ax5.set_ylabel('potential energy', rotation = 270, labelpad = 15)

    return fig1, ax1, ax2, ax3, ax4, ax5