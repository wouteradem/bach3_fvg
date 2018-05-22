import numpy as np
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy.optimize import leastsq
from service.Transform import Transform


class Orbit:
    MAX_RADIUS = 10

    def __init__(self, state, model):
        self.__r_peri = np.round(state[0], 2)
        self.__r_apo = np.round(state[1], 2)
        self.__model = model
        self.__transform_service = Transform(model)
        self.__momentum = self.set_momentum()
        self.__energy = self.set_binding_energy()
        if self.__r_peri != self.__r_apo:
            self.__radial_period = self.set_radial_period()
        else:
            self.__radial_period = 0.
        self.__orbit = None

    @property
    def radius_peri(self):
        return self.__r_peri

    @property
    def radius_apo(self):
        return self.__r_apo

    @property
    def energy(self):
        return self.__energy

    @property
    def momentum(self):
        return self.__momentum

    @property
    def radial_period(self):
        return self.__radial_period

    def get_energy_from_momentum(self, r, momentum):
        """Sets the energy from the momentum."""
        if momentum == 0.0:
            return self.__model.binding_potential(r)
        else:
            return self.__model.binding_potential(r) - np.power(momentum, 2) / (2.0 * np.power(r, 2))

    def get_momentum_from_energy(self, r, energy):
        """Sets the momentum from the energy."""
        momentum = np.sqrt(2 * np.power(r, 2) * (self.__model.binding_potential(r) - energy))
        return momentum

    @staticmethod
    def get_radii(energy, momentum):
        """Determines the peri and apo centre and filters out negative values."""
        c1 = 1.0
        c2 = 1.0 - 1.0 / energy
        c3 = np.power(momentum, 2) / (2.0 * energy)
        c4 = np.power(momentum, 2) / (2.0 * energy)
        coefficients = [c1, c2, c3, c4]
        roots = np.roots(coefficients)
        roots = np.sort(roots[roots >= 0.0])
        if len(roots) == 3:
            roots = np.delete(roots, 0)
        if isinstance(roots[0], complex) and isinstance(roots[1], complex):
            roots[0] = np.real(0.)
            roots[1] = np.real(0.)
        return roots

    def get_apocentre_from_pericentre(self, r_apo):
        pass

    def get_pericentre_from_apocentre(self, r_peri):
        pass

    def set_binding_energy(self):
        """Sets the binding energy."""
        return self.get_energy_from_momentum(self.__r_apo, self.__momentum)

    def set_momentum(self):
        """Sets the momentum of the orbit."""
        if self.__r_peri == 0.0 or self.__r_apo == 0.0:
            # (radial velocity = 0.0, angular velocity = 0.0).
            return 0.0
        elif self.__r_peri < self.__r_apo:
            # (radial velocity != 0.0, angular velocity != 0.0).
            nominator = 1.0 / (self.__r_apo + 1) - 1.0 / (self.__r_peri + 1)
            denominator = 1.0 / (2 * np.power(self.__r_apo, 2)) - 1. / (2 * np.power(self.__r_peri, 2))
            return np.sqrt(nominator/denominator)
        elif self.__r_peri == self.__r_apo:
            # (radial velocity = 0.0, angular velocity != 0.0).
            return np.sqrt(-1 * np.power(self.__r_apo, 3) * self.__model.first_derivative_binding_potential(self.__r_apo))

    def set_radial_period(self):
        """Sets the radial period."""
        if self.__r_peri == 0.0 and self.__r_apo == 0.0:
            return 0.0
        radial_period, error = quad(self.__transform_service.period_integral, self.__r_peri, self.__r_apo,
                                    args=(self.__energy, self.__momentum))
        return 2 * radial_period

    def solution_orbit(self):
        """Sets the orbit using odeint."""
        if self.__r_apo == 0.0 and self.__r_peri == 0.0:
            return [[0.0, 0.0, 0.0, 0.0]]
        time_down = np.linspace(0, self.__radial_period / 2.0, 41)
        if self.__momentum == 0.0:
            state = [self.__r_apo, 0.0]
        else:
            state = [self.__r_apo, 0.0, 0.0]
        orbit_down = odeint(self.__transform_service.motion_ode, state, time_down,
                            args=(self.__energy, self.__momentum, 1))
        if self.__momentum == 0.0:
            orbit_down = np.insert(orbit_down, 1, 0.0, axis=1)
        time_up = np.linspace(self.__radial_period / 2.0, self.__radial_period, 41)
        if self.__momentum == 0.0:
            state = [0.0, -orbit_down[-1][2]]
        else:
            state = [self.__r_peri, orbit_down[-1][1], 0.0]
        orbit_up = odeint(self.__transform_service.motion_ode, state, time_up,
                          args=(self.__energy, self.__momentum, -1))
        if self.__momentum == 0.0:
            orbit_up = np.insert(orbit_up, 1, np.pi, axis=1)
        orbit = np.concatenate((orbit_down, orbit_up), axis=0)
        times = np.concatenate((time_down, time_up), axis=0)
        self.__orbit = np.insert(orbit, 0, times, axis=1)
        return self.__orbit

    @staticmethod
    def get_time_in_orbit(orbit, r_1, r_2):
        """Gets the time in orbit."""
        if orbit is not None:
            orbit_dub = []
            for i in range(0, len(orbit)/2):
                if r_1 <= orbit[i][1] and r_1 <= orbit[i][1] <= r_2:
                    orbit_dub.append(orbit[i][0])

        # Now calculate the time delta's.
        time = 0.
        for t in range(1, len(orbit_dub)):
            delta = orbit_dub[t] - orbit_dub[t-1]
            time += delta
        return time

    @staticmethod
    def mass_increment(r_1, r_2, model):
        """Sets the mass increments."""
        return model.mass_within_radius(r_2) - model.mass_within_radius(r_1)

    def residual(self, mass_guess, masses, weight):
        """ Sets the fit."""
        model = mass_guess * weight
        return masses - model

    def mass_fit(self):
        """ Makes an estimation of the masses to fit the Hernquist model."""
        # TODO Using the calculated data from the test file for now.
        hernquist_masses = np.array([0.47532888391651557, 0.19081514722535292, 0.09009822394024258,
                                    0.05175695973895911, 0.03366687792495937, 0.02363632669717164,
                                    0.017571159870201525, 0.013465512077184605, 0.010690387067462614])
        weights = np.array([0.7975, 0.285, 0.1825, 0.0025, 0.0025, 0.0125, 0.01, 0.0125, 0.0125])
        guess_of_mk = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        final_mk, success = leastsq(self.residual, guess_of_mk[:], args=(hernquist_masses, weights))
        if success:
            return final_mk

    @staticmethod
    def get_fitted_mass_model(mk):
        """ Sets the fitted mass against the calculated weigths."""
        weights = np.array([0.7975, 0.285, 0.1825, 0.0025, 0.0025, 0.0125, 0.01, 0.0125, 0.0125])
        fitted_mass_model = []
        for i in range(len(mk)):
            fitted_mass_model.append(mk[i] * weights[i])
        return fitted_mass_model
