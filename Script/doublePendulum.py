import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from rungeKutta4 import rk4

def inputParameters():
    '''Read parameters from keyboard'''

    m1 = float(input('\nInscerisci la massa del primo punto: '))
    m2 = float(input('\nInscerisci la massa del secondo punto: '))
    l1 = float(input('\nInscerisci la lunghezza della prima fune: '))
    l2 = float(input('\nInscerisci la lunghezza della seconda fune: '))

    q01 = float(input('\nInscersci la posizione iniziale del primo punto (in deg): '))
    q02 = float(input('\nInscersci la posizione iniziale del secondo punto (in deg): '))

    u01 = float(input('\nInscersci la velocità iniziale del primo punto (in deg/s): '))
    u02 = float(input('\nInscersci la velocità iniziale del secondo punto (in deg/s): '))

    q0 = np.array([np.radians(q01), np.radians(u01), np.radians(q02), np.radians(u02)])

    t0 = int(input("\nInscerisci l'istante iniziale: "))
    tf = int(input("\nInscerisci l'istante finale: "))
    nstep = int(input('\nInscerisci il numero di iterazioni: '))

    par = [m1, m2, l1, l2, q0, t0, tf, nstep]

    return par


def computeCoordinates(t1, t2, par):
    '''Computes cartesian coordinates from generalized coordinates'''

    l1 = par[2]
    l2 = par[3]
    
    x1 = +l1*np.sin(t1)
    y1 = -l1*np.cos(t1)
    x2 = +l2*np.sin(t2) + x1
    y2 = -l2*np.cos(t2) + y1

    return x1, y1, x2, y2


def figureSetup(t1, t2, o1, o2, par):
    '''Plot figure configuration'''

    l1 = par[2]
    l2 = par[3]
    t0 = par[5]
    tf = par[6]

    t1Min = np.amin(t1)
    t2Min = np.amin(t2)
    tMin = np.minimum(t1Min, t2Min)

    t1Max = np.amax(t1)
    t2Max = np.amax(t2)
    tMax = np.maximum(t1Max, t2Max)

    o1Min = np.amin(o1)
    o2Min = np.amin(o2)
    oMin = np.minimum(o1Min, o2Min)

    o1Max = np.amax(o1)
    o2Max = np.amax(o2)
    oMax = np.maximum(o1Max, o2Max)


    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    fig1 = plt.figure(figsize=(14, 6))
    gs = fig1.add_gridspec(9, 33)

    ax1 = fig1.add_subplot(gs[:, 20:])
    ax2 = fig1.add_subplot(gs[0:4, 0:17])
    ax3 = fig1.add_subplot(gs[5:9, 0:17])

    ax1.set_xlim(-((l1+l2) + (l1+l2)/5), (l1+l2) + (l1+l2)/5)
    ax1.set_ylim(-((l1+l2) + (l1+l2)/5), (l1+l2) + (l1+l2)/5)

    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin - varT/2, tMax + varT)

    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin - varO/2, oMax + varO)

    
    ax1.set_title('Pendulum Trajectory')
    ax2.set_title('\u03B8 trend over time')
    ax3.set_title('\u03C9 trend over time')

    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')

    return fig1, ax1, ax2, ax3



def doublePendulum():
    '''Pendolo Doppio'''
    print('\nHai scelto il pendolo doppio')

    print('Premi "d" per parametri default\nPremi "s" per scegliere i parametri')
    choice = str(input(''))

    if choice == 'd':
        m1 = 1
        m2 = 1
        l1 = 1
        l2 = 1
        q0 = np.array([np.radians(135), np.radians(0), np.radians(135), np.radians(0)])
        t0 = 0
        tf = 10
        nstep = 1000
        par = [m1, m2, l1, l2, q0, t0, tf, nstep]
    
    elif choice == 's':
        par = inputParameters()
        m1, m2, l1, l2, q0, t0, tf, nstep = par

    g = 9.81

    print('\nDigita 0 per visualizzare grafici statici\nDigita 1 per visualizzare grafici animati\n')
    mode = int(input(''))

    #q[0] = theta1
    #q[1] = omega1
    #q[2] = theta2
    #q[3] = omega2
    def motion(q, t):
        '''Equazione del Moto'''

        td1 = q[1]
        td2 = q[3]
        od1 = (-g * (2*m1 + m2) * np.sin(q[0]) -m2 * g * np.sin(q[0]-2*q[2]) -2 * np.sin(q[0]-q[2]) * m2 * (l2 * q[3]**2 + l1 * q[1]**2 * np.cos(q[0]-q[2]))) / (l1 * (2*m1 + m2 - m2*np.cos(2*q[0]-2*q[2])))
        od2 = (2 * np.sin(q[0]-q[2]) * ( l1 * q[1]**2 * (m1+m2) + g * (m1+m2) * np.cos(q[0]) + m2 * l2 * q[3]**2 * np.cos(q[0]-q[2]))) / (l2 * (2*m1 + m2 - m2*np.cos(2*q[0]-2*q[2])))
        return np.array([td1, od1, td2, od2])


    q, t = rk4(motion, q0, t0 , tf , nstep)

    h = t[1]-t[0]
    t1, o1, t2, o2 = q.T


    x1, y1, x2, y2 = computeCoordinates(t1, t2, par)

    fig1, ax1, ax2, ax3 = figureSetup(t1, t2, o1, o2, par)
    
    # static plots
    if mode == 0:

        ax1.plot(x1, y1, '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
        ax1.plot(x2, y2, '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory') 
        ax2.plot(t, t1, '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        ax2.plot(t, t2, '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        ax3.plot(t, o1, '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
        ax3.plot(t, o2, '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')

        ax1.legend(loc = 'upper right', ncol = 1)
        ax2.legend(loc = 'upper right', ncol = 2)
        ax3.legend(loc = 'upper right', ncol = 2)

    # animated plots
    elif mode == 1:

        pendulumSegment, = ax1.plot([], [], 'o-', lw=2, color = '#000000')
        pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
        pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
        thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
        omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')

        ax1.legend(loc = 'upper right', ncol = 1)
        ax2.legend(loc = 'upper right', ncol = 2)
        ax3.legend(loc = 'upper right', ncol = 2)

        time_template = 'time = %.1fs'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes)


        def animate(i, x1, y1, x2, y2, line1, line2):
            line1.set_data(x1[:i], y1[:i])
            line2.set_data(x2[:i], y2[:i])
            return line1, line2,

        def pendulum(i, x1, y1, x2, y2, trace1, trace2, pendulum):
            segmentX = [0, x1[i], x2[i]]
            segmentY = [0, y1[i], y2[i]]
            trace1.set_data(x1[i-25:i], y1[i-25:i])
            trace2.set_data(x2[i-40:i], y2[i-40:i])
            pendulum.set_data(segmentX, segmentY)
            time_text.set_text(time_template % (i*h))
            return trace1, trace2, pendulum, time_text,

        anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x1, y1, x2, y2, pendulumTrace1, pendulumTrace2, pendulumSegment], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, t1, t, t2, thetaTrace1, thetaTrace2], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, o1, t, o2, omegaTrace1, omegaTrace2], interval=h, blit=True)


    plt.show()