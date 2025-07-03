import sys
import random
from logging import exception

import pygame

from modules import enemy


# weapons_bar (панель выбора оружия)
def weapons_bar(selected_weapon):
    if selected_weapon == "pistol":
        pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_selected.png")
    else:
        pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_not_selected.png")
    pistol_icon_on_bar_size = (80, 70)
    pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
    pistol_icon_on_bar_rect = pistol_icon_on_bar.get_rect()
    pistol_icon_on_bar_rect.x = 0
    if selected_weapon == "shotgun":
        shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_selected.png")
    else:
        shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_not_selected.png")
    shotgun_icon_on_bar_size = (80, 70)
    shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
    shotgun_icon_on_bar_rect = shotgun_icon_on_bar.get_rect()
    shotgun_icon_on_bar_rect.x = 80
    if selected_weapon == "mp5":
        mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_selected.png")
    else:
        mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_not_selected.png")
    mp5_icon_on_bar_size = (80, 70)
    mp5_icon_on_bar = pygame.transform.scale(mp5_icon_on_bar, shotgun_icon_on_bar_size)
    mp5_icon_on_bar_rect = mp5_icon_on_bar.get_rect()
    mp5_icon_on_bar_rect.x = 160
    if selected_weapon == "supershotgun":
        supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_selected.png")
    else:
        supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_not_selected.png")
    supershotgun_icon_on_bar_size = (80, 70)
    supershotgun_icon_on_bar = pygame.transform.scale(supershotgun_icon_on_bar, shotgun_icon_on_bar_size)
    supershotgun_icon_on_bar_rect = supershotgun_icon_on_bar.get_rect()
    supershotgun_icon_on_bar_rect.x = 240
    if selected_weapon == "machine_gun":
        machine_gun_icon_on_bar = pygame.image.load("assets/weapons_bar/machine_gun_selected.png")
    else:
        machine_gun_icon_on_bar = pygame.image.load("assets/weapons_bar/machine_gun_not_selected.png")
    machine_gun_icon_on_bar_size = (80, 70)
    machine_gun_icon_on_bar = pygame.transform.scale(machine_gun_icon_on_bar, shotgun_icon_on_bar_size)
    machine_gun_icon_on_bar_rect = machine_gun_icon_on_bar.get_rect()
    machine_gun_icon_on_bar_rect.x = 320
    return pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                    shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                    mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                    supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect, \
                    machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect


# Установка звука выбора оружия
def set_selected_weapon_sounds():
    selected_weapon_sound = pygame.mixer.Sound("assets/player/sounds/weapons/select_weapon.mp3")
    return selected_weapon_sound


def auto_gun_shooting(selected_weapon, ping, damage, inertion, shoot_button_pressed, current_time, shoot_start_time,
                      player_shoots_sound, player_shooting, player_image, shooting_player_image, player_size,
                      shoot_last_time, on_ground, player_pos_x, player_pos_y, enemy):
    keys = pygame.key.get_pressed()

    # Обработка зажатия кнопки выстрела при автоматической стрельбе
    if keys[pygame.K_SPACE] and selected_weapon in ["machine_gun", "mp5"]:
        shoot_button_pressed = True

        if current_time - shoot_start_time >= ping:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = current_time
            shoot_last_time = current_time

            # Построение линии выстрела
            line_height = 4  # уже, чем у shotgun
            line_length = 1000
            line_y = player_pos_y + player_size[1] // 2 - line_height // 2
            line_rect = pygame.Rect(player_pos_x + 40, line_y, line_length, line_height)

            # Найти ближайшего врага по линии
            enemies_hit = [e for e in enemy.enemies if e.hitbox.colliderect(line_rect) and e.health > 0]
            if enemies_hit:
                closest_enemy = min(enemies_hit, key=lambda e: e.rect.x)
                closest_enemy.health -= damage
                closest_enemy.rect.x += inertion  # инерция от выстрела
    else:
        shoot_button_pressed = False

    return shoot_button_pressed, current_time, shoot_start_time, player_shoots_sound, player_shooting, player_image, \
        shooting_player_image, player_size, shoot_last_time, on_ground


