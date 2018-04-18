from model.Hernquist import Hernquist

if __name__ == '__main__':
    model = Hernquist(10., 1, 1)
    print("Radius is {}.".format(model.radius))
    print("Density profile value is {}.".format(model.density_profile()))
    print("Gravitational potential is {}.".format(model.gravitational_potential()))
    print("Mass within radius is {}.".format(model.mass_within_radius()))
    print("Mass within half radius is {}.".format(model.mass_within_half_radius()))
