"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    DOUBLE PENDULUM MODULE

    The following code deals with the double pendulum simulation
"""

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from rungeKutta4 import RungeKutta4
from equationsMotion import doublePendulumEq
from inputParameters import inputParameters
from computeEnergy import doublePendulumEnergy
from figureSetup import staticFigure, animatedFigure
from computeCoordinates import computeCoordinates



def doublePendulum(n):
    '''Pendolo Doppio'''
    print('\nHai scelto il pendolo doppio')

    print('Premi "d" per parametri default\nPremi "s" per scegliere i parametri')
    choice = str(input(''))

    if choice == 'd':
        m1 = 1
        m2 = 1
        l1 = 1
        l2 = 1
        q0 = np.array([
                        np.radians(135), np.radians(0), 
                        np.radians(135), np.radians(0)
                        ])
        t0 = 0
        tf = 10
        nstep = 1000
        par = [m1, m2, l1, l2, q0, t0, tf, nstep]
    
    elif choice == 's':
        par = inputParameters(n)
        m1, m2, l1, l2, q0, t0, tf, nstep = par


    q, t, h = RungeKutta4(doublePendulumEq, par)

    E, U, T = doublePendulumEnergy(q, par)

    x, y = computeCoordinates(n, q, par)


    print('\nDigita 0 per visualizzare grafici statici\nDigita 1 per visualizzare grafici animati\n')
    mode = int(input(''))
    
    # static plots
    if mode == 0:

        fig1, ax1, ax2, ax3 = staticFigure(n, q, par)

        ax1.plot(x[:,0], y[:,0], '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
        ax1.plot(x[:,1], y[:,1], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory') 

        ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        ax2.plot(t, q[:,2], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        
        ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
        ax3.plot(t, q[:,3], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')

        ax1.legend(loc = 'upper right', ncol = 1)
        ax2.legend(loc = 'upper right', ncol = 2)
        ax3.legend(loc = 'upper right', ncol = 2)

    # animated plots
    elif mode == 1:

        fig1, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
        pendulumMass2, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m2)
        masses = [pendulumMass0, pendulumMass1, pendulumMass2]

        pendulumSegments, = ax1.plot([], [], '-', lw=2, color = '#000000')

        pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
        pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')

        thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')

        omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
        omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')

        ax1.legend(loc = 'upper right', ncol = 1)
        ax2.legend(loc = 'upper right', ncol = 2)
        ax3.legend(loc = 'upper right', ncol = 2)

        time_template = 'time = %.1fs'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

        totalEnergy_template = 'total energy = %.2f J'
        totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

        rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax4.add_patch(rect1)

        rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax5.add_patch(rect2)


        def animate(i, t, y1, y2, line1, line2):

            line1.set_data(t[:i], y1[:i])
            line2.set_data(t[:i], y2[:i])

            return line1, line2,
        
        def kineticEnergy_anim(i, ax):

            rect1 = ax.fill_between(x = (0, 1), y1 = 0, y2 = E[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), color = 'red')

            return rect1,
        
        def potentialEnergy_anim(i, ax):

            rect2 = ax.fill_between(x = (0, 1), y1 = 0, y2 = U[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), color = 'blue')

            return rect2,

        def pendulum(i, x, y, trace1, trace2, masses, segments):

            massX0 = [0]
            massY0 = [0]
            massX1 = [x[i, 0]]
            massY1 = [y[i, 0]]
            massX2 = [x[i, 1]]
            massY2 = [y[i, 1]]

            segmentX = [0, x[i, 0], x[i, 1]]
            segmentY = [0, y[i, 0], y[i, 1]]

            trace1.set_data(x[i-25:i, 0], y[i-25:i, 0])
            trace2.set_data(x[i-40:i, 1], y[i-40:i, 1])
            mass0, mass1, mass2 = masses

            mass0.set_data(massX0, massY0)
            mass1.set_data(massX1, massY1)
            mass2.set_data(massX2, massY2)

            segments.set_data(segmentX, segmentY)

            time_text.set_text(time_template % (i*h))

            totalEnergy_text.set_text(totalEnergy_template % (T[i]))


            return trace1, trace2, mass0, mass1, mass2, segments, time_text, totalEnergy_text,

        anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x, y, pendulumTrace1, pendulumTrace2, masses, pendulumSegments], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig1, kineticEnergy_anim, frames=len(t), fargs=[ax4], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig1, potentialEnergy_anim, frames=len(t), fargs=[ax5], interval=h, blit=True)
        anim4 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, q[:,0], q[:,2], thetaTrace1, thetaTrace2], interval=h, blit=True)
        anim5 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, q[:,1], q[:,3], omegaTrace1, omegaTrace2], interval=h, blit=True)


    plt.show()