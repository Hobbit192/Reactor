from constants import m_neutron


class Coolant:
    def __init__(self, temperature):
        self.temperature = temperature

    def draw(self):
        pass

    def collision_check(self):
        pass

class Neutron:
    def __init__(self, velocity, position, fast):
        self.velocity = velocity
        self.position = position
        self.fast = fast

    def draw(self):
        pass

    def energy(self):
        return 0.5 * m_neutron * (self.velocity ** 2)

class FuelRod:
    def fission(self):
        pass