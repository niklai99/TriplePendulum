"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    TRIPLE PENDULUM MODULE

    The following code deals with the triple pendulum simulation
"""

# Python modules
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

# Custom made modules
from rungeKutta4 import RungeKutta4
from equationsMotion import triplePendulumEq
from inputParameters import inputParameters
from computeEnergy import triplePendulumEnergy
from figureSetup import staticFigure, animatedFigure, addLegend
from computeCoordinates import computeCoordinates
from animationModule import triplePendulumTrend, kineticEnergyAnimation, potentialEnergyAnimation, triplePendulumAnimation


def triplePendulum(n):
    '''Triple pendulum integration and animation'''
    print('\nYou chose the Triple Pendulum\n')

     # Let the user decide whether to use deafult parameters or to insert custom parameters
    print('Insert "d" to choose default parameters\n')
    print('Insert "s" to input your parameters\n')
    choice = str(input(''))

    # If the user chose to use default parameters
    # Set the default parameters
    if choice == 'd':

        # Set the points mass to 1kg
        m1 = 1
        m2 = 1
        m3 = 1
        # Set the ropes length to 1m
        l1 = 1
        l2 = 1
        l3 = 1
        # Set the initial angles to 135deg and initial angular velocities to 0deg/s
        q0 = np.array([
                        np.radians(135), np.radians(0), 
                        np.radians(135), np.radians(0), 
                        np.radians(135), np.radians(0)
                        ])
        # Set the starting time to 0s
        t0 = 0
        # Set the ending time to 10s
        tf = 10
        # Set the number of iterations to 1000
        nstep = 1000

        # Create the parameter list
        par = [m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep]
    
    # If the user chose to insert custom parameters 
    # Call the inputParameters() function in inputParameters.py module
    elif choice == 's':
        par = inputParameters(n)
        m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep = par

    # Integrate the equation of motion using the RungeKutta4() function in rungeKutta4.py module
    # Arguments passed to the function are:
    # 1) the triple pendulum equation of motion from the equationsMotion.py module
    # 2) the parameters list
    q, t, h = RungeKutta4(triplePendulumEq, par)

    # Compute the kinetic, potential and total energy through the triplePendulumEnergy() function in computeEnergy.py module
    E, U, T = triplePendulumEnergy(q, par)

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
        ax1.plot(x[:,0], y[:,0], '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
        ax1.plot(x[:,1], y[:,1], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
        ax1.plot(x[:,2], y[:,2], '-', lw=2, color = '#00C415', label = '3rd mass trajectory') 

        # Plot the theta trend over time
        ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        ax2.plot(t, q[:,2], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        ax2.plot(t, q[:,3], '-', lw=2, color = '#00C415', label = '3rd mass \u03B8(t)')

        # Plot the omega trend over time
        ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
        ax3.plot(t, q[:,3], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
        ax3.plot(t, q[:,5], '-', lw=2, color = '#00C415', label = '3rd mass \u03C9(t)')

        # Add a legend to the figures using the addLegend() function in the figureSetup.py module
        addLegend(n, ax1, ax2, ax3)


    # If the user chose to display animated plots:
    elif mode == 1:
        
        # Create the figure and the axes using the animatedFigure() function in the figureSetup.py module
        fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

        # Create the fixed point and the pendulum mass points as empty plots (they will be animated!)
        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
        pendulumMass2, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m2)
        pendulumMass3, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m3)
        masses = [pendulumMass0, pendulumMass1, pendulumMass2, pendulumMass3]

        # Create the pendulum ropes as an empy plot (they will be animated!)
        pendulumSegments, = ax1.plot([], [], '-', lw=2, color = '#000000')

        # Create the pendulum trace of the trajectory as an empty plot (it will be animated!)
        pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
        pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
        pendulumTrace3, = ax1.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass trajectory')
        pendulumTraces = [pendulumTrace1, pendulumTrace2, pendulumTrace3]

        # Create the theta trend over time trace as an empy plot (it will be animated!)
        thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        thetaTrace3, = ax2.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass \u03B8(t)')
        thetaTraces = [thetaTrace1, thetaTrace2, thetaTrace3]

        # Create the omega trend over time trace as an empy plot (it will be animated!)
        omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
        omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
        omegaTrace3, = ax3.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass \u03C9(t)')
        omegaTraces = [omegaTrace1, omegaTrace2, omegaTrace3]

        # Add a legend to the figures using the addLegend() function in the figureSetup.py module
        addLegend(n, ax1, ax2, ax3)

        # Create the template and the text in which time will be displayed and updated each iteration
        time_template = 'time = %.1fs'
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
        anim1 = animation.FuncAnimation(fig, triplePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTraces, masses, pendulumSegments, texts, T, h], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
        anim4 = animation.FuncAnimation(fig, triplePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTraces], interval=h, blit=True)
        anim5 = animation.FuncAnimation(fig, triplePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTraces], interval=h, blit=True)


    plt.show()