import pygame
import time
import imageio
import sys

pygame.init()
start_time = pygame.time.get_ticks()
delay = 5000
mikeohearn_appear = False
screen = pygame.display.set_mode((800,400)) # window size

music1_path = 'audio/music.wav'  # replace with the path to your music file
music2_path = 'audio/baby-dont-hurt-me.wav'  # replace with the path to your second music file


sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Load the GIF using imageio
gif_path = 'graphics/ricardo milos.gif'
gif = imageio.mimread(gif_path)
frames = [pygame.surfarray.make_surface(img) for img in gif]


mike_surf = pygame.image.load('graphics/mikeohearn.png')
mike_rect = mike_surf.get_rect(center = (1000, 300))
x = 800

# Set up variables
condition_met = False
frame_index = 0
clock = pygame.time.Clock()

pygame.mixer.music.load(music1_path)
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

while True:
    current_time = pygame.time.get_ticks()

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
                    screen.blit(mike_surf, (x, 200))

                    # Set the time to resume music1 after music2 has played
                    resume_time = time.time() + pygame.mixer.Sound(music2_path).get_length()

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    
    elapse_time = current_time - start_time
    if elapse_time >= delay and not mikeohearn_appear:
        pygame.mixer.music.pause()
        mikeohearn_appear = True

        # Load and play music2 only once
        pygame.mixer.music.load(music2_path)
        pygame.mixer.music.play(1)  # 1 means play once

        # Set the time to resume music1 after music2 has played
        resume_time = time.time() + pygame.mixer.Sound(music2_path).get_length()

    # Check if music2 is still playing
    if mikeohearn_appear and not pygame.mixer.music.get_busy():
        # Check if it's time to resume music1
        if time.time() >= resume_time:
            pygame.mixer.music.load(music1_path)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    # Rotate the frame before displaying
    rotated_frame = pygame.transform.rotate(frames[frame_index], 90)

    # Display the current frame
    screen.blit(rotated_frame, (0, 0))
    
    if mikeohearn_appear:
        screen.blit(mike_surf, mike_rect)

    mike_rect.x -= 2
    if mike_rect.left < 400:
        mike_rect.x += 4
    # else:
        
    
    # mike_rect.move(x, 200)
    print(mike_rect.left)
    

    rotated_frame.get_rect()

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(10)

    # Move to the next frame
    frame_index = (frame_index + 1) % len(frames)

    time.sleep(0.1)
