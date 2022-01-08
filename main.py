import sys
import pygame
import os
import random


def load_image(name, colorkey=(255, 255, 255)):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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


def terminate():
    pygame.quit()
    sys.exit()


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("star.png"), (10, 10))
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.finish_y = pos[1] + 20
        self.rect.x, self.rect.y = pos

    def update(self, *args):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем
        if self.rect.y > self.finish_y:
            self.kill()
        # if not self.rect.colliderect(screen_rect):
        #     self.kill()


def create_particles(position):
    particle_count = 1
    numbers = range(-5, 3)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('mario.png')
        self.rect = self.image.get_rect()
        self.direction = 'R'
        self.particle_positions = {'R': (self.rect.x + 3, self.rect.y + self.rect.w),
                                   'L': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w),
                                   'U': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w),
                                   'D': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w),
                                   'RU': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w),
                                   'RD': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w),
                                   'LU': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w),
                                   'LD': (self.rect.x + 3 + self.rect.h, self.rect.y + self.rect.w)}

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


        self.rect = self.rect.move(*self.move)
        particle_pos = (self.rect.x, self.rect.y + self.rect.w)
        create_particles(particle_pos)

        if 0 not in self.move:
            self.move = list(map(lambda x: x // 2, self.move))

        # create_particles(self.rect.center)

        if pygame.sprite.spritecollideany(self, enemies):
            self.kill()


def get_pos(self):
    return self.rect.center


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
        self.rect.center = (400, 400)
        self.walk_range = 100
        self.counter = 0

    def update(self, *args):
        if player.alive():
            # target_x, target_y = player.get_pos()
            # move = [0, 0]
            # if self.rect.x + self.walk_range > target_x:
            #     move[0] -= 1
            # elif self.rect.x - self.walk_range < target_x:
            #     move[0] += 1
            #
            # if self.rect.y + self.walk_range > target_y:
            #     move[1] -= 1
            # elif self.rect.y - self.walk_range < target_y:
            #     move[1] += 1
            #
            # if move != [0, 0]:
            #     self.rect = self.rect.move(*move)
            self.counter += clock.get_time()
            if self.counter > 500:
                self.shoot()
                print(1111)
                self.counter = 0

    def shoot(self):
        move = [1, 2]
        bullet = Bullet(self.rect.center, move)


player = Player()
all_sprites.add(player)

enemy = ShootingEnemy()
enemies.add(enemy)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        all_sprites.update()
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        pygame.display.flip()
        ticks = clock.tick(FPS)
        all_sprites.update(ticks)


main()
