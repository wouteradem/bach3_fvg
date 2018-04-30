import numpy as np


class Transform:
    def __init__(self, model):
        self.__model = model

    def period_integral(self, r, energy, momentum):
        """Sets the integrand."""
        first_term = 2 * (self.__model.binding_potential(r) - energy)
        second_term = np.power(momentum, 2) / np.power(r, 2)
        return 1 / np.sqrt(first_term - second_term)

    def motion_ode(self, state, t, energy, momentum, direction):
        """ODE to calculate the position vectors."""

        # Sets the formatting.
        np.set_printoptions(suppress=True)

        r = state[0]
        t1 = self.__model.binding_potential(r)
        energy -= 0.00000001
        t2 = energy
        if momentum == 0.0:
            radix = t1 - t2
        else:
            t3 = np.power(momentum, 2) / (2 * np.power(r, 2))
            radix = t1 - t2 - t3
            dphi_dt = momentum / np.power(r, 2)
        if direction > 0.0:
            if radix > 0.0:
                dr_dt = -1.0 * np.sqrt(2 * radix)
            else:
                dr_dt = 0.0
        elif direction < 0.0:
            if radix > 0.0:
                dr_dt = np.sqrt(2 * radix)
            else:
                dr_dt = 0.0
        if momentum == 0.0:
            return [dr_dt]
        else:
            return [dr_dt, dphi_dt]
