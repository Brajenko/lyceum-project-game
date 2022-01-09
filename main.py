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
