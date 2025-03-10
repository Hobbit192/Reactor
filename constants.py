# Constants
import pygame

pygame.init()

h = 0.004
alpha = 0.1
q_e = 1.602176634e-19
coolant_inflow_temp = 260
min_temp = 260
desaturation = 0.46
max_temp = 295
m_neutron = 1.674927471e-27
number = 10e18
e = 2.718281828459045
barn_scale = 1e-24

fission_energy = 195e6
fission_heat = fission_energy * number * 0.9

delayed_neutron_decay = 0.1842

slow_speed = (2 * (150 ** 2)) ** 0.5
fast_speed = (2 * (250 ** 2)) ** 0.5

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
micro_cs = {
    "u235": {
        "thermal_f": 585.1,
        "thermal_a": 98,
        "thermal_t": 698.9,
        "fast_f": 1,
        "fast_a": 0.15,
        "fast_t": 5.894
    },
    "xe135": {
        "thermal_a": 2778000,
        "thermal_t": 3110000,
        "fast_a": 40,
        "fast_t": 100
    },
    "water": {
        "thermal_a": 0.3326
    }
}

n_density = {
    "u235": 1e22,
    "xe135": 3e13,
    "water": 1e23
}

macro_cs = {}

for element, data in micro_cs.items():
    macro_cs[element] = {}
    for key, value in data.items():
        macro_cs[element][key] = value * n_density[element]

# Probabilities

probability = {
    "u235": {
        "thermal_f": macro_cs["u235"]["thermal_f"] / macro_cs["u235"]["thermal_t"],
        "thermal_a": macro_cs["u235"]["thermal_a"] / macro_cs["u235"]["thermal_t"],
        "fast_f": macro_cs["u235"]["fast_f"] / macro_cs["u235"]["fast_t"],
        "fast_a": macro_cs["u235"]["fast_a"] / macro_cs["u235"]["fast_t"]
    },
    "xe135": {
        "thermal_a": macro_cs["xe135"]["thermal_a"] / macro_cs["xe135"]["thermal_t"],
        "fast_a": macro_cs["xe135"]["fast_a"] / macro_cs["xe135"]["fast_t"]
    },
    "water": {
        "thermal_a": 1 - (e ** (-macro_cs["water"]["thermal_a"] * barn_scale))
    }
}

