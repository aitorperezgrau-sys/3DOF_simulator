from simulator_3dof.simulation.flight import flight_3dof
from simulator_3dof.simulation.rocket import rocket_3dof
import pytest
import numpy as np
from ambiance import Atmosphere


@pytest.mark.parametrize('rocket, initial_altitude, inclination, heading, landing_elevation', [
    (0, 100, 40, 30, 1000),                                         # wrong rocket
    ("test_realistic_rocket_3dof", '100', 40, 30, 1000),            # wrong initial_altitude(str)
    ("test_realistic_rocket_3dof", -1, 40, 30, 1000),               # wrong initial_altitude(-)
    ("test_realistic_rocket_3dof", 81020 - 1e-10, 40, 30, -1),      # wrong initial_altitude(exceed bounds)
    ("test_realistic_rocket_3dof", 10, '40', 30, 0),                # wrong inclination (str)
    ("test_realistic_rocket_3dof", 10, 40, '30', 1000),             # wrong heading (str)
    ("test_realistic_rocket_3dof", 100, 40, 30, '1000'),            # wrong landing_elevation(str)
    ("test_realistic_rocket_3dof", 1, 40, 30, -1),                  # wrong landing_elevation(-)
    ("test_realistic_rocket_3dof", 10, 40, 30, 81020 - 1e-10),      # wrong landing_elevation(exceed bounds)

])
def test_check_flight_input_parameters(request, rocket, initial_altitude, inclination, heading, landing_elevation):
    if isinstance(rocket, str):
        rocket_obj = request.getfixturevalue(rocket)
    else:
        rocket_obj = rocket
    with pytest.raises(ValueError):
        flight_3dof(rocket_obj, initial_altitude, inclination, heading, landing_elevation)



