from abc import ABCMeta, abstractmethod


class IModel(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def density_profile(self): pass

    @abstractmethod
    def gravitational_potential(self): pass

    @abstractmethod
    def first_derivative_gravitation_potential(self): pass

    @abstractmethod
    def second_derivative_gravitation_potential(self): pass

    @abstractmethod
    def mass_within_radius(self): pass
