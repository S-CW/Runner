import pygame
import time
import imageio
import sys

pygame.init()
screen = pygame.display.set_mode((800,400)) # window size

music1_path = 'audio/music.wav'  # replace with the path to your music file
music2_path = 'audio/baby-dont-hurt-me.wav'  # replace with the path to your second music file


# Load the GIF using imageio
gif_path = 'graphics/ricardo milos.gif'
gif = imageio.mimread(gif_path)
frames = [pygame.surfarray.make_surface(img) for img in gif]

mike_surf = pygame.image.load('graphics/mikeohearn.png')
mike_rect = mike_surf.get_rect(center = (400, 200))

# Set up variables
condition_met = False
frame_index = 0
clock = pygame.time.Clock()

pygame.mixer.music.load(music1_path)
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Check for a specific key press (change to the key you want)
            if event.key == pygame.K_SPACE:
                if not condition_met:
                    pygame.mixer.music.pause()
                    condition_met = True

                    # Load and play music2 only once
                    pygame.mixer.music.load(music2_path)
                    pygame.mixer.music.play(1)  # 1 means play once

                    # Set the time to resume music1 after music2 has played
                    resume_time = time.time() + pygame.mixer.Sound(music2_path).get_length()

    # Check if music2 is still playing
    if condition_met and not pygame.mixer.music.get_busy():
        # Check if it's time to resume music1
        if time.time() >= resume_time:
            pygame.mixer.music.load(music1_path)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            condition_met = False

    # Rotate the frame before displaying
    rotated_frame = pygame.transform.rotate(frames[frame_index], 90)

    # Display the current frame
    screen.blit(rotated_frame, (0, 0))
    screen.blit(mike_surf)

    mike_rect.x += 10
    if mike_rect.left > 300:
        mike_rect.x += 1
    

    rotated_frame.get_rect()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)

    # Move to the next frame
    frame_index = (frame_index + 1) % len(frames)

    time.sleep(0.1)
