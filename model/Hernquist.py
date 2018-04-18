import numpy as np
from math import sqrt
from model.IModel import IModel


class Hernquist(IModel):
    GRAVITATIONAL_CONSTANT = 1

    def __init__(self, radius, mass=1, scale_factor=1):
        self.__radius = radius
        self.__mass = mass
        self.__scale_factor = scale_factor
        self.__half_radius = self.__scale_factor + sqrt(self.__radius)

    @property
    def radius(self):
        return self.__radius

    @property
    def mass(self):
        return self.__mass

    @property
    def scale_factor(self):
        return self.__scale_factor

    def density_profile(self):
        """Sets density profile"""
        nominator = self.GRAVITATIONAL_CONSTANT * self.__scale_factor
        denominator = np.pi * self.__radius * (self.__radius + self.__scale_factor) ** 3
        return nominator / denominator

    def gravitational_potential(self):
        """Sets gravitational potential"""
        return (self.GRAVITATIONAL_CONSTANT * self.__mass) / (self.__radius + self.__scale_factor)

    def first_derivative_gravitation_potential(self):
        """Sets first derivative of gravitational potential"""
        return -1 * (self.GRAVITATIONAL_CONSTANT * self.__mass) / (self.__radius + self.__scale_factor)**2

    def second_derivative_gravitation_potential(self):
        """Sets second derivative of gravitational potential"""
        return 2 * (self.GRAVITATIONAL_CONSTANT * self.__mass) / (self.__radius + self.__scale_factor)**3

    def mass_within_radius(self):
        """Sets mass within radius"""
        return (self.__mass * self.__radius ** 2) / (self.__radius + self.__scale_factor) ** 2

    def mass_within_half_radius(self):
        """Sets mass within half radius"""
        return (self.__mass * self.__half_radius ** 2) / (self.__half_radius + self.__scale_factor) ** 2
