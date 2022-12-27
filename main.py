import os
import sys
import pygame
from classes import *
from settings import *


def generate_level(level):
    player_x, player_y, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Empty('empty', x, y)
            elif level[y][x] == '#':
                Brick('wall', x, y)
            elif level[y][x] == '@':
                Empty('empty', x, y)
                player_x, player_y = x, y

    return Tank(player_x, player_y,1), x, y


pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Танчики')
clock = pygame.time.Clock()

if __name__ == '__main__':
    player, level_x, level_y = generate_level(board)
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            all_sprites.update(event)
        all_sprites.update()
        clock.tick(fps)
        all_sprites.draw(screen)
        pygame.display.flip()
