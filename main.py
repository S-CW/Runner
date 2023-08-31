import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400)) # window size
pygame.display.set_caption("Runner") # window title
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Stationary
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
score_surf = font.render("My game", False, "Black").convert()
score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600,300))

player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300)) # rectangle size of the image


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # backgeround
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(score_surf, score_rect)


    snail_rect.left -= 4
    if snail_rect.left < -100:
        snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60) # should not run faster than 60fps aka max fps
