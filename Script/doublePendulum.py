import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from rungeKutta4 import rk4


def pendoloDoppio():
    '''Pendolo Doppio'''
    print('\nHai scelto il pendolo doppio')

    g = 9.81

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


    x1 = +l1*np.sin(t1)
    y1 = -l1*np.cos(t1)
    x2 = +l2*np.sin(t2) + x1
    y2 = -l2*np.cos(t2) + y1
    
    fig1 = plt.figure(figsize=(14, 6))
    gs = fig1.add_gridspec(5, 9)

    ax1 = fig1.add_subplot(gs[:, 5:])
    ax2 = fig1.add_subplot(gs[0:2, :-5])
    ax3 = fig1.add_subplot(gs[3:5, :-5])

    ax1.set_xlim(-l1-l2, l1+l2)
    ax1.set_ylim(-l1-l2, l1+l2)

    ax2.set_xlim(0, 10)
    ax2.set_ylim(-10, 10)

    ax3.set_xlim(0, 10)
    ax3.set_ylim(-10, 10)

    
    
    ax1.set_title('Pendulum trajectory:')
    ax2.set_title('Theta vs Time:')
    ax3.set_title('Omega vs Time:')

    ax1.set_xlabel('x axis')
    ax1.set_ylabel('y axis')

    ax2.set_xlabel('time')
    ax2.set_ylabel('theta')

    ax3.set_xlabel('time')
    ax3.set_ylabel('omega')   

    pendulumSegment, = ax1.plot([], [], 'o-', lw=2, color = '#000000')
    pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF')
    pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00')
    thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF')
    thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00')
    omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF')
    omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00')

    time_template = 'time = %.1fs'
    time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)

    
    def animate(i, x1, y1, x2, y2, line1, line2):
        line1.set_data(x1[:i], y1[:i])
        line2.set_data(x2[:i], y2[:i])
        return line1, line2,
    
    def pendulum(i, x1, y1, x2, y2, trace1, trace2, pendulum):
        segmentX = [0, x1[i], x2[i]]
        segmentY = [0, y1[i], y2[i]]
        trace1.set_data(x1[i-15:i], y1[i-15:i])
        trace2.set_data(x2[i-15:i], y2[i-15:i])
        pendulum.set_data(segmentX, segmentY)
        time_text.set_text(time_template % (i*h))
        return trace1, trace2, pendulum, time_text,

  

    anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x1, y1, x2, y2, pendulumTrace1, pendulumTrace2, pendulumSegment], interval=h, blit=True)

    anim2 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, t1, t, t2, thetaTrace1, thetaTrace2], interval=h, blit=True)

    anim3 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, o1, t, o2, omegaTrace1, omegaTrace2], interval=h, blit=True)


    # plt.figure(1)
    # plt.title('Pendulum Motion:')
    # plt.plot(np.sin(t1), -np.cos(t1))
    # plt.plot(np.sin(t1)+np.sin(t2), -np.cos(t1)-np.cos(t2))
    
    # plt.figure(2)
    # plt.title('Theta vs Time:')
    # plt.plot(t, t1)
    # plt.plot(t, t2)

    # plt.figure(3)
    # plt.title('Omega vs Time:')
    # plt.plot(t, o1)
    # plt.plot(t, o2)

    plt.show()