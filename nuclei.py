import pygame

from constants import m_neutron, WHITE, DARKER_GREY, LIGHT_GREY, MID_DARK_GREY, rod_width, rod_height
from vectors import Vector


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, pixel_radius, fast):
        super().__init__()

        self.colour = colour
        self.pixel_radius = pixel_radius
        self.fast = fast
        self.image = pygame.Surface([pixel_radius * 2, pixel_radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        if fast:
            pygame.draw.circle(self.image, DARKER_GREY, (pixel_radius, pixel_radius), pixel_radius)
            pygame.draw.circle(self.image, colour, (pixel_radius, pixel_radius), pixel_radius - 3)

        else:
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

        if fast:
            self.sprite = Sprite(LIGHT_GREY, 7, True)

        else:
            self.sprite = Sprite(DARKER_GREY, 7, False)

        all_sprites_list.add(self.sprite)

    def move(self, dt):
        self.position += self.velocity * dt

    def energy(self):
        return 0.5 * m_neutron * (self.velocity ** 2)


class FuelRod:
    def __init__(self, temperature):
        self.temperature = temperature


class Xenon:
    pass


class FissionProduct:
    pass


class ControlRod:
    def __init__(self, screen, left_top, descent=0):
        self.descent = descent
        self.screen = screen
        self.left_top = left_top
        self.rect = pygame.Rect((left_top.x, left_top.y), (rod_width, rod_height))

    def descend(self, new_descent):
        self.descent = new_descent
        self.rect = pygame.Rect((self.left_top.x, self.left_top.y + rod_height * (new_descent / 100)),
                                (rod_width, rod_height))

    def draw(self):
        pygame.draw.rect(self.screen, MID_DARK_GREY, self.rect)


class Moderator:
    def __init__(self, screen, left_top):
        self.screen = screen
        self.left_top = left_top
        self.outer_rect = pygame.Rect((self.left_top.x, self.left_top.y), (rod_width, rod_height))
        self.inner_rect = pygame.Rect((self.left_top.x + 3, self.left_top.y + 3), (rod_width - 6, rod_height - 6))

    def draw(self):
        pygame.draw.rect(self.screen, DARKER_GREY, self.outer_rect)
        pygame.draw.rect(self.screen, LIGHT_GREY, self.inner_rect)

all_sprites_list = pygame.sprite.Group()
neutrons = []

starter = Neutron(Vector(0, 100), Vector(300, 300), True)
neutrons.append(starter)
