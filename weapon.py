import pygame
import sys
import random
import enemy

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
    return pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                    shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                    mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                    supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect

# Установка звука выбора оружия
def set_selected_weapon_sounds():
    selected_weapon_sound = pygame.mixer.Sound("assets/player/sounds/weapons/select_weapon.mp3")
    return selected_weapon_sound

def auto_gun_shooting(selected_weapon, ping, damage, inertion, shoot_button_pressed, current_time, shoot_start_time,
                      player_shoots_sound, player_shooting, player_image, shooting_player_image, player_size,
                      shoot_last_time, on_ground, player_pos_x):
    keys = pygame.key.get_pressed()
    # Обработка зажатия кнопки выстрела при автоматической стрельбе
    if keys[pygame.K_SPACE] and selected_weapon in ["mp5"]:
        shoot_button_pressed = True
        print(shoot_button_pressed)
        if current_time - shoot_start_time >= ping:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = current_time  # Запоминаем время начала выстрела
            shoot_last_time = current_time
            print(123)

            # Уменьшение здоровья врага при выстреле и уничтожение
            closest_enemy = enemy.find_closest_enemy(player_pos_x)
            if on_ground:  # Если игрок на земле, он попадает по противникам
                if closest_enemy:
                    if closest_enemy.health > 0:
                        closest_enemy.health -= damage
                        closest_enemy.rect.x += inertion  # Инерция противника от выстрела
    else:
        shoot_button_pressed = False
    return shoot_button_pressed, current_time, shoot_start_time, player_shoots_sound, player_shooting, player_image,\
        shooting_player_image, player_size, shoot_last_time, on_ground

def selected_weapon_parameters(selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting,
                               player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,
                               ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed):
    if selected_weapon == 'pistol':
        if current_time - shoot_start_time >= 150:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = pygame.time.get_ticks()  # Запоминаем время начала выстрела

            # Уменьшение здоровья врага при выстреле и уничтожение
            closest_enemy = enemy.find_closest_enemy(player_pos_x)
            if on_ground:  # Если игрок на земле, он попадает по противникам
                if closest_enemy:
                    if closest_enemy.health > 0:
                        closest_enemy.health -= 1
                        closest_enemy.rect.x += 10  # Инерция противника от выстрела
            else:
                pass

    elif selected_weapon == 'shotgun':
        if current_time - shoot_start_time >= 500:
            player_shoots_sound.play()
            player_shooting = True
            player_image = shooting_player_image
            player_image = pygame.transform.scale(player_image, player_size)
            shoot_start_time = pygame.time.get_ticks()  # Запоминаем время начала выстрела

            # Уменьшение здоровья врага при выстреле и уничтожение
            closest_enemy = enemy.find_closest_enemy(player_pos_x)
            if on_ground:  # Если игрок на земле, он попадает по противникам
                if closest_enemy:
                    if closest_enemy.health > 0:
                        closest_enemy.health -= 3
                        closest_enemy.rect.x += 30  # Инерция противника от выстрела
            else:
                pass

    elif selected_weapon == 'mp5':
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

            # Уменьшение здоровья врага при выстреле и уничтожение
            closest_enemy = enemy.find_closest_enemy(player_pos_x)
            if on_ground:  # Если игрок на земле, он попадает по противникам
                if closest_enemy:
                    if closest_enemy.health > 0:
                        closest_enemy.health -= 10
                        closest_enemy.rect.x += 40  # Инерция противника от выстрела

            if ammo_supershotgun_left == 1:
                supershotgun_reload_ping = 750
                ammo_supershotgun_left = 2
            else:
                ammo_supershotgun_left -= 1
            print(ammo_supershotgun_left)
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