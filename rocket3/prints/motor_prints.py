import numpy as np

class motor_prints_3dof():
    """
    
    This class holds the printing methods
    of the motor class

    Attributes
    ----------
    motor_prints_3dof.motor : motor_3dof
        Instance of motor_3dof, with which the prints are 
        obtained.
    """
    def __init__(self, motor) -> None:
        """
        Parameters
        ---------
        motor : motor_3dof
            Instance of motor_3dof, that will be used to 
            obtain the prints
        """
        self.motor = motor
    
    def thrust_info(self):
        """
        Prints the most relevant information of the thrust curve of the rocket
        """

        max_index = np.argmax(self.motor.thrust_array)
        max_thrust = self.motor.thrust_array[max_index]
        time_for_max = self.motor.t_array[max_index]
        print(f"Maximum thrust: {max_thrust} at time: {time_for_max}")
        
    def all(self) -> None:
        """
        prints all the methods in the motor_prints_3dof class
        """
        self.thrust_info()