import matplotlib.pyplot as plt
import numpy as np

class flight_plots_3dof():
    """
    This class holds the plotting methods
    of the flight class

    Attributes
    ----------
    flight_plots_3dof.flight : flight_3dof
        Instance of flight_3dof, with which the plots are 
        obtained.
    """
    def __init__(self, flight):
        """
        Parameters
        ---------
        flight : flight_3dof
            Instance of flight_3dof, that will be used to 
            obtain the plots
        """
        self.flight = flight
    

    def trajectory_3d(self) -> None:
        """
        Shows the trajectory of the flight
        """
        x = self.flight.x_list
        y = self.flight.y_list
        z = self.flight.z_list

        max_z = max(self.flight.z_list)
        min_z = min(self.flight.z_list)
        max_x = max(self.flight.x_list)
        min_x = min(self.flight.x_list)
        max_y = max(self.flight.y_list)
        min_y = min(self.flight.y_list)
        min_xy = min(min_x, min_y)
        max_xy = max(max_x, max_y)

        fig = plt.figure(figsize=(18,6))
        ax = fig.add_subplot(111, projection = "3d")
        ax.plot(x, y, z, color = "teal", label = self.flight.rocket.name)

        # Labels 
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_zlabel("Z (m)")
        ax.set_title("Flight Trajectory")
        ax.set_xlim(min_xy, max_xy)
        ax.set_ylim(min_xy, max_xy)
        ax.set_zlim(min_z, max_z)
        ax.view_init(15, 45)
        ax.set_box_aspect(None, zoom=0.95) 
        ax.legend()

    def all(self) -> None:
        """
        Prints all the printing methods in the fligth_plots_3dof class
        """

        self.trajectory_3d()