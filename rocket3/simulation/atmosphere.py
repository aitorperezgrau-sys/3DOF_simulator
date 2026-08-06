from ambiance import Atmosphere
from scipy.interpolate import interp1d
import numpy as np


class atmosphere():
    """
    Attributes
    ----------
    atmosphere.density_func: interp1d 
        Numpy interpolation function that returns the density for a given
        height above the sea level.
    """
    def __init__(self):
        """
        Initializes the atmosphere
        """
        self.density_function_definition()

    def density_function_definition(self) -> None:
        """
        Defines the function of the density as a function of the heigth above sea level. 
        The upper limit 81020 - 1e-8 because the upper limit of the atmospheric model is 
        81020 and the lower limit is set at 0, both included.  
        Returns
        -------
        None
        """
        z_list = np.linspace(0, 81020 - 1e-8, 10000) # above sea level
        atmosphere_instance = Atmosphere(z_list) # accepts above sea level and accepts numpy matrixes
        rho_list = atmosphere_instance.density
        self.density_func = interp1d(
            z_list, 
            rho_list, 
            kind="linear",
            bounds_error=True  
        )

