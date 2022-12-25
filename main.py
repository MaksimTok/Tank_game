import pygame
from settings import *
from classes import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Battle city')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    running = True
    tank = Tank('Type1', 100, 100, all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
