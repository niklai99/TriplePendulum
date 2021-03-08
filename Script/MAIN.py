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