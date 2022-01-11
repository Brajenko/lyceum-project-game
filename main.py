import math
import sys
import pygame
import os
import random

BULLET_V = 3
SHOOTING_ENEMY_POSITIONS = [(100, 100), (100, 900), (100, 500), (900, 100), (900, 900), (900, 500), (500, 100),
                            (500, 900), (250, 100), (750, 100), (250, 900), (750, 900), (100, 250), (100, 750),
                            (900, 250), (900, 750)]
SHOOTING_SPEED = 0.5  # bullets/sec
ENEMY_SPEED = 1
PLAYER_SPEED = 3
WAVE = 0


def load_image(name, colorkey=(255, 255, 255)):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def count_move(pos, dest):
    move = [0, 0]
    if pos[0] > dest[0]:
        move[0] -= 1
    elif pos[0] < dest[0]:
        move[0] += 1

    if pos[1] > dest[1]:
        move[1] -= 1
    elif pos[1] < dest[1]:
        move[1] += 1
    return move


pygame.init()
FPS = 60
SIZE = WIDTH, HEIGHT = 1000, 1000
screen_rect = 0, 0, *SIZE
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Марио?')
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.image = load_image('mario.png')
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)

    def update(self, *args):
        self.move = [0, 0]
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.move[0] += PLAYER_SPEED

        if pressed[pygame.K_LEFT]:
            self.move[0] -= PLAYER_SPEED

        if pressed[pygame.K_DOWN]:
            self.move[1] += PLAYER_SPEED

        if pressed[pygame.K_UP]:
            self.move[1] -= PLAYER_SPEED

        if 0 not in self.move:
            self.move = list(map(lambda x: (x // math.sqrt(PLAYER_SPEED)) + 1, self.move))

        self.rect = self.rect.move(*self.move)
        create_particles(self.rect.center)

        pygame.sprite.spritecollide(self, shooting_enemies, dokill=True)

    def get_pos(self):
        return self.rect.center


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(enemies, all_enemies, all_sprites)
        self.image = load_image('star.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, *args):
        if player.alive():
            move = count_move(self.rect.center, player.get_pos())
            self.rect = self.rect.move(*move)
            pygame.sprite.spritecollide(self, player_group, dokill=True)


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


def find_closest_point(pos, points):
    minn = 99999
    ans = points[0]
    for point in points:
        dist = math.sqrt((pos[0] - point[0]) ** 2 + (pos[1] - point[1]) ** 2)
        if minn > dist:
            ans = point
            minn = dist

    return ans


class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_enemies, shooting_enemies, all_sprites)
        self.image = load_image('mario.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0

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
                    # self.shoot()
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


player = Player()
all_sprites.add(player)


def main():
    random_spawn(3, shooting=True)
    spawn_delay = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        # spawn_delay += 1
        if spawn_delay == 100:
            pass

        if spawn_delay == 1000:
            spawn_delay = 0


        all_sprites.update()
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        ticks = clock.tick(FPS)
        all_sprites.update(ticks)


main()
