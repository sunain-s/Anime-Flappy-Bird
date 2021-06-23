import pygame, sys, main

def draw_floor(floor_surface, floor_x_pos):
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + SCREEN_WIDTH, 900))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def select_box(surface, colour, char_rect):
    select_rect = pygame.Rect(char_rect.left - 10, char_rect.top - 10, char_rect.right - char_rect.left + 15, char_rect.bottom - char_rect.top + 15)
    select_rect.center = (char_rect.centerx, char_rect.centery)
    pygame.draw.rect(surface, colour, select_rect, 5)


pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_font = pygame.font.Font('04B_19.ttf', 40)


def run():
    bg_surface = pygame.image.load('sprites/background-day.png').convert()
    bg_surface = pygame.transform.scale2x(bg_surface)

    floor_surface = pygame.image.load('sprites/base.png').convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0

    start_button = pygame.Rect(SCREEN_WIDTH/2 - 150, 800, 300, 50)

    # characters
    bird_surface = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
    bird_rect = bird_surface.get_rect(center = (SCREEN_WIDTH/2, 200))

    naruto_surface = pygame.transform.scale2x(pygame.image.load('sprites/naruto-2.png').convert_alpha())
    naruto_rect = naruto_surface.get_rect(center = (SCREEN_WIDTH/2, 300))

    l_surface = pygame.transform.scale2x(pygame.image.load('sprites/L-2.png').convert_alpha())
    l_rect = l_surface.get_rect(center = (SCREEN_WIDTH/2, 400))

    light_surface = pygame.transform.scale2x(pygame.image.load('sprites/Light-2.png').convert_alpha())
    light_rect = light_surface.get_rect(center = (SCREEN_WIDTH/2, 500))

    click = False
    char_selected = True
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        
        screen.blit(bg_surface, (0, 0))
        draw_text('Select Character', game_font, (255, 255, 255), screen, SCREEN_WIDTH/2, 100)
        screen.blit(bird_surface, bird_rect)
        screen.blit(naruto_surface, naruto_rect)
        screen.blit(l_surface, l_rect)
        screen.blit(light_surface, light_rect)
        pygame.draw.rect(screen, pygame.Color('#a7a69d'), start_button)
        draw_text('Click to start', game_font, (255, 255, 255), screen, start_button.centerx, start_button.centery)

        
        if click:
            if bird_rect.collidepoint(mx, my):
                select_box(screen, pygame.Color('#a7a69d'), bird_rect)
                char_selected = True
        if click:
            if naruto_rect.collidepoint(mx, my):
                select_box(screen, pygame.Color('#a7a69d'), naruto_rect)
                char_selected = True
        if click:
            if l_rect.collidepoint(mx, my):
                select_box(screen, pygame.Color('#a7a69d'), l_rect)
                char_selected = True
        if click:
            if light_rect.collidepoint(mx, my):
                select_box(screen, pygame.Color('#a7a69d'), light_rect)
                char_selected = True
        if start_button.collidepoint(mx, my):
            if char_selected and click:
                main.run()
        # floor
        floor_x_pos -= 1
        draw_floor(floor_surface, floor_x_pos)
        if floor_x_pos <= - SCREEN_WIDTH:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)
if __name__ == '__main__':
    run()