"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    MAIN MODULE

    The following code lets the user choose whether to go through a simple, double or triple pendulum simulation
"""

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from simplePendulum import simplePendulum
from doublePendulum import doublePendulum
from triplePendulum import triplePendulum


def main():
    '''Main Function'''
    
    print('\nInsert 1 for the Simple Pendulum')
    print('\nInsert 2 for the Double Pendulum')
    print('\nInsert 3 for the Triple Pendulum')

    try:
        n=int(input('\n'))
    except ValueError:
        print('\nMust be a number')


    if n == 1:
        simplePendulum(n)
    
    elif n == 2:
        doublePendulum(n)

    elif n == 3:
        triplePendulum(n)

    else:
        print('Not supported')


if __name__ == "__main__":
    main()