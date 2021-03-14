"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    SAVE FIGURE MODULE

    The following code enables the user to save figures and animations
"""

# Python modules
import matplotlib.pyplot as plt 
from matplotlib import animation


def saveStaticFig(n, fig):
    '''Save static figures'''

    # Set the path and file name to save the picture
    name = str(input('\nWrite the name of the file (without extention)\n'))
    png = '.png'
    path = './Pictures/'

    if n == 1:
        folder = 'simplePendulum/'
    elif n == 2:
        folder = 'doublePendulum/'
    elif n == 3:
        folder = 'triplePendulum/'

    fname = path + folder + name + png
    
    # Save the figure
    plt.savefig(fname, dpi=300, facecolor='w')

    return
