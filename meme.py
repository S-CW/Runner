import pygame
import time
import sys
import os
import re

pygame.init()
start_time = pygame.time.get_ticks()
delay = 5000
mikeohearn_appear = False
screen = pygame.display.set_mode((800,400)) # window size

music1_path = 'audio/music.wav'  # replace with the path to your music file
music2_path = 'audio/what-is-love.mp3'  # replace with the path to your second music file

class playGif(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, folder_path):
        super().__init__()
        def extract_number(filename):
            match = re.search(r'\d+', filename)
            return int(match.group()) if match else float('inf')
            
        self.files = os.listdir(folder_path)
        self.scale = scale
        self.images = []
        
        self.files.sort(key=extract_number)

        for file in self.files:
            
            img = pygame.image.load(f"{folder_path}/{file}").convert_alpha()

            if self.scale != 0:
                img = pygame.transform.scale(img, (img.get_size()[0] * self.scale, img.get_size()[1] * self.scale))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def animate(self):
        animation_speed = 1
        self.counter += 1

        # self.flip(self.image)
        if self.counter >= animation_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1

        if self.index >= len(self.images) - 1:
            self.index = 0

        self.image = self.images[int(self.index)]

    def update(self):
        self.animate()


richardo = playGif(400, 600, 1.5, 'graphics/richardo2')
bg = playGif(400, 200, 0, 'graphics/party')


mike_surf = pygame.image.load('graphics/mikeohearn.png')
mike_rect = mike_surf.get_rect(center = (1000, 300))
x = 800

# Set up variables
condition_met = False
frame_index = 0
destination = 400
direction = 'left'
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
                if not mikeohearn_appear:
                    pygame.mixer.music.pause()
                    mikeohearn_appear = True

                    # Load and play music2 only once
                    pygame.mixer.music.load(music2_path)
                    pygame.mixer.music.play(1)  # 1 means play once
                    screen.blit(mike_surf, (x, 200))

                    # Set the time to resume music1 after music2 has played
                    resume_time = time.time() + pygame.mixer.Sound(music2_path).get_length()

    # bg.draw(screen)
    # bg.update()
    screen.fill("black")

    richardo.draw(screen)
    richardo.update()
    
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

    

    if richardo.rect.y >= 80:
        richardo.rect.y -= 15
    
    if mikeohearn_appear:
        screen.blit(mike_surf, mike_rect)

    if direction == 'left':
        mike_rect.x -= 2

        if mike_rect.left <= 500:
            direction = 'right'
    elif direction == 'right':
        mike_rect.x += 2

        if mike_rect.x == 600:
            direction = 'left'

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

    time.sleep(0.1)
