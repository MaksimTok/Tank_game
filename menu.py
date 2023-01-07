import pygame
from classes import *
from settings import *
from main import game


pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Танчики')
clock = pygame.time.Clock()

def tank_type():
    screen.fill((0, 0, 0))
    button_group.empty()

    font = pygame.font.Font("fonts/PixelFont.ttf", 65)
    string_rendered = font.render("Тип Танков", 1, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)
    type = 1
    for i in range(1, 5):
        for j in range(2):
            image = load_image(f'Tanks/Player/Type{type}/top1.png')
            rect = image.get_rect().move(i * 150 - 100, 325 + j * 150)
            screen.blit(image, rect)
            tank_type_btn = Button(f"Танк {type}", pygame.Color('orange'), i * 150 - 100, 375 + j * 150, 20)
            type += 1

    return_btn = Button("Назад", pygame.Color('orange'), 50, 625)
    return_btn.onclick(menu)

def menu():
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

if __name__ == '__main__':
    menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        button_group.update()
        pygame.display.flip()
        clock.tick(fps)
