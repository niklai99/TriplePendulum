# TriplePendulum Script

The idea behind this script is to give the user a fully customizable system.

## Run the Script

To run the script, simply run the [MAIN.py](./MAIN.py) module 

```
$ python MAIN.py
```

and follow the instructions given.

## User's Choice

* The user can choose whether to work with a

   1. Simple Pendulum
   2. Double Pendulum
   3. Triple Pendulum

* The user can choose whether to insert values for

    1. Masses of the points
    2. Lengths of the ropes
    3. Initial angles
    4. Intitial angular velocities
    5. Starting time
    6. Ending time
    7. Number of iterations to perform

    Or decide to use default parameters, such as

    1. Masses equal to 1kg
    2. Lengths equal to 1m
    3. Initial angles equal to 135deg
    4. Initial velocities equal to 0deg/s
    5. Starting time equals to 0s
    6. Ending time equals to 10s
    7. Number of iterations equals to 1000

* The user can also choose whether to plot

    1. Static figures
    2. Animated figures

## Modules

### [MAIN.py](./MAIN.py)

The [MAIN.py](./MAIN.py) module contains the _main()_ function. It enables the user to choose between the simple, double and triple pendulum system

```python
# Read input from keyboard
try:
    n=int(input('\n'))
except ValueError:
    print('\nMust be a number')
```

and then, depending on the input number, it enters the appropriate function

```python
# Enter the appropriate function
if n == 1:
    simplePendulum(n)
    
elif n == 2:
    doublePendulum(n)

elif n == 3:
    triplePendulum(n)

else:
    print('Not supported')
```

### [inputParameters.py](./inputParameters.py)

The [inputParameters.py](./inputParameters.py) module contains the _inputParameters(n)_ function, which requires as argument the integer _n_ assigned in the _main()_ function and holding the information about the system (1 = simple pendulum, 2 = double pendulum, 3 = triple pendulum). 

Inside the _inputParameters(n)_ function, a temporary parameter array, the initial conditions array and the simulation time constraints array are filled as follows

```python
# Fill the p array with masses
for i in range(n):    
    p[i] = float(input('\nInsert mass for point %1.0f: ' % (i+1)))

# Fill the p array with lengths
for j in range(n):
    p[j+n] = float(input('\nInsert length for rope %1.0f: ' % (j+1)))
    
# Fill the q0 array with initial angles
for k in range(n):
    q0[2*k] = np.radians(float(input('\nInsert initial angle of point %1.0f (in deg): ' % (k+1))))

# Fill the q0 array with initial velocities
for l in range(n):
    q0[2*l + 1] = np.radians(float(input('\nInsert initial angular velocity of point %1.0f (in deg/s): ' % (l+1))))

# Fill the simTime array with the starting time, ending time and the number of iterations to perform
simTime[0] = int(input("\nInsert starting time: "))
simTime[1] = int(input("\nInsert ending time: "))
simTime[2] = int(input('\nInsert number of iterations: '))
```

Finally, a comprehensive parameter list is created and returned

```python
# Create the parameters list
par = [*p, q0, *simTime]

return par
```

The parameters list is thus in the form of [_masses_, _lengths_, _initial conditions_, _time constraints_].


### [equationsMotion.py](./equationsMotion.py)

The [equationsMotion.py](./equationsMotion.py) module contains three functions:

1. _simplePendulumEq(q, t, par)_
2. _doublePendulumEq(q, t, par)_
3. _triplePendulumEq(q, t, par)_

Each of these equations takes as arguments the generalized coordinates array _q_, the time series _t_ and the parameters list _par_. 

The _simplePendulumEq(q, t, par)_ function is used here as an example, since the other two functions share the same structure.

```python
def simplePendulumEq(q, t, par):
    '''Simple Pendulum equation of motion'''

    # Define relevant parameters
    g = 9.81
    m1 = par[0]
    l1 = par[1]

    # ThetaDot equation
    td = q[1]

    # OmegaDot equation
    od = -m1*(g/l1)*np.sin(q[0])

    return np.array([td, od])
```

In the first half of the function, relevant parameters such as the gravitational acceleration constant, the mass of the point and the length of the rope are defined/extracted in order to be used more comfortably in the following equations.

In the second half of the function, the first order differential system is defined and the array correspoding to the velocity and acceleration is returned. 

### [rungeKutta4.py](./rungeKutta4.py)

The [rungeKutta4.py](./rungeKutta4.py) module contains the _RungeKutta4(f, par)_ function shown below.

