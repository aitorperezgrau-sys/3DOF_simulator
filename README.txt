
INTRODUCITON
this python library is a prepartion of Aitor Pérez Grau
for the interview on the 6th of August for a software engineer
mission analysis intership at RFA. 


THEORETICAL DEVELOPMENT
The intertial frame used will be the East-North-up (ENU) frame
also known as local tangent plane. 

A 3DOF simulation treats the rocket as a point mass: there are 3 forces
acting on the body, aerodynamic drag, thurst and gravity. 
In 6DOF simulations there is also a body frame, because it is necessary 
to model rotations, torques and attitudes. 

Aerodynamic drag: rho(z), the expression is 1/2*rho*Cs*v^2
    it changes as a function of the altitude,  then a function must be developed
    the drag coefficient is a constatn
    the velocity depends on the previous iteration
    aerodynamic drag points opposite to the velocity vector

Thurst: thrust is given as a function of time, given a .eng file, which is the 
industry standard for rocket thurst, make an interpolation. time starts from 0

gravity: 
    mass: 
        The total mass of the rocket is the sum of the dry mass (without the fuel) and
        fuel mass. As the fuel burns the fuel mass decreases and so does the total mass.
        The burning rate is assumed to be constant meaning, the mass of fuel burned is constant
        for the entire burning time. 

The basic use of the library is the following
    1. atmosphere is initialized
    2. motor is initialized
    3. rocket_3dof is initialized
    4. motor is added to the rocket
    5. initialize the fight_3dof class with the rocket_3dof object
    6. use the simulate method from the fight_3dof object to perform the simulation 
    7. perfrom an analysis of the flight using all_info and export the data using export_trajectory


NOTES

At lauch site, the x,y,z values are considered to be 0. This is done to make the 
results of the simulation user friendly.
since the use of 3dof simulation entails that a small amount of inputs are required, 
it has been chosen a simple approach to make the code user-friednly 

PYTHON DEVELOPMENT
this library is based on a OOP programming style which includes a high modularity and 
composition. 
The interpolation is based on numpy method interp with anonymous (lambda) functions
the use of other interpolators was discarded since the initial values returned were wrong.



# Getting Started

## Quick Installation

TYPICAL WORKFLOW: 
It starts by importing the necessary classes to perform the simulation

```python
from rocketpy import atmosphere, rocket_3dof, motor_3dof, flight_3dof
```

then we go to step 1, initialize the atmosphere
```python
example_atm = atmosphere()
```
a motor can be created with the following code:
```python
example_motor = motor_3dof(thrust = 1100 , burn_out_time = 6, name = 'constant_thrust')
```

then we must initialize the rocket

```python
example_rocket_3dof = rocket_3dof(
    dry_mass = 14.035, 
    fuel_mass = 3.095,
    drag_coefficient = 0.75, 
    radius = 0.057,
    )
```
and add the motor to the rocket

```python
example_rocket_3dof.add_motor(example_motor)
```

know that we have all the classes required to perfom the simulation, we create the flight instance

```python
example_flight_3dof = flight_3dof(
    rocket = test_rocket_3dof,
    atm = test_atm, 
    initial_altitude = 10,
    inclination = 85,
    heading = -15
)
```

To simulate the flight we must call the simulate method of the flight_3dof class

```python
example_flight_3dof.simulate()
```

finally, once the simulation is done we can visualize and print all the results with:

```python
example_flight_3dof.all_info()
```

and export the data with:
```python
example_flight_3dof.export_trajectory('example_flight_3dof.csv')
```

