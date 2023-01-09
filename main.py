import pygame
from classes import *
import settings


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
            elif level[y][x] == "@":
                player_x, player_y = x, y
    [Brick(x, y) for x, y in brick]
    [Unbreak(x, y) for x, y in unbreak]
    player = Tank(player_x, player_y, settings.tank_type)
    [Leafs(x, y) for x, y in leafs]
    return player, x, y


pygame.init()
pygame.display.set_caption('Танчики')
clock = pygame.time.Clock()


def game(*args):
    screen.fill((0, 0, 0))
    button_group.empty()
    tiles_group.empty()
    all_sprites.empty()

    board = load_level(settings.maps[settings.map_id - 1])
    player, level_x, level_y = generate_level(board)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == 27:
                settings.pause = True
        if settings.pause == True:
            pause()
        screen.fill((0, 0, 0))
        all_sprites.update()
        clock.tick(fps)
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    game()
