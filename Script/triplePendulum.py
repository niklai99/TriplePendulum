import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import animation

from rungeKutta4 import rk4


def inputParameters():
    '''Read parameters from keyboard'''

    m1 = float(input('\nInscerisci la massa del primo punto: '))
    m2 = float(input('\nInscerisci la massa del secondo punto: '))
    m3 = float(input('\nInscerisci la massa del terzo punto: '))
    l1 = float(input('\nInscerisci la lunghezza della prima fune: '))
    l2 = float(input('\nInscerisci la lunghezza della seconda fune: '))
    l3 = float(input('\nInscerisci la lunghezza della terza fune: '))

    q01 = float(input('\nInscersci la posizione iniziale del primo punto (in deg): '))
    q02 = float(input('\nInscersci la posizione iniziale del secondo punto (in deg): '))
    q03 = float(input('\nInscersci la posizione iniziale del terzo punto (in deg): '))

    u01 = float(input('\nInscersci la velocità iniziale del primo punto (in deg/s): '))
    u02 = float(input('\nInscersci la velocità iniziale del secondo punto (in deg/s): '))
    u03 = float(input('\nInscersci la velocità iniziale del terzo punto (in deg/s): '))

    q0 = np.array([np.radians(q01), np.radians(u01), 
                    np.radians(q02), np.radians(u02),
                    np.radians(q03), np.radians(u03)])

    t0 = int(input("\nInscerisci l'istante iniziale: "))
    tf = int(input("\nInscerisci l'istante finale: "))
    nstep = int(input('\nInscerisci il numero di iterazioni: '))

    par = [m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep]

    return par



def computeCoordinates(t1, t2, t3, par):
    '''Computes cartesian coordinates from generalized coordinates'''

    l1 = par[3]
    l2 = par[4]
    l3 = par[5]
    
    x1 = +l1*np.sin(t1)
    y1 = -l1*np.cos(t1)
    x2 = +l2*np.sin(t2) + x1
    y2 = -l2*np.cos(t2) + y1
    x3 = +l3*np.sin(t3) + x2
    y3 = -l3*np.cos(t3) + y2

    return x1, y1, x2, y2, x3, y3



def figureSetup(t1, t2, t3, o1, o2, o3, par):
    '''Plot figure configuration'''

    l1 = par[3]
    l2 = par[4]
    l3 = par[5]
    t0 = par[7]
    tf = par[8]

    t1Min = np.amin(t1)
    t2Min = np.amin(t2)
    t3Min = np.amin(t3)
    tMin = np.amin([t1Min, t2Min, t3Min])

    t1Max = np.amax(t1)
    t2Max = np.amax(t2)
    t3Max = np.amax(t3)
    tMax = np.amax([t1Max, t2Max, t3Max])

    o1Min = np.amin(o1)
    o2Min = np.amin(o2)
    o3Min = np.amin(o3)
    oMin = np.amin([o1Min, o2Min, o3Min])

    o1Max = np.amax(o1)
    o2Max = np.amax(o2)
    o3Max = np.amax(o3)
    oMax = np.amax([o1Max, o2Max, o3Max])

    fig1 = plt.figure(figsize=(14, 6))
    gs = fig1.add_gridspec(5, 9)

    ax1 = fig1.add_subplot(gs[:, 5:])
    ax2 = fig1.add_subplot(gs[0:2, :-5])
    ax3 = fig1.add_subplot(gs[3:5, :-5])

    ax1.set_xlim(-l1-l2-l3, l1+l2+l3)
    ax1.set_ylim(-l1-l2-l3, l1+l2+l3)

    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin, tMax)

    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin, oMax)

    
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



