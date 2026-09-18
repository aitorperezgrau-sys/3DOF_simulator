import numpy as np

from simulator_3dof.simulation.motor import motor_3dof


class rocket_3dof:
    """ "
    This is the class that contains the charactersitics of the rocket to perform
    a 3DOF flight simulation.
    Since it is a 3DOF simulation, the rocket is modelled as a simple point mass
    thus there is no distintion between the center of mass and the center
    of dry mass.


    Attributes
    ----------
    rocket_3dof.mass : float
        Mass of the rocket in kg
    rocket_3dof.off_drag_coefficient: float 
        Drag coefficient when the motor is off. 
    rocket_3dof.on_drag_coefficient: float
        Drag coefficient when the motor is on. 
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
    """

    def __init__(
        self,
        dry_mass: float | int,
        fuel_mass: float | int,
        off_drag_coefficient: float | int,
        on_drag_coefficient: float | int,
        radius: float | int,
        name: str = "3DOF rocket",
    ):
        """
        Parameters
        ---------
        dry_mass : float, int
            Mass of the rocket without the fuel in kg.
        fuel_mass: float, int
            Mass of the fuel in kg.
        off_drag_coefficient : float, int
            Drag coefficient that will be used to calculate 
            aerodynamic drag when the motor is off. 
        on_drag_coefficient: float, int
            Drag coefficient that will be used to calculate
            aerodynamc drag when the motor is on.
        radius: float, int
            radius of the rocket in m.
        """
        self.check_input_parameters(dry_mass, fuel_mass, off_drag_coefficient, on_drag_coefficient, radius, name)
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.off_drag_coefficient = off_drag_coefficient
        self.on_drag_coefficient = on_drag_coefficient
        self.drag_function = None
        self.radius = radius
        self.area = np.pi * (self.radius**2)
        self.name = name
        self.motor = None
        self.mass_func = None
        self.drag_coefficient_list = []
        self.mach_list = []


    def check_input_parameters(
        self,
        dry_mass: float | int,
        fuel_mass: float | int,
        off_drag_coefficient: float | int,
        on_drag_coefficient: float | int,
        radius: float | int,
        name: str,
    ) -> None:
        """
        Auxiliary function used to check the validity of the input parameters
        """
        if not isinstance(dry_mass, (float, int)):
            raise ValueError(
                "The mass of the rocket without the fuel must be a float or int"
            )
        else:
            if dry_mass <= 0:
                raise ValueError(
                    "The mass of the rocket without the fuel must be greater than 0"
                )
        if not isinstance(fuel_mass, (float, int)):
            raise ValueError("The mass of the fule must be a float or int")
        else:
            if fuel_mass <= 0:
                raise ValueError("The mass of the fuel must be greater than 0")
        if not isinstance(off_drag_coefficient, (float, int)):
            raise ValueError("The off drag coeffient of the rocket must be a float or int")
        else:
            if off_drag_coefficient <= 0:
                raise ValueError(
                    "The off drag coefficient of the rocket must be greater than 0"
                )
        if not isinstance(on_drag_coefficient, (float, int)):
            raise ValueError("The on drag coeffient of the rocket must be a float or int")
        else:
            if on_drag_coefficient <= 0:
                raise ValueError(
                    "The on drag coefficient of the rocket must be greater than 0"
                )
        if not isinstance(radius, (float, int)):
            raise ValueError("The radius of the cross section must be a float or in")
        else:
            if radius <= 0:
                raise ValueError("The radius must be greater than 0")
        if not isinstance(name, str):
            raise ValueError("The rocket name must be a str")

    def add_motor(self, motor):
        """
        Adds the motor to the rocket, because it is a 3DOF simulation, there is no
        position to be defined.
        """
        if isinstance(motor, motor_3dof):
            self.motor = motor
        else:
            raise ValueError("The motor added must be a motor_3dof instance")

        self.mass_function_definition()

    def mass_function_definition(self) -> None:
        """
        Defines the mass of the rocket as a function of time attribute.

        Returns
        -------
        None
        """
        total_mass = self.dry_mass + self.fuel_mass
        m_list = np.linspace(total_mass, self.dry_mass, len(self.motor.t_motor_list))

        self.mass_func = lambda t: np.interp(
            t,  # current time we want to evaluate at
            self.motor.t_motor_list,
            m_list,
            left=total_mass,  # values before ignition (lower range)
            right=self.dry_mass,  # Values after burnout (upper range)
        )  # kg

    def drag_coeff_function(self, v, t, T):
        """
        Returns the drag coefficient as a function of the velocity and the flight time. 
        Parameters
        ----------
        t: float, int
            Flight time. 
        v: float, int
            Velocity of the rocket (TAS). 
        T: float, int
            Current temperature for the given altitude ICAO

        Returns
        -------
        drag_final: float, int
            Final Drag. 
        """
        
        def drag_by_thrust(drag: float | int, t: float | int) -> float:
            """
            Auxiliary function that adjusts the drag as a consequence of the motor state. 
            
            Parameters
            ----------
            drag: float, int
                Initial drag. 
            t: float, int
                Flight time. 

            Returns
            -------
            drag_post_motor: float, int
                Drag after the adjustment of the motor state. 
            """
            if self.motor.thrust_func(t) > 1e-6:
                drag_post_motor = self.on_drag_coefficient
            else:
                drag_post_motor = drag
            return drag_post_motor

        def drag_by_mach(drag: float | int, v: float | int, T) -> float:
            """
            Auxiliary function that adjusts the drag as a consequence of the velocity. 

            Parameters
            ----------
            drag: float, int
                Drag before adjustment due to velocity
            v: float, int
                Velocity of the rocket (TAS)
            T: float, int
                Current temperature for the given altitude ICAO

            Returns
            -------
            drag_post_v: float, int
                Drag after adjustment due to velocity
            """
            speed_of_sound = np.sqrt(1.4 * 287 * T)
            mach = v / speed_of_sound
            self.mach_list.append(mach)

            if mach >= 1:
                drag_post_v = drag + 0.5
            else:
                drag_post_v = drag
            return drag_post_v
        
        drag_post_motor = drag_by_thrust(self.off_drag_coefficient, t)
        drag_final = drag_by_mach(drag_post_motor, v, T)

        self.drag_coefficient_list.append(drag_final)
        return drag_final