```python
def RungeKutta4(f, par):
    ''' 
        Runge-Kutta 4: the algorithm asks for the function f, 
        which is the callable equation of motion function, 
        and the list of parameters of the system
    '''

    # Unpack initial conditions
    q0 = par[-4]

    # Unpack time conditions and number of iterations
    t0 = par[-3]
    tf = par[-2]
    n  = par[-1]

    # Make the time grid
    t = np.linspace(int(t0), int(tf), int(n)+1)
    h = t[1]-t[0]

    # Initialize the solution array
    q = np.array((int(n)+1)*[q0])
    
    # Fill the solution array using the RungeKutta 4 iterative method
    for i in range(int(n)):
        k1 = h * f(q[i], t[i], par)
        k2 = h * f(q[i] + 0.5 * k1, t[i] + 0.5*h, par)
        k3 = h * f(q[i] + 0.5 * k2, t[i] + 0.5*h, par)
        k4 = h * f(q[i] + k3, t[i] + h, par)
        q[i+1] = q[i] + (k1 + 2*(k2 + k3) + k4) / 6

    return q, t, h
```

The function requires as arguments the callable function _f_, which is going to be one of the three equations of motions defined in the [equationsMotion.py](./equationsMotion.py) module, and the parameters list _par_.

In the first part of the function parameters and the time serie are defined, along with the generalized coordinates solution array. 

In the ending part of the function, the RungeKutta 4 iterative method is implemented to evaluate the generalized positions by numerically integrating the equations of motion.

Finally, the function returns the generalized coordinates solution array _q_, the time serie _t_ and the time increment _h_.


### [computeCoordinates.py](./computeCoordinates.py)

The [computeCoordinates.py](./computeCoordinates.py) module contains the _computeCoordinates(n, q, par)_ function. 

This function is used to compute cartesian _(x, y)_ coordinates from the generalized coordinates _q_. For the pendulum system the generalized coordinates _q_ are chosen to be the pendulums angle from the vertical, thus the cartesian coordinates and the generalized coordinates are connected by a sine/cosine type of relation.

```python
# If the system is the simple pendulum
if n == 1:
    x[0] = +par[n] * np.sin(q[:,0])
    y[0] = -par[n] * np.cos(q[:,0])
    
# If the system is the double pendulum
elif n == 2:
    x[0] = +par[n] * np.sin(q[:,0])
    y[0] = -par[n] * np.cos(q[:,0])
    x[1] = +par[n+1] * np.sin(q[:,2]) + x[0]
    y[1] = -par[n+1] * np.cos(q[:,2]) + y[0]
    
# If the system is the triple pendulum
elif n == 3:
    x[0] = +par[n] * np.sin(q[:,0])
    y[0] = -par[n] * np.cos(q[:,0])
    x[1] = +par[n+1] * np.sin(q[:,2]) + x[0]
    y[1] = -par[n+1] * np.cos(q[:,2]) + y[0]
    x[2] = +par[n+2] * np.sin(q[:,4]) + x[1]
    y[2] = -par[n+2] * np.cos(q[:,4]) + y[1]
```



### [computeEnergy.py](./computeEnergy.py)

The [computeEnergy.py](./computeEnergy.py) module contains three functions:

1. _simplePendulumEnergy(q, par)_
2. _doublePendulumEnergy(q, par)_
3. _triplePendulumEnergy(q, par)_

Each function computes the kinetic, potential and total energy of the system at every time instant of the integration/simulation, thus returning arrays of kinetic, potential and total energy. 

Since all three functions share the same structure, the _simplePendulumEnergy(q, par)_ function is taken as example.

```python
def simplePendulumEnergy(q, par):
    '''Computes and returns total energy of the simple pendulum system'''

    # Unpack the relevant parameters
    m1 = par[0]
    l1 = par[1]

    # Unpack theta and omega from the generalized coordinates array q
    t1, o1 = q.T

    # Initialize arrays for the three energies
    E = np.zeros(len(t1))
    U = np.zeros(len(t1))
    T = np.zeros(len(t1))

    # Fill the energy arrays 
    for i in range(len(t1)):
        E[i] = 0.5 * m1 * l1**2 * o1[i]**2
        U[i] = - m1 * 9.81 * l1*np.cos(t1[i])
        T[i] = E[i] + U[i]

    return E, U, T
```

### [figureSetup.py](./figureSetup.py)

The [figureSetup.py](./figureSetup.py) module contains three functions:

1. _staticFigure(n, q, par)_
2. _animatedFigure(n, q, par)_
3. _addLegend(n, ax1, ax2, ax3)_

