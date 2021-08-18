import pygame, sys, random
import menu

def draw_floor(screen, SCREEN_WIDTH, floor_surface, floor_x_pos):
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + SCREEN_WIDTH, 900))

def create_pipe(pipe_height, pipe_surface):
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipe_list if pipe.right > - 50]
    return visible_pipes

def draw_pipes(screen, SCREEN_HEIGHT, pipe_list, pipe_surface):
    for pipe in pipe_list:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipe_list, bird_rect, can_score, death_sound):
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False
    return True
    
def rotate_bird(bird_surface, bird_movement):
    new_bird = pygame.transform.rotozoom(bird_surface, - bird_movement * 3, 1)
    return new_bird

def bird_animation(bird_frames, bird_index, bird_rect):
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(screen, SCREEN_WIDTH, game_font, game_state, score, highscore):
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

def pipe_score_check(score, scoring_active, pipe_list, score_sound):
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and scoring_active:
                score += 1
                score_sound.play()
                scoring_active = False
            if pipe.centerx < 0:
                scoring_active = True
    return score

def game(char_index):
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN_WIDTH = 576
    SCREEN_HEIGHT = 1024
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_font = pygame.font.Font('04B_19.ttf', 40)

    # game variables
    gravity = 0.25
    bird_movement = 0
    game_active = False
    score = 0
    highscore = 0
    can_score = True

    bg_surface = pygame.image.load('sprites/background-day.png').convert()
    bg_surface = pygame.transform.scale2x(bg_surface)

    floor_surface = pygame.image.load('sprites/base.png').convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0

    image = [['sprites/bluebird-downflap.png', 'sprites/bluebird-midflap.png', 'sprites/bluebird-upflap.png'],
            ['sprites/Naruto-1.png', 'sprites/Naruto-2.png', 'sprites/Naruto-3.png'],
            ['sprites/L-1.png', 'sprites/L-2.png', 'sprites/L-3.png'],
            ['sprites/Luffy-1.png', 'sprites/Luffy-2.png', 'sprites/Luffy-3.png'],
            ['sprites/Light-1.png', 'sprites/Light-2.png', 'sprites/Light-3.png'],
            ['sprites/Hisoka-1.png', 'sprites/Hisoka-2.png', 'sprites/Hisoka-3.png']
            ]
    bird_downflap = pygame.transform.scale2x(pygame.image.load(image[char_index][0]).convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load(image[char_index][1]).convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load(image[char_index][2]).convert_alpha())
    bird_frames = [bird_downflap, bird_midflap, bird_upflap]
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center = (100, SCREEN_HEIGHT/2))
    BIRD_FLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRD_FLAP, 400)

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

    timer = 20

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    menu.run()
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 10
                    flap_sound.play()
                if event.key == pygame.K_SPACE and not game_active and timer <= 0:
                    pipe_list = []
                    timer = 20
                    game_active = True
                    bird_movement = 0
                    score = 0
                    bird_rect.center = (100, SCREEN_HEIGHT/2)
            if event.type == SPAWN_PIPE:
                pipe_list.extend(create_pipe(pipe_height, pipe_surface))
            if event.type == BIRD_FLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird_surface, bird_rect = bird_animation(bird_frames, bird_index, bird_rect)

        screen.blit(bg_surface, (0, 0))

        if game_active:
            # bird
            bird_movement += gravity
            rotated_bird = rotate_bird(bird_surface, bird_movement)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list, bird_rect, can_score, death_sound)

            # pipes
            pipe_list = move_pipes(pipe_list)
            draw_pipes(screen, SCREEN_HEIGHT, pipe_list, pipe_surface)

            # score
            score = pipe_score_check(score, can_score, pipe_list, score_sound )
            score_display(screen, SCREEN_WIDTH, game_font, 'main_game', score, highscore)
        else:
            timer -= 1
            screen.blit(game_over_surface, game_over_rect)
            highscore = update_score(score, highscore)
            score_display(screen, SCREEN_WIDTH, game_font, 'game_over', score, highscore)
            

        # floor
        floor_x_pos -= 1
        draw_floor(screen, SCREEN_WIDTH, floor_surface, floor_x_pos)
        if floor_x_pos <= - SCREEN_WIDTH:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)