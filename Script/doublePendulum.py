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
from figureSetup import staticFigure, animatedFigure, addLegend
from computeCoordinates import computeCoordinates
from animationModule import doublePendulumTrend, kineticEnergyAnimation, potentialEnergyAnimation, doublePendulumAnimation



def doublePendulum(n):
    '''Pendolo Doppio'''
    print('\nYou chose the Double Pendulum')

    print('Insert "d" to choose default parameters\nInsert "s" to input your parameters')
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


    print('\nInsert 0 for static plots\nInsert 1 to see animations\n')
    mode = int(input(''))
    
    # static plots
    if mode == 0:

        fig, ax1, ax2, ax3 = staticFigure(n, q, par)

        ax1.plot(x[:,0], y[:,0], '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
        ax1.plot(x[:,1], y[:,1], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory') 

        ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        ax2.plot(t, q[:,2], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        
        ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
        ax3.plot(t, q[:,3], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')

        addLegend(n, ax1, ax2, ax3)

    # animated plots
    elif mode == 1:

        fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
        pendulumMass2, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m2)
        masses = [pendulumMass0, pendulumMass1, pendulumMass2]

        pendulumSegments, = ax1.plot([], [], '-', lw=2, color = '#000000')

        pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
        pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
        pendulumTraces = [pendulumTrace1, pendulumTrace2]

        thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        thetaTraces = [thetaTrace1, thetaTrace2]

        omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
        omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
        omegaTraces = [omegaTrace1, omegaTrace2]

        addLegend(n, ax1, ax2, ax3)

        time_template = 'time = %.1fs'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

        totalEnergy_template = 'total energy = %.2f J'
        totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

        texts = [time_template, time_text, totalEnergy_template, totalEnergy_text]

        rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax4.add_patch(rect1)

        rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax5.add_patch(rect2)


        anim1 = animation.FuncAnimation(fig, doublePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTraces, masses, pendulumSegments, texts, T, h], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
        anim4 = animation.FuncAnimation(fig, doublePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTraces], interval=h, blit=True)
        anim5 = animation.FuncAnimation(fig, doublePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTraces], interval=h, blit=True)


    plt.show()