*   The _staticFigure(n, q, par)_ deals with the settings for the static plots. 

    ```python
    # Create the figure
    fig = plt.figure(figsize=(14, 6))
    # Set the figure axes grid
    gs = fig.add_gridspec(9, 33)

    # Create the axes:
    # ax1 holds the pendulum trajectory
    # ax2 holds the theta trend
    # ax3 holds the omega trend
    ax1 = fig.add_subplot(gs[:, 20:])
    ax2 = fig.add_subplot(gs[0:4, 0:17])
    ax3 = fig.add_subplot(gs[5:9, 0:17])

    # ax1 title and labels
    ax1.set_title('Pendulum Trajectory')
    ax1.set_xlabel('x coordinate (m)')
    ax1.set_ylabel('y coordinate (m)')

    # ax2 title and labels
    ax2.set_title('\u03B8 trend over time')
    ax2.set_xlabel('time (s)', loc = 'right')
    ax2.set_ylabel('\u03B8 (rad)', loc = 'top')

    # ax3 title and labels
    ax3.set_title('\u03C9 trend over time')
    ax3.set_xlabel('time (s)', loc = 'right')
    ax3.set_ylabel('\u03C9 (rad/s)', loc = 'top')
    ```

    The function, by taking as arguments the type of system _n_, the generalized coordinates _q_ and the parameters list _par_, computes automatically the best plot ranges for each  static axes. For example, when dealing with a double pendulum

    ```python
    # Unpack the length of the ropes
    l1 = par[n]
    l2 = par[n+1]

    # Compute the total length
    l = l1 + l2

    # Compute the maximum and minimum of the theta trend
    t1Min = np.amin(q[:,0])
    t2Min = np.amin(q[:,2])
    tMin = np.minimum(t1Min, t2Min)

    t1Max = np.amax(q[:,0])
    t2Max = np.amax(q[:,2])
    tMax = np.maximum(t1Max, t2Max)

    # Compute the maximum and minimum of the omega trend
    o1Min = np.amin(q[:,1])
    o2Min = np.amin(q[:,3])
    oMin = np.minimum(o1Min, o2Min)

    o1Max = np.amax(q[:,1])
    o2Max = np.amax(q[:,3])
    oMax = np.maximum(o1Max, o2Max)

    # Compute the half span of theta and omega trends
    varT = (tMax - tMin) / 2
    varO = (oMax - oMin) / 2

    # Set ax1 plot range
    ax1.set_xlim(-(l + l/5), l + l/5)
    ax1.set_ylim(-(l + l/5), l + l/5)

    # Set ax2 plot range
    ax2.set_xlim(t0, tf)
    ax2.set_ylim(tMin - varT/2, tMax + varT)

    # Set ax3 plot range
    ax3.set_xlim(t0, tf)
    ax3.set_ylim(oMin - varO/2, oMax + varO)
    ```

    axis limits are automatically computed and the three axes, along with the figure, are returned. 

*   The _animatedFigure(n, q, par)_ deals with the settings for the animated plots. 

    The structure of this function is exactly the same as the _staticFigure(n, q, par)_ one. The difference between the two is that, when dealing with animated figures, two more axes, the kinetic and potential energy bars, are created and displayed.

    ```python
    #ax4 title and labels
    ax4.set_title(r'E$_k$')
    ax4.axes.xaxis.set_ticks([])
    ax4.axes.yaxis.set_ticks([])
    
    # ax5 title and labels
    ax5.set_title(r'E$_p$')
    ax5.axes.xaxis.set_ticks([])
    ax5.axes.yaxis.set_ticks([])
    ```

*   The _addLegend(n, ax1, ax2, ax3)_ function simply adds the plot legend to each plot.

    ```python
    ax1.legend(loc = 'upper right', ncol = n)
    ax2.legend(loc = 'upper right', ncol = n)
    ax3.legend(loc = 'upper right', ncol = n)
    ```


### [animationModule.py](./animationModule.py)

The [animationModule.py](./animationModule.py) module contains the animation functions, used to achieve moving pendulums and coordinate trends.  

1.  The first three functions,

    *  _simplePendulumTrend()_
    *  _doublePendulumTrend()_
    *  _triplePendulumTrend()_

    simply animate the generalized coordinates and velocities trends over time. They all share the same structure, thus the third one is taken as an example.

    ```python
    def triplePendulumTrend(i, s, t, q, lines):
        '''Animate coordinate trends over time for a triple pendulum'''

        # Unpack the lines to plot
        line1, line2, line3 = lines

        # If the line refers to the angle
        if s == 'theta':  
            # Set new data for each iteration
            line1.set_data(t[:i], q[:i, 0])
            line2.set_data(t[:i], q[:i, 2])
            line3.set_data(t[:i], q[:i, 4])

        # If the line refers to the velocity
        elif s == 'omega':
            # Set new data for each iteration
            line1.set_data(t[:i], q[:i, 1])
            line2.set_data(t[:i], q[:i, 3])
            line3.set_data(t[:i], q[:i, 5])

        return line1, line2, line3,
    ```

    The function requires five parameters passed as arguments:

    *   The parameter _i_ refers to the iteration necessary to animate objects
    *   The parameter _s_ is a string that may be either 'theta' or 'omega', specifying whether the trend refers to the coordinates or the velocities
    *   The parameter _t_ is the time serie to be plotted on the x-axis
    *   The parameter _q_ holds the generalized coordinates and velocities
    *   The parameter _lines_ holds the lineplot's lines to be updated with new data each iteration

