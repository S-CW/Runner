import pygame
import sys


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotating Image")


image = pygame.image.load("./graphics/Player/player_stand.png")  # Replace with the path to your image file
angle = 0
rotation_speed = 2  # Adjust the speed as needed


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Rotate the image
    rotated_image = pygame.transform.rotate(image, angle)

    # Get the rectangle of the rotated image and center it on the screen
    rect = rotated_image.get_rect(center=(width // 2, height // 2))

    # Draw the rotated image on the screen
    screen.blit(rotated_image, rect.topleft)

    # Update the display
    pygame.display.flip()

    # Increment the rotation angle
    angle += rotation_speed

    # Limit the frame rate (optional, but recommended)
    pygame.time.delay(10)  # Adjust the delay as needed
