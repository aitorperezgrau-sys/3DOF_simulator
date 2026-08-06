import matplotlib.pyplot as plt
import numpy as np

class motor_plots_3dof():
    """
    This class holds the plotting methods
    of the motor_3dof class

    Attributes
    ----------
    motor_plots_3dof.motor : motor_3dof
        Instance of motor_3dof, with which the plots are 
        obtained.
    """
    def __init__(self, motor):
        """
        Parameters
        ---------
        motor : motor_3dof
            Instance of motor_3dof, that will be used to 
            obtain the plots
        """
        self.motor = motor

    def thrust_against_time(
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
        # check input parameters
        if not isinstance(extend_lower_bound, bool):
            raise ValueError("extend_lower_bound must be a boolean, True or False")
        if not isinstance(extend_upper_bound, bool):
            raise ValueError("extend_uppper_bound must be a boolean, True or False")
        if not isinstance(real_points, bool):
            raise ValueError("real_points must be a boolean, True or False")
        
        # plot
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111)
        if not real_points:
            if extend_lower_bound and extend_upper_bound: 
                t_min = 0
                t_max = self.motor.t_motor_list[-1] + 1
            elif extend_lower_bound:
                t_min = 0
                t_max = self.motor.t_motor_list[-1]
            else:
                t_min = self.motor.t_motor_list[0]
                t_max = self.motor.t_motor_list[-1]
            
            t_list = np.linspace(t_min, t_max, 1000)
            thrust_list = []
            for t in t_list:
                thrust_list.append(self.motor.thrust_func(t))
        else:
            t_list = self.motor.t_motor_list
            thrust_list = self.motor.thrust_list

        ax.set_title("Thrust against time")
        x_min = t_list[0]
        x_max = t_list[-1]
        ax.plot(t_list, thrust_list, color = "teal", label = self.motor.name)
        ax.set_xlim(left = x_min, right = x_max)
        ax.set_ylim(bottom = 0, top = max(thrust_list) * 1.2)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Thrust (N)")

    def all(self) -> None:
        """
        Plots all the plotting methods in the motor_plots_3dof class
        """
        self.thrust_against_time()

        
    
