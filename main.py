import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
info = pygame.display.Info()
width, height = info.current_w - 10, info.current_h - 100  # Width and height of the window (full screen)
gap = 50  # Gap between the window edge and the grid
rows, columns = 20, 40  # Number of rows and columns for the grid (adjusted to make the grid rectangular)

# Calculate square size ensuring they fit perfectly within the window with gaps
available_width = width - 2 * gap - (columns - 1) * 5  # Total width available for squares (excluding gaps between squares)
available_height = height - 2 * gap - (rows - 1) * 5  # Total height available for squares (excluding gaps between squares)
square_width = available_width // columns  # Width of each square
square_height = available_height // rows  # Height of each square
square_gap = 5  # Gap between squares

# Adjust gap to ensure grid is centered vertically
grid_height = rows * square_height + (rows - 1) * square_gap
vertical_gap = (height - grid_height) // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reactor")

# Function to draw the grid
def draw_grid():
    for row in range(rows):
        for col in range(columns):
            x = gap + col * (square_width + square_gap)
            y = vertical_gap + row * (square_height + square_gap)
            rect = pygame.Rect(x, y, square_width, square_height)
            pygame.draw.rect(screen, GREY, rect)  # Fill the square with grey

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Fill the background with white
    draw_grid()  # Draw the grid

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()