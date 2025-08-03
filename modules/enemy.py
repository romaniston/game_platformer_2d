import sys
import random
import math

import pygame

from modules.player import player_pos_x_val, set_player_parameters


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


# Установка спрайтов проджектайлов
def set_enemy_projectiles(who_is):
    if who_is == 'imp':
        projectile_path = "assets/enemies/imp/projectile.png"
        projectiles_sprite = pygame.image.load(projectile_path)
        projectile_size = (50, 50)
        damage = -2
    elif who_is == 'cacodemon':
        projectile_path = "assets/enemies/cacodemon/projectile.png"
        projectiles_sprite = pygame.image.load(projectile_path)
        projectile_size = (60, 60)
        damage = -3
    elif who_is == 'baron':
        projectile_path = "assets/enemies/baron/projectile.png"
        projectiles_sprite = pygame.image.load(projectile_path)
        projectile_size = (80, 80)
        damage = -5
    elif who_is == 'cyberdemon':
        projectile_path = "assets/enemies/cyberdemon/projectile.png"
        projectiles_sprite = pygame.image.load(projectile_path)
        projectile_size = (100, 100)
        damage = -10
    return projectiles_sprite, projectile_size, damage


# Установка звуков врагов
def set_enemy_sounds(who_is):
    if who_is == 'imp':
        enemy_dies_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_death.wav")
        enemy_attack_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_attack_sound.wav")
        enemy_proj_blow_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_proj_blow_sound.wav")
    elif who_is == 'pinky':
        enemy_dies_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_death.wav")
        enemy_attack_sound = None
        enemy_proj_blow_sound = None
    elif who_is == 'baron':
        enemy_dies_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_death.wav")
        enemy_attack_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_attack_sound.wav")
        enemy_proj_blow_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_proj_blow_sound.wav")
    elif who_is == 'cyberdemon':
        enemy_dies_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_death.wav")
        enemy_attack_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_attack_sound.wav")
        enemy_proj_blow_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_proj_blow_sound.wav")
    elif who_is == 'cacodemon':
        enemy_dies_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_death.wav")
        enemy_attack_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_attack_sound.wav")
        enemy_proj_blow_sound = pygame.mixer.Sound(f"assets/enemies/{who_is}/sounds/enemy_proj_blow_sound.wav")
    return enemy_dies_sound, enemy_attack_sound, enemy_proj_blow_sound


def damage_to_player(enemy_projectiles, player_hitbox):
    for projectile in enemy_projectiles:
        if projectile.rect.colliderect(player_hitbox):  # или другой hitbox игрока
            if not projectile.is_destroying:
                projectile.start_destruction()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y, who_is):
        super().__init__()

        self.who_is = who_is
        self.projectile_sprite, self.projectile_size, self.damage = set_enemy_projectiles(self.who_is)
        self.enemy_dies_sound, self.enemy_attack_sound, self.enemy_proj_blow_sound = set_enemy_sounds(self.who_is)
        self.image = pygame.transform.scale(self.projectile_sprite, self.projectile_size)
        self.rect = self.image.get_rect(center=(x, y))
        self.attack_sound_active = False
        self.proj_blow_sound_active = False
        self.getting_damage = False

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.is_destroying = False
        self.destroy_index = 0
        self.destroy_timer = 0
        self.destroy_images = [
            pygame.transform.scale(pygame.image.load(
                f"assets/enemies/{who_is}/projectile_destroy_1.png").convert_alpha(), self.projectile_size),
            pygame.transform.scale(pygame.image.load(
                f"assets/enemies/{who_is}/projectile_destroy_2.png").convert_alpha(), self.projectile_size),
            pygame.transform.scale(pygame.image.load(
                f"assets/enemies/{who_is}/projectile_destroy_3.png").convert_alpha(), self.projectile_size),
        ]

    def start_destruction(self):
        self.is_destroying = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.destroy_index = 0
        self.destroy_timer = 0

    def update(self, player_speed=0):
        if not self.is_destroying:

            self.pos_x += self.velocity_x + player_speed
            self.pos_y += self.velocity_y
            self.rect.center = (int(self.pos_x), int(self.pos_y))

            if (self.rect.right < 0 or self.rect.left > 2000 or
                    self.rect.bottom < 0 or self.rect.top > 1200):
                self.kill()
        else:
            if not  self.proj_blow_sound_active:
                self.enemy_proj_blow_sound.play()
                self.proj_blow_sound_active = True

            if not self.getting_damage:
                self.getting_damage = True
                set_player_parameters(only_health=False, change_health=True, change_val=self.damage)

            self.destroy_timer += 1
            if self.destroy_timer >= 5:
                if self.destroy_index < len(self.destroy_images):
                    self.image = self.destroy_images[self.destroy_index]
                    self.destroy_index += 1
                    self.destroy_timer = 0
                else:
                    self.kill()  # Завершить анимацию и удалить снаряд


# Класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, background, enemy_sprite, enemy_size, WIDTH, player_on_ground_y, player_speed,
                 enemy_dies_sound, enemy_attack_sound, enemy_proj_blow_sound, who_is, player_pos_y):
        super().__init__()
        self.enemy_size = enemy_size
        self.image = enemy_sprite
        self.image = pygame.transform.scale(enemy_sprite, self.enemy_size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 200) # Появление за правой границей экрана
        self.attack_images = []
        self.attack_index = 0
        self.attack_timer = 0
        self.enemy_attack_sound_active = False

        if who_is == 'imp':
            self.attack_cooldown = random.randint(50, 100)
        elif who_is == 'cacodemon':
            self.attack_cooldown = random.randint(100, 200)
        elif who_is == 'baron':
            self.attack_cooldown = random.randint(300, 400)
        elif who_is == 'cyberdemon':
            self.attack_cooldown = random.randint(400, 600)

        self.target_player = player_pos_y
        self.projectiles = pygame.sprite.Group()
        self.player_pos_x = player_pos_x_val

        if who_is == 'cyberdemon':
            self.hitbox = self.rect.inflate(-100, 100)
        else:
            self.hitbox = self.rect.inflate(-10, -10)
        if who_is == 'cacodemon':
            self.rect.y = 5
        else:
            self.rect.y = player_on_ground_y - self.rect.height + 100  # Высота противника

            self.attack_index = 0
            self.attack_timer = 0
            self.attacking = False
            self.attack_cooldown = random.randint(200, 400)
            self.attack_counter = 0

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
        self.enemy_attack_sound = enemy_attack_sound
        self.enemy_proj_blow_sound = enemy_proj_blow_sound
        self.who_is = who_is

        self.enemy_dies_sound.set_volume(0.2)
        if self.who_is != 'pinky':
            self.enemy_attack_sound.set_volume(0.2)
            self.enemy_proj_blow_sound.set_volume(0.2)

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
        self.death_index = 0 # Индекс текущего изображения анимации смерти
        self.death_timer = 0 # Таймер для анимации смерти

        # Анимация ходьбы
        self.walks_images = []
        for img_wlk in range(sprite_count['walks']):
            self.walks_images.append(pygame.image.load(f"assets/enemies/{who_is}/enemy_walks_{img_wlk + 1}.png"))
        self.walks_index = 0  # Индекс текущего изображения анимации ходьбы
        self.walks_timer = 0 # Таймер для анимации ходьбы

        # Attack animation
        self.attack_images = []
        if who_is in ['imp', 'baron', 'cacodemon', 'cyberdemon']:
            for i in range(2):
                self.attack_images.append(pygame.image.load(f"assets/enemies/{who_is}/enemy_attacks_{i + 1}.png"))

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

    def shoot_projectile(self, player_pos_y, who_is):
        start_x = self.rect.centerx
        start_y = self.rect.centery

        # Центр игрока (или его положение)
        target_x = self.player_pos_x
        target_y = player_pos_y + 50

        # Вектор направления
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1  # во избежание деления на ноль

        if self.who_is == 'imp':
            speed = 2
        elif self.who_is == 'cacodemon':
            speed = 2
        elif self.who_is == 'baron':
            speed = 4
        elif self.who_is == 'cyberdemon':
            speed = 8

        velocity_x = dx / distance * speed
        velocity_y = dy / distance * speed

        projectile = Projectile(
            x=start_x,
            y=start_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            who_is=self.who_is
        )
        enemy_projectiles.add(projectile)

    # Функция постоянного обновления состояния противника
    def update(self, player_speed, player_on_ground_y, player_pos_y):
        self.rect.x -= self.speed - player_speed

        if self.who_is == 'cyberdemon':
            self.hitbox = self.rect.inflate(-150, -60)
            self.hitbox.x = self.rect.x + 80
            self.hitbox.y = self.rect.y + 60
        else:
            self.hitbox = self.rect.inflate(-10, -10)
            self.hitbox.x = self.rect.x
            self.hitbox.y = self.rect.y

        if self.rect.right <= -100:
            self.kill()
        elif self.health > 0:
            self.walks_timer += 1
            self.attack_timer += 1

            # Анимация ходьбы
            if self.walks_timer >= 15 / self.speed:
                self.image = pygame.transform.scale(self.walks_images[self.walks_index], self.enemy_size)
                self.walks_index = (self.walks_index + 1) % len(self.walks_images)
                self.walks_timer = 0

            # Атака проджектайлом
            if self.who_is in ['imp', 'baron', 'cacodemon', 'cyberdemon']:
                if self.attack_timer >= self.attack_cooldown:
                    if self.rect.x < 700:  # if enemy not out the screen
                        if not self.enemy_attack_sound_active:
                            self.enemy_attack_sound.play()
                            self.enemy_attack_sound_active = True

                        self.image = pygame.transform.scale(self.attack_images[self.attack_index], self.enemy_size)
                        self.attack_index += 1
                        if self.attack_index >= len(self.attack_images):
                            dx = self.player_pos_x
                            dy = player_on_ground_y
                            length = max(1, math.hypot(dx, dy))
                            self.shoot_projectile(player_pos_y, self.who_is)
                            self.attack_timer = 0
                            self.attack_index = 0

        elif self.health <= 0:
            self.is_alive = False
            self.speed = 0
            self.death_timer += 1

            # Cacodemon падает вниз
            if self.who_is == 'cacodemon' and self.rect.y < (player_on_ground_y - 25):
                self.rect.y += 10

            # Анимация смерти
            if self.death_index < len(self.death_images):
                if self.death_timer >= 5:
                    self.image = pygame.transform.scale(self.death_images[self.death_index], self.enemy_size)
                    self.death_index += 1
                    self.death_timer = 0
                    if not self.death_sound_active:
                        self.enemy_dies_sound.play()
                        self.death_sound_active = True


# Создание группы для противников и проджектайлов для отрисовки всех противников одновременно
enemies = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()


def chance(start, end):
    return random.randint(start, end)


# VVV For Game Circle VVV


# Создание противника с определенной вероятностью
def enemy_random_create(background, WIDTH, player_on_ground_y, player_speed, player_pos_y):
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

    enemy_dies_sound, enemy_attack_sound, enemy_proj_blow_sound = set_enemy_sounds(who_is)

    enemy = Enemy(
        background=background,
        enemy_sprite=enemy_sprite,
        enemy_size=enemy_size,
        WIDTH=WIDTH,
        player_on_ground_y=player_on_ground_y,
        player_speed=player_speed,
        enemy_dies_sound=enemy_dies_sound,
        enemy_attack_sound=enemy_attack_sound,
        enemy_proj_blow_sound=enemy_proj_blow_sound,
        who_is=who_is,
        player_pos_y=player_pos_y
    )
    enemies.add(enemy)
    return enemy


# Обновление позиций противников
def enemy_position_update(player_speed, player_on_ground_y, player_pos_y):
    for enemy in enemies:
        enemy.update(player_speed, player_on_ground_y, player_pos_y)
    enemy_projectiles.update()

