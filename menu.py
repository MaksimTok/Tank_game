import pygame
from classes import *
import settings
from main import game


pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Танчики')
clock = pygame.time.Clock()

def tank_type(*args):

    def newtype(button):
        settings.type = int(button.name[-1])
        tank_type()

    screen.fill((0, 0, 0))
    button_group.empty()

    font = pygame.font.Font("fonts/PixelFont.ttf", 65)
    string_rendered = font.render("Тип Танков", 1, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)
    id = 1
    for j in range(4):
        for i in range(1, 3):
            image = load_image(f'Tanks/Player/Type{id}/top1.png')
            rect = image.get_rect().move(i * 300 - 200, 150 + j * 130)
            screen.blit(image, rect)

            tank_info = settings.tank_settings[id]
            specific = ["hp", "damage", "wspeed", "hspeed"]

            font = pygame.font.Font("fonts/PixelFont.ttf", 10)

            string_rendered = font.render(f"{' '.join(f'{specific[i]}: {tank_info[i]};' for i in range(2))}", 1, pygame.Color('orange'))
            intro_rect = string_rendered.get_rect()
            intro_rect.y = 200 + j * 130
            intro_rect.x = i * 300 - 200
            screen.blit(string_rendered, intro_rect)

            string_rendered = font.render(f"{' '.join(f'{specific[i]}: {tank_info[i]};' for i in range(2, 4))}", 1,
                                          pygame.Color('orange'))
            intro_rect = string_rendered.get_rect()
            intro_rect.y = 220 + j * 130
            intro_rect.x = i * 300 - 200
            screen.blit(string_rendered, intro_rect)

            if id == settings.type:
                tank_type_btn = Button(f"Танк {id}", pygame.Color('green'), i * 300 - 200, 240 + j * 130, 20)
            else:
                tank_type_btn = Button(f"Танк {id}", pygame.Color('orange'), i * 300 - 200, 240 + j * 130, 20)
            tank_type_btn.onclick(newtype)
            id += 1

    return_btn = Button("Назад", pygame.Color('orange'), 50, 675)
    return_btn.onclick(menu)


def menu(*args):
    screen.fill((0, 0, 0))
    button_group.empty()

    font = pygame.font.Font("fonts/PixelFont.ttf", 90)
    string_rendered = font.render("Танчики", 1, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)

    start_btn = Button("Начать", pygame.Color('orange'), 50, 300)
    start_btn.onclick(game)

    tank_type_btn = Button("Выбрать танк", pygame.Color('orange'), 50, 375)
    tank_type_btn.onclick(tank_type)

    map_type_btn = Button("Выбрать карту", pygame.Color('orange'), 50, 450)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        button_group.update()
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    menu()
