# TO DO

# creare un modulo "figureSetup" e dividere i casi in cui i grafici siano statici o animati

# se possibile creare un modulo, o almeno una funzione separata, per gestire le animazioni


"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    SIMPLE PENDULUM MODULE

    The following code deals with the simple pendulum simulation
"""

# python modules
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

# custom made modules
from rungeKutta4 import RungeKutta4
from equationsMotion import simplePendulumEq
from inputParameters import inputParameters
from computeEnergy import simplePendulumEnergy


def computeCoordinates(t1, par):
    '''Computes cartesian coordinates from generalized coordinates'''

    l1 = par[1]

    x1 = +l1*np.sin(t1)
    y1 = -l1*np.cos(t1)
    return x1, y1

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



def simplePendulum(n):
    '''Pendolo Semplice'''
    print('\nHai scelto il Pendolo Semplice\n')

    print('Premi "d" per parametri default\nPremi "s" per scegliere i parametri')
    choice = str(input(''))

    if choice == 'd':
        m1 = 1
        l1 = 1
        q0 = np.array([np.radians(135), np.radians(0)])
        t0 = 0
        tf = 10
        nstep = 1000
        par = [m1, l1, q0, t0, tf, nstep]
        print(par)
    
    elif choice == 's':
        par = inputParameters(n)
        m1, l1, q0, t0, tf, nstep = par

    g = 9.81

    print('\nDigita 0 per visualizzare grafici statici\nDigita 1 per visualizzare grafici animati\n')
    mode = int(input(''))


    q, t = RungeKutta4(simplePendulumEq, par)

    E, U, T = simplePendulumEnergy(q, par)

    h = t[1]-t[0]
    t1, o1 = q.T

    x1, y1 = computeCoordinates(t1, par)


    fig1, ax1, ax2, ax3, ax4, ax5 = figureSetup(t1, o1, par)

    # static plots
    if mode == 0:

        ax1.plot(x1, y1, '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
        ax2.plot(t, t1, '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        ax3.plot(t, o1, '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
        ax1.legend(loc = 'upper right')
        ax2.legend(loc = 'upper right')
        ax3.legend(loc = 'upper right')

    # animated plots
    elif mode == 1:

        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)

        masses = [pendulumMass0, pendulumMass1]

        pendulumSegment, = ax1.plot([], [], '-', lw=2, color = '#000000')

        pendulumTrace, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')

        thetaTrace, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')

        omegaTrace, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

        ax1.legend(loc = 'upper right')
        ax2.legend(loc = 'upper right')
        ax3.legend(loc = 'upper right')

        time_template = 'time = %.1f s'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

        kineticEnergy_template = 'kenetic energy = %.2f J'
        kineticEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes, fontsize = 0)
        potentialEnergy_template = 'potential energy = %.2f J'
        potentialEnergy_text = ax1.text(0.05, 0.82, '', transform=ax1.transAxes, fontsize = 0)
        totalEnergy_template = 'total energy = %.2f J'
        totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)


        ax4.set_xlim(left = 0, right = 1)
        ax4.set_ylim(bottom = -1, top = 1)

        rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax4.add_patch(rect1)

        ax5.set_xlim(left = 0, right = 1)
        ax5.set_ylim(bottom =-1, top = 1)

        rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax5.add_patch(rect2)

        def animate(i, x, y, line):

            line.set_data(x[:i], y[:i])

            return line,

        def kineticEnergy_anim(i, ax):

            rect1 = ax.fill_between(x = (0, 1), y1 = 0, y2 = E[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), color = 'red')

            return rect1,
        
        def potentialEnergy_anim(i, ax):

            rect2 = ax.fill_between(x = (0, 1), y1 = 0, y2 = U[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), color = 'blue')

            return rect2,

        def pendulum(i, x, y, trace, masses, segments):
    
            massX0 = [0]
            massY0 = [0]
            massX1 = [x1[i]]
            massY1 = [y1[i]]
            
            segmentX = [0, x[i]]
            segmentY = [0, y[i]]

            mass0, mass1 = masses

            trace.set_data(x[i-15:i], y[i-15:i])

            mass0.set_data(massX0, massY0)
            mass1.set_data(massX1, massY1)

            segments.set_data(segmentX, segmentY)

            time_text.set_text(time_template % (i*h))

            totalEnergy_text.set_text(totalEnergy_template % (T[i]))
            kineticEnergy_text.set_text(kineticEnergy_template % (E[i]))
            potentialEnergy_text.set_text(potentialEnergy_template % (U[i]))

            return trace, mass0, mass1, segments, time_text, totalEnergy_text, kineticEnergy_text, potentialEnergy_text,


        anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x1, y1, pendulumTrace, masses, pendulumSegment], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig1, kineticEnergy_anim, frames=len(t), fargs=[ax4], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig1, potentialEnergy_anim, frames=len(t), fargs=[ax5], interval=h, blit=True)
        anim4 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, t1, thetaTrace], interval=h, blit=True)
        anim5 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, o1, omegaTrace], interval=h, blit=True)


    plt.show()