import os
import sys

import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('Sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


SIZE = WIDTH, HEIGHT = 675, 720
fps = 24
type = 1
board = load_level('maps1.txt')
tile_width, tile_height = 45, 48
all_sprites = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
unbreak_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
screen = pygame.display.set_mode(SIZE)
blocks = ["#", "$", "W"]

#              [hp, damage, wspeed, hspeed]
tank_settings = {1: [30, 35, 9, 12],  # из-за разницы между шириной и высотой клетки пришлось делать две скорости
                 2: [60, 35, 9, 12],  # вертикальную и горизонтальную и так во всех типах
                 3: [60, 50, 9, 12],
                 4: [100, 35, 9, 12],
                 5: [60, 35, 15, 16],
                 6: [30, 35, 15, 16],
                 7: [60, 50, 15, 16],
                 8: [110, 50, 9, 12]}
