from random import randint
from random import randint

import pygame.sprite

from main import p
from settings import *


class Leafs(pygame.sprite.Sprite):
    image = load_image('Blocks/leafs.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Leafs.image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Brick(pygame.sprite.Sprite):
    image = load_image('Blocks/brick.png')
    destroy = [load_image("Effects/boom1.png"), load_image("Effects/boom2.png"), load_image("Effects/boom3.png")]

    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, brick_group, all_sprites)
        self.image = Brick.image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.count = 0
        self.hp = 100

    def update(self, *args):
        if self.hp <= 0 and round(self.count) < 3:
            self.image = Brick.destroy[round(self.count)]
            self.count += 0.5
        if round(self.count) >= 3:
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
        self.start_x, self.start_y = pos_x, pos_y
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
        self.respawn_image = [load_image("Effects/spawn1.png"), load_image("Effects/spawn2.png"),
                              load_image("Effects/spawn3.png"), load_image("Effects/spawn4.png"),
                              load_image("Effects/spawn5.png"), load_image("Effects/spawn6.png")]
        self.count = 0
        self.kd = 10
        self.spawn_kd = 0
        self.image = self.player_image[self.player_vel][self.count]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x, self.y = self.rect.x, self.rect.y
        self.bullet = None
        self.hp, self.damage, self.wspeed, self.hspeed = tank_settings[tank_type]

    def respawn(self):
        self.count = 0
        self.hp = tank_settings[self.tank_type][0]
        self.player_vel = "top"
        self.spawn_kd = 10
        self.image = self.player_image[self.player_vel][self.count]
        self.rect = self.image.get_rect().move(
            tile_width * self.start_x, tile_height * self.start_y)
        self.x, self.y = self.rect.x, self.rect.y

    def draw(self):
        if self.spawn_kd > 0:
            self.count = 0 if round(self.count) >= len(self.respawn_image) else self.count
            self.image = self.respawn_image[round(self.count)]
        else:
            self.image = self.player_image[self.player_vel][round(self.count)]
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self, *args):
        if self.spawn_kd == 0:
            self.count = 0

        if self.spawn_kd <= 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.wspeed
                self.player_vel = "left"
                self.count = (self.count + 1) % 2
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.wspeed
                self.player_vel = "right"
                self.count = (self.count + 1) % 2
            elif keys[pygame.K_UP]:
                self.rect.y -= self.hspeed
                self.player_vel = "top"
                self.count = (self.count + 1) % 2
            elif keys[pygame.K_DOWN]:
                self.rect.y += self.hspeed
                self.player_vel = "down"
                self.count = (self.count + 1) % 2
            if keys[pygame.K_SPACE] and self.bullet is None and self.kd <= 0:
                if self.player_vel == "down":
                    vx, vy = 0, 1
                elif self.player_vel == "top":
                    vx, vy = 0, -1
                elif self.player_vel == "left":
                    vx, vy = -1, 0
                elif self.player_vel == "right":
                    vx, vy = 1, 0
                self.bullet = Bullet(self, self.x + tile_width // 2 - 3, self.y + tile_height // 2 - 3, vx, vy,
                                     self.damage)
                self.kd = 10
            elif self.bullet and not self.bullet.live:
                self.bullet = None
            if pygame.sprite.spritecollideany(self, tiles_group) or pygame.sprite.spritecollideany(self,
                                                                                                   borders_group) or \
                    pygame.sprite.spritecollideany(self, enemy_group):
                self.rect.x, self.rect.y = self.x, self.y
            else:
                self.x, self.y = self.rect.x, self.rect.y
            if self.kd > 0:
                self.kd -= 1
        else:
            self.count = self.count + (self.spawn_kd / len(self.respawn_image))
        self.draw()
        self.spawn_kd -= 1


