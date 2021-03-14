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

The [rungeKutta4.py](./rungeKutta4.py) module contains the _RungeKutta4(f, par)_ function

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


### [computeCoordinates.py](./computeCoordinates.py)

coming soon...

### [computeEnergy.py](./computeEnergy.py)

coming soon...

### [figureSetup.py](./figureSetup.py)

coming soon...

### [animationModule.py](./animationModule.py)

coming soon...

### [simplePendulum.py](./simplePendulum.py)

coming soon...

### [doublePendulum.py](./doublePendulum.py)

coming soon...

### [triplePendulum.py](./triplePendulum.py)

coming soon...

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

