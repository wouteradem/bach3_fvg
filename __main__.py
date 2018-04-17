from entities.model import Model

if __name__ == '__main__':
    model = Model(1.)
    print(model)
    print("Density profile value is {}.".format(model.density_profile()))
    print("Gravitational potential is {}.".format(model.gravitational_potential()))
    print("Mass within radius is {}".format(model.mass_within_radius()))
