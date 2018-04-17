import numpy as np
from math import sqrt


class Model:
    GRAVITATIONAL_CONSTANT = 1
    MASS = 1
    SCALE_FACTOR = 1

    def __init__(self, radius):
        """TODO Need to set a max radius"""
        self.type = 'Hernquist'
        self.radius = radius
        self.half_radius = self.SCALE_FACTOR + sqrt(self.radius)

    def density_profile(self):
        """Sets density profile"""
        nominator = self.GRAVITATIONAL_CONSTANT * self.SCALE_FACTOR
        denominator = np.pi * self.radius * (self.radius + self.SCALE_FACTOR)**3
        return nominator / denominator

    def gravitational_potential(self):
        """Sets gravitational potential"""
        return -(self.GRAVITATIONAL_CONSTANT * self.MASS) / (self.radius + self.SCALE_FACTOR)

    def mass_within_radius(self):
        """Sets mass within radius"""
        return (self.MASS * self.radius**2) / (self.radius + self.SCALE_FACTOR)**2

    """TODO First and Second derivatives"""

    def __str__(self):
        return "Using {} modelling.".format(self.type)
