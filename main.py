import pygame
from classes import *
from settings import *


def generate_level(level):
    player_x, player_y, x, y = None, None, None, None
    brick, leafs, unbreak, empty = [], [], [], []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                brick.append((x, y))
            elif level[y][x] == '$':
                unbreak.append((x, y))
            elif level[y][x] == 'L':
                leafs.append((x, y))
            elif level[y][x].isdigit():
                player_x, player_y, type = x, y, int(level[y][x])
    [Brick(x, y) for x, y in brick]
    [Unbreak(x, y) for x, y in unbreak]
    player = Tank(player_x, player_y, type)
    [Leafs(x, y) for x, y in leafs]
    return player, x, y


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
        screen.fill((0, 0, 0))
        all_sprites.update()
        clock.tick(fps)
        all_sprites.draw(screen)
        pygame.display.flip()
