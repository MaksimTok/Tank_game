import neat
import settings
from classes import *


def terminate():
    config.save('config-feedforward.txt')
    pygame.quit()
    sys.exit()


def game_over(state):
    game_screen = settings.screen.copy()

    def in_menu(*args):
        settings.game_over = False
        menu()

    def play_again(*args):
        settings.game_over = True
        p.run(game, 1000)

    game_over = pygame.Surface(settings.SIZE, pygame.SRCALPHA).convert_alpha()
    game_over.fill((0, 0, 0, 100))

    state_text = Label(state, pygame.Color('orange'), 15, 200, 80)

    ui_group.draw(game_over)
    settings.screen.blit(game_over, game_over.get_rect())

    time_out = False
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                time_out = True
                pygame.time.set_timer(pygame.USEREVENT, 0)

        if time_out:
            game_over = pygame.Surface(settings.SIZE, pygame.SRCALPHA).convert_alpha()
            game_over.fill((0, 0, 0, 100))

            state_text.kill()
            settings.screen.blit(game_screen, game_screen.get_rect())

            Label(state, pygame.Color('orange'), 20, 100, 70)

            play_again_btn = Button("Заново", pygame.Color('orange'), 50, 300)
            play_again_btn.onclick(play_again)

            menu_btn = Button("Выйти в главное меню", pygame.Color('orange'), 50, 350)
            menu_btn.onclick(in_menu)

            ui_group.draw(game_over)

            settings.screen.blit(game_over, game_over.get_rect())

        if not settings.game_over:
            ui_group.empty()
            return
        ui_group.update()
        pygame.display.flip()


def pause():
    def unpause(*args):
        settings.pause = False

    def in_menu(*args):
        settings.pause = False
        menu()

    pause_screen = pygame.Surface(settings.SIZE, pygame.SRCALPHA).convert_alpha()
    pause_screen.fill((0, 0, 0, 100))

    Label("Пауза", pygame.Color('orange'), 20, 100, 90)

    return_btn = Button("Вернуться", pygame.Color('orange'), 50, 300)
    return_btn.onclick(unpause)

    menu_btn = Button("Выйти в главное меню", pygame.Color('orange'), 50, 350)
    menu_btn.onclick(in_menu)

    ui_group.draw(pause_screen)
    screen.blit(pause_screen, pause_screen.get_rect())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == 27:
                settings.pause = False

        if not settings.pause:
            ui_group.empty()
            return
        ui_group.update()
        pygame.display.flip()


def map_type(*args):
    def newtype(button):
        settings.map_id = int(button.name[-1])
        map_type()

    screen.fill((0, 0, 0))
    ui_group.empty()
    all_sprites.empty()

    Label("Карты", pygame.Color('orange'), 20, 10, 65)

    map_id = 1
    for j in range(2):
        for i in range(0, 2):
            image = load_image(f'UI/maps/map{map_id}.png')
            rect = image.get_rect().move(i * 300 + 100, 100 + j * 300)
            screen.blit(image, rect)

            if map_id == settings.map_id:
                map_type_btn = Button(f"Карта {map_id}", pygame.Color('green'), i * 300 + 100, 350 + j * 300, 20)
            else:
                map_type_btn = Button(f"Карта {map_id}", pygame.Color('orange'), i * 300 + 100, 350 + j * 300, 20)
            map_type_btn.onclick(newtype)
            map_id += 1

    return_btn = Button("Назад", pygame.Color('orange'), 50, 675)
    return_btn.onclick(menu)


