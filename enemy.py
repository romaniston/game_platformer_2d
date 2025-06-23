import sys
import random

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
        enemy_size = (150, 150)
    elif who_is == 'baron':
        enemy_sprite_path = "assets/enemies/baron/enemy_walks_1.png"
        enemy_sprite = pygame.image.load(enemy_sprite_path)
        enemy_size = (200, 200)
    return enemy_sprite_path, enemy_sprite, enemy_size

# Установка звуков врагов
def set_enemy_sounds(who_is):
    if who_is == 'imp':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/imp/sounds/enemy_death.wav")
    elif who_is == 'pinky':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/pinky/sounds/enemy_death.wav")
    elif who_is == 'baron':
        enemy_dies_sound = pygame.mixer.Sound("assets/enemies/baron/sounds/enemy_death.wav")
    return enemy_dies_sound

# Класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound, who_is):
        super().__init__()
        self.image = enemy_sprite
        self.image = pygame.transform.scale(enemy_sprite, enemy_size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 200) # Появление за правой границей экрана
        self.rect.y = (player_on_ground_y) # Высота противника
        if who_is == 'imp':
            self.speed = random.randint(1, 3) # Случайная скорость
        elif who_is == 'pinky':
            self.speed = random.randint(3, 6) # Случайная скорость
        elif who_is == 'baron':
            self.speed = random.randint(4, 8) # Случайная скорость
        self.background = background

        self.enemy_dies_sound = enemy_dies_sound
        self.who_is = who_is

        # Загружаем анимации противника
        # Список изображений для анимации уничтожения
        self.death_images = []
        # Подсчет числа спрайтов относительно выбранного негодника
        if who_is == 'imp':
            sprite_count = {'death': 6, 'walks': 4}
        elif who_is == 'pinky':
            sprite_count = {'death': 7, 'walks': 4}
        elif who_is == 'baron':
            sprite_count = {'death': 6, 'walks': 4}

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
        if who_is == 'pinky':
            self.health = 8 # Здоровье
        if who_is == 'baron':
            self.health = 30 # Здоровье
        self.is_alive = True # Флаг жив ли противник

        self.death_sound_active = False

    # Функция постоянного обновления состояния противника
    def update(self, player_speed, enemy_size):
        self.rect.x -= self.speed - player_speed # Движение противника на игрока
        # Если противник (живой либо уничтоженный) уходит за левый край на -100 по x, то он исчезает
        if self.rect.right <= -100:
            self.kill()
        elif self.health > 0: # Если противник жив
            # Запуск анимации ходьбы противника
            if self.walks_index < len(self.walks_images):
                self.walks_timer += 1
                if self.walks_timer >= 15 / self.speed :  # Задержка, зависящая от скорости движения противника, чем он
                                                          # медленнее идет, тем выше задержка переключения кадров
                    self.image = pygame.transform.scale(self.walks_images[self.walks_index], enemy_size)
                    self.walks_index += 1
                    self.walks_timer = 0
                    if self.walks_index == len(self.walks_images):
                        self.walks_index = 0
        else: # Если убит
            self.is_alive = False
            self.speed = 0
            # Запуск анимации уничтожения противника
            if self.death_index < len(self.death_images):
                self.death_timer += 1
                if self.death_timer >= 5:  # Задержка в пол секунды
                    self.image = pygame.transform.scale(self.death_images[self.death_index], enemy_size)
                    self.death_index += 1
                    self.death_timer = 0
                    if not self.death_sound_active:
                        self.enemy_dies_sound.play()
                        self.death_sound_active = True
            else:
                self.speed = 0


# Создание группы для противников для отрисовки всех противников одновременно
enemies = pygame.sprite.Group()


# Функция для определения самого ближайшего живого противника к игроку
def find_closest_enemy(player_pos_x):
    closest_enemy = None
    min_distance = float('inf')  # Для вычисления противника с наименьшей дистанцией к игроку
    # Перебор всех существующих противников
    for enemy in enemies:
        if not enemy.is_alive: # Если противник убит, исключаем его из цикла
            continue
        else:
            distance = abs(enemy.rect.x - player_pos_x) # Вычисление дистанции до игрока текущего противника
            if enemy.rect.x > player_pos_x:
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
                if enemy.health <= 0:  # Проверяем, жив ли противник
                    if distance < min_distance:
                        min_distance = distance
                        closest_enemy = enemy
    return closest_enemy


# Функция для определения ближайших живых противников к игроку
def find_n_closest_enemies(player_x, enemies, n=3):
    enemies_with_distance = []
    for enemy in enemies:
        if not enemy.is_alive: # Если противник убит, исключаем его из цикла
            continue
        else:
            for enemy in enemies:
                distance = abs(enemy.rect.centerx - player_x)
                if enemy.health <= 0:
                    pass
                else:
                    enemies_with_distance.append((distance, enemy))
            enemies_with_distance.sort(key=lambda x: x[0])  # сортируем по расстоянию
            return [enemy for _, enemy in enemies_with_distance[:n]]  # возвращаем только объекты врагов


# VVV Игровой цикл VVV


# Создание противника с определенной вероятностью
def enemy_random_create(background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed,
                        enemy_dies_sound_imp, enemy_dies_sound_pinky, enemy_dies_sound_baron):
    if random.randint(1, 50) == 1:
        enemy_var = Enemy(background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound_imp, who_is='imp')
        enemies.add(enemy_var)
    elif random.randint(1, 100) == 2:
        enemy_var = Enemy(background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound_pinky, who_is='pinky')
        enemies.add(enemy_var)
    elif random.randint(1, 200) == 3:
        enemy_var = Enemy(background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound_baron, who_is='baron')
        enemies.add(enemy_var)
    else:
        enemy_var = None
    return enemy_var

# Обновление позиций противников
def enemy_position_update(enemy_var, player_speed, enemy_size):
    enemies.update(player_speed, enemy_size)