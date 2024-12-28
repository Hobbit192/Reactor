import pygame
import sys
import random

from constants import alpha, WHITE, GREY, BLUE, LIGHT_BLUE, PURPLE, LIGHT_GREY, DARKER_GREY, \
    delayed_neutron_decay, square_size, gap, row_height, column_width, rod_width, width, height, \
    total_columns, total_rows, start_x, start_y, rod_height, fast_speed, slow_speed
from nuclei import Coolant, neutrons, all_sprites_list, FuelRod, FissionProduct, Neutron, Xenon, ControlRod, Moderator
from vectors import Vector

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((width, height))
coolant_surface = pygame.Surface((width, height))
pygame.display.set_caption("Nuclear Reactor")

# Coolant grid setup
coolant_grid = []

# Each coolant square can be accessed by its position in the array
for col in range(total_columns):
    coolant_grid.append([])
    for row in range(total_rows):
        coolant_square = Coolant(21)
        coolant_grid[col].append(coolant_square)

# Nuclei grid setup
nuclei_grid = []

nucleus_diameter = int(square_size * 0.7)

for col in range(total_columns):
    nuclei_grid.append([])
    for row in range(total_rows):
        if random.randint(1, 10) == 1:
            uranium = FuelRod(21)
            nuclei_grid[col].append(uranium)

        else:
            nucleus = FissionProduct()
            nuclei_grid[col].append(nucleus)

# Control rod setup
control_rods = []
total_rods = (total_columns - 1) // 4 + 1

for control_rod in range(total_rods):
    control_rod_x = start_x + (control_rod * (square_size + gap) * 4) - rod_width / 2
    control_rod_y = start_y - rod_height

    control_rods.append(ControlRod(screen, Vector(control_rod_x, control_rod_y), 0))

# Moderator setup
moderators = []
total_moderators = total_rods - 1

for moderator in range(total_moderators):
    moderator_x = start_x + (moderator * (square_size + gap) * 4) - rod_width / 2 + (square_size + gap) * 2
    moderator_y = start_y

    moderators.append(Moderator(screen, Vector(moderator_x, moderator_y)))

def heat_transfer(grid, i, j):
    current_temp = grid[i][j].temperature

    conduction = alpha * (grid[i + 1][j] + grid[i - 1][j] + grid[i][j + 1] + grid[i][j - 1] - 4 * current_temp)

    convection = (1 - F) * current_temp + (F / 4) * (grid[i + 1][j] + grid[i - 1][j] + grid[i][j + 1] + grid[i][j - 1])

    if neutron_collision:
        pass

    dT = conduction + convection + fuel_rod_transfer + neutron_heating
    return dT


def chance(percentage):
    return random.randint(1, 100) <= percentage


# ------------------------------------- Main loop ----------------------------------------------------------------------
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    # Grid drawing
    for column in range(total_columns):
        for row in range(total_rows):
            coolant_x = start_x + column * (square_size + gap)
            coolant_y = start_y + row * (square_size + gap)
            pygame.draw.rect(screen, BLUE, (coolant_x, coolant_y, square_size, square_size))

            nuclei_x = start_x + column * (square_size + gap) + square_size // 2
            nuclei_y = start_y + row * (square_size + gap) + square_size // 2

            if isinstance(nuclei_grid[column][row], FuelRod):
                pygame.draw.circle(screen, LIGHT_BLUE, (nuclei_x, nuclei_y), nucleus_diameter // 2)

            elif isinstance(nuclei_grid[column][row], FissionProduct):
                pygame.draw.circle(screen, GREY, (nuclei_x, nuclei_y), nucleus_diameter // 2)

            elif isinstance(nuclei_grid[column][row], Xenon):
                pygame.draw.circle(screen, PURPLE, (nuclei_x, nuclei_y), nucleus_diameter // 2)

            new_fuel = random.randint(1, 3000)
            xenon_production = random.randint(1, 4500)
            delayed_emission = random.randint(1, 10000)

            if isinstance(nuclei_grid[column][row], FissionProduct):
                if delayed_emission <= delayed_neutron_decay * 10:
                    angle = random.randint(0, 360)
                    delayed_neutron = Neutron(position=Vector(nuclei_x, nuclei_y),
                                              velocity=Vector(200, 200).rotate(angle),
                                              fast=True)
                    neutrons.append(delayed_neutron)

                if new_fuel == 1:
                    nuclei_grid[column][row] = FuelRod(21)

                elif xenon_production == 1:
                    nuclei_grid[column][row] = Xenon()

    # Control rod drawing
    for control_rod in control_rods:
        control_rod.draw()

    # Moderator drawing
    for moderator in moderators:
        moderator.draw()

    time_delta = clock.tick(60) / 1000

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        for rod in control_rods:
            rod.descend(min(rod.descent + 1, 100))

    elif keys[pygame.K_UP]:
        for rod in control_rods:
            rod.descend(max(rod.descent - 1, 0))


    # Game state updates
    # Neutron handling
    for neutron in neutrons:
        neutron.move(time_delta)

        neutron_column = int((neutron.position.x - start_x) // column_width)
        neutron_row = int((neutron.position.y - start_y) // row_height)

        if (neutron.position.x < 0 or neutron.position.x > width or
                neutron.position.y < 0 or neutron.position.y > height):
            neutrons.remove(neutron)
            neutron.sprite.kill()
            continue

        elif 0 <= neutron_column < total_columns and 0 <= neutron_row < total_rows:

            nucleus_position = Vector(neutron_column * column_width + (column_width // 2) + start_x,
                                      neutron_row * column_width + (column_width // 2) + start_y)

            separation = neutron.position - nucleus_position

            if separation.magnitude() < nucleus_diameter / 2 + neutron.sprite.pixel_radius:
                if isinstance(nuclei_grid[neutron_column][neutron_row], FuelRod) and chance(100):
                    nuclei_grid[neutron_column][neutron_row] = FissionProduct()

                    neutrons.remove(neutron)
                    neutron.sprite.kill()

                    for i in range(3):
                        angle = random.randint(0, 360)
                        new_neutron = Neutron(nucleus_position, Vector(200, 200).rotate(angle), True)
                        neutrons.append(new_neutron)

                    continue

                elif isinstance(nuclei_grid[neutron_column][neutron_row], Xenon) and chance(100):
                    nuclei_grid[neutron_column][neutron_row] = FissionProduct()

                    neutrons.remove(neutron)
                    neutron.sprite.kill()
                    continue

        for control_rod in control_rods:
            if neutron.collision_check(control_rod):
                neutrons.remove(neutron)
                neutron.sprite.kill()
                break

        for moderator in moderators:
            if neutron.collision_check(moderator):
                if neutron.fast:
                    neutron.set_fast(False)
                    neutron.velocity.x = -(neutron.velocity.x / fast_speed) * slow_speed
                    neutron.velocity.y = (neutron.velocity.y / fast_speed) * slow_speed

        neutron.sprite.set_pos(neutron.position)

    all_sprites_list.draw(screen)
    pygame.display.flip()

    print(len(neutrons))

pygame.quit()
sys.exit()