class Bullet(pygame.sprite.Sprite):
    live = True

    def __init__(self, parent, pos_x, pos_y, vel_x, vel_y, damage):
        super().__init__(bullet_group, all_sprites)
        self.parent = parent
        if vel_x == 0 and vel_y == 1:
            self.image = load_image('Tanks/Bullet/bullet_down.png')
        elif vel_x == 0 and vel_y == -1:
            self.image = load_image('Tanks/Bullet/bullet_top.png')
        elif vel_x == -1 and vel_y == 0:
            self.image = load_image('Tanks/Bullet/bullet_left.png')
        elif vel_x == 1 and vel_y == 0:
            self.image = load_image('Tanks/Bullet/bullet_right.png')
        self.damage = damage
        self.vx, self.vy = vel_x, vel_y
        self.rect = self.image.get_rect().move(pos_x + (tile_width // 2 * vel_x), pos_y + (tile_height // 2 * vel_y))

    def update(self, *args):
        self.rect.x += self.vx * 20
        self.rect.y += self.vy * 20
        if (player := pygame.sprite.spritecollideany(self, player_group)) and player != self.parent:
            player.hp -= self.damage
            self.kill()
            self.live = False
        if (enemy := pygame.sprite.spritecollideany(self, enemy_group)) and enemy != self.parent:
            enemy.hp -= self.damage
            enemy.is_alive = False
            self.kill()
            self.live = False
        elif brick := pygame.sprite.spritecollideany(self, brick_group):
            brick.hp -= self.damage
            self.kill()
            self.live = False
        elif base := pygame.sprite.spritecollideany(self, base_group):
            base.hp -= self.damage
            self.kill()
            self.live = False
        elif self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()
            self.live = False


class Button(pygame.sprite.Sprite):

    def __init__(self, text, color, pos_x, pos_y, size=30):
        super().__init__(ui_group)
        self.name = text
        self.font = pygame.font.Font("fonts/PixelFont.ttf", size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.event = None
        self.args = None

    def onclick(self, func, args=None):
        self.event = func
        self.args = args

    def update(self, *args):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.args is not None:
                p.run(*self.args)
            else:
                self.event(self)


class Base(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, base_group, all_sprites)
        self.image = load_image('Blocks/base.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.hp = 100

    def update(self, *args):
        if self.hp <= 0:
            self.hp = 0
            self.image = load_image('Blocks/fall_base.png')


class SpawnPoint(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spawn_group, all_sprites)
        self.image = pygame.Surface((45, 48))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, *args):
        all_tanks = player_group.sprites() + enemy_group.sprites()
        is_free = True
        for tank in all_tanks:
            if tank.rect.colliderect(self.rect):
                is_free = False
        if is_free and randint(0, 50) == 1 and len(enemys) <= max_count_of_enemys:
            enemys.append(EnemyTank(self.rect[0] // tile_width, self.rect[1] // tile_height, randint(1, 7)))


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tank_type):
        super().__init__(enemy_group, all_sprites)
        self.tank_type = tank_type
        self.vel = "down"
        self.player_image = {"top": [load_image(f'Tanks/Enemy/Type{self.tank_type}/top1.png'),
                                     load_image(f'Tanks/Enemy/Type{self.tank_type}/top2.png')],
                             "down": [load_image(f'Tanks/Enemy/Type{self.tank_type}/down1.png'),
                                      load_image(f'Tanks/Enemy/Type{self.tank_type}/down2.png')],
                             "left": [load_image(f'Tanks/Enemy/Type{self.tank_type}/left1.png'),
                                      load_image(f'Tanks/Enemy/Type{self.tank_type}/left2.png')],
                             "right": [load_image(f'Tanks/Enemy/Type{self.tank_type}/right1.png'),
                                       load_image(f'Tanks/Enemy/Type{self.tank_type}/right2.png')]}
        self.count = 0
        self.output = []
        self.is_alive = True
        self.kd = 10
        self.image = self.player_image[self.vel][self.count]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x, self.y = self.rect.x, self.rect.y
        self.bullet = None
        self.hp, self.damage, self.wspeed, self.hspeed = tank_settings[tank_type]

    def draw(self):
        self.image = self.player_image[self.vel][self.count]
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        if self.hp <= 0:
            self.kill()
            enemys.remove(self)
        moved = self.output.index(max(self.output))
        if moved == 0:
            self.rect.x -= self.wspeed // 3
            self.vel = "left"
            self.count = (self.count + 1) % 2
        elif moved == 1:
            self.rect.x += self.wspeed // 3
            self.vel = "right"
            self.count = (self.count + 1) % 2
        elif moved == 2:
            self.rect.y -= self.hspeed // 3
            self.vel = "top"
            self.count = (self.count + 1) % 2
        elif moved == 3:
            self.rect.y += self.hspeed // 3
            self.vel = "down"
            self.count = (self.count + 1) % 2
        if moved == 4 and self.bullet is None and self.kd <= 0:
            if self.vel == "down":
                vx, vy = 0, 1
            elif self.vel == "top":
                vx, vy = 0, -1
            elif self.vel == "left":
                vx, vy = -1, 0
            elif self.vel == "right":
                vx, vy = 1, 0
            self.bullet = Bullet(self, self.x + tile_width // 2 - 3, self.y + tile_height // 2 - 3, vx, vy, self.damage)
            self.kd = 10
        elif self.bullet and not self.bullet.live:
            self.bullet = None
        if pygame.sprite.spritecollideany(self, tiles_group) or pygame.sprite.spritecollideany(self, borders_group) or \
                pygame.sprite.spritecollideany(self, player_group):
            self.rect.x, self.rect.y = self.x, self.y
        else:
            self.x, self.y = self.rect.x, self.rect.y
        if self.kd > 0:
            self.kd -= 1
        self.draw()

    def get_data(self):
        is_bullet = 0
        is_block = 0
        rects = [elem.rect for elem in tiles_group.sprites()] + [elem.rect for elem in enemy_group.sprites()] + [
            elem.rect for elem in player_group.sprites()]
        if self.bullet:
            is_bullet = 1
        for elem in rects:
            if self.vel == 'top' and self.rect.collidepoint(self.rect.x, self.rect.y - 1):
                is_block = 1
                break
            elif self.vel == 'down' and self.rect.collidepoint(self.rect.x, self.rect.y + 1):
                is_block = 1
                break
            elif self.vel == 'right' and self.rect.collidepoint(self.rect.x + 1, self.rect.y):
                is_block = 1
                break
            elif self.vel == 'left' and self.rect.collidepoint(self.rect.x - 1, self.rect.y):
                is_block = 1
                break
        return [player_group.sprites()[0].rect[0] // tile_width, player_group.sprites()[0].rect[1] // tile_height,
                base_group.sprites()[0].rect[0] // tile_width, base_group.sprites()[0].rect[1] // tile_height,
                is_block, is_bullet]

    def get_reward(self, count=1):
        return count


class Label(pygame.sprite.Sprite):

    def __init__(self, text, color, pos_x, pos_y, size=30):
        super().__init__(ui_group)
        self.name = text
        self.font = pygame.font.Font("fonts/PixelFont.ttf", size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(borders_group, all_sprites)
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
