import pygame, sys, time
import loading

def draw_floor(screen, SCREEN_WIDTH, floor_surface, floor_x_pos):
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + SCREEN_WIDTH, 900))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def character_display_and_select(char_surface, SCREEN_WIDTH, screen, y_pos, mx, my, click, char_selected, char_index):
    char_rect = char_surface.get_rect(center = (SCREEN_WIDTH/2, y_pos))
    screen.blit(char_surface, char_rect)
    if not char_selected:
        if char_rect.collidepoint(mx, my):
                select_box(screen, pygame.Color('#ffffff'), char_rect)
        if click:
            if char_rect.collidepoint(mx, my):
                start = time.time()
                seconds = 1
                while True:
                    end = time.time()
                    elapsed = end - start
                    if elapsed >= seconds:
                        char_selected = True
                        break
            else:
                pass
    if char_selected:
        loading.run(char_index)
        
def select_box(surface, colour, char_rect):
    select_rect = pygame.Rect(char_rect.left - 10, char_rect.top - 10, char_rect.right - char_rect.left + 15, char_rect.bottom - char_rect.top + 15)
    select_rect.center = (char_rect.centerx, char_rect.centery)
    pygame.draw.rect(surface, colour, select_rect, 5)

def run():
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN_WIDTH = 576
    SCREEN_HEIGHT = 1024
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_font = pygame.font.Font('04B_19.ttf', 60)
    game_font_2 = pygame.font.Font('04B_19.ttf', 24)

    bg_surface = pygame.image.load('sprites/background-day.png').convert()
    bg_surface = pygame.transform.scale2x(bg_surface)
    floor_surface = pygame.image.load('sprites/base.png').convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0
    credit_x_pos = 0

    # characters
    bird_surface = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap_35x35.png').convert_alpha())
    naruto_surface = pygame.transform.scale2x(pygame.image.load('sprites/naruto-2.png').convert_alpha())
    l_surface = pygame.transform.scale2x(pygame.image.load('sprites/L-2.png').convert_alpha())
    luffy_surface = pygame.transform.scale2x(pygame.image.load('sprites/Luffy-2.png').convert_alpha())
    light_surface = pygame.transform.scale2x(pygame.image.load('sprites/Light-2.png').convert_alpha())
    hisoka_surface =  pygame.transform.scale2x(pygame.image.load('sprites/Hisoka-2.png').convert_alpha())
    characters = [bird_surface, naruto_surface, l_surface, luffy_surface, light_surface, hisoka_surface]

    click = False
    char_selected = False
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
        draw_text('Select Avatar', game_font, (255, 255, 255), screen, SCREEN_WIDTH/2, 100)

        for i in range(len(characters)):
            y_pos = 150 + (100 * (i+1))
            character_display_and_select(characters[i], SCREEN_WIDTH, screen, y_pos, mx, my, click, char_selected, i)

        draw_text('Click your avatar to start the game', game_font_2, (255, 255, 255), screen, SCREEN_WIDTH/2, 160)
        floor_x_pos -= 1
        draw_floor(screen, SCREEN_WIDTH, floor_surface, floor_x_pos)
        if floor_x_pos <= - SCREEN_WIDTH:
            floor_x_pos = 0

        draw_text('Default Art - samuelcust     Special Thanks To Mei For Custom Art', game_font_2, (255, 255, 255), screen, SCREEN_WIDTH + 500 + credit_x_pos, 975)
        credit_x_pos -= 1.75
        if credit_x_pos <= -1500:
            credit_x_pos = 0
        pygame.display.update()
        clock.tick(120)

if __name__ == '__main__':
    run()