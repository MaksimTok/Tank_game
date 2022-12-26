import pygame
from settings import *

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    border = 1
                else:
                    border = self.cell_size
                pygame.draw.rect(screen, 'white',
                                 pygame.Rect(self.left + j * self.cell_size, self.top + i * self.cell_size,
                                             self.cell_size, self.cell_size), width=border)

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if self.left + j * self.cell_size <= mouse_pos[0] <= \
                        self.left + j * self.cell_size + self.cell_size and \
                        self.top + i * self.cell_size <= mouse_pos[1] <= self.top + i * self.cell_size + self.cell_size:
                    return i, j
        return

    def on_click(self, cell_coords):
        if cell_coords:
            if self.board[cell_coords[0]][cell_coords[1]] == 0:
                self.board[cell_coords[0]][cell_coords[1]] = 1
            else:
                self.board[cell_coords[0]][cell_coords[1]] = 0

    def get_click(self, mouse_pos):
        self.on_click(self.get_cell(mouse_pos))



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if self.image:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        else:

            self.image = pygame.Surface((tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)



class Tank(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x, self.y = self.rect.x, self.rect.y

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].unicode.lower() == "w":
                self.y -= tile_height
            elif args[0].unicode.lower() == "s":
                self.y += tile_height
            elif args[0].unicode.lower() == "a":
                self.x -= tile_width
            elif args[0].unicode.lower() == "d":
                self.x += tile_width
            if board[self.y // tile_height][self.x // tile_width] != "#":
                self.rect.x, self.rect.y = self.x, self.y
            else:
                self.x, self.y = self.rect.x, self.rect.y



class TankType1(Tank):
    pass


class TankType2(Tank):
    pass


class TankType3(Tank):
    pass


class TankType4(Tank):
    pass


class TankType5(Tank):
    pass


class TankType6(Tank):
    pass


class TankType7(Tank):
    pass


class TankType8(Tank):
    pass
