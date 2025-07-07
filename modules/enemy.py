import sys
import random
import math

import pygame


# Установка спрайтов врагов
def set_enemy_sprites(who_is):
    if who_is == 'imp':
        enemy_sprite_path = "assets/enemies/imp/enemy_walks_1.png"
        enemy_sprite = pygame.image.load(enemy_sprite_path)
        enemy_size = (100, 100)
    elif who_is == 'pinky':
        enemy_sprite_path = "assets/enemies/pinky/enemy_walks_1.png"
        enemy_sprite = pygame.image.load(enemy_sprite_path)
        enemy_size = (115, 115)
    elif who_is == 'cacodemon':
        enemy_sprite_path = "assets/enemies/cacodemon/enemy_walks_1.png"
        enemy_sprite = pygame.image.load(enemy_sprite_path)
        enemy_size = (125, 125)
    elif who_is == 'baron':
        enemy_sprite_path = "assets/enemies/baron/enemy_walks_1.png"
        enemy_sprite = pygame.image.load(enemy_sprite_path)
        enemy_size = (100, 140)
    elif who_is == 'cyberdemon':
        enemy_sprite_path = "assets/enemies/cyberdemon/enemy_walks_1.png"
        enemy_sprite = pygame.image.load(enemy_sprite_path)
        enemy_size = (300, 250)
    return enemy_sprite_path, enemy_sprite, enemy_size


# Установка звуков врагов
def set_enemy_sounds(who_is):
    if who_is == 'imp':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/imp/sounds/enemy_death.wav")
    elif who_is == 'pinky':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/pinky/sounds/enemy_death.wav")
    elif who_is == 'baron':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/baron/sounds/enemy_death.wav")
    elif who_is == 'cyberdemon':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/cyberdemon/sounds/enemy_death.wav")
    elif who_is == 'cacodemon':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/cacodemon/sounds/enemy_death.wav")
    return enemy_dies_sound


# Класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed,
                 enemy_dies_sound, who_is):
        super().__init__()
        self.enemy_size = enemy_size
        self.image = enemy_sprite
        self.image = pygame.transform.scale(enemy_sprite, self.enemy_size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 200) # Появление за правой границей экрана
        if who_is == 'cyberdemon':
            self.hitbox = self.rect.inflate(-100, -100)
        else:
            self.hitbox = self.rect.inflate(-10, -10)
        if who_is == 'cacodemon':
            self.rect.y = 5
        else:
            self.rect.y = player_on_ground_y - self.rect.height + 100  # Высота противника

        if who_is == 'imp':
            self.speed = random.randint(1, 3) # Случайная скорость
        elif who_is == 'pinky':
            self.speed = random.randint(3, 6) # Случайная скорость
        elif who_is == 'cacodemon':
            self.speed = random.randint(2, 3) # Случайная скорость
        elif who_is == 'baron':
            self.speed = random.randint(2, 4) # Случайная скорость
        elif who_is == 'cyberdemon':
            self.speed = random.randint(2, 3) # Случайная скорость
        self.background = background

        self.enemy_dies_sound = enemy_dies_sound
        self.who_is = who_is

        # Подсчет числа спрайтов относительно выбранного негодника
        if who_is == 'imp':
            sprite_count = {'death': 6, 'walks': 4}
        elif who_is == 'pinky':
            sprite_count = {'death': 7, 'walks': 4}
        elif who_is == 'cacodemon':
            sprite_count = {'death': 5, 'walks': 1}
        elif who_is == 'baron':
            sprite_count = {'death': 6, 'walks': 6}
        elif who_is == 'cyberdemon':
            sprite_count = {'death': 9, 'walks': 4}

        # Загружаем анимации противника
        # Список изображений для анимации уничтожения
        self.death_images = []
        for img_dth in range(sprite_count['death']):
            self.death_images.append(pygame.image.load(f"assets/enemies/{who_is}/enemy_death_{img_dth + 1}.png"))
        self.death_index = 0  # Индекс текущего изображения анимации смерти
        self.death_timer = 0 # Таймер для анимации смерти

        # Анимация ходьбы
        self.walks_images = []
        for img_wlk in range(sprite_count['walks']):
            self.walks_images.append(pygame.image.load(f"assets/enemies/{who_is}/enemy_walks_{img_wlk + 1}.png"))
        self.walks_index = 0  # Индекс текущего изображения анимации ходьбы
        self.walks_timer = 0 # Таймер для анимации ходьбы

        if who_is == 'imp':
            self.health = 3 # Здоровье
        elif who_is == 'pinky':
            self.health = 8 # Здоровье
        elif who_is == 'cacodemon':
            self.health = 15 # Здоровье
        elif who_is == 'baron':
            self.health = 40 # Здоровье
        elif who_is == 'cyberdemon':
            self.health = 100 # Здоровье

        self.is_alive = True # Флаг жив ли противник

        self.death_sound_active = False

    # Функция постоянного обновления состояния противника
    def update(self, player_speed, player_on_ground_y):
        self.rect.x -= self.speed - player_speed
        self.hitbox = self.rect.inflate(-10, -10)
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y
        if self.rect.right <= -100:
            self.kill()
        elif self.health > 0:
            self.walks_timer += 1
            if self.walks_timer >= 15 / self.speed:
                self.image = pygame.transform.scale(self.walks_images[self.walks_index], self.enemy_size)
                self.walks_index = (self.walks_index + 1) % len(self.walks_images)
                self.walks_timer = 0
        else:
            self.is_alive = False
            self.speed = 0
            self.death_timer += 1

            # Enemy falling down after destroy
            if self.who_is == 'cacodemon':
                if self.rect.y >= (player_on_ground_y - 25):
                    pass
                else:
                    self.rect.y += 10

            if self.death_index < len(self.death_images):
                if self.death_timer >= 5:
                    self.image = pygame.transform.scale(self.death_images[self.death_index], self.enemy_size)
                    self.death_index += 1
                    self.death_timer = 0
                    if not self.death_sound_active:
                        self.enemy_dies_sound.play()
                        self.death_sound_active = True


# Создание группы для противников для отрисовки всех противников одновременно
enemies = pygame.sprite.Group()


def chance(start, end):
    return random.randint(start, end)


# VVV For Game Circle VVV


# Создание противника с определенной вероятностью
def enemy_random_create(background, WIDTH, player_on_ground_y, player_speed):
    if chance(1, 50) == 1:
        who_is = 'imp'
    elif chance(1, 100) == 2:
        who_is = 'pinky'
    elif chance(1, 200) == 3:
        who_is = 'cacodemon'
    elif chance(1, 300) == 4:
        who_is = 'baron'
    elif chance(1, 600) == 5:
        who_is = 'cyberdemon'
    else:
        return None

    enemy_sprite_path, enemy_sprite, enemy_size = set_enemy_sprites(who_is)

    enemy_dies_sound = set_enemy_sounds(who_is)

    enemy = Enemy(
        background=background,
        enemy_sprite=enemy_sprite,
        enemy_size=enemy_size,
        WIDTH=WIDTH,
        player_on_ground_y=player_on_ground_y,
        player_speed=player_speed,
        enemy_dies_sound=enemy_dies_sound,
        who_is=who_is
    )
    enemies.add(enemy)
    return enemy


# Обновление позиций противников
def enemy_position_update(player_speed, player_on_ground_y):
    enemies.update(player_speed, player_on_ground_y)
