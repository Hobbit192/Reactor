import pygame
import sys
import random

from constants import alpha, WHITE, GREY, LIGHT_GREY, LIGHT_BLUE, PURPLE, MID_DARK_GREY
from nuclei import Coolant, neutrons, all_sprites_list, FuelRod, FissionProduct, Neutron, Xenon, ControlRod
from vectors import Vector

# Initialize Pygame
pygame.init()

# Screen dimensions
info = pygame.display.Info()
width, height = info.current_w - 10, info.current_h - 100

# Set up the display
screen = pygame.display.set_mode((width, height))
coolant_surface = pygame.Surface((width, height))
pygame.display.set_caption("Nuclear Reactor")

# Coolant grid setup
coolant_grid = []

aspect_ratio = width / height
border_gap = 70
gap = 3
square_size = 30

column_width = square_size + gap
row_height = square_size + gap

total_columns = int((width - 2 * border_gap - gap) / (square_size + gap))
total_rows = int(total_columns / aspect_ratio)

total_grid_width = (total_columns * square_size) + (gap * (total_columns - 1))
total_grid_height = (total_rows * square_size) + (gap * (total_rows - 1))

start_x = (width - total_grid_width) // 2
start_y = (height - total_grid_height) // 2

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

rod_width = 0.25 * square_size + gap
rod_height = row_height * total_rows - gap

for rod in range((total_columns - 1) // 3 + 1):
    control_rod = ControlRod()
    control_rods.append(control_rod)

def heat_transfer(grid, i, j):
    current_temp = grid[i][j].temperature

    conduction = alpha * (grid[i+1][j] + grid[i-1][j] + grid[i][j+1] + grid[i][j-1] - 4 * current_temp)

    convection = (1 - F) * current_temp + (F / 4) * (grid[i+1][j] + grid[i-1][j] + grid[i][j+1] + grid[i][j-1])

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
            pygame.draw.rect(screen, LIGHT_GREY, (coolant_x, coolant_y, square_size, square_size))

            nuclei_x = start_x + column * (square_size + gap) + square_size // 2
            nuclei_y = start_y + row * (square_size + gap) + square_size // 2

            if isinstance(nuclei_grid[column][row], FuelRod):
                pygame.draw.circle(screen, LIGHT_BLUE, (nuclei_x, nuclei_y), nucleus_diameter // 2)

            if isinstance(nuclei_grid[column][row], FissionProduct):
                pygame.draw.circle(screen, GREY, (nuclei_x, nuclei_y), nucleus_diameter // 2)

            if isinstance(nuclei_grid[column][row], Xenon):
                pygame.draw.circle(screen, PURPLE, (nuclei_x, nuclei_y), nucleus_diameter // 2)

            new_fuel = random.randint(1, 1000)
            xenon_production = random.randint(1, 5000)

            if new_fuel == 1:
                nuclei_grid[column][row] = FuelRod(21)

            if xenon_production == 1:
                nuclei_grid[column][row] = Xenon()

    # Control rod drawing
    for column in range(0, total_columns, 4):
        rod_x = start_x + column * (square_size + gap) - rod_width / 2
        pygame.draw.rect(screen, MID_DARK_GREY, (rod_x, start_y, rod_width, rod_height))

    time_delta = clock.tick(60)/1000

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

        if 0 <= neutron_column < total_columns and 0 <= neutron_row < total_rows:

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
                        new_neutron = Neutron(nucleus_position, Vector(300, 300).rotate(angle), False)
                        neutrons.append(new_neutron)

                if isinstance(nuclei_grid[neutron_column][neutron_row], Xenon) and chance(100):
                    nuclei_grid[neutron_column][neutron_row] = FissionProduct()

                    neutrons.remove(neutron)
                    neutron.sprite.kill()

        neutron.sprite.set_pos(neutron.position)

    all_sprites_list.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()