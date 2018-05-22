import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from model.Orbit import Orbit
from model.Hernquist import Hernquist


if __name__ == '__main__':

    # Sets print options.
    np.set_printoptions(suppress=True)
    model = Hernquist()
    choice = raw_input("Test or not to test?(y/n):")
    if choice == "y":

        # r_peri and r_apo can be changed here.
        state_0 = np.array([0., 0.])

        # Step 2 & 3.
        orbit = Orbit(state_0, model)
        print("Peri centre = {}".format(orbit.radius_peri))
        print("Apo centre = {}".format(orbit.radius_apo))
        print("Energy = {}".format(orbit.energy))
        print("Momentum = {}".format(orbit.momentum))
        print("Radial period = {}".format(orbit.radial_period))
        print("Orbit ODE = {}".orbit.solution_orbit())
    elif choice == "n":

        # Step 4.
        MAX_RADIUS = 20
        nr_of_steps = 100  # This must be a big number.
        radii = np.linspace(0, MAX_RADIUS, nr_of_steps)
        energies_momenta = list()
        for i in range(len(radii)):
            state = np.array([round(radii[i], 2), round(radii[i], 2)])
            orbit = Orbit(state, model)
            energies_momenta.append([orbit.energy, orbit.momentum])
        Es = []
        Ls = []
        for E, L in reversed(energies_momenta):
            Es.append(E)
            Ls.append(L)
        spl = UnivariateSpline(Es, Ls, s=0.1)
        plt.plot(Es, spl(Es), 'b', lw=3)
        plt.xlabel("Energy")
        plt.ylabel("Angular Momentum")
        plt.show()

        # Step 5.
        radii = np.linspace(0, MAX_RADIUS, 10)
        mass_increments = list()
        for i in range(len(radii)):
            if i < (len(radii) - 1):
                mass_increments.append(Orbit.mass_increment(round(radii[i], 2), round(radii[i + 1], 2), model))
        energies = np.linspace(np.amin(Es), np.amax(Es), 10)
        momenta = np.linspace(np.amin(Ls), np.amax(Ls), 10)
        ee, pp = np.meshgrid(energies, momenta)
        peri_radii = np.zeros(shape=(10, 10))
        apo_radii = np.zeros(shape=(10, 10))
        for i in range(0, 10):
            for j in range(0, 10):
                peri_and_apo = Orbit.get_radii(ee[i][j], pp[i][j])
                peri_radii[i][j] = np.real(peri_and_apo[0])
                apo_radii[i][j] = np.real(peri_and_apo[1])

        # Loop for E.
        for i in range(10):
            # Loop for L.
            for j in range(10):
                index = str(i) + '_' + str(j)
                f = open('data/EL_%s.csv' % index, 'a')
                state = np.array([peri_radii[i][j], apo_radii[i][j]])
                orbit = Orbit(state, model)
                orbit_data = orbit.solution_orbit()
                for r in range(len(radii) - 1):
                    time = Orbit.get_time_in_orbit(orbit_data, radii[r], radii[r + 1])
                    if orbit.radial_period:
                        time = time / (orbit.radial_period/2)
                        f.write(str(time) + '\n')
                    else:
                        f.write(str(0.) + '\n')
                f.close()

        # Step 6.
        mass_fit = orbit.mass_fit()
        fitted_mass_model = Orbit.get_fitted_mass_model(mass_fit)

        # Step 7.
        # Plot fitted mass versus Hernquist mass.
        # Fit dimension.
        energies = energies[:-1]
        plt.scatter(fitted_mass_model, mass_increments)
        plt.xlabel("Total star mass")
        plt.ylabel("Hernquist mass")
        plt.show()

        # Plot fitted mass versus energies.
        plt.scatter(mass_fit, energies)
        plt.xlabel("Fitted mass")
        plt.ylabel("Energy")
        plt.show()

    else:
        "Please read Shakespeare!"
