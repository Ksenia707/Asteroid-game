import pygame
from random import randrange, random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load('ass/Orbital_Colossus.mp3')

# настройка игры
GAME_WIDTH = 1000
GAME_HEIGHT = 650

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Attack')

bg = pygame.image.load('ass/space-1.png')
sound = pygame.mixer.Sound('ass/shoot.wav')
sound2 = pygame.mixer.Sound('ass/boom.wav')
sound3 = pygame.mixer.Sound('ass/power.mp3')

exposion = {'exple': []}
for i in range(9):
    file = f'blast0{i}.png'
    img = pygame.image.load('ass/' + file)
    exposion['exple'].append(img)


def draw_lives(screen, x, y, lives):
    image = pygame.image.load('ass/img.png')
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 45 * i
        img_rect.y = y
        screen.blit(image, img_rect)


def menu(gameState):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        title = pygame.image.load('ass/title.jpeg')

        if gameState == 'start':
            start_game = pygame.image.load('ass/BtnPlay.png')  # 128, 128
        else:
            start_game = pygame.image.load('ass/BtnReset.png')  # 256, 128

        start_game_rect = start_game.get_rect()
        start_game_rect.x = GAME_WIDTH // 2 - start_game.get_width() // 2
        start_game_rect.y = GAME_HEIGHT // 2 - start_game.get_height() // 2

        mouse_pos = pygame.mouse.get_pos()
        if start_game_rect.collidepoint(mouse_pos):
            scaled_img = pygame.transform.scale(start_game, (start_game.get_width() + 10, start_game.get_height() + 10))
        else:
            scaled_img = pygame.transform.scale(start_game, (start_game.get_width(), start_game.get_height()))

        click = pygame.mouse.get_pressed()
        if start_game_rect.collidepoint(mouse_pos) and click[0]:
            return

        screen.blit(title, (0, 0))
        screen.blit(scaled_img, start_game_rect)
        pygame.display.update()


menu('start')


# class player
class Player(pygame.sprite.Sprite):
    # КОНСТРУКТОР КЛАССА
    def __init__(self):
        super().__init__()  # вызов конструктора класса Sprite
        self.images = (
            pygame.image.load('ass/ship.png'),
            pygame.image.load('ass/shield.png'))
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 300))
        self.speed = 5
        self.lives = 3
        self.radius = 15
        self.timeShield = 400

    def update(self):
        # щит
        if self.image_index == 1:
            self.timeShield -= 1
            if self.timeShield == 0:
                self.image_index = 0
                self.timeShield = 100
        self.image = self.images[self.image_index]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed

        # граниы
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= GAME_WIDTH - self.rect.width:
            self.rect.x = GAME_WIDTH - self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= GAME_HEIGHT - self.rect.height:
            self.rect.y = GAME_HEIGHT - self.rect.height


# класс астероид
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.image.load('ass/asteroid1.png'),
            pygame.image.load('ass/asteroid2.png'),
            pygame.image.load('ass/asteroid3.png'),
            pygame.image.load('ass/asteroid4.png')
        ]
        self.image_index = 0  # индеск первой картинки
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = randrange(GAME_WIDTH - self.rect.width)
        self.rect.y = randrange(-100, -10)
        self.speed = 3
        self.frame_delay = 10
        self.frame_countdown = 5
        self.radius = 15

    def update(self):
        self.rect.y += self.speed

        self.frame_countdown -= 1
        if self.frame_countdown == 0:
            self.frame_countdown = self.frame_delay
            if self.image_index != 3:
                self.image_index += 1
            else:
                self.image_index = 0
            self.image = self.images[self.image_index]

        if self.rect.y > GAME_HEIGHT:
            self.kill()


class Shoot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('ass/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < -50:
            self.kill()


class Expoltion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = exposion['exple'][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        no = pygame.time.get_ticks()
        if no - self.last_update > self.frame_rate:
            self.last_update = no
            self.frame += 1
            if self.frame == len(exposion['exple']):
                self.kill()
            else:
                center = self.rect.center
                self.image = exposion['exple'][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(GAME_WIDTH)
        self.rect.y = randrange(GAME_HEIGHT)
        self.speed = randrange(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > GAME_HEIGHT:
            self.rect.y = 0
            self.rect.x = randrange(GAME_WIDTH)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.image.load('ass/img_1.png'),
            pygame.image.load('ass/img_2.png'),
            pygame.image.load('ass/img_3.png'),
        ]
        self.type = randrange(0, 3)  # 0 / 1 / 2
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
        self.radius = 15

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > GAME_HEIGHT:
            self.kill()


player = Player()

# группа для обновления всех спратов
all_sprites = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
powerups_group = pygame.sprite.Group()
all_sprites.add(player)

for _ in range(100):
    star = Star()
    all_sprites.add(star)

pygame.mixer.music.play(loops=-1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ne_shoot = Shoot(player.rect.centerx, player.rect.top)
            sound.play()
            all_sprites.add(ne_shoot)
            shoot_group.add(ne_shoot)

    # создание астероида
    if pygame.time.get_ticks() % 10 == 0:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroid_group.add(asteroid)

    # столкновение групп
    hits = pygame.sprite.groupcollide(asteroid_group, shoot_group, True, True)
    for hit in hits:
        sound2.play()
        expl = Expoltion(hit.rect.center)
        all_sprites.add(expl)
        x = random()
        if x > 0.9:
            powerX = PowerUp(hit.rect.x, hit.rect.y)
            powerups_group.add(powerX)
            all_sprites.add(powerX)

    # столкновение астероидов с игроком
    hits = pygame.sprite.spritecollide(player, asteroid_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        sound2.play()
        expl = Expoltion(hit.rect.center)
        all_sprites.add(expl)
        if player.image_index != 1:
            if player.lives > 0:
                player.lives -= 1
                if player.lives == 0:
                    pygame.mixer.music.stop()
                    for sprite in all_sprites.sprites():
                        if sprite != player:
                            sprite.kill()
                    menu('game over')
                    pygame.mixer.music.play(loops=-1)
                    player.lives = 3
                    player.rect.center = (GAME_WIDTH // 2, GAME_HEIGHT - 200)
                    for _ in range(100):
                        star = Star()
                        all_sprites.add(star)

    # столкновение игрока с powerup
    hits = pygame.sprite.spritecollide(player, powerups_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        sound3.play()
        if hit.type == 1:  # взрываем все метеориты на экране
            print(1)
            for i in asteroid_group:
                i.kill()
                expl = Expoltion(i.rect.center)
                all_sprites.add(expl)
        elif hit.type == 0:  # пополняем жизни
            print(0)
            player.lives = 3
        else:  # щит
            print(2)
            player.image_index = 1

    all_sprites.update()

    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    draw_lives(screen, GAME_WIDTH - 150, 5, player.lives)
    pygame.display.update()
    clock.tick(100)

pygame.quit()
