import math
import sys
import pygame
import os
import random

BULLET_V = 5
SHOOTING_ENEMY_WALK_RANGE = 100


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
GRAVITY = 1
screen_rect = 0, 0, *SIZE
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Марио?')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
draw_first = pygame.sprite.Group()


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

    def update(self, *args):
        alpha = 128
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        alpha -= 2
        if alpha < 0:
            self.kill()


def create_particles(position):
    for i in range(2):
        x, y = position
        Particle(x + i, y)
        Particle(x, y + i)
        Particle(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, draw_first)
        self.image = load_image('mario.png')
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.move = [0, 0]
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.move[0] += 2

        if pressed[pygame.K_LEFT]:
            self.move[0] -= 2

        if pressed[pygame.K_DOWN]:
            self.move[1] += 2

        if pressed[pygame.K_UP]:
            self.move[1] -= 2

        if 0 not in self.move:
            self.move = list(map(lambda x: x // 2, self.move))

        self.rect = self.rect.move(*self.move)
        create_particles(self.rect.center)

        if pygame.sprite.spritecollideany(self, enemies):
            self.kill()


def get_pos(self):
    return self.rect.center

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemies, all_sprites)
        self.image = load_image('star.png')
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)

    def update(self, *args):
        if player.alive():
            target_x, target_y = player.get_pos()
            move = [0, 0]
            if self.rect.x > target_x:
                move[0] -= 1
            elif self.rect.x < target_x:
                move[0] += 1

            if self.rect.y > target_y:
                move[1] -= 1
            elif self.rect.y < target_y:
                move[1] += 1

            self.rect = self.rect.move(*move)


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


class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemies, all_sprites)
        self.image = load_image('mario.png')
        self.rect = self.image.get_rect()
        self.rect.center = (419, 1000)
        self.counter = 0

        self.moving = True
        self.dest = [0, 0]
        if self.rect.centerx > player.rect.centerx:
            self.dest[0] = player.rect.centerx + SHOOTING_ENEMY_WALK_RANGE
        else:
            self.dest[0] = player.rect.centerx - SHOOTING_ENEMY_WALK_RANGE

        if self.rect.centery > player.rect.centery:
            self.dest[1] = player.rect.centery + SHOOTING_ENEMY_WALK_RANGE
        else:
            self.dest[1] = player.rect.centery - SHOOTING_ENEMY_WALK_RANGE

    def update(self, *args):
        if player.alive():
            if self.moving:
                move = count_move(self.rect.center, self.dest)
                self.rect = self.rect.move(move)
            else:
                self.counter += clock.get_time()
                if self.counter > 500:
                    # self.shoot()
                    self.counter = 0

    def shoot(self):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        x_speed = BULLET_V / (math.sqrt(1 + ((dy ** 2) / (dx ** 2))))
        y_speed = BULLET_V / (math.sqrt(1 + ((dx ** 2) / (dy ** 2))))
        if dx < 0:
            x_speed *= -1
        if dy < 0:
            y_speed *= -1
        move = [x_speed, y_speed]
        bullet = Bullet(self.rect.center, move)


player = Player()
all_sprites.add(player)


# enemy = ShootingEnemy()
# enemies.add(enemy)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        all_sprites.update()
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        draw_first.draw(screen)
        pygame.display.flip()
        ticks = clock.tick(FPS)
        all_sprites.update(ticks)


main()
