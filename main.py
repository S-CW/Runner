import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400)) # window size
pygame.display.set_caption("Runner") # window title
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    pygame.display.update()
    clock.tick(60) # should not run faster than 60fps aka max fps