def selected_weapon_parameters(selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting,
                               player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,
                               ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed, player_pos_y):
    if selected_weapon == 'pistol':
        if current_time - shoot_start_time >= 150:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = pygame.time.get_ticks()  # Запоминаем время начала выстрела

            # Линия выстрела
            line_height = 1
            line_length = 1000  # насколько далеко стреляет
            line_y = player_pos_y + player_size[1] // 2 - line_height // 2  # центр игрока по вертикали
            line_rect = pygame.Rect(player_pos_x + 40, line_y, line_length, line_height)

            # Найти всех врагов, пересекающихся с линией
            enemies_hit = [e for e in enemy.enemies if e.hitbox.colliderect(line_rect) and e.health > 0]

            if enemies_hit:
                # Выбрать ближайшего по x (вперед по оси x)
                closest_enemy = min(enemies_hit, key=lambda e: e.rect.x)
                # Нанести урон и инерцию
                closest_enemy.health -= 1  # урон
                closest_enemy.rect.x += 10  # инерция

    elif selected_weapon == 'shotgun':
        if current_time - shoot_start_time >= 500:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = pygame.time.get_ticks()  # Запоминаем время начала выстрела

            # Линия выстрела
            line_height = 5
            line_length = 1000  # насколько далеко стреляет
            line_y = player_pos_y + player_size[1] // 2 - line_height // 2  # центр игрока по вертикали
            line_rect = pygame.Rect(player_pos_x + 40, line_y, line_length, line_height)

            # Найти всех врагов, пересекающихся с линией
            enemies_hit = [e for e in enemy.enemies if e.hitbox.colliderect(line_rect) and e.health > 0]

            if enemies_hit:
                # Выбрать ближайшего по x (вперед по оси x)
                closest_enemy = min(enemies_hit, key=lambda e: e.rect.x)
                # Нанести урон и инерцию
                closest_enemy.health -= 3  # урон
                closest_enemy.rect.x += 30  # инерция

    elif selected_weapon == 'mp5':
        while shoot_button_pressed:
            pass

    elif selected_weapon == 'machine_gun':
        while shoot_button_pressed:
            pass

    elif selected_weapon == 'supershotgun':
        if ammo_supershotgun_left == 2:
            player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/supershotgun_single_shoot.wav")
            if ammo_supershotgun_left != 2:
                supershotgun_reload_ping = 100
        elif ammo_supershotgun_left == 1:
            player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/supershotgun_shoot.wav")
            supershotgun_reload_ping = 100

        if current_time - shoot_start_time >= supershotgun_reload_ping:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = current_time  # Запоминаем время начала выстрела

            # Линия выстрела
            line_height = 12  # шире, чем у пистолета
            line_length = 1000
            line_y = player_pos_y + player_size[1] // 2 - line_height // 2
            line_rect = pygame.Rect(player_pos_x + 40, line_y, line_length, line_height)

            # Найти всех врагов, пересекающихся с линией
            enemies_hit = [e for e in enemy.enemies if e.hitbox.colliderect(line_rect) and e.health > 0]

            if enemies_hit:
                # Отсортировать по расстоянию по X и выбрать до 3-х ближайших
                enemies_hit.sort(key=lambda e: e.rect.x)
                for e in enemies_hit[:3]:  # максимум 3 врага
                    e.health -= 10
                    e.rect.x += 40  # инерция

            # Управление перезарядкой
            if ammo_supershotgun_left == 1:
                supershotgun_reload_ping = 750
                ammo_supershotgun_left = 2
            else:
                ammo_supershotgun_left -= 1
    else:
        pass

    return selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting,\
        player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,\
        ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed


    # Обработка выстрела. Если после начала выстрела прошло более N млс, то возвращаем спрайт player_stands
def shot_image_ping(current_time, shoot_start_time, player_image, player_image_player_stands_path, player_size,
                    player_shooting):
    if current_time - shoot_start_time >= 100:
        player_image = pygame.image.load(player_image_player_stands_path)
        player_image = pygame.transform.scale(player_image, player_size)
        player_shooting = False
    return shoot_start_time, player_image, player_image_player_stands_path, player_size, player_shooting