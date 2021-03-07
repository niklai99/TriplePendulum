import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from rungeKutta4 import rk4

def inputParameters():
    '''Read parameters from keyboard'''

    m1 = float(input('\nInscerisci la massa del punto: '))
    l1 = float(input('\nInscerisci la lunghezza della fune: '))

    q01 = float(input('\nInscersci la posizione iniziale del pendolo (in deg): '))
    u01 = float(input('\nInscersci la velocità iniziale del pendolo (in deg/s): '))

    q0 = np.array([np.radians(q01), np.radians(u01)])

    t0 = int(input("\nInscerisci l'istante iniziale: "))
    tf = int(input("\nInscerisci l'istante finale: "))
    nstep = int(input('\nInscerisci il numero di iterazioni: '))

    par = [m1, l1, q0, t0, tf, nstep]

    return par


def computeCoordinates(theta1, par):
    '''Computes cartesian coordinates from generalized coordinates'''

    l1 = par[1]

    x1 = +l1*np.sin(theta1)
    y1 = -l1*np.cos(theta1)
    return x1, y1

def figureSetup(theta1, omega1, par):
    '''Plot figure configuration'''

    l1 = par[1]
    t0 = par[3]
    tf = par[4]

    fig1 = plt.figure(figsize=(14, 6))
    gs = fig1.add_gridspec(5, 9)

    ax1 = fig1.add_subplot(gs[:, 5:])
    ax2 = fig1.add_subplot(gs[0:2, :-5])
    ax3 = fig1.add_subplot(gs[3:5, :-5])

    ax1.set_xlim(-l1, l1)
    ax1.set_ylim(-l1, l1)

    ax2.set_xlim(t0, tf)
    ax2.set_ylim(np.amin(theta1), np.amax(theta1))

    ax3.set_xlim(t0, tf)
    ax3.set_ylim(np.amin(omega1), np.amax(omega1))

    ax1.set_title('Pendulum trajectory:')
    ax2.set_title('Theta vs Time:')
    ax3.set_title('Omega vs Time:')

    ax1.set_xlabel('x axis')
    ax1.set_ylabel('y axis')

    ax2.set_xlabel('time')
    ax2.set_ylabel('theta')

    ax3.set_xlabel('time')
    ax3.set_ylabel('omega')

    return fig1, ax1, ax2, ax3



def simplePendulum():
    '''Pendolo Semplice'''
    print('\nHai scelto il Pendolo Semplice\n')

    g = 9.81

    par = inputParameters()
    m1, l1, q0, t0, tf, nstep = par

    print('\nDigita 0 per visualizzare grafici statici\nDigita 1 per visualizzare grafici animati\n')
    mode = int(input(''))

    #q[0] = theta1
    #q[1] = omega1
    def motion(q, t):
        '''Equazione del Moto'''

        td = q[1]
        od = -m1*(g/l1)*np.sin(q[0])
        return np.array([td, od])


    q, t = rk4(motion, q0, t0 , tf , nstep)

    h = t[1]-t[0]
    theta1, omega1 = q.T

    x1, y1 = computeCoordinates(theta1, par)


    fig1, ax1, ax2, ax3 = figureSetup(theta1, omega1, par)

    # static plots
    if mode == 0:

        ax1.plot(x1, y1, '-', lw=2, color = '#047FFF') 
        ax2.plot(t, theta1, '-', lw=2, color = '#047FFF')
        ax3.plot(t, omega1, '-', lw=2, color = '#047FFF')

    # animated plots
    elif mode == 1:

        pendulumSegment, = ax1.plot([], [], 'o-', lw=2, color = '#000000')
        pendulumTrace, = ax1.plot([], [], '-', lw=2, color = '#047FFF')
        thetaTrace, = ax2.plot([], [], '-', lw=2, color = '#047FFF')
        omegaTrace, = ax3.plot([], [], '-', lw=2, color = '#047FFF')

        time_template = 'time = %.1fs'
        time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)


        def animate(i, x, y, line):
            line.set_data(x[:i], y[:i])
            return line,

        def pendulum(i, x, y, trace, pendulum):
            segmentX = [0, x[i]]
            segmentY = [0, y[i]]
            trace.set_data(x[i-15:i], y[i-15:i])
            pendulum.set_data(segmentX, segmentY)
            time_text.set_text(time_template % (i*h))
            return trace, pendulum, time_text


        anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x1, y1, pendulumTrace, pendulumSegment], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, theta1, thetaTrace], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, omega1, omegaTrace], interval=h, blit=True)


    plt.show()