2.  The next three functions,

    *   _simplePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h)_
    *   _doublePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h)_
    *   _triplePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h)_

    animate the pendulum itself and plot trajectory traces relative to each mass point of the pendulum. They all share the same structure, thus the third one is taken as an example.

    ```python
    def triplePendulumAnimation(i, x, y, traces, masses, segments, texts, T, h):
        '''Animate the triple pendulum'''

        # Set the points position over each iteration
        massX0 = [0]
        massY0 = [0]
        massX1 = [x[i, 0]]
        massY1 = [y[i, 0]]
        massX2 = [x[i, 1]]
        massY2 = [y[i, 1]]
        massX3 = [x[i, 2]]
        massY3 = [y[i, 2]]

        # Set the segment position over each iteration
        segmentX = [0, x[i, 0], x[i, 1], x[i, 2]]
        segmentY = [0, y[i, 0], y[i, 1], y[i, 2]]

        # Unpack the trajecotry traces
        trace1, trace2, trace3 = traces

        # Plot the trajectory trace data over each iteration
        trace1.set_data(x[i-25:i, 0], y[i-25:i, 0])
        trace2.set_data(x[i-40:i, 1], y[i-40:i, 1])
        trace3.set_data(x[i-65:i, 2], y[i-65:i, 2])

        # Unpack mass points
        mass0, mass1, mass2, mass3 = masses
        # Plot point positions
        mass0.set_data(massX0, massY0)
        mass1.set_data(massX1, massY1)
        mass2.set_data(massX2, massY2)
        mass3.set_data(massX3, massY3)

        # Plot segments position
        segments.set_data(segmentX, segmentY)

        # Unpack texts
        time_template, time_text, totalEnergy_template, totalEnergy_text = texts

        # Plot time text
        time_text.set_text(time_template % (i*h))
        # Plot total energy text
        totalEnergy_text.set_text(totalEnergy_template % (T[i]))

        return trace1, trace2, trace3, mass0, mass1, mass2, mass3, segments, time_text, totalEnergy_text,
    ```

    The function requires nine parameters passed as arguments:

     *   The parameter _i_ refers to the iteration necessary to animate objects
     *   The parameters _x_ and _y_ are the cartesian coordinates of the pendulum trajectory
     *   The parameter _traces_ is the list of lineplot's lines to be updated with new data each iteration
     *   The parameter _masses_ is the list of points, referring to the masses position, to be updated with new data each iteration
     *   The parameter _segments_ is the list of segments position connecting two mass points to be updated with new data each iteration
     *   The parameter _texts_ is the list containing text templates and text objects to be updated each iteration
     *   The parameter _T_ refers to the total energy of the system
     *   The parameter _h_ is the time step of the time serie

    With the use of this function, several objects are updated each iteration and thus animated! The result is an animated pendulum with trajectory traces attached to each mass point, which are constantly connected by a rigid segment. The passage of time is also made clear by updating the time text. Finally the total energy of the system is also updated and shown as a text object right below the time text. Since energy is conserved in such systems, the energy text object should not change over time. Though, if the dynamic of the system is very intricate due to unfavorable parameters choice, the total energy might change over time. In this case, the user should consider using a finer time grid, achieved by increasing the number of iterations while keeping the time limits constant. 

3. The last two functions animate the kinetic and potential energy bar as follows

    ```python
    def kineticEnergyAnimation(i, ax, E, U):
    '''Animate the kinetic energy bar'''

        # Fill the bar with the kinetic energy
        rect1 = ax.fill_between(x = (0, 1), y1 = 0, y2 = E[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), 
                                color = 'red')

        return rect1,

    def potentialEnergyAnimation(i, ax, E, U):
    '''Animate the potential energy bar'''

        # Fill the bar with the potential energy
        rect2 = ax.fill_between(x = (0, 1), y1 = 0, y2 = U[i] / (np.abs(np.amax(E))+np.abs(np.amax(U))), 
                                color = 'blue')

        return rect2,
    ```

    They both requires the same parameters, which are indeed the iteration parameter _i_, the axes containing the bar to be updated each interation and the kinetic and potential energy arrays.

### [simplePendulum.py](./simplePendulum.py)

The [simplePendulum.py](./simplePendulum.py) module basically uses all the modules shown above to produce all the relevant informations about the simple pendulum motion. 

Initially, the user is asked whether to use default parameters or to choose each value of such parameters:

```python
# Let the user decide whether to use deafult parameters or to insert custom parameters
print('Insert "d" to choose default parameters\n')
print('Insert "s" to input your parameters\n')
choice = str(input(''))
```

If the user chooses to utilize default values for the parameters of the system, then such parameters are set to those default values

```python
# If the user chose to use default parameters
# Set the default parameters
if choice == 'd':
    # Set the point mass to 1kg
    m1 = 1
    # Set the rope length to 1m
    l1 = 1
    # Set the initial angle to 135deg and initial angular velocity to 0deg/s
    q0 = np.array([np.radians(135), np.radians(0)])
    # Set the starting time to 0s
    t0 = 0
    # Set the ending time to 10s
    tf = 10
    # Set the number of iterations to 1000
    nstep = 1000
    # Create the parameter list
    par = [m1, l1, q0, t0, tf, nstep]
```

