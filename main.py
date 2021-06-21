from typing import ChainMap
import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + SCREEN_WIDTH, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > - 50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False
    return True
    
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (SCREEN_WIDTH/2, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (SCREEN_WIDTH/2, 100))
        screen.blit(score_surface, score_rect)

        highscore_surface = game_font.render(f'Highscore: {int(highscore)}' , True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center = (SCREEN_WIDTH/2, 850))
        screen.blit(highscore_surface, highscore_rect)

def update_score(score, highscore):
    if score > highscore:
        highscore = score
    return highscore

def pipe_score_check(score, scoring_active):
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and scoring_active:
                score += 1
                score_sound.play()
                scoring_active = False
            if pipe.centerx < 0:
                scoring_active = True
    return score

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_font = pygame.font.Font('04B_19.ttf', 40)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
highscore = 0
can_score = True

bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, SCREEN_HEIGHT/2))

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400, 500, 600, 700, 800]
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

flap_sound = pygame.mixer.Sound('audio/sfx_wing.wav')
death_sound = pygame.mixer.Sound('audio/sfx_hit.wav')
score_sound = pygame.mixer.Sound('audio/sfx_point.wav')
score_sound_countdown = 100


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_movement = 0
                score = 0
                bird_rect.center = (100, SCREEN_HEIGHT/2)
                score_sound_countdown = 100
        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # score
        score = pipe_score_check(score, can_score)
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        highscore = update_score(score, highscore)
        score_display('game_over')
        

    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= - SCREEN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)