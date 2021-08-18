import pygame, sys, random, time
import game

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

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
        pipe.centerx -= 3
    visible_pipes = [pipe for pipe in pipe_list if pipe.right > - 50]
    return visible_pipes

def draw_pipes(screen, SCREEN_HEIGHT, pipe_list, pipe_surface):
    for pipe in pipe_list:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def run(char_index):
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN_WIDTH = 576
    SCREEN_HEIGHT = 1024
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    foreground = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    game_font = pygame.font.Font('04B_19.ttf', 30)

    bg_surface = pygame.image.load('sprites/background-day.png').convert()
    bg_surface = pygame.transform.scale2x(bg_surface)
    floor_surface = pygame.image.load('sprites/base.png').convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0

    pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list = []
    pipe_height = [400, 500, 600, 700, 800]
    SPAWN_PIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWN_PIPE, 1500)

    start = time.time()
    seconds = random.randint(3, 5)
    while True:
        end = time.time()
        elapsed = end - start
        if elapsed >= seconds:
            game.game(char_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWN_PIPE:
                pipe_list.extend(create_pipe(pipe_height, pipe_surface))
        
        screen.blit(bg_surface, (0, 0))
        pipe_list = move_pipes(pipe_list)
        draw_pipes(screen, SCREEN_HEIGHT, pipe_list, pipe_surface)

        draw_rect_alpha(screen, (255, 255, 255, 127), foreground)
        draw_text('Generating pipes', game_font, pygame.Color('#ffffff'), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        draw_text('and preparing coffins..', game_font, pygame.Color('#ffffff'), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)

        floor_x_pos -= 0.5
        draw_floor(screen, SCREEN_WIDTH, floor_surface, floor_x_pos)
        if floor_x_pos <= - SCREEN_WIDTH:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)
