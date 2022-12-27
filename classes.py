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


class Brick(pygame.sprite.Sprite):
    image = load_image('Blocks/brick0.1.png')
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = Brick.image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.hp = 100

class Empty(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.Surface((tile_width, tile_height))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tank_type):
        super().__init__(player_group, all_sprites)
        self.tank_type = tank_type
        self.player_vel = "top"
        self.player_image = {"top": [load_image(f'Tanks/Player/Type{self.tank_type}/top10.1.png'),
                                     load_image(f'Tanks/Player/Type{self.tank_type}/top20.1.png')],
                             "down": [load_image(f'Tanks/Player/Type{self.tank_type}/down10.1.png'),
                                      load_image(f'Tanks/Player/Type{self.tank_type}/down20.1.png')],
                             "left": [load_image(f'Tanks/Player/Type{self.tank_type}/left10.1.png'),
                                      load_image(f'Tanks/Player/Type{self.tank_type}/left20.1.png')],
                             "right": [load_image(f'Tanks/Player/Type{self.tank_type}/right10.1.png'),
                                       load_image(f'Tanks/Player/Type{self.tank_type}/right20.1.png')]}
        self.count = 0
        self.image = self.player_image[self.player_vel][self.count]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x, self.y = tile_width * pos_x, tile_height * pos_y

    def draw(self):
        self.count = (self.count + 1) % len(self.player_image[self.player_vel])
        self.image = self.player_image[self.player_vel][self.count]
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= tile_width
            self.player_vel = "left"
        elif keys[pygame.K_RIGHT]:
            self.x += tile_width
            self.player_vel = "right"
        elif keys[pygame.K_UP]:
            self.y -= tile_height
            self.player_vel = "top"
        elif keys[pygame.K_DOWN]:
            self.y += tile_height
            self.player_vel = "down"
        if board[self.y // tile_height][self.x // tile_width] == "#":
            self.x, self.y = self.rect.x, self.rect.y
        self.draw()


class TankType1(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 1)


class TankType2(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 2)


class TankType3(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 3)


class TankType4(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 4)


class TankType5(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 5)


class TankType6(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 6)


class TankType7(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 7)


class TankType8(Tank):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, 8)

