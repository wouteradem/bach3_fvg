import numpy as np
from model.IModel import IModel


class Hernquist(IModel):
    GRAVITATIONAL_CONSTANT = 1

    def __init__(self, mass=1., scale_factor=1.):
        self.__mass = mass
        self.__scale_factor = scale_factor

    @property
    def mass(self):
        return self.__mass

    @property
    def scale_factor(self):
        return self.__scale_factor

    def density_profile(self, radius):
        """Sets density profile."""
        nominator = self.GRAVITATIONAL_CONSTANT * self.__scale_factor
        denominator = 2.0 * np.pi * radius * np.power(radius + self.__scale_factor, 3)
        return nominator / denominator

    def binding_potential(self, radius):
        """Sets binding potential."""
        return (self.GRAVITATIONAL_CONSTANT * self.__mass) / (radius + self.__scale_factor)

    def first_derivative_binding_potential(self, radius):
        """Sets first derivative of binding potential."""
        return -1.0 * (self.GRAVITATIONAL_CONSTANT * self.__mass) / np.power(radius + self.__scale_factor, 2)

    def second_derivative_binding_potential(self, radius):
        """Sets second derivative of binding potential."""
        return 2.0 * (self.GRAVITATIONAL_CONSTANT * self.__mass) / np.power(radius + self.__scale_factor, 3)

    def mass_within_radius(self, radius):
        """Sets mass within radius."""
        return (self.__mass * np.power(radius, 2)) / np.power(radius + self.__scale_factor, 2)

    def half_radius(self):
        """Sets the half radius."""
        return self.__scale_factor + np.sqrt(2)
