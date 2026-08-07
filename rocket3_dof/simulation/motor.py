import numpy as np
from rocket3_dof.plots.motor_plots import motor_plots_3dof
from rocket3_dof.prints.motor_prints import motor_prints_3dof

class motor_3dof():
    """
    Motor class necessary to perform a 3DOF simulation

    Attributes
    ----------
    motor_3dof.thrust_func: lambda function 
        Tthrust of the motor as a function of the simulation time. 
    motor_3dof.burn_out_time: float
        Time at which the motor no longer provides thrust
    """
    def __init__(
            self, 
            thrust: str | float | int, 
            burn_out_time: float | int = None,
            name: str = "Motor"
    ):
        """
        Initializes the motor class

        Parameters
        ----------
        thurst : float, int, str
            Thurst that the motor of the rocket has.
            The accepted entries are:
            - If a float or in, the thurst is assumed to be constant in N
            - direction of the .eng file, the thurst curve given by this file will be taken
        burn_out_time: float, int, optional
            Time in which the motor will no longer provide thrust in s
            It is a mandatory parameter when thrust is a constant value, otherwise it will be 
            defined as the last time in the .eng file. 
        """
        self.check_input_parameters(thrust, burn_out_time, name)
        self.name = name
        self.thurst_function_definition(thrust, burn_out_time)
        self.plots = motor_plots_3dof(self)
        self.prints = motor_prints_3dof(self)
    

    def check_input_parameters(
            self, 
            thrust: str | float | int, 
            burn_out_time: float | int,
            name: str,
    ) -> None:
        """
        Checks the input parameters of the motor_3dof initialization
        """
        if not isinstance(name, str):
            raise ValueError("The name must be a string")
        if not isinstance(thrust, (float, int, str)):
            raise ValueError("The thurst of the rocket must be a float, int or str")
        else: 
            if isinstance(thrust, (float, int)):
                if thrust > 0:
                    if burn_out_time is None:
                        raise ValueError("Burn time must be defined when the thrust is constant")
                    elif isinstance(burn_out_time, (float, int)):
                        if burn_out_time < 0:
                            raise ValueError("The burn time must be greater than 0")
                    else:
                        raise ValueError("Burn time must be a float or int")
                else:
                    raise ValueError("If constant thrust must be greater than 0")

            
    def thurst_function_definition(self, thrust, burn_out_time) -> None:
        """
        Defines the attribute function of the thrust as a function of the time of the simulation. 
        """
        if isinstance(thrust, (float, int)):
            self.thrust_func = lambda t: thrust if 0 < t <= burn_out_time else 0
            self.t_motor_list = [0, 1e-10, burn_out_time]
            self.thrust_list = [0, thrust, thrust]
            self.t_array = np.array(self.t_motor_list)
            self.thrust_array = np.array(self.thrust_list)
            
        else: 
            try:
                eng_file = open(thrust, "r")
                self.t_motor_list = []
                self.thrust_list = []
                eng_file.readline() # title line
                for raw_line in eng_file:
                    line = raw_line.strip()
                    if not line: 
                        continue
                    try:
                        parts = line.split()
                        if len(parts) != 2:
                            raise ValueError
                        to_append_at_t = float(parts[0])
                        to_append_at_thrust = float(parts[1])
                        
                    except ValueError: 
                        raise ValueError(f"There is a value missing or unreadable at line {len(self.t_motor_list) + 2}: '{line}'")

                    self.t_motor_list.append(to_append_at_t)
                    self.thrust_list.append(to_append_at_thrust)
                
            except FileNotFoundError:
                raise FileNotFoundError(f"The motor file '{thrust}' does not exist.")  
            
            if not self.thrust_list:
                raise ValueError("No thrust data was read from the .eng file.")
                
            self.t_array = np.array(self.t_motor_list)
            self.thrust_array = np.array(self.thrust_list)
            if np.any(self.thrust_array < 0):
                raise ValueError("There is a negative thrust value in the .eng file.")
            if np.any(self.t_array < 0): 
                raise ValueError("There is a negative time value in the .eng file.")
            if np.max(self.thrust_array) == 0.0:
                raise ValueError("Invalid motor data: Maximum thrust must be greater than 0.")

            self.burn_out_time = self.t_motor_list[-1]              
            self.thrust_func = lambda t: np.interp(
                t,                  
                self.t_motor_list,
                self.thrust_list,
                left=0.0,           # Values before ignition 
                right=0.0           # Values after burnout 
            )
                    

    def plot_thrust(
            self, 
            real_points: bool = True,
            extend_lower_bound: bool = True, 
            extend_upper_bound: bool = True,
    ) -> None:
        """
        Plots the thrust of the motor defined through the initialization
        of the motor, as a function of time. 

        Parameters
        ----------
        real_points: bool
            If True the real points will be used instead of iterating through
            the interpolator. Default is True. 
        extend_lower_bound: bool
            Only used if real_points is False
            If extend_upper_bound is True, thrust will be shown from 0,
            instead of the first thrust value. Default is True. 
        extend_upper_bound: bool
            Only used if real_points is False
            If extend_upper_bound is True, thrust plot will be extended
            up to 1 second after the burn_out_time. Default is True.
        """
        self.plots.thrust_against_time(real_points, extend_lower_bound, extend_upper_bound)

    def all_info(self) -> None:
        """
        Prints all the relevant information and shows
        all the relevant plots
        """
        self.plots.all()
        self.prints.all()



        
