import pygame
import sys

from constants import alpha, WHITE, GREY, LIGHT_GREY
from nuclei import Coolant, neutrons, all_sprites_list

# Initialize Pygame
pygame.init()

# Screen dimensions
info = pygame.display.Info()
width, height = info.current_w - 10, info.current_h - 100

gap = 50
rows, columns = 25, 50

# Calculate square size ensuring they fit perfectly within the window with gaps
available_width = width - (2 * gap) - (columns - 1) * 5  # Total width available for squares (excluding gaps between squares)
available_height = height - (2 * gap) - (rows - 1) * 5  # Total height available for squares (excluding gaps between squares)
square_width = available_width // columns  # Width of each square
square_height = available_height // rows  # Height of each square
square_gap = 5

# Adjust gap to ensure grid is centered vertically
grid_height = rows * square_height + (rows - 1) * square_gap
vertical_gap = (height - grid_height) // 2

# Set up the display
screen = pygame.display.set_mode((width, height))
coolant_surface = pygame.Surface((width, height))
pygame.display.set_caption("Nuclear Reactor")

def heat_transfer(grid, i, j):
    current_temp = grid[i][j]

    conduction = alpha * (grid[i+1][j] + grid[i-1][j] + grid[i][j+1] + grid[i][j-1] - 4 * current_temp)

    convection = (1 - F) * current_temp + (F / 4) * (grid[i+1][j] + grid[i-1][j] + grid[i][j+1] + grid[i][j-1])

    if neutron_collision:
        pass

    dT = conduction + convection + fuel_rod_transfer + neutron_heating
    return dT

coolant_grid = []

# Each coolant square can be accessed by its position in the array
for i in range(columns):
    coolant_grid.append([])
    for j in range(rows):
        coolant_grid[i].append(Coolant(21))


def draw_grid():
    for row in range(rows):
        for col in range(columns):
            x = gap + col * (square_width + square_gap)
            y = vertical_gap + row * (square_height + square_gap)
            rect = pygame.Rect(x, y, square_width, square_height)
            pygame.draw.rect(screen, LIGHT_GREY, rect)

# ------------------------------------- Main loop ----------------------------------------------------------------------
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    draw_grid()

    time_delta = clock.tick(75)/1000

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game state updates
    for neutron in neutrons:
        neutron.move(time_delta)
        neutron.sprite.set_pos(neutron.position)

    all_sprites_list.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()