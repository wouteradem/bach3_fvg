from abc import ABCMeta, abstractmethod


class IModel(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def density_profile(self, radius): pass

    @abstractmethod
    def binding_potential(self, radius): pass

    @abstractmethod
    def first_derivative_binding_potential(self, radius): pass

    @abstractmethod
    def second_derivative_binding_potential(self, radius): pass

    @abstractmethod
    def mass_within_radius(self, radius): pass

    @abstractmethod
    def half_radius(self, radius): pass
