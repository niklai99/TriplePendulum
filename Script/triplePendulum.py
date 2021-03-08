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


def computeEnergy(q, par):
    '''Computes total energy of the system'''

    m1 = par[0]
    m2 = par[1]
    m3 = par[2]
    l1 = par[3]
    l2 = par[4]
    l3 = par[5]
    t1, o1, t2, o2, t3, o3 = q.T

    E = np.zeros(len(t1))
    U = np.zeros(len(t1))
    T = np.zeros(len(t1))

    for i in range(len(t1)):
        E[i] = 0.5 * (m1+m2+m3) * l1**2 * o1[i]**2 + 0.5 * (m2+m3) * l2**2 * o2[i]**2 + 0.5 * m3 * l3**2 * o3[i]**2 + (m2+m3)*l1*l2*o1[i]*o2[i]*np.cos(t1[i]-t2[i]) +  m3*l1*l3*o1[i]*o3[i]*np.cos(t1[i]-t3[i]) + m3*l2*l3*o2[i]*o3[i]*np.cos(t2[i]-t3[i])
        U[i] = - 9.81 * ( l1*(m1+m2+m3)*np.cos(t1[i]) + l2*(m2+m3)*np.cos(t2[i]) +  l3*m3*np.cos(t3[i]) )
        T[i] = E[i] + U[i]

    return E, U, T



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

    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    fig1 = plt.figure(figsize=(14, 6))
    gs = fig1.add_gridspec(9, 33)

    ax1 = fig1.add_subplot(gs[:, 20:])
    ax2 = fig1.add_subplot(gs[0:4, 0:17])
    ax3 = fig1.add_subplot(gs[5:9, 0:17])

    ax1.set_xlim(-((l1+l2+l3) + (l1+l2+l3)/5), (l1+l2+l3) + (l1+l2+l3)/5)
    ax1.set_ylim(-((l1+l2+l3) + (l1+l2+l3)/5), (l1+l2+l3) + (l1+l2+l3)/5)

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



def triplePendulum():
    '''Pendolo Triplo'''
    print('\nHai scelto il pendolo triplo')


    print('Premi "d" per parametri default\nPremi "s" per scegliere i parametri')
    choice = str(input(''))

    if choice == 'd':
        m1 = 1
        m2 = 1
        m3 = 1
        l1 = 1
        l2 = 1
        l3 = 1
        q0 = np.array([np.radians(135), np.radians(0), np.radians(135), np.radians(0), np.radians(135), np.radians(0)])
        t0 = 0
        tf = 10
        nstep = 1000
        par = [m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep]
    
    elif choice == 's':
        par = inputParameters()
        m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep = par

    g = 9.81

    
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

    E, U, T = computeEnergy(q, par)

    h = t[1]-t[0]
    t1, o1, t2, o2, t3, o3 = q.T

    x1, y1, x2, y2, x3, y3 = computeCoordinates(t1, t2, t3, par)


    fig1, ax1, ax2, ax3 = figureSetup(t1, t2, t3, o1, o2, o3, par)

    # static plots
    if mode == 0:

        ax1.plot(x1, y1, '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
        ax1.plot(x2, y2, '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
        ax1.plot(x3, y3, '-', lw=2, color = '#00C415', label = '3rd mass trajectory') 
        ax2.plot(t, t1, '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        ax2.plot(t, t2, '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        ax2.plot(t, t3, '-', lw=2, color = '#00C415', label = '3rd mass \u03B8(t)')
        ax3.plot(t, o1, '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
        ax3.plot(t, o2, '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
        ax3.plot(t, o3, '-', lw=2, color = '#00C415', label = '3rd mass \u03C9(t)')

        ax1.legend(loc = 'upper right', ncol = 1)
        ax2.legend(loc = 'upper right', ncol = 3)
        ax3.legend(loc = 'upper right', ncol = 3)


    # animated plots
    elif mode == 1:

        pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
        pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
        pendulumMass2, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m2)
        pendulumMass3, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m3)
        masses = [pendulumMass0, pendulumMass1, pendulumMass2, pendulumMass3]

        pendulumSegments, = ax1.plot([], [], '-', lw=2, color = '#000000')

        pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
        pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
        pendulumTrace3, = ax1.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass trajectory')

        thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
        thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        thetaTrace3, = ax2.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass \u03B8(t)')

        omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
        omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
        omegaTrace3, = ax3.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass \u03C9(t)')

        ax1.legend(loc = 'upper right', ncol = 1)
        ax2.legend(loc = 'upper right', ncol = 3)
        ax3.legend(loc = 'upper right', ncol = 3)

        time_template = 'time = %.1fs'
        time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

        kineticEnergy_template = 'kenetic energy = %.2f J'
        kineticEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)
        potentialEnergy_template = 'potential energy = %.2f J'
        potentialEnergy_text = ax1.text(0.05, 0.82, '', transform=ax1.transAxes)
        totalEnergy_template = 'total energy = %.2f J'
        totalEnergy_text = ax1.text(0.05, 0.77, '', transform=ax1.transAxes)


        def animate(i, x1, y1, x2, y2, x3, y3, line1, line2, line3):
            line1.set_data(x1[:i], y1[:i])
            line2.set_data(x2[:i], y2[:i])
            line3.set_data(x3[:i], y3[:i])
            return line1, line2, line3,

        def pendulum(i, x1, y1, x2, y2, x3, y3, trace1, trace2, trace3, masses, segments):

            massX0 = [0]
            massY0 = [0]
            massX1 = [x1[i]]
            massY1 = [y1[i]]
            massX2 = [x2[i]]
            massY2 = [y2[i]]
            massX3 = [x3[i]]
            massY3 = [y3[i]]

            segmentX = [0, x1[i], x2[i], x3[i]]
            segmentY = [0, y1[i], y2[i], y3[i]]

            trace1.set_data(x1[i-25:i], y1[i-25:i])
            trace2.set_data(x2[i-40:i], y2[i-40:i])
            trace3.set_data(x3[i-70:i], y3[i-70:i])

            mass0, mass1, mass2, mass3 = masses

            mass0.set_data(massX0, massY0)
            mass1.set_data(massX1, massY1)
            mass2.set_data(massX2, massY2)
            mass3.set_data(massX3, massY3)

            segments.set_data(segmentX, segmentY)

            time_text.set_text(time_template % (i*h))

            totalEnergy_text.set_text(totalEnergy_template % (T[i]))
            kineticEnergy_text.set_text(kineticEnergy_template % (E[i]))
            potentialEnergy_text.set_text(potentialEnergy_template % (U[i]))


            return trace1, trace2, trace3, mass0, mass1, mass2, mass3, segments, time_text, totalEnergy_text, kineticEnergy_text, potentialEnergy_text,

    
        anim1 = animation.FuncAnimation(fig1, pendulum, frames=len(t), fargs=[x1, y1, x2, y2, x3, y3, pendulumTrace1, pendulumTrace2, pendulumTrace3, masses, pendulumSegments], interval=h, blit=True)
        anim2 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, t1, t, t2, t, t3, thetaTrace1, thetaTrace2, thetaTrace3], interval=h, blit=True)
        anim3 = animation.FuncAnimation(fig1, animate, frames=len(t), fargs=[t, o1, t, o2, t, o3, omegaTrace1, omegaTrace2, omegaTrace3], interval=h, blit=True)


    plt.show()