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
        self.rect = self.image.get_rect()
        self.update_image()

    def update_image(self):
        self.image.fill(WHITE)

        if self.fast:
            pygame.draw.circle(self.image, DARKER_GREY, (self.pixel_radius, self.pixel_radius), self.pixel_radius)
            pygame.draw.circle(self.image, self.colour, (self.pixel_radius, self.pixel_radius), self.pixel_radius - 3)

        else:
            pygame.draw.circle(self.image, self.colour, (self.pixel_radius, self.pixel_radius), self.pixel_radius)

    def set_pos(self, position):
        self.rect.x = position.x - self.pixel_radius
        self.rect.y = position.y - self.pixel_radius

    def set_fast(self, fast):
        self.fast = fast


class Coolant:
    def __init__(self, temperature):
        self.temperature = temperature


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

    def set_fast(self, fast):
        self.fast = fast
        all_sprites_list.remove(self.sprite)

        if self.fast:
            self.sprite = Sprite(LIGHT_GREY, 7, True)

        else:
            self.sprite = Sprite(DARKER_GREY, 7, False)

        all_sprites_list.add(self.sprite)
        self.sprite.set_pos(self.position)
        self.sprite.set_fast(self.fast)

    def move(self, dt):
        self.position += self.velocity * dt

    def energy(self):
        return 0.5 * m_neutron * (self.velocity ** 2)

    def collision_check(self, rod):
        closest_x = max(rod.rect.left, min(self.position.x, rod.rect.right))
        closest_y = max(rod.rect.top, min(self.position.y, rod.rect.bottom))

        distance = ((self.position.x - closest_x) ** 2 + (self.position.y - closest_y) ** 2) ** 0.5
        return distance < self.sprite.pixel_radius


class FuelRod:
    def __init__(self, temperature):
        self.temperature = temperature


class Xenon:
    def __init__(self, temperature):
        self.temperature = temperature

class FissionProduct:
    def __init__(self, temperature):
        self.temperature = temperature


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
        self.rect = pygame.Rect((self.left_top.x, self.left_top.y), (rod_width, rod_height))
        self.inner_rect = pygame.Rect((self.left_top.x + 3, self.left_top.y + 3), (rod_width - 6, rod_height - 6))

    def draw(self):
        pygame.draw.rect(self.screen, DARKER_GREY, self.rect)
        pygame.draw.rect(self.screen, LIGHT_GREY, self.inner_rect)

all_sprites_list = pygame.sprite.Group()
neutrons = []

starter = Neutron(position=Vector(0, 100), velocity=Vector(200, 200), fast=True)
neutrons.append(starter)
