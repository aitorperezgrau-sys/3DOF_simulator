from rocketpy import Environment
from rocketpy import PointMassMotor
from rocketpy import PointMassRocket
from rocketpy.simulation import FlightDataExporter

env = Environment(
    latitude=32.990254,
    longitude=-106.974998,
    elevation=10
)

env.set_atmospheric_model(type="standard_atmosphere")

# Using a thrust curve file
motor = PointMassMotor(
    thrust_source=800,
    dry_mass= 3.6599000000000004,
    propellant_initial_mass = 3.095,
    burn_time = 6
)

rocket = PointMassRocket(
    radius=0.057,  # meters
    mass=10.385,  # kg (dry mass without motor)
    center_of_mass_without_motor=0.0,
    power_off_drag=0.75,  # Constant drag coefficient
    power_on_drag=0.75,
)

rocket.add_motor(motor, position = 0)


from rocketpy import Flight

flight = Flight(
    rocket=rocket,
    environment=env,
    rail_length=5,
    inclination=85,  
    heading= -15,  
    simulation_mode="3 DOF",
    terminate_on_apogee=False,
)

# show results
flight.prints.apogee_conditions()
flight.prints.impact_conditions()
flight.plots.trajectory_3d()

# export data
exporter = FlightDataExporter(flight)
exporter.export_data(
    "rocketpy_trajectory_3dof.csv",
    "x",
    "y",
    "z",
    "vx",
    "vy",
    "vz",
)