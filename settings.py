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
fps = 20
board = load_level('maps1.txt')
tile_width, tile_height = 45, 48
all_sprites = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
unbreak_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
blocks = ["#", "$", "W"]