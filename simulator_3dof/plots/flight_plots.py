import matplotlib.pyplot as plt
import numpy as np


class flight_plots_3dof:
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

        max_z = max(self.flight.z_list) * 1.1
        min_z = min(self.flight.z_list) * 1.1
        max_x = max(self.flight.x_list) * 1.1
        min_x = min(self.flight.x_list) * 1.1
        max_y = max(self.flight.y_list) * 1.1
        min_y = min(self.flight.y_list) * 1.1
        min_xy = min(min_x, min_y)
        max_xy = max(max_x, max_y)

        fig = plt.figure(figsize=(18, 6))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(x, y, z, color="teal", label=self.flight.rocket.name)

        # Labels
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_zlabel("Z (m)")
        ax.set_title("Flight Trajectory")
        ax.set_xlim(min_xy, max_xy)
        ax.set_ylim(min_xy, max_xy)
        ax.set_zlim(min_z, max_z)
        ax.view_init(15, 45)
        ax.set_box_aspect(None, zoom=0.88)
        ax.legend()


    def drag_coefficient(self) -> None:
        """
        Shows the drag graph as a function of time. 
        """
        fig = plt.figure(figsize=(18, 6))
        ax = fig.add_subplot(111)
        label = "Cd" + self.flight.rocket.name
        ax.plot(np.linspace(0, self.flight.impact_t, len(self.flight.rocket.drag_coefficient_list)), self.flight.rocket.drag_coefficient_list, color="darkorange", label=label)

        # labels
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Cd")
        ax.set_title("Drag coefficient vs time")


    def drag_force(self) -> None:
        """
        Shows the drag force magnitude as a function of time. 
        """
        fig = plt.figure(figsize=(18, 6))
        ax = fig.add_subplot(111)
        label = "D" + self.flight.rocket.name
        ax.plot(np.linspace(0, self.flight.impact_t, len(self.flight.rocket.drag_coefficient_list)), self.flight.drag_list, color="steelblue", label=label)

        # labels
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("D (N)")
        ax.set_title("Drag vs time")

    def mach_coefficient(self) -> None:
        """
        Shows the mach as a function of time. 
        """
        fig = plt.figure(figsize=(18, 6))
        ax = fig.add_subplot(111)
        label = "M" + self.flight.rocket.name
        ax.plot(np.linspace(0, self.flight.impact_t, len(self.flight.mach_list)), self.flight.mach_list, color="seagreen", label=label)

        # labels
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("M")
        ax.set_title("Mach vs time")


    def all(self) -> None:
        """
        Prints all the printing methods in the fligth_plots_3dof class
        """

        self.trajectory_3d()
        self.drag_coefficient()
        self.mach_coefficient()
        self.drag_force()
