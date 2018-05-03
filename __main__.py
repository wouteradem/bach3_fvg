import numpy as np
from model.Orbit import Orbit
from model.Hernquist import Hernquist

if __name__ == '__main__':

    state_0 = np.array([0.5, 1.5])

    # Step 1.
    model = Hernquist()

    # Step 2 & 3.
    orbit = Orbit(state_0, model)
    #print("Peri centre = {}".format(orbit.radius_peri))
    #print("Apo centre = {}".format(orbit.radius_apo))
    #print("Energy = {}".format(orbit.energy))
    #print("Momentum = {}".format(orbit.momentum))
    #print("Peri and Apo centre = {}".format(orbit.get_radii()))
    #print("Radial period = {}".format(orbit.radial_period))
    #print(orbit.solution_orbit())

    # Step 4.
    #orbit.interpolation()

    # Step 5.
    print(orbit.mass_increment())

    # Step 6.

    # Step 7.
