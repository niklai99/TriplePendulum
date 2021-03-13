"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    MAIN MODULE

    The following code lets the user choose whether to go through a simple, double or triple pendulum simulation
"""

# python modules
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

# custom made modules
from simplePendulum import simplePendulum
from doublePendulum import doublePendulum
from triplePendulum import triplePendulum


def main():
    '''Main Function, it lets the user choose between simple, double and triple pendulum integration and simulation'''
    
    print('\nInsert 1 for the Simple Pendulum')
    print('\nInsert 2 for the Double Pendulum')
    print('\nInsert 3 for the Triple Pendulum')


    # Read input from keyboard
    try:
        n=int(input('\n'))
    except ValueError:
        print('\nMust be a number')

    # Enter in the appropriate function
    if n == 1:
        simplePendulum(n)
    
    elif n == 2:
        doublePendulum(n)

    elif n == 3:
        triplePendulum(n)

    else:
        print('Not supported')


# Call the main function when running the scrip
if __name__ == "__main__":
    main()