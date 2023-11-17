import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    sprite_initial_speed = 0
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.speed = Player.sprite_initial_speed
        self.acceleration = 0.0005

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            gameSound.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        self.speed += 0.1 * self.acceleration

        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:            
            self.player_index += (0.1 + self.speed)
            
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class GameSound():
    def __init__(self):
        self.default_volume = 0.5
        self.volume = 0.5
        self.is_mute = False

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(self.default_volume)

    def background_music(self):
        self.increase_volume()
        self.decrease_volume()
        pygame.mixer.music.load('audio/music.wav')
        pygame.mixer.music.set_volume(self.default_volume)
        pygame.mixer.music.play(loops = -1)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        self.jump_sound.set_volume(volume)

    def adjust_volume(self, change):
        if change == -1:
            self.decrease_volume()
        else:
            self.increase_volume()


    def increase_volume(self):
        if self.volume <= 1:
            self.volume += 0.02
            self.set_volume(self.volume)


    def decrease_volume(self):
        if self.volume >= 0:
            self.volume -= 0.02
            self.set_volume(self.volume)

    def mute(self):
        if self.is_mute:
            self.set_volume(self.volume)
            self.is_mute = False
        else:
            self.set_volume(0)
            self.is_mute = True


class Obstacle(pygame.sprite.Sprite):
    sprite_initial_speed = 6
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.speed = Obstacle.sprite_initial_speed
        self.acceleration = 0.0001
        self.action_speed = 0

    def animation_state(self):
        self.action_speed += 0.1 * 0.0005
        self.animation_index += (0.1 + self.action_speed) 
        if self.animation_index > len(self.frames): self.animation_index = 0
        
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            Obstacle.sprite_initial_speed = self.speed
            self.kill()

    def update(self):
        self.animation_state()

        # Max speed 50
        if self.speed < 50:
            self.speed += self.acceleration * score
        self.rect.x -= self.speed

        self.destroy()


def display_score():
    # latest time - start game time - time paused
    current_time = int(pygame.time.get_ticks() / 1000) - start_time - elapse_time

    score_surf = font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)

    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800,400)) # window size
pygame.display.set_caption("Runner") # window title
clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 50)
start_time = 0
score = 0
game_active = False

gameSound = GameSound()


####################    groups    ####################
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()


####################    background    ####################
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()


####################    intro screen    ####################
player_stand = pygame.image.load("./graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))


####################    timer    ####################
obstacle_timer = pygame.USEREVENT + 1 # create a custom event
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


####################    text    ####################
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect(center = (x, y))
    surface.blit(text_obj, text_rect)

    return text_rect

# Game screen
gameSound.background_music()

# Setting screen
def settings():
    running = True
    text_col = (255, 255, 255)
    while running:
        current_time = int(pygame.time.get_ticks() / 1000) - stopped_time

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            
        screen.fill((0, 0, 0))
        draw_text('Settings', font, text_col, screen, 400, 100)
        RESUME = draw_text('Resume game', font, text_col, screen, 400, 175)
        OPTIONS = draw_text('Options', font, text_col, screen, 400, 225)
        QUIT = draw_text('Quit', font, text_col, screen, 400, 275)

        mouse_pos = pygame.mouse.get_pos()
        if RESUME.collidepoint(mouse_pos):
            draw_text('Resume game', font, (255, 255, 0), screen, 400, 175)
            if click:
                running = False
        if OPTIONS.collidepoint(mouse_pos):
            draw_text('Options', font, (255, 255, 0), screen, 400, 225)
            if click:
                options()
        if QUIT.collidepoint(mouse_pos):
            draw_text('Quit', font, (255, 255, 0), screen, 400, 275)
            if click:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
    
    return current_time

# Option screen
def options():
    running = True
    text_col = (255, 255, 255)
    mute = False
    mute_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    mute_font.set_strikethrough(True)
    mouse_hold = False
    target_time = 0
    delay = 500 # delay in miliseconds

    def handle_volume_control(mouse_stat, mouse_pos, volume, timer, target_time, delay, click):
        if SOUND_DECREASE.collidepoint(mouse_pos):
            draw_text('-', font, (255, 255, 0), screen, 475, 175)
            return volume_change(mouse_stat, volume, timer, target_time, delay, click, -1)
    

        if SOUND_INCREASE.collidepoint(mouse_pos):
            draw_text('+', font, (255, 255, 0), screen, 575, 175)
            return volume_change(mouse_stat, volume, timer, target_time, delay, click, 1)
            

    def volume_change(mouse_stat, volume, timer, target_time, delay, click, change):
        if mouse_stat[0] and 0 <= volume + change <= 100:
            if timer >= target_time or click:
                gameSound.adjust_volume(change)
                draw_text(f'{volume}', font, text_col, screen, 525, 175)

                target_time = timer + delay
                return target_time
        return target_time

    while running:
        volume = round(gameSound.volume * 100)
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to setting screen
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        timer = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        mouse_stat = pygame.mouse.get_pressed()

        if mouse_stat[0]:
            if not mouse_hold:
                mouse_hold = True
                target_time = timer + delay
            elif timer >= target_time:
                delay /= 1.6
        else:
            mouse_hold = False
            delay = 500

        screen.fill((0, 0, 0))
        draw_text('Settings', font, text_col, screen, 400, 100)
        draw_text('Sound: ', font, text_col, screen, 400, 175)
        draw_text(f'{volume}', font, text_col, screen, 525, 175)

        # Buttons
        SOUND_DECREASE = draw_text('-', font, text_col, screen, 475, 175)
        SOUND_INCREASE = draw_text('+', font, text_col, screen, 575, 175)
        MUTE = draw_text('Mute', font, text_col, screen, 400, 225)
        BACK = draw_text('Back', font, text_col, screen, 400, 275)

        if mute == True:
            draw_text('Mute', mute_font, text_col, screen, 400, 225)
        if MUTE.collidepoint(mouse_pos):
            draw_text('Mute', font, (255, 255, 0), screen, 400, 225)
            if click:
                gameSound.mute()
                mute = not mute

        result = handle_volume_control(mouse_stat, mouse_pos, volume, timer, target_time, delay, click)
        target_time = result if result else target_time

        if BACK.collidepoint(mouse_pos):
            draw_text('Back', font, (255, 255, 0), screen, 400, 275)
            if click:
                running = False

        pygame.display.update()
        clock.tick(60)


elapse_time = 0
while True:
    pause = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                stopped_time = int(pygame.time.get_ticks() / 1000)
                elapse_time += settings()

        if not game_active: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # sprite_initial speed is set before add sprite
                    Obstacle.sprite_initial_speed = 6
                    Player.sprite_initial_speed = 0

                    player.add(Player())
                    game_active = True

                    start_time = int(pygame.time.get_ticks() / 1000)
                    elapse_time = 0
            
                if event.key == pygame.K_m:
                    gameSound.mute()
        
        if game_active:
            # when custom event is triggered by the timer, add sprite obstacle
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                gameSound.mute()
        
    if game_active:
        # background
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        score = display_score()

        # player
        player.draw(screen)
        player.update()

        # obstacle movement
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        game_name = draw_text("Pixel Runner", font, (111,196,169), screen, 400, 80)

        score_message = font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            game_mesage = draw_text("Press space to run", font, (111,196,169), screen, 400, 340)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60) # should not run faster than 60fps aka max fps
