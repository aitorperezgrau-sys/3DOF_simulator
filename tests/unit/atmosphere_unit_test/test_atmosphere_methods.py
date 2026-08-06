import pytest
import numpy as np
from ambiance import Atmosphere
from rocket3.simulation import atmosphere


def test_pressure_density_funct(test_atmosphere):
    z_above_sea_level_list = [0, 81020, 81020 - 1e-10]
    for i in range(10):
        z_above_sea_level_list.append(np.random.uniform(0,80000))

    for z_above_sea_level in z_above_sea_level_list:
        if z_above_sea_level <= 81020 - 1e-8: # upper limit of the model:
            atmosphere_model_instance = Atmosphere(z_above_sea_level)
            rho_model = atmosphere_model_instance.density
            rho_function = test_atmosphere.density_func(z_above_sea_level)
            assert rho_model - 1e-7 <= rho_function <= rho_model + 1e-7
        else:
            with pytest.raises(ValueError):
                test_atmosphere.density_func(z_above_sea_level)