def tank_type(*args):
    def newtype(button):
        settings.tank_type = int(button.name[-1])
        tank_type()

    screen.fill((0, 0, 0))
    ui_group.empty()
    all_sprites.empty()

    Label("Типы Танков", pygame.Color('orange'), 20, 50, 65)

    tank_id = 1
    for j in range(4):
        for i in range(1, 3):
            image = load_image(f'Tanks/Player/Type{tank_id}/top1.png')
            rect = image.get_rect().move(i * 300 - 220, 150 + j * 130)
            screen.blit(image, rect)

            tank_info = settings.tank_settings[tank_id]
            specific = ["hp", "damage", "wspeed", "hspeed"]

            string_rendered = f"{' '.join(f'{specific[i]}: {tank_info[i]};' for i in range(2))}"
            Label(string_rendered, pygame.Color('orange'), i * 300 - 220, 200 + j * 130, 10)

            string_rendered = f"{' '.join(f'{specific[i]}: {tank_info[i]};' for i in range(2, 4))}"
            Label(string_rendered, pygame.Color('orange'), i * 300 - 220, 220 + j * 130, 10)

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
    ui_group.empty()
    all_sprites.empty()

    Label("Танчики", pygame.Color('orange'), 20, 100, 90)

    start_btn = Button("Начать", pygame.Color('orange'), 50, 300)
    start_btn.onclick(p.run, (game, 1000))

    tank_type_btn = Button("Выбрать танк", pygame.Color('orange'), 50, 375)
    tank_type_btn.onclick(tank_type)

    image = load_image(f'Tanks/Player/Type{settings.tank_type}/top1.png')
    rect = image.get_rect().move(500, 340)
    screen.blit(image, rect)

    Label(f"Танк {settings.tank_type}", pygame.Color('gray'), 500, 400, 20)

    map_type_btn = Button("Выбрать карту", pygame.Color('orange'), 50, 450)
    map_type_btn.onclick(map_type)

    Label(f"Карта {settings.map_id}", pygame.Color('gray'), 500, 460, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        ui_group.update()
        ui_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def ui(player, base):
    ui_group.empty()

    Label("Time:", pygame.Color("orange"), 575, 5, 30)
    Label(str(settings.time), pygame.Color("orange"), 575, 55, 30)

    Label("Hp:", pygame.Color("orange"), 10, 5, 30)
    Label(str(player.hp), pygame.Color("orange"), 10, 55, 30)

    Label("Respawn:", pygame.Color("orange"), 10, 625, 30)
    Label(str(settings.respawn), pygame.Color("orange"), 10, 675, 30)

    Label("Base Hp:", pygame.Color("orange"), 530, 625, 30)
    Label(str(base.hp), pygame.Color("orange"), 530, 675, 30)


def generate_level(level):
    Border(-5, -5, WIDTH, -5)
    Border(-5, HEIGHT, WIDTH, HEIGHT)
    Border(-5, -5, -5, HEIGHT)
    Border(WIDTH, -5, WIDTH, HEIGHT)

    player_x, player_y, base_x, base_y, x, y = None, None, None, None, None, None
    brick, leafs, unbreak, spawn, empty = [], [], [], [], []
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
                base_x, base_y = x, y
            elif level[y][x] == "S":
                spawn.append((x, y))
    [Brick(x, y) for x, y in brick]
    [Unbreak(x, y) for x, y in unbreak]
    [SpawnPoint(x, y) for x, y in spawn]
    player = Tank(player_x, player_y, settings.tank_type)
    base = Base(base_x, base_y)
    [Leafs(x, y) for x, y in leafs]
    return player, base


pygame.init()
pygame.display.set_caption('Танчики')
clock = pygame.time.Clock()


def game(genomes, config):
    settings.screen.fill((0, 0, 0))
    enemys.clear()
    borders_group.empty()
    ui_group.empty()
    spawn_group.empty()
    enemy_group.empty()
    tiles_group.empty()
    all_sprites.empty()
    base_group.empty()
    brick_group.empty()
    unbreak_group.empty()
    player_group.empty()
    bullet_group.empty()

    board = load_level(settings.maps[settings.map_id - 1])
    player, base = generate_level(board)
    settings.time = 100
    settings.respawn = 3
    pygame.time.set_timer(pygame.USEREVENT, settings.time * 10)  # 100 second
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == 27:
                settings.pause = not settings.pause
            if event.type == pygame.USEREVENT:
                settings.time -= 1
        if settings.enemys:
            # init genomes
            for i, g in genomes:
                net = neat.nn.FeedForwardNetwork.create(g, config)
                nets.append(net)
                g.fitness = 0  # every genome is not successful at the start

            for i, tank in enumerate(enemys):
                tank.output = nets[i].activate(tank.get_data())
                # tank.output = outputs.index(max(outputs))

            # now, update tank and set fitness (for alive tanks only)
            for i, tank in enumerate(enemys):
                if tank.is_alive:
                    tank.update()
                    if base.hp <= 0:
                        genomes[i][1].fitness += tank.get_reward(count=50)  # new fitness (aka tank instance success)
                    elif player.hp <= 0:
                        genomes[i][1].fitness += tank.get_reward(count=10)
                    else:
                        genomes[i][1].fitness += tank.get_reward(count=-1)
                else:
                    genomes[i][1].fitness += tank.get_reward(count=-10)
        if settings.pause:
            pause()
        if player.hp <= 0 and settings.respawn > 0:
            settings.respawn -= 1
            player.respawn()
        if player.hp <= 0 and settings.respawn <= 0 or base.hp <= 0:
            settings.screen.fill((0, 0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            ui(player, base)
            ui_group.update()
            ui_group.draw(screen)
            settings.game_over = True
            game_over("Вы Проиграли")
        if settings.time <= 0:
            settings.screen.fill((0, 0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            ui(player, base)
            ui_group.update()
            ui_group.draw(screen)
            settings.game_over = True
            game_over("Вы Выиграли")
        settings.screen.fill((0, 0, 0))
        all_sprites.update()
        clock.tick(fps)
        all_sprites.draw(screen)
        ui(player, base)
        ui_group.update()
        ui_group.draw(screen)
        pygame.display.flip()


config_path = "./config-feedforward.txt"
#config_path2 = "./config-feedforward2.txt"
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                            neat.DefaultStagnation, config_path)
#config2 = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
#                             neat.DefaultStagnation, config_path2)
# init NEAT
p = neat.Population(config)

if __name__ == '__main__':
    menu()
