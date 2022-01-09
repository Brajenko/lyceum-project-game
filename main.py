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
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    fire.append(pygame.transform.scale(fire[0], (10, 10)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.finish_y = pos[1] + 20
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self, *args):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем
        if self.rect.y > self.finish_y:
            self.kill()
        # if not self.rect.colliderect(screen_rect):
        #     self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 5
    # возможные скорости
    numbers = range(-5, 3)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
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
        # create_particles(self.rect.center)

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

player = Player()
all_sprites.add(player)

enemy = Enemy()
enemies.add(enemy)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        pygame.display.flip()
        ticks = clock.tick(FPS)
        all_sprites.update(ticks)


main()
