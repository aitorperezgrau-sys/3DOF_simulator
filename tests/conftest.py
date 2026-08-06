'''
This file contains all the fixures, used for testing
'''

import pytest
from rocket3 import rocket_3dof
from rocket3 import flight_3dof
from rocket3 import motor_3dof
from rocket3 import atmosphere
from rocket3 import flight_plots_3dof
from rocket3 import flight_prints_3dof
from rocket3 import motor_plots_3dof

'''
Definition of the fixtures that can be used in all the directories and subdirectiories
included in the test dictionary
'''


@pytest.fixture(scope = 'function')
def test_atmosphere():
    '''
    atmosphere class. 
    '''
    return atmosphere()
    

@pytest.fixture(scope = 'function')
def test_constant_thrust_motor_3dof():
    '''
    Initializes the test motor with constant thrust
    '''
    return motor_3dof(thrust = 800, burn_out_time = 5, name = 'test_constant_thrust_motor_3dof')


@pytest.fixture(scope = 'function')
def test_file_thrust_motor_3dof():
    '''
    Initializes the test motor with constant thrust
    '''
    return motor_3dof(thrust='/Users/aitorpg/Documents/LEARNING/3DOF_simulator/tests/extra_files/M1128_95.eng', name = 'test_file_thrust_motor_3dof')

@pytest.fixture(scope = 'function')
def test_rocket_3dof(): 
    '''
    Values of mass, radius and are taken from the skybreaker Faraday rocket, 
    with an arbritray drag_coefficiet. 
    '''
    return rocket_3dof(
    dry_mass = 14.035, 
    fuel_mass = 3.095,
    drag_coefficient = 0.75, 
    radius = 0.057,
    name = 'test_rocket_3dof'
    )

@pytest.fixture(scope = 'function')
def test_flight_3dof(test_rocket_3dof, test_atmosphere):
    '''
    test flight class with the test_rocket_3dof fixture
    '''
    test_rocket_3dof.add_motor(test_file_thrust_motor_3dof)
    return flight_3dof(
        rocket = test_rocket_3dof,
        atm = test_atmosphere,
        initial_altitude = 0
        )



@pytest.fixture(scope = 'function')
def test_flight_prints_3dof(test_flight_3dof):
    '''
    test fligth print class
    '''
    return flight_prints_3dof(test_flight_3dof)

@pytest.fixture(scope = 'function')
def test_flight_plots_3dof(test_flight_3dof):
    '''
    test fligth print class
    '''
    return flight_plots_3dof(test_flight_3dof)


