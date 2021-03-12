"""
    TRIPLE PENDULUM SCRIPT

    Author: Nicolò Lai
    Project: Triple Pendulum 
    Goal: Solving the equation of motions of a triple pendulum
    Means: Runge-Kutta 4 iterative method

    ANIMATION MODULE

    The following code deals with the animations
"""

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation


def simplePendulumTrend(i, s, t, q, lines):

    line1 = lines

    if s == 'theta':  
        line1.set_data(t[:i], q[:i, 0])
    
    elif s == 'omega':
        line1.set_data(t[:i], q[:i, 1])

    return line1,

def doublePendulumTrend(i, s, t, q, lines):

    line1, line2 = lines

    if s == 'theta':  
        line1.set_data(t[:i], q[:i, 0])
        line2.set_data(t[:i], q[:i, 2])
    
    elif s == 'omega':
        line1.set_data(t[:i], q[:i, 1])
        line2.set_data(t[:i], q[:i, 3])

    return line1, line2,

def triplePendulumTrend(i, s, t, q, lines):

    line1, line2, line3 = lines

    if s == 'theta':  
        line1.set_data(t[:i], q[:i, 0])
        line2.set_data(t[:i], q[:i, 2])
        line3.set_data(t[:i], q[:i, 4])
    
    elif s == 'omega':
        line1.set_data(t[:i], q[:i, 1])
        line2.set_data(t[:i], q[:i, 3])
        line3.set_data(t[:i], q[:i, 5])

    return line1, line2, line3,

def simplePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h):

    massX0 = [0]
    massY0 = [0]
    massX1 = [x[i, 0]]
    massY1 = [y[i, 0]]

    segmentX = [0, x[i, 0]]
    segmentY = [0, y[i, 0]]

    trace1 = traces

    trace1.set_data(x[i-25:i, 0], y[i-25:i, 0])

    mass0, mass1 = masses
    mass0.set_data(massX0, massY0)
    mass1.set_data(massX1, massY1)

    segments.set_data(segmentX, segmentY)

    time_template, time_text, totalEnergy_template, totalEnergy_text = texts
    time_text.set_text(time_template % (i*h))
    totalEnergy_text.set_text(totalEnergy_template % (T[i]))

    return trace1, mass0, mass1, segments, time_text, totalEnergy_text,

def doublePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h):

    massX0 = [0]
    massY0 = [0]
    massX1 = [x[i, 0]]
    massY1 = [y[i, 0]]
    massX2 = [x[i, 1]]
    massY2 = [y[i, 1]]

    segmentX = [0, x[i, 0], x[i, 1]]
    segmentY = [0, y[i, 0], y[i, 1]]

    trace1, trace2 = traces

    trace1.set_data(x[i-25:i, 0], y[i-25:i, 0])
    trace2.set_data(x[i-40:i, 1], y[i-40:i, 1])

    mass0, mass1, mass2 = masses
    mass0.set_data(massX0, massY0)
    mass1.set_data(massX1, massY1)
    mass2.set_data(massX2, massY2)

    segments.set_data(segmentX, segmentY)

    time_template, time_text, totalEnergy_template, totalEnergy_text = texts
    time_text.set_text(time_template % (i*h))
    totalEnergy_text.set_text(totalEnergy_template % (T[i]))

    return trace1, trace2, mass0, mass1, mass2, segments, time_text, totalEnergy_text,

def triplePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h):

    massX0 = [0]
    massY0 = [0]
    massX1 = [x[i, 0]]
    massY1 = [y[i, 0]]
    massX2 = [x[i, 1]]
    massY2 = [y[i, 1]]
    massX3 = [x[i, 2]]
    massY3 = [y[i, 2]]

    segmentX = [0, x[i, 0], x[i, 1], x[i, 2]]
    segmentY = [0, y[i, 0], y[i, 1], y[i, 2]]

    trace1, trace2, trace3 = traces

    trace1.set_data(x[i-25:i, 0], y[i-25:i, 0])
    trace2.set_data(x[i-40:i, 1], y[i-40:i, 1])
    trace3.set_data(x[i-65:i, 2], y[i-65:i, 2])

    mass0, mass1, mass2, mass3 = masses
    mass0.set_data(massX0, massY0)
    mass1.set_data(massX1, massY1)
    mass2.set_data(massX2, massY2)
    mass3.set_data(massX3, massY3)

    segments.set_data(segmentX, segmentY)

    time_template, time_text, totalEnergy_template, totalEnergy_text = texts
    time_text.set_text(time_template % (i*h))
    totalEnergy_text.set_text(totalEnergy_template % (T[i]))

    return trace1, trace2, trace3, mass0, mass1, mass2, mass3, segments, time_text, totalEnergy_text,


def kineticEnergyAnimation(i, ax, E, U):

    rect1 = ax.fill_between(x = (0, 1), y1 = 0, y2 = E[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), color = 'red')

    return rect1,

def potentialEnergyAnimation(i, ax, E, U):

    rect2 = ax.fill_between(x = (0, 1), y1 = 0, y2 = U[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), color = 'blue')

    return rect2,