import numpy as np
import pandas as pd


class flight_reader:
    """This function allows to read a given flight with the structure:
    X (m),      Y (m),      Z (m),      Vx (m/s),     Vy (m/s),     Vz(m/s)
    and enables the creation of a list for all values. Path given as a string
    """

    def __init__(self, path):
        """
        Parameters:
        ----------
        path: str
            Path of the file we want to read.
        """
        self.check_input_parameters(path)
        self.path = path
        self.t_final = None

    def check_input_parameters(self, path):
        """
        Checks that input parameter is a string
        """
        if not isinstance(path, str):
            raise ValueError("Path given must be a string")

    def create_lists(
        self,
        is_t: bool = True,
        is_x: bool = True,
        is_y: bool = True,
        is_z: bool = True,
        is_vx: bool = True,
        is_vy: bool = True,
        is_vz: bool = True,
        is_ax: bool = True,
        is_ay: bool = True,
        is_az: bool = True,
    ) -> list:
        """
        This method returns the desired variables between T, X, Y, Z, Vx, Vy, Vz, Ax, Ay, Az of the rocket trajectory.

        Parameters
        ---------
        is_t, bool
            True if the Time list is wanted to be returned.
        is_x, bool
            True if the X list is wanted to be returned.
        is_y, bool
            True if the Y list is wanted to be returned.
        is_z, bool
            True if the Z list is wanted to be returned.
        is_vx, bool
            True if the Vx list is wanted to be returned.
        is_vy, bool
            True if the Vy list is wanted to be returned.
        is_vz, bool
            True if the Vz list is wanted to be returned.
        is_ax, bool
            True if the Ax list is wanted to be returned.
        is_ay, bool
            True if the Ay list is wanted to be returned.
        is_az, bool
            True if the Az list is wanted to be returned.
        Returns
        -------
        variables: list
            Returns a list containing the desired lists.
        """

        def from_v_to_a(v_list):
            """
            Generates the list of accelerations for the given list of velocities

            Parameters
            ----------
            v_list: list
                List of velocities to be differentiated.

            Returns
            -------
            a_list: list
                List of the accelerations for the given velocities
            """
            a_list = [None] * len(v_list)
            t_list = np.linspace(0, self.t_final, len(v_list))
            for i in range(len(v_list) - 1):
                a_list[i] = (v_list[i + 1] - v_list[i]) / (t_list[i + 1] - t_list[i])
            a_list[-1] = a_list[-2]

            return a_list

        variables = []
        try:
            p_file = pd.read_csv(self.path)
            p_file.columns = p_file.columns.str.lstrip("#").str.strip()
            p_file.columns = p_file.columns.str.lower()

            if is_t:
                t_list = p_file["time (s)"].tolist()
                variables.append(t_list)
                self.t_final = t_list[-1]
                print(self.t_final)
            if is_x:
                x_list = p_file["x (m)"].tolist()
                variables.append(x_list)
            if is_y:
                y_list = p_file["y (m)"].tolist()
                variables.append(y_list)
            if is_z:
                z_list = p_file["z (m)"].tolist()
                variables.append(z_list)
            if is_vx:
                vx_list = p_file["vx (m/s)"].tolist()
                variables.append(vx_list)
            if is_vy:
                vy_list = p_file["vy (m/s)"].tolist()
                variables.append(vy_list)
            if is_vz:
                vz_list = p_file["vz (m/s)"].tolist()
                variables.append(vz_list)
            if is_ax:
                try:
                    ax_list = p_file["ax (m/s^2)"].tolist()
                except KeyError:
                    try:
                        ax_list = from_v_to_a(vx_list)
                    except NameError:
                        vx_list = p_file["vx (m/s)"].tolist()
                        ax_list = from_v_to_a(vx_list)
                variables.append(ax_list)

            if is_ay:
                try:
                    ay_list = p_file["ay (m/s^2)"].tolist()
                except KeyError:
                    try:
                        ay_list = from_v_to_a(vy_list)
                    except NameError:
                        vy_list = p_file["vy (m/s)"].tolist()
                        ay_list = from_v_to_a(vy_list)
                variables.append(ay_list)

            if is_az:
                try:
                    az_list = p_file["az (m/s^2)"].tolist()
                except KeyError:
                    try:
                        az_list = from_v_to_a(vz_list)
                    except NameError:
                        vz_list = p_file["vz (m/s)"].tolist()
                        az_list = from_v_to_a(vz_list)
                variables.append(az_list)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"The trajectory file '{self.path}' does not exist."
            ) from None

        return variables
