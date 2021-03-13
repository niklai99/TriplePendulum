"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    SIMPLE PENDULUM MODULE

    The following code deals with the simple pendulum simulation
"""

# Python modules
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

# Custom made modules
from rungeKutta4 import RungeKutta4
from equationsMotion import simplePendulumEq
from inputParameters import inputParameters
from computeEnergy import simplePendulumEnergy
from figureSetup import staticFigure, animatedFigure, addLegend
from computeCoordinates import computeCoordinates
from animationModule import simplePendulumTrend, kineticEnergyAnimation, potentialEnergyAnimation, simplePendulumAnimation


def simplePendulum(n):
    '''Simple pendulum integration and animation'''
    print('\nYou chose the Simple Pendulum\n')

    # Let the user decide whether to use deafult parameters or to insert custom parameters
    print('Insert "d" to choose default parameters\n')
    print('Insert "s" to input your parameters\n')
    choice = str(input(''))

    # If the user chose to use default parameters
    # Set the default parameters
    if choice == 'd':

        # Set the point mass to 1kg
        m1 = 1
        # Set the rope length to 1m
        l1 = 1
        # Set the initial angle to 135deg and initial angular velocity to 0deg/s
        q0 = np.array([np.radians(135), np.radians(0)])
        # Set the starting time to 0s
        t0 = 0
        # Set the ending time to 10s
        tf = 10
        # Set the number of iterations to 1000
        nstep = 1000

        # Create the parameter list
        par = [m1, l1, q0, t0, tf, nstep]
        
    # If the user chose to insert custom parameters 
    # Call the inputParameters() function in inputParameters.py module
    elif choice == 's':
        par = inputParameters(n)
        m1, l1, q0, t0, tf, nstep = par

    # Integrate the equation of motion using the RungeKutta4() function in rungeKutta4.py module
    # Arguments passed to the function are:
    # 1) the simple pendulum equation of motion from the equationsMotion.py module
    # 2) the parameters list
    q, t, h = RungeKutta4(simplePendulumEq, par)

    # Compute the kinetic, potential and total energy through the simplePendulumEnergy() function in computeEnergy.py module
    E, U, T = simplePendulumEnergy(q, par)

    # Compute the cartesian (x, y) coordinates from the generalized coordinates q (i.e. angular positions)
    # using the computeCoordinates() function in computeCoordinates.py module
    x, y = computeCoordinates(n, q, par)


    # Let the user decide whether to plot static figures or animated figures
    print('\nInsert 0 for static plots')
    print('Insert 1 to see animations\n')
    mode = int(input(''))
    
    # If the user chose to display static plots:
    if mode == 0:

        # Create the figure and the axes using the staticFigure() function in the figureSetup.py module
        fig, ax1, ax2, ax3 = staticFigure(n, q, par)

        # Plot the pendulum trajectory
        ax1.plot(x, y, '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 

        # Plot the theta trend over time
        ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        
        # Plot the omega trend over time
        ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

        # Add a legend to the figures using the addLegend() function in the figureSetup.py module
        addLegend(n, ax1, ax2, ax3)

    # If the user chose to display animated plots:
    elif mode == 1:

        # Create the figure and the axes using the animatedFigure() function in the figureSetup.py module
        fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

        # Create the fixed point and the pendulum mass point as empty plots (they will be animated!)
        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
        masses = [pendulumMass0, pendulumMass1]

        # Create the pendulum rope as an empy plot (it will be animated!)
        pendulumSegment, = ax1.plot([], [], '-', lw=2, color = '#000000')

        # Create the pendulum trace of the trajectory as an empty plot (it will be animated!)
        pendulumTrace, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')

        # Create the theta trend over time trace as an empy plot (it will be animated!)
        thetaTrace, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')

        # Create the omega trend over time trace as an empy plot (it will be animated!)
        omegaTrace, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

        # Add a legend to the figures using the addLegend() function in the figureSetup.py module
        addLegend(n, ax1, ax2, ax3)

        # Create the template and the text in which time will be displayed and updated each iteration
        time_template = 'time = %.1f s'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

        # Create the template and the text in which the total energy of the system will be displayed and updated each iteration
        totalEnergy_template = 'total energy = %.2f J'
        totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

        texts = [time_template, time_text, totalEnergy_template, totalEnergy_text]

        # Create the kinetic energy bar
        rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax4.add_patch(rect1)

        # Create the potential energy bar
        rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
        ax5.add_patch(rect2)

        # Animate the plots using functions in the animationModule.py module
        anim1 = animation.FuncAnimation(fig, simplePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTrace, masses, pendulumSegment, texts, T, h], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
        anim4 = animation.FuncAnimation(fig, simplePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTrace], interval=h, blit=True)
        anim5 = animation.FuncAnimation(fig, simplePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTrace], interval=h, blit=True)


    plt.show()