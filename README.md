# 3DOF Rocket Trajectory Simulator

## Overview

This library provides a user-friendly, highly modular Object-Oriented Programming (OOP) approach to simulating unguided sounding rockets. Since 3DOF simulations require a specific subset of inputs, the architecture was designed to minimize setup time while delivering robust kinematic analysis.

* **Architecture:** Heavily relies on OOP principles, composition, and high modularity.
* **Interpolation:** Utilizes `numpy.interp` with anonymous (lambda) functions for precise data handling. The use of other interpolators was discarded since the initial values returned were inaccurate.
* **Coordinate System:** The simulation uses an East-North-Up (ENU) inertial frame (local tangent plane). For ease of use and user-friendly results, the launch site coordinates (x, y, z) are initialized at 0.

---

## Theoretical Development

A 3-Degree-of-Freedom (3DOF) simulation treats the rocket as a point mass. Unlike 6DOF models—which require a rigid body frame to calculate rotations, torques, and attitudes—there are exactly three primary forces acting on the vehicle in this engine: aerodynamic drag, thrust, and gravity.

### Aerodynamic Drag

Drag points strictly opposite to the velocity vector. The aerodynamic drag force is calculated as:

$$F_{drag} = \frac{1}{2} \rho(z) C_s v^2$$

* $\rho(z)$: Atmospheric density as a function of altitude.
* $C_s$: Drag coefficient (assumed constant).
* $v$: Velocity magnitude, derived from the previous iteration.

### Thrust

Thrust is modeled as a function of time ($t=0$ at ignition). Given a `.eng` file (the industry standard for rocket thrust), the engine performs a direct interpolation to determine the thrust curve.

### Gravity & Mass Variation

The total mass of the vehicle decreases dynamically as propellant is consumed, affecting gravitational acceleration and inertia.

* **Total Mass:** The sum of the dry mass (without fuel) and the fuel mass.

* **Burn Rate:** Assumed to be constant, meaning the mass of the fuel burned is linearly distributed across the entire motor burn time.

---

## Getting Started

### Quick Installation & Workflow

The basic use of the library follows a linear 7-step process. Start by importing the necessary classes from the package to perform the simulation:

```python
from rocket3 import atmosphere, rocket_3dof, motor_3dof, flight_3dof
```

#### Step 1: Initialize the atmosphere

```python
example_atm = atmosphere()
```

#### Step 2: Initialize the motor

```python
example_motor = motor_3dof(thrust=1100, burn_out_time=6, name='constant_thrust')
```

#### Step 3: Initialize the rocket

```python
example_rocket = rocket_3dof(
    dry_mass=14.035, 
    fuel_mass=3.095,
    drag_coefficient=0.75, 
    radius=0.057
)
```

#### Step 4: Add the motor to the rocket

```python
example_rocket.add_motor(example_motor)
```

#### Step 5: Initialize the flight environment

```python
example_flight = flight_3dof(
    rocket=example_rocket,
    atm=example_atm, 
    initial_altitude=10,
    inclination=85,
    heading=-15
)
```

#### Step 6: Execute the simulation loop

```python
example_flight.simulate()
```

#### Step 7: Analyze and export the telemetry data

```python
example_flight.all_info()
example_flight.export_trajectory('example_flight_3dof.csv')
```
