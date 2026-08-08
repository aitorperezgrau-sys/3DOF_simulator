from simulator_3dof.simulation.rocket import rocket_3dof
from simulator_3dof.plots.flight_plots import flight_plots_3dof
from simulator_3dof.prints.flight_prints import flight_prints_3dof
import numpy as np
from simulator_3dof.simulation.atmosphere import atmosphere
from scipy.integrate import ode

class flight_3dof():
    """
    This class contains the methods that performs the simulation. 

    Attributes
    ----------
    fligth_3dof.initial_altitude : float
        Initial altitude from which the rocket is launched
    fligth_3dof.rocket : rocket_3dof
        Rocket that will be used to perform the simulation
    fligth_3dof.x : float
        X positon of the rocket relative to the interial frame, defined as
        East-North-up (ENU), lauch site is considered to have x = 0. 
    fligth_3dof.y : float
        Y position of the rocket relative to the interial frame, defined as
        East-North-up (ENU), lauch site is considered to have y = 0. 
    fligth_3dof.z : float
        Z position of the rocket relative to the interial frame, defined as
        East-North-up (ENU) the lauch site is considered to have z = 0. 
    fligth_3dof.vx : float
        Velocity on the x axis of the rocket. 
    fligth_3dof.vy : float
        Velocity on the y axis of the rocket. 
    fligth_3dof.vz : float
        Velocity on the z axis of the rocket. 
    fligth_3dof.u : list
        State vector of the rocket, it contains the x, y and z position
        and vx, vy, vz. 
    fligth_3dof.apogee_z : float
        Z value in the intertial frame in which the apogee has been achieved. 
    fligth_3dof.apogee_t : float
        Time from the begging of the simulation at which the apogee was detected
    fligth_3dof.impact_elevation : float | int
        Elevation above the sea level, in which the rocket is assumed to impact. 
    fligth_3dof.impact_downrange : list
        Distance from the origin in the xy plane, when the rocket has impacted
    fligth_3dof.impact_t : float
        Time from the begging of the simulation at which the impact was detected
    """
    
    def __init__(
            self, 
            rocket: rocket_3dof, 
            atm: atmosphere,
            initial_altitude: float | int, 
            inclination: float | int = 80, 
            heading: float | int = 90,
            impact_elevation: float | int = 0
    ):
        """
        rocket : rocket_3dof
            Rocket instance that the simulation will use
        initial_altitude : float, int
            Rocket true height Above Sea Level
        inclination : float, int, optional
            Rocket"s initial position relative to the ground
            given in degrees. Angle from the xy plane
            to the z axis. 90 degrees means that it is in the z axis.
            Default is 80 degrees. 
        heading : float, int, optional
            Rocket"s initial position relative to north 
            given in degrees. It is positive from the north (y)
            to the east (x). Default is 90, meaning, in the x direciton
        impact_elevation: float, int, optional
            Landing elevation of the rocket in m. Default value is 0 above the sea level
        """
        # check inpu parameters 
        self.check_input_parameters(rocket, atm, initial_altitude, inclination, heading, impact_elevation)
        self.rocket = rocket
        self.atm = atm
        self.initial_altitude = initial_altitude # m
        self.inclination = inclination * (np.pi / 180) # rad
        self.heading = heading * (np.pi / 180) # rad
        self.impact_elevation = impact_elevation # m

        # plots and print attributes
        self.plots = flight_plots_3dof(self)
        self.prints = flight_prints_3dof(self)

        # initialization of flight variables
        self.u = [0, 0, 1e-3, 0, 0, 0]
        self.us =[]
        self.us.append(self.u)
        self.dt = 0.001
        self.ts = [0]
        self.apogee_t = None
        self.apogee_z = None

    def check_input_parameters(
            self, 
            rocket: rocket_3dof,
            atm: atmosphere, 
            initial_altitude: float | int, 
            inclination: float | int, 
            heading: float | int,
            impact_elevation : float | int
    ) -> None:
        """
        Auxiliary function used to check the validity of the input parameters

        Returns
        -------
        None
        """
        if not isinstance(rocket, rocket_3dof): 
            raise ValueError("The rocket parameter must be a rocket_3dof instance")
        if not isinstance(atm, atmosphere):
            raise ValueError("The atm parameter must be a atmosphere instance")
        if isinstance(initial_altitude, (float, int)):
            if initial_altitude < 0:
                raise ValueError("The initial altitude above the sea level must be greater than 0")
            elif initial_altitude > 81020 - 1e-6:
                raise ValueError("The initial altitude cannot be greater or equal than 81020 m above sea level")
        else: 
            raise ValueError("The initial altitude above the sea level must be a float or int")
        if not isinstance(inclination, (float, int)):
            raise ValueError("The inclination must be a float or int")
        if not isinstance(heading, (float, int)):
            raise ValueError("The heading must be a float or int")
        if isinstance(impact_elevation, (float, int)):
            if impact_elevation < 0:
                raise ValueError("The impact altitude above the sea level must be greater than 0")
            elif impact_elevation > 81020 - 1e-6:
                raise ValueError("The impact altitude cannot be greater or equal than 81020 m above sea level")
        else: 
            raise ValueError("The impact altitude above the sea level must be a float or int")
    

    def simulate(self):
        """
        Function that starts the simulation
        """
        self.solver = ode(self._diff_equation)
        self.solver.set_integrator("lsoda")
        self.solver.set_initial_value(self.u, 0)

        finish = False
        while self.solver.successful() and not finish:
            self.solver.integrate(self.solver.t + self.dt)
            if self.solver.y[5] < 0 and self.apogee_t is None and self.solver.t > 0.5:
                self.apogee_u = self.solver.y
                self.apogee_z = self.apogee_u[2]
                self.apogee_t = self.solver.t
            self.u = self.solver.y
            self.x, self.y, self.z, self.vx, self.vy, self.vz = self.u
            self.us.append(self.u)
            self.t = self.solver.t
            self.ts.append(self.solver.t)
            if self.solver.y[2] + self.initial_altitude <= self.impact_elevation and self.solver.y[5] < 0 and self.solver.t > 0.5:
                finish = True
        last_u = self.us[-1]
        self.impact_downrange =  np.sqrt(last_u[0]**2 + last_u[1]**2)
        self.impact_t = self.ts[-1]
        self.us = np.array(self.us)
        self.x_list = list(self.us[:, 0])
        self.y_list = list(self.us[:, 1])
        self.z_list = list(self.us[:, 2])

    def _diff_equation(self, t, u):
        x, y, z, vx, vy, vz = u

        # due to interpolation variability and bound limits
        z = max(z, 0.0) 
        t = max(t, 0.0)
        v_mag = np.linalg.norm([vx, vy, vz])
        r_t = z + (6.371 * 1e6)

        g_mag = 3.986004418 * 1e14 / (r_t ** 2)
        gravity_array = np.array([0, 0, - g_mag]) 
        current_mass = self.rocket.mass_func(t)
        
        if t < 0.5: # --- rail phase ---
            heading = self.heading
            inclination = self.inclination
            
            rail_direction = np.array([
                np.cos(inclination) * np.sin(heading),
                np.cos(heading) * np.cos(inclination),
                np.sin(inclination) # align in the rail direciton
            ])
            rail_force = self.rocket.mass_func(t) * g_mag * np.sin(inclination) # force that the rail generates on the point mass rocket
            rail_accel_array = rail_force / self.rocket.mass_func(t) * rail_direction
            aero_drag = 0.5 * self.atm.density_func(z) * (v_mag**2) * self.rocket.drag_coefficient * self.rocket.area
            aero_accel_array = ( - aero_drag / current_mass) * rail_direction
            thrust_accel_array = (self.rocket.motor.thrust_func(t) / current_mass) * rail_direction
            ax, ay, az = thrust_accel_array + gravity_array + aero_accel_array + rail_accel_array
            
        else: # --- flight phase ---
            vel_dir = np.array([vx, vy, vz]) / v_mag # align in the rocket direction
            aero_drag = 0.5 * self.atm.density_func(z) * (v_mag**2) * self.rocket.drag_coefficient * self.rocket.area
            aero_accel_array = ( - aero_drag / current_mass) * vel_dir
            thrust_accel_array = (self.rocket.motor.thrust_func(t) / current_mass) * vel_dir
            ax, ay, az = thrust_accel_array + gravity_array + aero_accel_array

        return [vx, vy, vz, ax, ay, az]


    def export_trajectory(self, filename) -> None:
        """
        Creates a csv file with the data of the flight in the directory where the file is
        being executed. It has on the first column the time, and then the x, y, z, and velocities
        vx, vy, vz.
        """
        plot_array = np.column_stack((np.array(self.ts), self.us))
        np.savetxt(filename, plot_array, delimiter=",", header="t (s),      x (m),      y (m),      z (m),      vx (m/s),     vy (m/s),     vz(m/s)", comments="") 


    def draw3d(self) -> None:
        """
        Plots the 3d trajectory of the rocket with 3DOF. 
        """
        self.plots.trajectory()


    def all_info(self) -> None:
        """
        Prints all the relevant information and shows
        all the relevant plots. 
        """
        self.plots.all()
        self.prints.all()



        