Otherwise, the function _inputParameters(n)_ is called.

```python
# If the user chose to insert custom parameters 
# Call the inputParameters() function in inputParameters.py module
elif choice == 's':
    par = inputParameters(n)
    m1, l1, q0, t0, tf, nstep = par
```

After that, the equations of motion are integrated using the _RungeKutta4(f, par)_ function

```python
# Integrate the equation of motion using the RungeKutta4() function in rungeKutta4.py module
# Arguments passed to the function are:
# 1) the simple pendulum equation of motion from the equationsMotion.py module
# 2) the parameters list
q, t, h = RungeKutta4(simplePendulumEq, par)
```

Then, the kinetic, potential and totale energy are computed using the _simplePendulumEnergy(q, par)_ function

```python
# Compute the kinetic, potential and total energy 
# through the simplePendulumEnergy() function in computeEnergy.py module
E, U, T = simplePendulumEnergy(q, par)
```

Moving forward, the (x, y) coordinates are computed by using the _computeCoordinates(n, q, par)_ function

```python
# Compute the cartesian (x, y) coordinates from the generalized coordinates q (i.e. angular positions)
# using the computeCoordinates() function in computeCoordinates.py module
x, y = computeCoordinates(n, q, par)
```

At this point, the user is asked to choose whether to display static or animated figures

```python
# Let the user decide whether to plot static figures or animated figures
print('\nInsert 0 for static plots')
print('Insert 1 to see animations\n')
mode = int(input(''))
```

If static figures has been chosen, then the figure, axes, plots and legends are created

```python
# Create the figure and the axes using the staticFigure() function in the figureSetup.py module
fig, ax1, ax2, ax3 = staticFigure(n, q, par)

# Plot the pendulum trajectory
ax1.plot(x, y, '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
# Plot the theta trend over time
ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')     
# Plot the omega trend over time
ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

# Add a legend to the figures using the addLegend() function in the figureSetup.py module
addLegend(n, ax1, ax2, ax3)
```

Otherwise, figure and axes are created, along with all the elements needed to provide an animation as output

```python
# Create the figure and the axes using the animatedFigure() function in the figureSetup.py module
fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

# Create the fixed point and the pendulum mass point as empty plots (they will be animated!)
pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
masses = [pendulumMass0, pendulumMass1]

# Create the pendulum rope as an empy plot (it will be animated!)
pendulumSegment, = ax1.plot([], [], '-', lw=2, color = '#000000')

# Create the pendulum trace of the trajectory as an empty plot (it will be animated!)
pendulumTrace, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')

# Create the theta trend over time trace as an empy plot (it will be animated!)
thetaTrace, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')

# Create the omega trend over time trace as an empy plot (it will be animated!)
omegaTrace, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')

# Add a legend to the figures using the addLegend() function in the figureSetup.py module
addLegend(n, ax1, ax2, ax3)

# Create the template and the text in which time will be displayed and updated each iteration
time_template = 'time = %.1f s'
time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

# Create the template and the text in which the total energy of the system will be displayed and updated each iteration
totalEnergy_template = 'total energy = %.2f J'
totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

texts = [time_template, time_text, totalEnergy_template, totalEnergy_text]

# Create the kinetic energy bar
rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
ax4.add_patch(rect1)

# Create the potential energy bar
rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
ax5.add_patch(rect2)

# Animate the plots using functions in the animationModule.py module
anim1 = animation.FuncAnimation(fig, simplePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTrace, masses, pendulumSegment, texts, T, h], interval=h, blit=True)
anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
anim4 = animation.FuncAnimation(fig, simplePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTrace], interval=h, blit=True)
anim5 = animation.FuncAnimation(fig, simplePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTrace], interval=h, blit=True)
```



### [doublePendulum.py](./doublePendulum.py)

The [doublePendulum.py](./doublePendulum.py) module basically uses all the modules shown above to produce all the relevant informations about the double pendulum motion. 

Initially, the user is asked whether to use default parameters or to choose each value of such parameters:

```python
# Let the user decide whether to use deafult parameters or to insert custom parameters
print('Insert "d" to choose default parameters\n')
print('Insert "s" to input your parameters\n')
choice = str(input(''))
```

If the user chooses to utilize default values for the parameters of the system, then such parameters are set to those default values

