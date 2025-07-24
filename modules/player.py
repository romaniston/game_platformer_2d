import sys
import random

import pygame


player_health = 100

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

player_pos_x_val = 75

# Установка параметров игрока
def set_player_parameters(only_health, change_health, change_val):

    global player_health

    player_on_ground_y = 202
    player_pos_x = player_pos_x_val
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

    if only_health:
        return player_health
    elif change_health:
        player_health += int(change_val)
        print(change_val)
        return player_health
    else:
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


# Воспроизведение звука бега, если игрок находится на земле и движется
def player_walks_sound(on_ground, player_speed, is_running_sound_playing, player_runs_sound):
    if on_ground and (player_speed != 0):
        if not is_running_sound_playing:
            player_runs_sound.play(-1)
            is_running_sound_playing = True
    elif (player_speed == 0) or (not on_ground):
        player_runs_sound.stop()
        is_running_sound_playing = False
    return is_running_sound_playing


# Увеличение скорости игрока при прыжке
def increase_speed_when_player_jump(on_ground, player_speed, speed_val):
    keys = pygame.key.get_pressed()

    if not on_ground:
        if player_speed > 0:
            player_speed = speed_val + 5
        if player_speed < 0:
            player_speed = speed_val - 15
    elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] and on_ground:
        if player_speed > 0:
            player_speed = speed_val + 5
        if player_speed < 0:
            player_speed = speed_val - 15
    else:
        if player_speed > 0:
            player_speed = speed_val
        if player_speed < 0:
            player_speed = - speed_val
    return player_speed


# Применение гравитации и инерции к прыжку игрока
def player_jump(on_ground, player_pos_y, jump_speed, gravity, player_on_ground_y):
    if not on_ground:
        player_pos_y -= jump_speed
        jump_speed -= gravity
        # Если игрок касается земли, устанавливаем булеву on_ground в True
        if player_pos_y >= player_on_ground_y:
            player_pos_y = player_on_ground_y
            on_ground = True
    return on_ground, player_pos_y, jump_speed, gravity, player_on_ground_y


# Анимация player_walks + замена спрайта игрока при выстреле при ходьбе
def player_walks(player_speed, player_shooting, player_image, shooting_player_image, player_size, player_pos_x,
                 player_pos_y, on_ground, player_walks, current_walk_frame, screen):
    if player_speed < 0:
        if player_shooting == True:
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            screen.blit(player_image, (player_pos_x, player_pos_y))
        elif on_ground == True:
            screen.blit(player_walks[current_walk_frame], (player_pos_x, player_pos_y))
        else:
            pass
    elif player_speed > 0:
        if player_shooting == True:
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            screen.blit(player_image, (player_pos_x, player_pos_y))
        elif on_ground == True:
            screen.blit(player_walks[current_walk_frame], (player_pos_x, player_pos_y))
        else:
            pass
    else:
        # Игрок стоит на месте
        screen.blit(player_image, (player_pos_x, player_pos_y))
    return player_speed, player_shooting, player_image, shooting_player_image, player_size, player_pos_x,\
                 player_pos_y, on_ground, player_walks, current_walk_frame, screen


# Замена спрайта игрока в прыжке на player_stands
def set_sprite_while_jumping(on_ground, player_shooting, player_image_player_stands_path, player_image,
                             player_size, screen, player_pos_x, player_pos_y):
    if not on_ground:
        if not player_shooting:
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            screen.blit(player_image, (player_pos_x, player_pos_y))
        else:
            pass
    return on_ground, player_shooting, player_image_player_stands_path, player_image,\
                             player_size, screen, player_pos_x, player_pos_y


# Изменение current_walk_frame каждые 100 млс
def player_walking(last_frame_change_time, player_speed, current_walk_frame, player_walks, current_time):
    if current_time - last_frame_change_time >= 100:  # Переключение кадров player_walks каждые 0.1 секунды
        if player_speed < 0:
            current_walk_frame = (current_walk_frame + 1) % len(player_walks)
            last_frame_change_time = current_time
        if player_speed > 0:
            current_walk_frame = (current_walk_frame - 1) % len(player_walks)
            last_frame_change_time = current_time
    return last_frame_change_time, player_speed, current_walk_frame, player_walks


# Анимация стойки игрока
def player_staying_and_breating_animation(current_time, last_frame_change_time_stands, on_ground, player_image_player_stands_path,
                                          player_image, player_size):
    if current_time - last_frame_change_time_stands >= 300 and on_ground:
        if player_image_player_stands_path == "assets/player/player_stands_1.png":
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            last_frame_change_time_stands = current_time
            player_image_player_stands_path = "assets/player/player_stands_2.png"
        else:
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            last_frame_change_time_stands = current_time
            player_image_player_stands_path = "assets/player/player_stands_1.png"
    return last_frame_change_time_stands, on_ground, player_image_player_stands_path,\
                                          player_image, player_size


# Создание хитбокса игрока
def get_player_hitbox(player_pos_x, player_pos_y, player_size):
    hitbox_width = int(player_size[0] * 0.2)
    hitbox_height = int(player_size[1] * 0.6)
    hitbox_x = player_pos_x + int(player_size[0] - 200)
    hitbox_y = player_pos_y + int(player_size[1] * 0.2)
    return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)
