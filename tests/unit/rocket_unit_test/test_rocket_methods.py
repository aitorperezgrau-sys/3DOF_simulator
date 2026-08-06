import pytest
from rocket3.simulation.rocket import rocket_3dof
from rocket3.simulation.motor import motor_3dof
import numpy as np

@pytest.mark.parametrize('dry_mass, fuel_mass, drag_coefficient, radius, name', [
    ('2', 2, 0.3, 1, 'rocket_3dof'),    # wrong mass (str)
    (-3, 2, 0.3, 1, 'rocket_3dof'),     # wrong mass (-)
    (4, '2', 0.3, 1, 'rocket_3dof'),    # wrong fuel_mass (str)
    (3, -2, 0.3, 1, 'rocket_3dof'),     # wrong fuel_mass (-)
    (10, 2, '0.3', 1, 'rocket_3dof'),   # wrong drag_coefficient (str)
    (10, 2, -0.3, 1, 'rocket_3dof'),    # wrong drag_coefficient (-)
    (10, 2, 0.3, '1', 'rocket_3dof'),   # wrong radius (str)
    (10, 2, 0.3, -1, 'rocket_3dof'),    # wrong radius (-)
    (3, 2, 0.3, 1, 10),                 # wrong name (int)
])
def test_rocket_check_input_parameters(dry_mass, fuel_mass, drag_coefficient, radius, name):
    with pytest.raises(ValueError):
        rocket_3dof(dry_mass, fuel_mass, drag_coefficient, radius, name)


@pytest.mark.parametrize("motor",[
        "test_constant_thrust_motor_3dof",
        "test_file_thrust_motor_3dof",
])
def test_bounds_mass_funct(request, motor, test_rocket_3dof):
    '''
    checks the bounds of the mass function
    '''
    motor_obj = request.getfixturevalue(motor)
    test_rocket_3dof.add_motor(motor_obj)
    prev_mass = test_rocket_3dof.dry_mass + test_rocket_3dof.fuel_mass 
    for t in np.linspace(motor_obj.t_motor_list[0], motor_obj.t_motor_list[-1] + 4, 1000):
        current_mass = test_rocket_3dof.mass_func(t)
        if t == motor_obj.t_motor_list[0]:
            assert current_mass == test_rocket_3dof.dry_mass + test_rocket_3dof.fuel_mass 
        elif t > motor_obj.t_motor_list[-1]:
            assert current_mass == test_rocket_3dof.dry_mass
        else:
            assert prev_mass > current_mass
            prev_mass = current_mass

def test_other_attributes(test_rocket_3dof, test_file_thrust_motor_3dof):
    test_rocket_3dof.add_motor(test_file_thrust_motor_3dof)
    assert test_rocket_3dof.name == 'test_rocket_3dof'
    assert isinstance(test_rocket_3dof.motor, motor_3dof)
    