```python
# If the user chose to use default parameters
# Set the default parameters
if choice == 'd':
    # Set the points mass to 1kg
    m1 = 1
    m2 = 1
    # Set the ropes length to 1m
    l1 = 1
    l2 = 1
    # Set the initial angles to 135deg and initial angular velocities to 0deg/s
    q0 = np.array([
                    np.radians(135), np.radians(0), 
                    np.radians(135), np.radians(0)
                    ])
    # Set the starting time to 0s
    t0 = 0
    # Set the ending time to 10s
    tf = 10
    # Set the number of iterations to 1000
    nstep = 1000
    # Create the parameter list
    par = [m1, m2, l1, l2, q0, t0, tf, nstep]
```

Otherwise, the function _inputParameters(n)_ is called.

```python
# If the user chose to insert custom parameters 
# Call the inputParameters() function in inputParameters.py module
elif choice == 's':
    par = inputParameters(n)
    m1, m2, l1, l2, q0, t0, tf, nstep = par
```

After that, the equations of motion are integrated using the _RungeKutta4(f, par)_ function

```python
# Integrate the equation of motion using the RungeKutta4() function in rungeKutta4.py module
# Arguments passed to the function are:
# 1) the double pendulum equation of motion from the equationsMotion.py module
# 2) the parameters list
q, t, h = RungeKutta4(doublePendulumEq, par)
```

Then, the kinetic, potential and totale energy are computed using the _simplePendulumEnergy(q, par)_ function

```python
# Compute the kinetic, potential and total energy 
# through the doublePendulumEnergy() function in computeEnergy.py module
E, U, T = doublePendulumEnergy(q, par)
```

Moving forward, the (x, y) coordinates are computed by using the _computeCoordinates(n, q, par)_ function

```python
# Compute the cartesian (x, y) coordinates from the generalized coordinates q (i.e. angular positions)
# using the computeCoordinates() function in computeCoordinates.py module
x, y = computeCoordinates(n, q, par)
```

At this point, the user is asked to choose whether to display static or animated figures

```python
# Let the user decide whether to plot static figures or animated figures
print('\nInsert 0 for static plots')
print('Insert 1 to see animations\n')
mode = int(input(''))
```

If static figures has been chosen, then the figure, axes, plots and legends are created

```python
# Create the figure and the axes using the staticFigure() function in the figureSetup.py module
fig, ax1, ax2, ax3 = staticFigure(n, q, par)

# Plot the pendulum trajectory
ax1.plot(x[:,0], y[:,0], '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
ax1.plot(x[:,1], y[:,1], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory') 

# Plot the theta trend over time
ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
ax2.plot(t, q[:,2], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
        
# Plot the omega trend over time
ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
ax3.plot(t, q[:,3], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')

# Add a legend to the figures using the addLegend() function in the figureSetup.py module
addLegend(n, ax1, ax2, ax3)
```

Otherwise, figure and axes are created, along with all the elements needed to provide an animation as output

```python
# Create the figure and the axes using the animatedFigure() function in the figureSetup.py module
fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

# Create the fixed point and the pendulum mass points as empty plots (they will be animated!)
pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
pendulumMass2, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m2)
masses = [pendulumMass0, pendulumMass1, pendulumMass2]

# Create the pendulum ropes as an empy plot (they will be animated!)
pendulumSegments, = ax1.plot([], [], '-', lw=2, color = '#000000')

# Create the pendulum trace of the trajectory as an empty plot (it will be animated!)
pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
pendulumTraces = [pendulumTrace1, pendulumTrace2]

# Create the theta trend over time trace as an empy plot (it will be animated!)
thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
thetaTraces = [thetaTrace1, thetaTrace2]

# Create the omega trend over time trace as an empy plot (it will be animated!)
omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
omegaTraces = [omegaTrace1, omegaTrace2]

# Add a legend to the figures using the addLegend() function in the figureSetup.py module
addLegend(n, ax1, ax2, ax3)

# Create the template and the text in which time will be displayed and updated each iteration
time_template = 'time = %.1fs'
time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

# Create the template and the text in which the total energy of the system will be displayed and updated each iteration
totalEnergy_template = 'total energy = %.2f J'
totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

texts = [time_template, time_text, totalEnergy_template, totalEnergy_text]

# Create the kinetic energy bar
rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
ax4.add_patch(rect1)

# Create the potential energy bar
rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
ax5.add_patch(rect2)
        
# Animate the plots using functions in the animationModule.py module
anim1 = animation.FuncAnimation(fig, doublePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTraces, masses, pendulumSegments, texts, T, h], interval=h, blit=True)
anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
anim4 = animation.FuncAnimation(fig, doublePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTraces], interval=h, blit=True)
anim5 = animation.FuncAnimation(fig, doublePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTraces], interval=h, blit=True)
```

### [triplePendulum.py](./triplePendulum.py)

The [triplePendulum.py](./triplePendulum.py) module basically uses all the modules shown above to produce all the relevant informations about the triple pendulum motion. 

Initially, the user is asked whether to use default parameters or to choose each value of such parameters:

```python
# Let the user decide whether to use deafult parameters or to insert custom parameters
print('Insert "d" to choose default parameters\n')
print('Insert "s" to input your parameters\n')
choice = str(input(''))
```

