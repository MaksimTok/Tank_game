import pygame.sprite

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


class Leafs(pygame.sprite.Sprite):
    image = load_image('Blocks/leafs.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Leafs.image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Brick(pygame.sprite.Sprite):
    image = load_image('Blocks/brick.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, brick_group, all_sprites)
        self.image = Brick.image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.hp = 100

    def update(self, *args):
        if self.hp <= 0:
            self.kill()


class Unbreak(pygame.sprite.Sprite):
    image = load_image('Blocks/unbreak.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, unbreak_group, all_sprites)
        self.image = Unbreak.image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tank_type):
        super().__init__(player_group, all_sprites)
        self.tank_type = tank_type
        self.player_vel = "top"
        self.player_image = {"top": [load_image(f'Tanks/Player/Type{self.tank_type}/top1.png'),
                                     load_image(f'Tanks/Player/Type{self.tank_type}/top2.png')],
                             "down": [load_image(f'Tanks/Player/Type{self.tank_type}/down1.png'),
                                      load_image(f'Tanks/Player/Type{self.tank_type}/down2.png')],
                             "left": [load_image(f'Tanks/Player/Type{self.tank_type}/left1.png'),
                                      load_image(f'Tanks/Player/Type{self.tank_type}/left2.png')],
                             "right": [load_image(f'Tanks/Player/Type{self.tank_type}/right1.png'),
                                       load_image(f'Tanks/Player/Type{self.tank_type}/right2.png')]}
        self.count = 0
        self.image = self.player_image[self.player_vel][self.count]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.kd = 0
        self.hp = 100
        self.x, self.y = self.rect.x, self.rect.y

    def draw(self):
        self.count = (self.count + 1) % len(self.player_image[self.player_vel])
        self.image = self.player_image[self.player_vel][self.count]
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= tile_width // 3
            self.player_vel = "left"
        elif keys[pygame.K_RIGHT]:
            self.rect.x += tile_width // 3
            self.player_vel = "right"
        elif keys[pygame.K_UP]:
            self.rect.y -= tile_height // 3
            self.player_vel = "top"
        elif keys[pygame.K_DOWN]:
            self.rect.y += tile_height // 3
            self.player_vel = "down"
        if keys[pygame.K_SPACE] and self.kd <= 0:
            if self.player_vel == "down":
                vx, vy = 0, 1
            elif self.player_vel == "top":
                vx, vy = 0, -1
            elif self.player_vel == "left":
                vx, vy = -1, 0
            elif self.player_vel == "right":
                vx, vy = 1, 0
            Bullet(self.x + tile_width // 2, self.y + tile_height // 2, vx, vy)
            self.kd = 2 * fps
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.x, self.rect.y = self.x, self.y
        else:
            self.x, self.y = self.rect.x, self.rect.y
        self.draw()
        self.kd -= 1


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        super().__init__(bullet_group, all_sprites)
        self.image = pygame.Surface((4, 4))
        pygame.draw.circle(self.image, pygame.Color("white"), (2, 2), 2)
        self.vx, self.vy = vel_x, vel_y
        self.rect = self.image.get_rect().move(pos_x + (tile_width // 2 * vel_x), pos_y + (tile_height // 2 * vel_y))

    def update(self, *args):
        self.rect.x += self.vx * 10
        self.rect.y += self.vy * 10
        if player := pygame.sprite.spritecollideany(self, player_group):
            player.hp -= 5
        elif brick := pygame.sprite.spritecollideany(self, brick_group):
            brick.hp -= 35

        if pygame.sprite.spritecollideany(self, tiles_group) or pygame.sprite.spritecollideany(self, player_group):
            self.kill()