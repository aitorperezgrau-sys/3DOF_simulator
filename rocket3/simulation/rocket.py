import numpy as np
from rocket3.simulation.motor import motor_3dof

class rocket_3dof():
    ''''
    This is the class that contains the charactersitics of the rocket to perform 
    a 3DOF flight simulation. 
    Since it is a 3DOF simulation, the rocket is modelled as a simple point mass
    thus there is no distintion between the center of mass and the center 
    of dry mass. 

    
    Attributes
    ----------
    rocket_3dof.mass : float
        Mass of the rocket in kg
    rocket_3dof.drag_coefficient : float 
        Drag coefficient that used to calculate the 
        aerodynamic drag. 
    rocket_3dof.dry_mass : float 
        Mass of the rocket in kg without the fuel. 
    rocket_3dof.fuel_mass : float 
        Mass of the fuel of the rocket in kg.
    rocket_3dof.radius : float 
        Radius of the rocket in m.   
    rocket_3dof.area : float 
        Area of the rocket in m^2.  
    rocket_3dof.thrust : float 
        Thrust of the rocket as a function of time. 
    '''
    

    def __init__(
            self, 
            dry_mass: float | int,
            fuel_mass: float | int,
            drag_coefficient: float | int, 
            radius: float | int,                
            name : str = '3DOF rocket'
    ):
        '''
        Parameters
        ---------
        dry_mass : float, int
            Mass of the rocket without the fuel in kg. 
        fuel_mass: float, int
            Mass of the fuel in kg.
        drag_coefficient : float, int
            Drag coefficient that will be used to calculate the 
            aerodynamic drag.
        radius: float, int
            radius of the rocket in m. 
        '''
        self.check_input_parameters(dry_mass, fuel_mass, drag_coefficient, radius, name)
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.drag_coefficient = drag_coefficient
        self.radius = radius
        self.area = np.pi * (self.radius ** 2)
        self.name = name

    def check_input_parameters(
            self, 
            dry_mass: float | int, 
            fuel_mass: float | int, 
            drag_coefficient: float | int, 
            radius: float | int, 
            name: str
    ) -> None:
        '''
        Auxiliary function used to check the validity of the input parameters
        '''
        if not isinstance(dry_mass, (float, int)):
            raise ValueError('The mass of the rocket without the fuel must be a float or int')
        else:
            if dry_mass <= 0:
                raise ValueError('The mass of the rocket without the fuel must be greater than 0')
        if not isinstance(fuel_mass, (float, int)):
            raise ValueError('The mass of the fule must be a float or int')
        else:
            if fuel_mass <= 0:
                raise ValueError('The mass of the fuel must be greater than 0')
        if not isinstance(drag_coefficient, (float, int)):
            raise ValueError('The drag coeffient of the rocket must be a float or int')
        else:
            if drag_coefficient <= 0:
                raise ValueError('The drag coefficient of the rocket must be greater than 0')
        if not isinstance(radius, (float, int)):
            raise ValueError('The radius of the cross section must be a float or in')
        else:
            if radius <= 0:
                raise ValueError('The radius must be greater than 0')
        if not isinstance(name, str):
            raise ValueError('The rocket name must be a str')
    

    def add_motor(self, motor):
        '''
        Adds the motor to the rocket, because it is a 3DOF simulation, there is no 
        position to be defined. 
        '''
        if isinstance(motor, motor_3dof):
            self.motor = motor
        else: 
            raise ValueError('The motor added must be a motor_3dof instance')
        
        self.mass_function_definition()


    def mass_function_definition(self) -> None:
        '''
        Defines the mass of the rocket as a function of time attribute. 

        Returns
        -------
        None
        '''
        total_mass = self.dry_mass + self.fuel_mass
        m_list = np.linspace(total_mass, self.dry_mass, len(self.motor.t_motor_list))
        
        self.mass_func = lambda t: np.interp(
            t,                        # current time we want to evaluate at
            self.motor.t_motor_list,              
            m_list,                          
            left=total_mass,          # values before ignition (lower range)
            right=self.dry_mass       # Values after burnout (upper range)
        ) # kg
