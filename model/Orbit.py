import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy.interpolate import UnivariateSpline
from service.Transform import Transform


class Orbit:
    MAX_RADIUS = 100

    def __init__(self, state, model):
        if state[0] > state[1]:
            self.__r_peri = state[1]
            self.__r_apo = state[0]
        else:
            self.__r_peri = state[0]
            self.__r_apo = state[1]
        self.__model = model
        self.__transform_service = Transform(model)
        self.__momentum = self.set_momentum()
        self.__energy = self.set_binding_energy()
        self.__radial_period = self.set_radial_period()

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

    def get_radii(self):
        """Determines the peri and apo centre and filters out negative values."""
        c1 = 1.0
        c2 = 1.0 - 1.0 / self.__energy
        c3 = np.power(self.__momentum, 2) / (2.0 * self.__energy)
        c4 = np.power(self.__momentum, 2) / (2.0 * self.__energy)
        coefficients = [c1, c2, c3, c4]
        roots = np.roots(coefficients)
        return np.sort(roots[roots >= 0.0])

    def get_apocentre_from_pericentre(self, r_apo):
        """TODO Is this needed?"""
        pass

    def get_pericentre_from_apocentre(self, r_peri):
        """TODO Is this needed?"""
        pass

    def set_binding_energy(self):
        """Sets the binding energy."""
        return self.get_energy_from_momentum(self.__r_apo, self.__momentum)

    def set_momentum(self):
        """Sets the momentum of the orbit."""
        if self.__r_peri == 0.0 and self.__r_apo == 0.0:
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
            return [0.0, 0.0, 0.0]
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
        orbit = np.insert(orbit, 0, times, axis=1)
        return orbit

    def interpolation(self):
        """Interpolates the (E,L) couples on circular orbits."""
        radii = np.linspace(1, self.MAX_RADIUS, 1000)
        energy = np.empty(1000)
        momentum = np.empty(1000)
        for r in range(len(radii)):
            radius = r / 100.0
            self.__r_peri = radius
            self.__r_apo = radius
            momentum[r] = self.set_momentum()
            self.__momentum = momentum[r]
            energy[r] = self.set_binding_energy()
            self.__energy = energy[r]
        spl = UnivariateSpline(momentum, energy, s=0.1)
        plt.plot(radii, spl(radii), 'b', lw=3)
        plt.show()
        return

    def mass_increment(self):
        """Sets the mass increments."""

        # Sets the formatting.
        np.set_printoptions(suppress=True)

        radii = np.linspace(1, self.MAX_RADIUS, 1000)
        mass = np.empty(1000)
        for r in range(len(radii)):
            radius = r / 100.0
            mass[r] = self.__model.mass_within_radius(radius)
        i = 1
        mass_increment = np.empty(999)
        while i < len(mass):
            mass_increment[i-1] = mass[i] - mass[i-1]
            i = i + 1
        return mass_increment

    def radial_distribution(self):
        pass
