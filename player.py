import pygame
import sys
import random

# Установка спрайтов игрока
def set_player_sprites():
    player_image_player_stands_path = "assets/player/player_stands_1.png"
    player_image = pygame.image.load(player_image_player_stands_path)
    player_size = (200, 100)
    player_image = pygame.transform.scale(player_image, player_size) # Изменение разрешения спрайта
    player_walks = [pygame.image.load(f"assets/player/player_walks_{i}.png") for i in range(1, 5)]
    player_size_walks = (200, 100)
    player_walks = [pygame.transform.scale(img, player_size_walks) for img in player_walks]
    return player_image_player_stands_path, player_image, player_size, player_image, player_walks, player_size_walks, player_walks

# Установка параметров игрока
def set_player_parameters():
    player_on_ground_y = 202
    player_pos_x = 75
    player_pos_y = player_on_ground_y
    jump_strength = 18
    gravity = 1
    jump_speed = jump_strength  # Начальная скорость прыжка
    on_ground = True
    shoot_start_time = 0
    shoot_last_time = 0
    player_speed = 0
    current_walk_frame = 0 # Индекс текущего кадра анимации ходьбы
    player_shooting = False
    is_running_sound_playing = False # Переменная для отслеживания проигрывания звука бега
    speed_val = 5
    selected_weapon = 'pistol'
    shooting_player_image = pygame.image.load("assets/player/player_pistol_shoots.png")
    shoot_button_pressed = False
    ammo_supershotgun_left = 2
    supershotgun_reload_ping = 0
    return player_on_ground_y, player_pos_x, player_pos_y, jump_strength, gravity, jump_speed, on_ground,\
        shoot_start_time, shoot_last_time, player_speed, current_walk_frame, player_shooting, is_running_sound_playing,\
        speed_val, selected_weapon, shooting_player_image, shoot_button_pressed, ammo_supershotgun_left,\
        supershotgun_reload_ping

# Установка звуков игрока
def set_player_sounds():
    player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/pistol_shoot.wav")
    player_jumps_sound = pygame.mixer.Sound("assets/player/sounds/player_jumps.wav")
    player_runs_sound = pygame.mixer.Sound("assets/player/sounds/player_runs_1.wav")
    return player_shoots_sound, player_jumps_sound, player_runs_sound