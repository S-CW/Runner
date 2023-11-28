import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Rect")

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)

# Set up the Rect
rect_width, rect_height = 50, 50
rect = pygame.Rect(50, height // 2 - rect_height // 2, rect_width, rect_height)

# Set up the clock
clock = pygame.time.Clock()

# Set up the speed
speed = 5

# Set up destination points
point_a = 50
point_b = 750
destination = point_b

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the Rect
    if rect.x < destination:
        rect.x += speed
    elif rect.x > destination:
        rect.x -= speed

    # Check if the Rect reached the destination
    if rect.x == destination:
        # Swap destination points
        if destination == point_a:
            destination = point_b
        else:
            destination = point_a

    # Draw the background
    screen.fill(white)

    # Draw the Rect
    pygame.draw.rect(screen, red, rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