def pendoloTriplo():
    '''Pendolo Triplo'''
    print('\nHai scelto il pendolo triplo')

    g = 9.81

    par = inputParameters()
    m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep = par

    print('\nDigita 0 per visualizzare grafici statici\nDigita 1 per visualizzare grafici animati\n')
    mode = int(input(''))

    #q[0] = theta0
    #q[1] = omega0
    #q[2] = theta1
    #q[3] = omega1
    #q[4] = theta2
    #q[5] = omega2
    def motion(q, t):
        '''Equazione del Moto'''

        m01 = m1 + m2
        m02 = m1 + m3
        m12 = m2 + m3
        m012 = m1 + m2 + m3
        mf = m012/4

        cos0 = np.cos(q[0])
        cos1 = np.cos(q[2])
        cos2 = np.cos(q[4])
        sin0 = np.sin(q[0])
        sin1 = np.sin(q[2])
        sin2 = np.sin(q[4])

        cos01 = np.cos(q[0]-q[2])
        cos02 = np.cos(q[0]-q[4])
        cos12 = np.cos(q[2]-q[4])
        sin01 = np.sin(q[0]-q[2])
        sin02 = np.sin(q[0]-q[4])
        sin12 = np.sin(q[2]-q[4])

        r1 = m12*cos01*cos02 - m012*cos12
        r2 = m012 - m12*(cos01)**2
        r3 = -m012 + m3*(cos02)**2

        od1_1 = 4*m3*m12
        od1_2 = r1*cos01 + r2*cos02
        od1_3 = -g*sin2 + l1*sin02*q[1]**2 + l2*sin12*q[3]**2
        od1_4 = -g*m2*sin1 - g*m3*sin1 + l1*m2*sin01*q[1]**2 + l1*m3*sin01*q[1]**2 - l3*m3*sin12*q[5]**2
        od1_5 = -m3*m12*( -cos02 + np.cos(q[0]-2*q[2]+q[4]) )**2 * m012
        od1_6 = g*m1*sin0 + g*m2*sin0 + g*m3*sin0 + l2*m2*sin01*q[3]**2 + l2*m3*sin01*q[3]**2 + l3*m3*sin02*q[5]**2
        od1_7 = m3*r1**2 + m12*r3*r2

        od2_1 = -g*sin2 + l1*sin02*q[1]**2 + l2*sin12*q[3]**2
        od2_2 = g*m1*sin0 + g*m2*sin0 + g*m3*sin0 + l2*m2*sin01*q[3]**2 + l2*m3*sin01*q[3]**2 + l3*m3*sin02*q[5]**2
        od2_3 = -g*m2*sin1 - g*m3*sin1 + l1*m2*sin01*q[1]**2 + l1*m3*sin01*q[1]**2 - l3*m3*sin12*q[5]**2

        od3_1 = g*m1*sin0 + g*m2*sin0 + g*m3*sin0 + l2*m2*sin01*q[3]**2 + l2*m3*sin01*q[3]**2 + l3*m3*sin02*q[5]**2
        od3_2 = -g*sin2 + l1*sin02*q[1]**2 + l2*sin12*q[3]**2
        od3_3 = g*m2*sin1 + g*m3*sin1 - l1*m2*sin01*q[1]**2 - l1*m3*sin01*q[1]**2 + l3*m3*sin12*q[5]**2


        td1 = q[1]
        td2 = q[3]
        td3 = q[5]

        od1 = mf * ( od1_1 * od1_2 * od1_3 * r2 - 4 * ( -m3 * od1_2 * r1 + ( m3 * r1**2 + m12 * r3 * r2 ) * cos01 ) * od1_4 - ( od1_5 + 4*m3*r1**2 + 4*m12*r3*r2 ) * od1_6 ) / ( l1 * od1_7 * m012 * r2)
        od2 = ( -m3 * r1 * m012 * od2_1 * r2 - ( m3 * ( r1*cos01 + r2*cos02 ) * r1 - ( m3*r1**2 + m12*r3*r2 ) * cos01 ) * od2_2 + m012*r3*r2*od2_3 ) / ( l2 * od1_7 * r2 )
        od3 = -( m12 * (od1_2) * (od3_1) + m12 * m012 * (od3_2) * r2 - r1*m012 * od3_3 ) / ( l3 * ( m3*r1**2 + m12*r3*r2 ) )

        return np.array([td1, od1, td2, od2, td3, od3])


    q, t = rk4(motion, q0, t0 , tf , nstep)

    h = t[1]-t[0]
    t1, o1, t2, o2, t3, o3 = q.T

    x1, y1, x2, y2, x3, y3 = computeCoordinates(t1, t2, t3, par)


    fig1, ax1, ax2, ax3 = figureSetup(t1, t2, t3, o1, o2, o3, par)

    # static plots
    if mode == 0:

        ax1.plot(x1, y1, '-', lw=2, color = '#047FFF') 
        ax1.plot(x2, y2, '-', lw=2, color = '#FF4B00')
        ax1.plot(x3, y3, '-', lw=2, color = '#00C415') 
        ax2.plot(t, t1, '-', lw=2, color = '#047FFF')
        ax2.plot(t, t2, '-', lw=2, color = '#FF4B00')
        ax2.plot(t, t3, '-', lw=2, color = '#00C415')
        ax3.plot(t, o1, '-', lw=2, color = '#047FFF') 
        ax3.plot(t, o2, '-', lw=2, color = '#FF4B00')
        ax3.plot(t, o3, '-', lw=2, color = '#00C415')


    # animated plots
    elif mode == 1:

        pendulumSegment, = ax1.plot([], [], 'o-', lw=2, color = '#000000')
        pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF')
        pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00')
        pendulumTrace3, = ax1.plot([], [], '-', lw=2, color = '#00C415')
        thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF')
        thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00')
        thetaTrace3, = ax2.plot([], [], '-', lw=2, color = '#00C415')
        omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF')
        omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00')
        omegaTrace3, = ax3.plot([], [], '-', lw=2, color = '#00C415')

        time_template = 'time = %.1fs'
        time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)


        def animate(i, x1, y1, x2, y2, x3, y3, line1, line2, line3):
            line1.set_data(x1[:i], y1[:i])
            line2.set_data(x2[:i], y2[:i])
            line3.set_data(x3[:i], y3[:i])
            return line1, line2, line3,

        def pendulum(i, x1, y1, x2, y2, x3, y3, trace1, trace2, trace3, pendulum):
            segmentX = [0, x1[i], x2[i], x3[i]]
            segmentY = [0, y1[i], y2[i], y3[i]]
            trace1.set_data(x1[i-25:i], y1[i-25:i])
            trace2.set_data(x2[i-40:i], y2[i-40:i])
            trace3.set_data(x3[i-70:i], y3[i-70:i])
            pendulum.set_data(segmentX, segmentY)
            time_text.set_text(time_template % (i*h))
            return trace1, trace2, trace3, pendulum, time_text,

    
        anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x1, y1, x2, y2, x3, y3, pendulumTrace1, pendulumTrace2, pendulumTrace3, pendulumSegment], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, t1, t, t2, t, t3, thetaTrace1, thetaTrace2, thetaTrace3], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, o1, t, o2, t, o3, omegaTrace1, omegaTrace2, omegaTrace3], interval=h, blit=True)


    plt.show()