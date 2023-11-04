import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
BACKGROUND_COLOR = (255, 255, 255)
CIRCLE_COLOR = (0, 0, 0)
FONT_SIZE = 36
MIN_INTERVAL = 100  # Minimum interval in milliseconds

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Click and Hold")

# Font for displaying the speed
font = pygame.font.Font(None, FONT_SIZE)

# Initialize variables
speed = 1
counter = 0
holding = False
interval = 1000  # Initial interval (1 second)
last_draw_time = 0
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_state = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks()

    if mouse_state[0]:  # Check if the left mouse button is held down
        if not holding:
            holding = True
            counter = 0
            last_draw_time = current_time
        elif current_time - last_draw_time >= interval:
            counter += speed
            speed *= 1.02  # Adjust the exponent value as needed
            last_draw_time = current_time

    else:
        holding = False
        speed = 1

    # Draw a circle
    pygame.draw.circle(screen, CIRCLE_COLOR, mouse_pos, int(counter))

    # Display the speed
    speed_text = font.render(f"Speed: {speed:.2f}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    # Reduce the interval gradually
    if interval > MIN_INTERVAL:
        interval -= 1

pygame.quit()
sys.exit()
