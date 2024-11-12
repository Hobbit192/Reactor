import pygame

from constants import m_neutron, WHITE, DARK_GREY
from vectors import Vector


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, pixel_radius):
        super().__init__()

        self.colour = colour
        self.pixel_radius = pixel_radius
        self.image = pygame.Surface([pixel_radius * 2, pixel_radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.circle(self.image, colour, (pixel_radius, pixel_radius), pixel_radius)
        self.rect = self.image.get_rect()

    def set_pos(self, position):
        self.rect.x = position.x - self.pixel_radius
        self.rect.y = position.y - self.pixel_radius

class Coolant:
    def __init__(self, temperature):
        self.temperature = temperature

    def collision_check(self):
        pass

class Neutron:
    def __init__(self, position, velocity, fast):
        self.position = position
        self.velocity = velocity
        self.fast = fast
        self.speed = velocity.magnitude()

        self.sprite = Sprite(DARK_GREY, 8)
        all_sprites_list.add(self.sprite)

        neutrons.append(self)

    def draw(self):
        if self.fast:
            pass

        else:
            pass

    def move(self, dt):
        self.position += self.velocity * dt

    def energy(self):
        return 0.5 * m_neutron * (self.velocity ** 2)

class FuelRod:
    def __init__(self, temperature):
        self.temperature = temperature

    def fission(self):
        pass

class Xenon:
    pass

class FissionProduct:
    pass

all_sprites_list = pygame.sprite.Group()
neutrons = []

test = Neutron(Vector(0, 0), Vector(500, 500), False)