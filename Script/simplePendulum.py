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
from figureSetup import staticFigure, animatedFigure, addLegend
from computeCoordinates import computeCoordinates
from animationModule import simplePendulumTrend, kineticEnergyAnimation, potentialEnergyAnimation, simplePendulumAnimation


def simplePendulum(n):
    '''Pendolo Semplice'''
    print('\nYou chose the Simple Pendulum\n')

    print('Insert "d" to choose default parameters\n')
    print('Insert "s" to input your parameters\n')
    choice = str(input(''))

    if choice == 'd':
        m1 = 1
        l1 = 1
        q0 = np.array([np.radians(135), np.radians(0)])
        t0 = 0
        tf = 10
        nstep = 1000
        par = [m1, l1, q0, t0, tf, nstep]
        
    
    elif choice == 's':
        par = inputParameters(n)


    q, t, h = RungeKutta4(simplePendulumEq, par)

    E, U, T = simplePendulumEnergy(q, par)

    x, y = computeCoordinates(n, q, par)


    print('\nInsert 0 for static plots')
    print('Insert 1 to see animations\n')
    mode = int(input(''))
    
    # static plots
    if mode == 0:

        fig, ax1, ax2, ax3 = staticFigure(n, q, par)

        ax1.plot(x, y, '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 

        ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        
        ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

        addLegend(n, ax1, ax2, ax3)

    # animated plots
    elif mode == 1:

        fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
        masses = [pendulumMass0, pendulumMass1]

        pendulumSegment, = ax1.plot([], [], '-', lw=2, color = '#000000')

        pendulumTrace, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')

        thetaTrace, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')

        omegaTrace, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

        addLegend(n, ax1, ax2, ax3)

        time_template = 'time = %.1f s'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

        totalEnergy_template = 'total energy = %.2f J'
        totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

        texts = [time_template, time_text, totalEnergy_template, totalEnergy_text]

        rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax4.add_patch(rect1)

        rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax5.add_patch(rect2)

        
        anim1 = animation.FuncAnimation(fig, simplePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTrace, masses, pendulumSegment, texts, T, h], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
        anim4 = animation.FuncAnimation(fig, simplePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTrace], interval=h, blit=True)
        anim5 = animation.FuncAnimation(fig, simplePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTrace], interval=h, blit=True)


    plt.show()