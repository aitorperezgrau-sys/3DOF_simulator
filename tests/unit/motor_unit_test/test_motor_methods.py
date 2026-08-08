import pytest
from simulator_3dof.simulation.motor import motor_3dof
from simulator_3dof.plots import motor_plots_3dof
import numpy as np


@pytest.mark.parametrize('thrust, burn_out_time', [
    (-700, 3),     # wrong thrust (-)
    (700, None),   # wrong burn_out_time (not defined)
    (700, -3),     # wrong burn_out_time (-)
    (700, '0'),    # wrong burn_out_time (str)
])
def test_rocket_check_input_parameters(thrust, burn_out_time):
    with pytest.raises(ValueError):
        motor_3dof(thrust, burn_out_time)



@pytest.mark.parametrize("motor",[
        "test_constant_thrust_motor_3dof",
        "test_file_thrust_motor_3dof",
])
def test_bouns_thrust_func(request, motor):
    '''
    checks the upper bound of the thrust function
    '''
    motor_obj = request.getfixturevalue(motor)
    for t in np.linspace(0, motor_obj.t_motor_list[-1] + 4, 1000):
        if t < motor_obj.t_motor_list[0]:
            assert motor_obj.thrust_func(t) == 0
        if t > motor_obj.t_motor_list[-1]:
            assert motor_obj.thrust_func(t) == 0


@pytest.mark.parametrize('thrust', [
    0,                                                                                          # zero
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/no_lines.eng',          # no thrust readings in file
    - 400,                                                                                      # negative thrust
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/negative_thrust.eng',   # negative thrust in file
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/negative_time.eng',     # negative time in file
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/empty_spaces.eng',      # empty spaces
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/string.eng',            # string
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/several_values.eng',    # several values in one line
    '/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/zeros_file.eng',        # thrust values are 0
])
def test_0_thrust_func(thrust):
    '''
    Check 0 thrust because when thrust = 0, is passed as a constant
    value, or no lines are present in the .eng file, the initialization raises 
    ValueError.  
    '''
    with pytest.raises(ValueError):
        motor_3dof(thrust, 8)

def test_other_attributes(test_file_thrust_motor_3dof):
    assert test_file_thrust_motor_3dof.name == 'test_file_thrust_motor_3dof'
    assert isinstance(test_file_thrust_motor_3dof.plots, motor_plots_3dof)
    

