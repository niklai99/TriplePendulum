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
    
    print('\nPremi 1 per il Pendolo Semplice')
    print('\nPremi 2 per il Pendolo Doppio')
    print('\nPremi 3 per il Pendolo Triplo')

    try:
        mode=int(input('\n\nInserisci la tua scelta: '))
    except ValueError:
        print('\nMust be a number')


    if mode == 1:
        simplePendulum()
    
    elif mode == 2:
        doublePendulum()

    elif mode == 3:
        triplePendulum()

    else:
        print('Opzione non supportata')


if __name__ == "__main__":
    main()