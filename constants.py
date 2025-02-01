# Constants
import pygame

pygame.init()

c_p = 4184
rho = 997
k = 0.6
#h = 5000
h = 0.5
#alpha = k / (rho * c_p)
alpha = 0.1
e = 1.602176634e-19
flow_rate = 0.005
coolant_inflow_temp = 260
min_temp = 260
desaturation = 0.46
max_temp = 285
m_neutron = 1.674927471e-27
number = 10e18

fission_energy = 195e6
fission_heat = fission_energy * number * 0.9

delayed_neutron_decay = 0.1842

slow_speed = (2 *(150 ** 2)) ** 0.5
fast_speed = (2 *(250 ** 2)) ** 0.5

# Screen dimensions
info = pygame.display.Info()
width, height = info.current_w - 10, info.current_h - 100

border_gap = 70
gap = 3
square_size = 30

aspect_ratio = width / height

total_columns = int((width - 2 * border_gap - gap) / (square_size + gap))
total_rows = int(total_columns / aspect_ratio)

total_grid_width = (total_columns * square_size) + (gap * (total_columns - 1))
total_grid_height = (total_rows * square_size) + (gap * (total_rows - 1))

start_x = (width - total_grid_width) // 2
start_y = (height - total_grid_height) // 2

column_width = square_size + gap
row_height = square_size + gap

rod_width = 0.25 * square_size + gap
rod_height = row_height * total_rows - gap

# Colours
WHITE = (255, 255, 255)
DARKER_GREY = (25, 25, 25)
DARK_GREY = (86, 86, 86)
MID_DARK_GREY = (100, 100, 100)
GREY = (150, 150, 150)
LIGHT_GREY = (200, 200, 200)
BLUE = (189, 206, 219)
RED = (193, 18, 31)
LIGHT_BLUE = (124, 180, 184)
PURPLE = (87, 70, 123)

# Cross-sections
u235_fission_thermal = 0
u235_fission_fast = 0
u235_absorption_thermal = 0
u235_absorption_fast = 0

xe135_absorption_thermal = 0
xe135_absorption_fast = 0

water_absorption_thermal = 0
