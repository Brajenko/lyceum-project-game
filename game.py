import math
import sys
import pygame
import os
import pygame.freetype
import random
import pygame_menu
from menu_theme import start_menu_theme, finish_menu_theme, ingame_menu_theme
import results

BULLET_V = 3
SHOOTING_ENEMY_POSITIONS = [(100, 100), (100, 900), (100, 500), (900, 100), (900, 900), (900, 500), (500, 100),
                            (500, 900), (250, 100), (750, 100), (250, 900), (750, 900), (100, 250), (100, 750),
                            (900, 250), (900, 750)]
SHOOTING_SPEED = 0.5  # bullets/sec
ENEMY_SPEED = 1
ANIMATION_SPEED = 5  # fps
PLAYER_SPEED = 3
player_name = 'User'
WASD_MOVEMENT = {'R': pygame.K_d,
                 'L': pygame.K_a,
                 'U': pygame.K_w,
                 'D': pygame.K_s}
ARROWS_MOVEMENT = movement = {'R': pygame.K_RIGHT,
                              'L': pygame.K_LEFT,
                              'U': pygame.K_UP,
                              'D': pygame.K_DOWN}


def load_image(name, colorkey=(255, 255, 255)):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(colorkey)
    return image


def load_background(name):
    fullname = os.path.join('data/ingame_backgrounds', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def count_move(pos, dest, return_orient=False):
    move = [0, 0]
    orient = 'D'
    if pos[0] > dest[0]:
        move[0] -= 1
        orient = 'L'

    elif pos[0] < dest[0]:
        move[0] += 1
        orient = 'R'

    if pos[1] > dest[1]:
        move[1] -= 1
        orient = 'D'
    elif pos[1] < dest[1]:
        move[1] += 1
        orient = 'D'
    if return_orient:
        return move, orient
    return move


def generate_new_wave(n, shooting, enemy):
    if enemy > 4:
        enemy += 4
    else:
        enemy += 2

    if shooting > 2:
        shooting += 2
    else:
        shooting += 1

    return n + 1, shooting, enemy


pygame.init()
FPS = 50
SIZE = WIDTH, HEIGHT = 1000, 1000
INGAME_FONT = pygame.freetype.Font("pixelfont.ttf", 24)
TRANSITION_FONT = pygame.freetype.Font("pixelfont.ttf", 100)
screen_rect = 0, 0, *SIZE
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
enemies = pygame.sprite.Group()
shooting_enemies = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alpha = 128

    def update(self, *args):
        global k
        self.image.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
        self.alpha -= 0.3
        if self.alpha < 0:
            self.kill()


def create_particles(position):
    x, y = position
    Particle(x + 1, y)
    Particle(x, y + 1)
    Particle(x, y)


def modify_speed(v):
    if v > 0:
        return v // math.sqrt(v) + 1
    return -(abs(v) // math.sqrt(abs(v)) + 1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.frames = []
        sheet = load_image('main_hero.png')
        self.cut_sheet(sheet, 4, 4)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(500, 500)
        self.d = {
            'R': self.frames[2],
            'L': self.frames[1],
            'U': self.frames[3],
            'D': self.frames[0]
        }
        self.image = self.d['L'][self.cur_frame]
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            a = []
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                a.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
            self.frames.append(a)

    def update(self, *args):
        self.move = [0, 0]
        pressed = pygame.key.get_pressed()
        orientation = 'D'
        if pressed[movement['R']]:
            self.move[0] += PLAYER_SPEED
            orientation = 'R'

        if pressed[movement['L']]:
            self.move[0] -= PLAYER_SPEED
            orientation = 'L'

        if pressed[movement['D']]:
            self.move[1] += PLAYER_SPEED
            orientation = 'D'

        if pressed[movement['U']]:
            self.move[1] -= PLAYER_SPEED
            orientation = 'U'

        if 0 not in self.move:
            self.move = list(map(lambda x: modify_speed(x), self.move))

        self.rect = self.rect.move(*self.move)
        create_particles(self.rect.center)
        self.counter += 1
        if self.counter == 60 // ANIMATION_SPEED:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.d[orientation][self.cur_frame]
            self.counter = 0

        pygame.sprite.spritecollide(self, shooting_enemies, dokill=True)

    def get_pos(self):
        return self.rect.center


def split_list(lst, n):
    return [lst[i: i + n] for i in range(0, len(lst), n)]


class BackgroudImage:
    def __init__(self):
        self.ingame_images = os.listdir(path="data/ingame_backgrounds")

    def for_wave(self):
        name = random.choice(self.ingame_images)
        return self.scale_im(load_background(name))

    def scale_im(self, im):
        pygame.transform.scale(im, (1000, 1000))
        return im


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(enemies, all_enemies, all_sprites)
        self.frames = []
        self.d = self.cut_sheet(load_image('enemies.png'), 12, 8)
        self.cur_frame = 0
        self.rect.center = pos
        self.color = random.choice(['Y', 'G', 'DB', 'R', 'W', 'P', 'B', 'O'])
        self.counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(8):
            a = []
            for i in range(12):
                frame_location = (self.rect.w * i, self.rect.h * j)
                a.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
            self.frames.append(a)

        self.image = self.frames[0][0]
        self.frames = [split_list(i, 3) for i in self.frames]

        d = {}
        for i, dest in enumerate(['D', 'L', 'R', 'U']):
            d[dest] = {}
            for j, color in enumerate(['Y', 'G', 'DB', 'R']):
                d[dest][color] = self.frames[i][j]

        self.frames = self.frames[4:]
        for i, dest in enumerate(['D', 'L', 'R', 'U']):
            for j, color in enumerate(['W', 'P', 'B', 'O']):
                d[dest][color] = self.frames[i][j]

        return d

    def update(self, *args):
        orientation = 'D'
        if player.alive():
            move, orientation = count_move(self.rect.center, player.get_pos(), return_orient=True)
            self.rect = self.rect.move(*move)
            pygame.sprite.spritecollide(self, player_group, dokill=True)

        self.counter += 1
        if self.counter == 60 // ANIMATION_SPEED:
            self.cur_frame = (self.cur_frame + 1) % 3
            self.image = self.d[orientation][self.color][self.cur_frame]
            self.counter = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, center, move):
        super().__init__(enemies, all_sprites)
        im = load_image('star.png')
        self.image = pygame.transform.scale(im, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.move = move

    def update(self, *args):
        if self.rect.y > HEIGHT or self.rect.y < 0 or self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()
        else:
            self.rect = self.rect.move(*self.move)
        pygame.sprite.spritecollide(self, player_group, dokill=True)


def find_closest_point(pos, points):
    minn = 99999
    ans = points[0]
    for point in points:
        dist = math.sqrt((pos[0] - point[0]) ** 2 + (pos[1] - point[1]) ** 2)
        if minn > dist:
            ans = point
            minn = dist

    return ans


class WaveText(pygame.sprite.Sprite):
    def __init__(self, group, wave):
        super().__init__(group)
        self.image, self.rect = TRANSITION_FONT.render("WAVE {}".format(wave[0]), (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = -self.image.get_width()
        self.rect.y = 0
        self.move = True

    def update(self, *args):
        if self.move:
            self.rect = self.rect.move(5, 0)
            if self.rect.left >= 0:
                self.rect.left = 0
                self.move = False


class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_enemies, shooting_enemies, all_sprites)
        self.image = load_image('shooting_enemy.jpg', colorkey=(48, 20, 58))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.moving = True
        self.dest = find_closest_point(self.rect.center, SHOOTING_ENEMY_POSITIONS)

    def update(self, *args):
        if player.alive():
            if pygame.sprite.collide_mask(self, player):
                self.kill()
            if self.moving:
                move = count_move(self.rect.center, self.dest)
                self.rect = self.rect.move(move)
                if self.rect.center == self.dest:
                    self.moving = False
            else:
                self.counter += 1
                if self.counter == 60 // SHOOTING_SPEED:
                    self.shoot()
                    self.counter = 0

    def shoot(self):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        x_speed = y_speed = 0
        try:
            x_speed = BULLET_V / (math.sqrt(1 + ((dy ** 2) / (dx ** 2))))
            y_speed = BULLET_V / (math.sqrt(1 + ((dx ** 2) / (dy ** 2))))
        except ZeroDivisionError:
            if dx == 0:
                x_speed = 0
                y_speed = BULLET_V / (math.sqrt(1 + ((dx ** 2) / (dy ** 2))))
            elif dy == 0:
                x_speed = BULLET_V / (math.sqrt(1 + ((dy ** 2) / (dx ** 2))))
                y_speed = 0
        finally:
            if dx < 0:
                x_speed *= -1
            if dy < 0:
                y_speed *= -1
            move = [x_speed, y_speed]
            bullet = Bullet(self.rect.center, move)


def text_to_screen(screen, text, x, y, size=50,
                   color=(200, 000, 000), font_type=''):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


def spawn_enemy(pos: (int, int), shooting=False):
    if shooting:
        enemy = ShootingEnemy(pos)
    else:
        enemy = Enemy(pos)
    enemies.add(enemy)


def generate_random_pos(shooting: bool) -> (int, int):
    if shooting:
        positions = [list(range(0, 101)) + list(range(900, 1001)), list(range(0, 1001))]
    else:
        positions = [list(range(0, 301)) + list(range(700, 1001)), list(range(0, 1001))]
    random.shuffle(positions)
    x = random.choice(positions[0])
    y = random.choice(positions[1])
    return x, y


def random_spawn(n: int, shooting=False) -> None:
    positions = [generate_random_pos(shooting) for _ in range(n)]
    for pos in positions:
        spawn_enemy(pos, shooting)


def spawn_wave(wave):
    random_spawn(wave[1], shooting=True)
    random_spawn(wave[2], shooting=False)


def check_pos(pos):
    mouse = pygame.sprite.Sprite()
    mouse.image = pygame.Surface((1, 1))
    mouse.rect = mouse.image.get_rect()
    mouse.rect.center = pos
    enemies_to_kill = pygame.sprite.spritecollide(mouse, enemies, dokill=False)
    for enemy in enemies_to_kill:
        if enemy not in shooting_enemies:
            enemy.kill()


SPAWN_EVENT = pygame.event.Event(pygame.USEREVENT)


def spawn_player():
    global player
    player = Player()
    all_sprites.add(player)


def start_game():
    pause = False
    bi = BackgroudImage()
    spawn_player()
    wave = 0, 0, 0
    wave_text = WaveText(all_sprites, wave)
    spawn_delayed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_pos(event.pos)
            if event.type == SPAWN_EVENT.type:
                spawn_wave(wave)
                spawn_delayed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    def close():
                        menu.disable()

                    menu = pygame_menu.Menu('Pause', 1000, 1000, theme=ingame_menu_theme)
                    menu.add.button('continue', close)
                    menu.add.button('restart', restart)
                    menu.add.button('Leave game', leave_game)
                    menu.mainloop(screen)

        if not all_enemies.sprites() and not spawn_delayed:
            wave = generate_new_wave(*wave)
            wave_text.kill()
            wave_text = WaveText(all_sprites, wave)
            pygame.time.set_timer(SPAWN_EVENT, 1000, loops=1)
            backgroung = bi.for_wave()
            spawn_delayed = True

        if not player.alive():
            all_sprites.empty()
            all_enemies.empty()
            wave_text.kill()
            results.write_new(player_name, wave[0])
            finish_menu()
            return

        all_sprites.update()
        ticks = clock.tick(FPS)
        all_sprites.update(ticks)
        screen.blit(backgroung, (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


def set_player_name(name):
    global player_name
    player_name = name


def change_controls(controls: str, *args):
    global movement
    if controls[0] == 'arrows':
        movement = ARROWS_MOVEMENT
    else:
        movement = WASD_MOVEMENT


def start_menu():
    menu = pygame_menu.Menu('Do you want to launch rocket?', 1000, 1000,
                            theme=start_menu_theme)
    menu.add.text_input('Name -', default=player_name, onchange=set_player_name)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    best_res = results.get_best()
    if best_res:
        menu.add.label('Best Result - {1} By {0}'.format(*best_res))
    else:
        menu.add.label('No results yet')
    menu.add.button('Settings', settings_menu)

    back = pygame_menu.baseimage.BaseImage(
        image_path=os.path.join('data', 'finish_menu.jpg'),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
    )

    menu.background_color = back

    menu.mainloop(screen)


def finish_menu():
    menu = pygame_menu.Menu('Oh, you lose, rocket is falling', 1000, 1000,
                            theme=finish_menu_theme)
    prev_result = results.get_last()
    menu.add.label('Your result - {}'.format(prev_result[1]))
    menu.add.button('Try again', start_game)
    menu.add.button('Return to main menu', start_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.label('Best Result - {1} By {0}'.format(*results.get_best()))
    back = pygame_menu.baseimage.BaseImage(
        image_path=os.path.join('data', 'finish_menu.jpg'),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )

    menu.background_color = back
    menu.mainloop(screen)


def settings_menu():
    menu = pygame_menu.Menu('Settings', 1000, 1000, theme=start_menu_theme)
    default = int(movement != WASD_MOVEMENT)
    menu.add.selector('choose controls', ['wasd', 'arrows'], onchange=change_controls, default=default)
    menu.add.button('Back', start_menu)
    menu.mainloop(screen)


def ingame_menu():
    menu = pygame_menu.Menu('Pause', 1000, 1000, theme=ingame_menu_theme)
    menu.add.button('continue', pygame_menu.events.CLOSE)
    menu.add.button('restart', restart)
    menu.add.button('Leave game', leave_game)
    menu.mainloop(screen)


def leave_game():
    all_sprites.empty()
    all_enemies.empty()
    player_group.empty()
    start_menu()


def restart():
    all_sprites.empty()
    all_enemies.empty()
    player_group.empty()
    start_game()


start_menu()
