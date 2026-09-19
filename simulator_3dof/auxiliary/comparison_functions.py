import matplotlib.pyplot as plt
from simulator_3dof.auxiliary.read_class import flight_reader



def flight_comparison(trajectories: list) -> None:
    """Generates a plot of the trajectory given
    
    Parameters
    ----------
    trajectories: lists
        Set of the path trajectories to be plotted
    """

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for path_trajectory in trajectories:
        trajectory_reader = flight_reader(path_trajectory)
        variables = trajectory_reader.create_lists(False, True, True, True, False, False, False)
        x_list = variables[0]
        y_list = variables[1]
        z_list = variables[2]
        ax.plot(x_list, y_list, z_list, label=path_trajectory.split('/')[-1])

    ax.set_title('3DOF Rocket Trajectory Comparison')
    ax.set_xlabel('X  (m)')
    ax.set_ylabel('Y  (m)')
    ax.set_zlabel('Z  (m)')
    ax.view_init(elev=50, azim = 40)
    ax.legend()

    plt.show()

def axis_comparison(x_list_values: list, y_list_values: list, title: str, y_label: str, legend: list) -> None:
    """Generates a plot containing several axis values for the values given in the list
    Parameters
    ----------
    x_list_values: list
        List containg the x values to be plotted
    y_list_values: list
        List containg the y values to be plotted
    title: str
        Title of the graph
    y_label: str
        Label in the y axis
    legend: list
        List of the names of each axis
    """

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    for y_values, x_values, label in zip(y_list_values, x_list_values, legend):
        ax.plot(x_values, y_values, label=label)

    ax.set_title(title)
    ax.set_xlabel('T  (s)')
    ax.set_ylabel(y_label)
    ax.legend()