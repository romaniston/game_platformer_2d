import pygame
import sys
import random

# Установка спрайтов врагов
def set_enemy_sprites():
    enemy_sprite_path = "assets/enemies/enemy_walks_1.png"
    enemy_sprite = pygame.image.load(enemy_sprite_path)
    enemy_size = (100, 100)
    return enemy_sprite_path, enemy_sprite, enemy_size

# Установка звуков врагов
def set_enemy_sounds():
    enemy_dies_sound = pygame.mixer.Sound("assets/enemies/sounds/enemy_death.wav")
    return enemy_dies_sound

# Класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound):
        super().__init__()
        self.image = enemy_sprite
        self.image = pygame.transform.scale(enemy_sprite, enemy_size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 200) # Появление за правой границей экрана
        self.rect.y = (player_on_ground_y) # Высота противника
        self.speed = random.randint(1, 3) # Случайная скорость
        self.background = background

        # Загружаем анимации противника
        # Список изображений для анимации уничтожения
        self.death_images = []
        for img_dth in range(6):
            self.death_images.append(pygame.image.load(f"assets/enemies/enemy_death_{img_dth + 1}.png"))
        self.death_index = 0  # Индекс текущего изображения анимации смерти
        self.death_timer = 0 # Таймер для анимации смерти
        # Анимация ходьбы
        self.walks_images = []
        for img_wlk in range(4):
            self.walks_images.append(pygame.image.load(f"assets/enemies/enemy_walks_{img_wlk + 1}.png"))
        self.walks_index = 0  # Индекс текущего изображения анимации ходьбы
        self.walks_timer = 0 # Таймер для анимации ходьбы

        self.speed = random.randint(1, 3) # Случайная скорость
        self.health = 3 # Здоровье
        self.is_alive = True # Флаг жив ли противник
        self.death_sound_active = False

    # Функция постоянного обновления состояния противника
    def update(self, player_speed, enemy_size, enemy_dies_sound):
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
                        enemy_dies_sound.play()
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



# VVV Игровой цикл VVV



# Создание противника с определенной вероятностью
def enemy_random_create(background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound):
    if random.randint(1, 50) == 1:
        enemy_var = Enemy(background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed, enemy_dies_sound)
        enemies.add(enemy_var)
    else:
        enemy_var = None
    return enemy_var

# Обновление позиций противников
def enemy_position_update(enemy_var, player_speed, enemy_size, enemy_dies_sound):
    enemies.update(player_speed, enemy_size, enemy_dies_sound)