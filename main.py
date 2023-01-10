import pygame
from classes import *
import settings

def pause():

    def unpause(*args):
        settings.pause = False

    def in_menu(*args):
        settings.pause = False
        menu()

    pause_screen = pygame.Surface(settings.SIZE, pygame.SRCALPHA).convert_alpha()
    pause_screen.fill((0, 0, 0, 100))

    font = pygame.font.Font("fonts/PixelFont.ttf", 90)
    string_rendered = font.render("Пауза", True, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 20
    pause_screen.blit(string_rendered, intro_rect)

    return_btn = Button("Вернуться", pygame.Color('orange'), 50, 300)
    return_btn.onclick(unpause)

    menu_btn = Button("Выйти в главное меню", pygame.Color('orange'), 50, 350)
    menu_btn.onclick(in_menu)

    button_group.draw(pause_screen)

    screen.blit(pause_screen, pause_screen.get_rect())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == 27:
                settings.pause = False

        if not settings.pause:
            button_group.empty()
            return
        button_group.update()
        pygame.display.flip()


def map_type(*args):
    def newtype(button):
        settings.map_id = int(button.name[-1])
        map_type()

    screen.fill((0, 0, 0))
    button_group.empty()

    font = pygame.font.Font("fonts/PixelFont.ttf", 65)
    string_rendered = font.render("Карты", True, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)
    tank_id = 1
    for j in range(2):
        for i in range(0, 2):
            image = load_image(f'UI/maps/map{tank_id}.png')
            rect = image.get_rect().move(i * 300 + 100, 100 + j * 300)
            screen.blit(image, rect)

            if tank_id == settings.map_id:
                map_type_btn = Button(f"Карта {tank_id}", pygame.Color('green'), i * 300 + 100, 350 + j * 300, 20)
            else:
                map_type_btn = Button(f"Карта {tank_id}", pygame.Color('orange'), i * 300 + 100, 350 + j * 300, 20)
            map_type_btn.onclick(newtype)
            tank_id += 1

    return_btn = Button("Назад", pygame.Color('orange'), 50, 675)
    return_btn.onclick(menu)


def tank_type(*args):
    def newtype(button):
        settings.tank_type = int(button.name[-1])
        tank_type()

    screen.fill((0, 0, 0))
    button_group.empty()

    font = pygame.font.Font("fonts/PixelFont.ttf", 65)
    string_rendered = font.render("Тип Танков", True, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)
    tank_id = 1
    for j in range(4):
        for i in range(1, 3):
            image = load_image(f'Tanks/Player/Type{tank_id}/top1.png')
            rect = image.get_rect().move(i * 300 - 220, 150 + j * 130)
            screen.blit(image, rect)

            tank_info = settings.tank_settings[tank_id]
            specific = ["hp", "damage", "wspeed", "hspeed"]

            font = pygame.font.Font("fonts/PixelFont.ttf", 10)

            string_rendered = font.render(f"{' '.join(f'{specific[i]}: {tank_info[i]};' for i in range(2))}", True,
                                          pygame.Color('orange'))
            intro_rect = string_rendered.get_rect()
            intro_rect.y = 200 + j * 130
            intro_rect.x = i * 300 - 220
            screen.blit(string_rendered, intro_rect)

            string_rendered = font.render(f"{' '.join(f'{specific[i]}: {tank_info[i]};' for i in range(2, 4))}", True,
                                          pygame.Color('orange'))
            intro_rect = string_rendered.get_rect()
            intro_rect.y = 220 + j * 130
            intro_rect.x = i * 300 - 220
            screen.blit(string_rendered, intro_rect)

            if tank_id == settings.tank_type:
                tank_type_btn = Button(f"Танк {tank_id}", pygame.Color('green'), i * 300 - 220, 240 + j * 130, 20)
            else:
                tank_type_btn = Button(f"Танк {tank_id}", pygame.Color('orange'), i * 300 - 220, 240 + j * 130, 20)
            tank_type_btn.onclick(newtype)
            tank_id += 1

    return_btn = Button("Назад", pygame.Color('orange'), 50, 675)
    return_btn.onclick(menu)


def menu(*args):
    screen.fill((0, 0, 0))
    button_group.empty()

    font = pygame.font.Font("fonts/PixelFont.ttf", 90)
    string_rendered = font.render("Танчики", True, pygame.Color('orange'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 20
    screen.blit(string_rendered, intro_rect)

    start_btn = Button("Начать", pygame.Color('orange'), 50, 300)
    start_btn.onclick(game)

    tank_type_btn = Button("Выбрать танк", pygame.Color('orange'), 50, 375)
    tank_type_btn.onclick(tank_type)

    image = load_image(f'Tanks/Player/Type{settings.tank_type}/top1.png')
    rect = image.get_rect().move(500, 340)
    screen.blit(image, rect)

    Button(f"Танк {settings.tank_type}", pygame.Color('gray'), 500, 400, 20)

    map_type_btn = Button("Выбрать карту", pygame.Color('orange'), 50, 450)
    map_type_btn.onclick(map_type)

    Button(f"Карта {settings.map_id}", pygame.Color('gray'), 500, 460, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        button_group.update()
        button_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def generate_level(level):
    player_x, player_y, x, y = None, None, None, None
    brick, leafs, unbreak, base, empty = [], [], [], [], []
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
            elif level[y][x] == "B":
                base.append((x, y))
    [Brick(x, y) for x, y in brick]
    [Base(x, y) for x, y in base]
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
                settings.pause = not settings.pause
        if settings.pause == True:
            pause()
        screen.fill((0, 0, 0))
        all_sprites.update()
        clock.tick(fps)
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    menu()