If the user chooses to utilize default values for the parameters of the system, then such parameters are set to those default values

```python
# If the user chose to use default parameters
# Set the default parameters
if choice == 'd':
# Set the points mass to 1kg
    m1 = 1
    m2 = 1
    m3 = 1
    # Set the ropes length to 1m
    l1 = 1
    l2 = 1
    l3 = 1
    # Set the initial angles to 135deg and initial angular velocities to 0deg/s
    q0 = np.array([
                    np.radians(135), np.radians(0), 
                    np.radians(135), np.radians(0), 
                    np.radians(135), np.radians(0)
                    ])
    # Set the starting time to 0s
    t0 = 0
    # Set the ending time to 10s
    tf = 10
    # Set the number of iterations to 1000
    nstep = 1000

    # Create the parameter list
    par = [m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep]
```

Otherwise, the function _inputParameters(n)_ is called.

```python
# If the user chose to insert custom parameters 
# Call the inputParameters() function in inputParameters.py module
elif choice == 's':
    par = inputParameters(n)
    m1, m2, m3, l1, l2, l3, q0, t0, tf, nstep = par
```

After that, the equations of motion are integrated using the _RungeKutta4(f, par)_ function

```python
# Integrate the equation of motion using the RungeKutta4() function in rungeKutta4.py module
# Arguments passed to the function are:
# 1) the triple pendulum equation of motion from the equationsMotion.py module
# 2) the parameters list
q, t, h = RungeKutta4(triplePendulumEq, par)
```

Then, the kinetic, potential and totale energy are computed using the _simplePendulumEnergy(q, par)_ function

```python
# Compute the kinetic, potential and total energy 
# through the triplePendulumEnergy() function in computeEnergy.py module
E, U, T = triplePendulumEnergy(q, par)
```

Moving forward, the (x, y) coordinates are computed by using the _computeCoordinates(n, q, par)_ function

```python
# Compute the cartesian (x, y) coordinates from the generalized coordinates q (i.e. angular positions)
# using the computeCoordinates() function in computeCoordinates.py module
x, y = computeCoordinates(n, q, par)
```

At this point, the user is asked to choose whether to display static or animated figures

```python
# Let the user decide whether to plot static figures or animated figures
print('\nInsert 0 for static plots')
print('Insert 1 to see animations\n')
mode = int(input(''))
```

If static figures has been chosen, then the figure, axes, plots and legends are created

```python
# Create the figure and the axes using the staticFigure() function in the figureSetup.py module
fig, ax1, ax2, ax3 = staticFigure(n, q, par)

# Plot the pendulum trajectory
ax1.plot(x[:,0], y[:,0], '-', lw=2, color = '#047FFF', label = '1st mass trajectory') 
ax1.plot(x[:,1], y[:,1], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
ax1.plot(x[:,2], y[:,2], '-', lw=2, color = '#00C415', label = '3rd mass trajectory') 

# Plot the theta trend over time
ax2.plot(t, q[:,0], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
ax2.plot(t, q[:,2], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
ax2.plot(t, q[:,3], '-', lw=2, color = '#00C415', label = '3rd mass \u03B8(t)')
        
# Plot the omega trend over time
ax3.plot(t, q[:,1], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)') 
ax3.plot(t, q[:,3], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
ax3.plot(t, q[:,5], '-', lw=2, color = '#00C415', label = '3rd mass \u03C9(t)')

# Add a legend to the figures using the addLegend() function in the figureSetup.py module
addLegend(n, ax1, ax2, ax3)
```

Otherwise, figure and axes are created, along with all the elements needed to provide an animation as output

