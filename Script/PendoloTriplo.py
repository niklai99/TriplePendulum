import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from simplePendulum import pendoloSemplice
from doublePendulum import pendoloDoppio
from triplePendulum import pendoloTriplo


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
        pendoloSemplice()
    
    elif mode == 2:
        pendoloDoppio()

    elif mode == 3:
        pendoloTriplo()

    else:
        print('Opzione non supportata')


if __name__ == "__main__":
    main()