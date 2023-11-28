import pygame
import imageio
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GIF in Pygame")

# Load the GIF using imageio
gif_path = 'graphics/ricardo milos.gif'
gif = imageio.mimread(gif_path)
frames = [pygame.surfarray.make_surface(img) for img in gif]

mike_surf = pygame.image.load('graphics/mikeohearn.png')

# Set up variables
frame_index = 0
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rotate the frame before displaying
    rotated_frame = pygame.transform.rotate(frames[frame_index], 90)

    # Display the current frame
    screen.blit(rotated_frame, (0, 0))
    screen.blit(mike_surf, (300, 400))

    rotated_frame.get_rect()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)

    # Move to the next frame
    frame_index = (frame_index + 1) % len(frames)