```python
# Create the figure and the axes using the animatedFigure() function in the figureSetup.py module
fig, ax1, ax2, ax3, ax4, ax5 = animatedFigure(n, q, par)

# Create the fixed point and the pendulum mass points as empty plots (they will be animated!)
pendulumMass0, = ax1.plot([], [], 'o', color = '#000000', markersize = 5)
pendulumMass1, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m1)
pendulumMass2, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m2)
pendulumMass3, = ax1.plot([], [], 'o', color = '#000000', markersize = 5+m3)
masses = [pendulumMass0, pendulumMass1, pendulumMass2, pendulumMass3]

# Create the pendulum ropes as an empy plot (they will be animated!)
pendulumSegments, = ax1.plot([], [], '-', lw=2, color = '#000000')

# Create the pendulum trace of the trajectory as an empty plot (it will be animated!)
pendulumTrace1, = ax1.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass trajectory')
pendulumTrace2, = ax1.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass trajectory')
pendulumTrace3, = ax1.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass trajectory')
pendulumTraces = [pendulumTrace1, pendulumTrace2, pendulumTrace3]

# Create the theta trend over time trace as an empy plot (it will be animated!)
thetaTrace1, = ax2.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03B8(t)')
thetaTrace2, = ax2.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03B8(t)')
thetaTrace3, = ax2.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass \u03B8(t)')
thetaTraces = [thetaTrace1, thetaTrace2, thetaTrace3]

# Create the omega trend over time trace as an empy plot (it will be animated!)
omegaTrace1, = ax3.plot([], [], '-', lw=2, color = '#047FFF', label = '1st mass \u03C9(t)')
omegaTrace2, = ax3.plot([], [], '-', lw=2, color = '#FF4B00', label = '2nd mass \u03C9(t)')
omegaTrace3, = ax3.plot([], [], '-', lw=2, color = '#00C415', label = '3rd mass \u03C9(t)')
omegaTraces = [omegaTrace1, omegaTrace2, omegaTrace3]

# Add a legend to the figures using the addLegend() function in the figureSetup.py module
addLegend(n, ax1, ax2, ax3)

# Create the template and the text in which time will be displayed and updated each iteration
time_template = 'time = %.1fs'
time_text = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, weight = 'bold')

# Create the template and the text in which the total energy of the system will be displayed and updated each iteration
totalEnergy_template = 'total energy = %.2f J'
totalEnergy_text = ax1.text(0.05, 0.87, '', transform=ax1.transAxes)

texts = [time_template, time_text, totalEnergy_template, totalEnergy_text]

# Create the kinetic energy bar
rect1 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
ax4.add_patch(rect1)

# Create the potential energy bar
rect2 = plt.Rectangle((0, -1), 1, 1, fill=True, color='white', ec='black')
ax5.add_patch(rect2)
        
# Animate the plots using functions in the animationModule.py module
anim1 = animation.FuncAnimation(fig, doublePendulumAnimation, frames=len(t), fargs=[x, y, pendulumTraces, masses, pendulumSegments, texts, T, h], interval=h, blit=True)
anim2 = animation.FuncAnimation(fig, kineticEnergyAnimation, frames=len(t), fargs=[ax4, E, U], interval=h, blit=True)
anim3 = animation.FuncAnimation(fig, potentialEnergyAnimation, frames=len(t), fargs=[ax5, E, U], interval=h, blit=True)
anim4 = animation.FuncAnimation(fig, doublePendulumTrend, frames=len(t), fargs=['theta', t, q, thetaTraces], interval=h, blit=True)
anim5 = animation.FuncAnimation(fig, doublePendulumTrend, frames=len(t), fargs=['omega', t, q, omegaTraces], interval=h, blit=True)
```

## Figures

### Simple Pendulum

* **STATIC**

    <img src="./Pictures/simplePendulum/simplePendulum_default_static.png" alt="simplePendulum_default_static" width="720">

* **ANIMATED**
  
    ![simplePendulum_default_anim](./Videos/simplePendulum/Gifs/simplePendulum_default.gif)

### Double Pendulum

* **STATIC**

    <img src="./Pictures/doublePendulum/doublePendulum_default_static.png" alt="doublePendulum_default_static" width="720">

* **ANIMATED**
  
    ![doublePendulum_default_anim](./Videos/doublePendulum/Gifs/doublePendulum_default.gif)
    ![doublePendulum_custom1_anim](./Videos/doublePendulum/Gifs/doublePendulum_custom1.gif)
    ![doublePendulum_custom2_anim](./Videos/doublePendulum/Gifs/doublePendulum_custom2.gif)
    ![doublePendulum_custom3_anim](./Videos/doublePendulum/Gifs/doublePendulum_custom3.gif)
    ![doublePendulum_custom4_anim](./Videos/doublePendulum/Gifs/doublePendulum_custom4.gif)
    ![doublePendulum_custom5_anim](./Videos/doublePendulum/Gifs/doublePendulum_custom5.gif)
    ![doublePendulum_custom6_anim](./Videos/doublePendulum/Gifs/doublePendulum_custom6.gif)

### Triple Pendulum

* **STATIC**

    <img src="./Pictures/triplePendulum/triplePendulum_default_static.png" alt="triplePendulum_default_static" width="720">

* **ANIMATED**
  
    ![triplePendulum_default_anim](./Videos/triplePendulum/Gifs/triplePendulum_default.gif)
    ![triplePendulum_custom1_anim](./Videos/triplePendulum/Gifs/triplePendulum_custom1.gif)
    ![triplePendulum_custom2_anim](./Videos/triplePendulum/Gifs/triplePendulum_custom2.gif)
    ![triplePendulum_custom3_anim](./Videos/triplePendulum/Gifs/triplePendulum_custom3.gif)
    ![triplePendulum_custom4_anim](./Videos/triplePendulum/Gifs/triplePendulum_custom4.gif)
    ![triplePendulum_custom5_anim](./Videos/triplePendulum/Gifs/triplePendulum_custom5.gif)
    ![triplePendulum_custom6_anim](./Videos/triplePendulum/Gifs/triplePendulum_custom6.gif)

