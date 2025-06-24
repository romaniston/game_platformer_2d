import sys
import random

import pygame

import game, player, enemy, weapon


# Инициализация Pygame
pygame.init()

# Установка разрешения
screen, WIDTH, HEIGHT =\
    game.set_screen_resolution(800, 360)

# Установка бэкграунда
background, background_rect, background_width, background1_rect, background2_rect =\
    game.set_backrounds("assets/background/background.jpg")

# Установка и запуск фоновой музыки
game.set_background_music("assets/background/background_music.mp3")

# Установка спрайтов игрока
player_image_player_stands_path, player_image, player_size, player_image, player_walks,\
        player_size_walks, player_walks =\
    player.set_player_sprites()

# Установка спрайтов врагов
enemy_sprite_path, enemy_sprite, enemy_size =\
    enemy.set_enemy_sprites('imp')

# Установка параметров игрока
player_on_ground_y, player_pos_x, player_pos_y, jump_strength, gravity, jump_speed, on_ground, \
        shoot_start_time, shoot_last_time, player_speed, current_walk_frame, player_shooting,\
        is_running_sound_playing, speed_val, selected_weapon, shooting_player_image, shoot_button_pressed,\
        ammo_supershotgun_left, supershotgun_reload_ping =\
    player.set_player_parameters()

# Установка параметров панели с оружием
pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect,\
        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect,\
        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect,\
        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect,\
        machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect =\
    weapon.weapons_bar("pistol")

# Установка звуковых эффектов
player_shoots_sound, player_jumps_sound, player_runs_sound = player.set_player_sounds()
enemy_dies_sound_imp = enemy.set_enemy_sounds('imp')
enemy_dies_sound_pinky = enemy.set_enemy_sounds('pinky')
enemy_dies_sound_baron = enemy.set_enemy_sounds('baron')

selected_weapon_sound = weapon.set_selected_weapon_sounds()

# Переменные для отслеживания времени смены кадров анимации
last_frame_change_time = pygame.time.get_ticks()
last_frame_change_time_stands = pygame.time.get_ticks()

# Переменная для текущего времени
current_time = pygame.time.get_ticks()

# Игровой цикл
while True:

    # Словарь состояния клавиш клавиатуры в нажатом состоянии
    shooting_button_pressed = False

    # Стрельба из автоматического оружия
    if selected_weapon == 'mp5':
        shoot_button_pressed, current_time, shoot_start_time, player_shoots_sound, player_shooting, player_image,\
            shooting_player_image, player_size, shoot_last_time, on_ground =\
                weapon.auto_gun_shooting(selected_weapon, 125, 1.5, 20, shoot_button_pressed, current_time,
                                         shoot_start_time,
                                         player_shoots_sound, player_shooting, player_image, shooting_player_image, player_size,
                                         shoot_last_time, on_ground, player_pos_x)
    elif selected_weapon == 'machine_gun':
        shoot_button_pressed, current_time, shoot_start_time, player_shoots_sound, player_shooting, player_image,\
            shooting_player_image, player_size, shoot_last_time, on_ground =\
                weapon.auto_gun_shooting(selected_weapon, 100, 5, 75, shoot_button_pressed, current_time,
                                         shoot_start_time,
                                         player_shoots_sound, player_shooting, player_image, shooting_player_image,
                                         player_size,
                                         shoot_last_time, on_ground, player_pos_x)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_speed = speed_val
            elif event.key == pygame.K_d:
                player_speed = - speed_val
            elif event.key == pygame.K_w and on_ground:
                player_jumps_sound.play()
                jump_speed = jump_strength # Восстанавливаем начальную скорость прыжка
                on_ground = False
                player_runs_sound.stop()

            # Выбор оружия
            elif event.key == pygame.K_1:
                selected_weapon = 'pistol'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/pistol_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_pistol_shoots.png")

                pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect, \
                        machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect =\
                    weapon.weapons_bar("pistol")

                selected_weapon_sound.play()

            elif event.key == pygame.K_2:
                selected_weapon = 'shotgun'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/shotgun_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_shotgun_shoots.png")

                pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect, \
                        machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect =\
                    weapon.weapons_bar("shotgun")

                selected_weapon_sound.play()

            elif event.key == pygame.K_3:
                selected_weapon = 'mp5'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/mp5_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_mp5_shoots.png")

                pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect, \
                        machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect =\
                    weapon.weapons_bar("mp5")

                selected_weapon_sound.play()

            elif event.key == pygame.K_4:
                selected_weapon = 'supershotgun'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/supershotgun_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_supershotgun_shoots.png")

                pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect, \
                        machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect =\
                    weapon.weapons_bar("supershotgun")

                selected_weapon_sound.play()

            elif event.key == pygame.K_5:
                selected_weapon = 'machine_gun'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/machine_gun_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_supershotgun_shoots.png")

                pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect, \
                        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect, \
                        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect, \
                        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect, \
                        machine_gun_icon_on_bar, machine_gun_icon_on_bar_size, machine_gun_icon_on_bar_rect =\
                    weapon.weapons_bar("machine_gun")

                selected_weapon_sound.play()

            # Обработка выстрелов
            elif event.key == pygame.K_SPACE:
                if selected_weapon == 'pistol':
                    selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting, \
                            player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,\
                            ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed =\
                        weapon.selected_weapon_parameters(selected_weapon, current_time, shoot_start_time,
                                                          player_shoots_sound, player_shooting, player_image,
                                                          shooting_player_image, on_ground, player_size, player_pos_x,
                                                          shoot_last_time, ammo_supershotgun_left,
                                                          supershotgun_reload_ping, shoot_button_pressed)

                elif selected_weapon == 'shotgun':
                    selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting, \
                            player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,\
                            ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed =\
                        weapon.selected_weapon_parameters(selected_weapon, current_time, shoot_start_time,
                                                          player_shoots_sound, player_shooting, player_image,
                                                          shooting_player_image, on_ground, player_size, player_pos_x,
                                                          shoot_last_time, ammo_supershotgun_left,
                                                          supershotgun_reload_ping, shoot_button_pressed)

                elif selected_weapon == 'mp5':
                    selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting, \
                            player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,\
                            ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed =\
                        weapon.selected_weapon_parameters(selected_weapon, current_time, shoot_start_time,
                                                          player_shoots_sound, player_shooting, player_image,
                                                          shooting_player_image, on_ground, player_size, player_pos_x,
                                                          shoot_last_time, ammo_supershotgun_left,
                                                          supershotgun_reload_ping, shoot_button_pressed)

                elif selected_weapon == 'supershotgun':
                    selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting, \
                            player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,\
                            ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed =\
                        weapon.selected_weapon_parameters(selected_weapon, current_time, shoot_start_time,
                                                          player_shoots_sound, player_shooting, player_image,
                                                          shooting_player_image, on_ground, player_size, player_pos_x,
                                                          shoot_last_time, ammo_supershotgun_left,
                                                          supershotgun_reload_ping, shoot_button_pressed)

                elif selected_weapon == 'machine_gun':
                    selected_weapon, current_time, shoot_start_time, player_shoots_sound, player_shooting, \
                            player_image, shooting_player_image, on_ground, player_size, player_pos_x, shoot_last_time,\
                            ammo_supershotgun_left, supershotgun_reload_ping, shoot_button_pressed =\
                        weapon.selected_weapon_parameters(selected_weapon, current_time, shoot_start_time,
                                                          player_shoots_sound, player_shooting, player_image,
                                                          shooting_player_image, on_ground, player_size, player_pos_x,
                                                          shoot_last_time, ammo_supershotgun_left,
                                                          supershotgun_reload_ping, shoot_button_pressed)

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                player_speed = 0
                player_runs_sound.stop()

    # Воспроизведение звука бега, если игрок находится на земле и движется
    is_running_sound_playing = player.player_walks_sound(on_ground, player_speed, is_running_sound_playing, player_runs_sound)

    # Получение обновляемого текущего времени
    current_time = pygame.time.get_ticks()

    # Увеличение скорости игрока при прыжке
    player_speed = player.increase_speed_when_player_jump(on_ground, player_speed, speed_val)

    # Обработка выстрела. Если после начала выстрела прошло более N млс, то возвращаем спрайт player_stands
    shoot_start_time, player_image, player_image_player_stands_path, player_size, player_shooting =\
        weapon.shot_image_ping(current_time, shoot_start_time, player_image, player_image_player_stands_path,
                               player_size, player_shooting)

    # Перемещение фонов для создания иллюзии движения игрока
    game.background_movement(background1_rect, background2_rect, background_width, player_speed, WIDTH)

    # Применение гравитации и инерции к прыжку игрока
    on_ground, player_pos_y, jump_speed, gravity, player_on_ground_y =\
        player.player_jump(on_ground, player_pos_y, jump_speed, gravity, player_on_ground_y)

    # Создание противника с определенной вероятностью
    enemy_var = enemy.enemy_random_create(background, WIDTH, player_on_ground_y, player_speed)


    # Обновление позиций противников
    enemy.enemy_position_update(player_speed)

    # Отрисовка объектов
    (screen, background, background1_rect, background2_rect, pistol_icon_on_bar, pistol_icon_on_bar_rect,
            shotgun_icon_on_bar, shotgun_icon_on_bar_rect, mp5_icon_on_bar, mp5_icon_on_bar_rect,
            supershotgun_icon_on_bar, supershotgun_icon_on_bar_rect, machine_gun_icon_on_bar,
            machine_gun_icon_on_bar_rect, enemy) =\
        game.drawing_objects(screen, background, background1_rect, background2_rect, pistol_icon_on_bar,
                             pistol_icon_on_bar_rect, shotgun_icon_on_bar, shotgun_icon_on_bar_rect,
                             mp5_icon_on_bar, mp5_icon_on_bar_rect, supershotgun_icon_on_bar,
                             supershotgun_icon_on_bar_rect, machine_gun_icon_on_bar, machine_gun_icon_on_bar_rect,
                             enemy)

    # Анимация player_walks + замена спрайта игрока при выстреле при ходьбе
    player_speed, player_shooting, player_image, shooting_player_image, player_size, player_pos_x,\
            player_pos_y, on_ground, player_walks, current_walk_frame, screen =\
        player.player_walks(player_speed, player_shooting, player_image, shooting_player_image, player_size,
                            player_pos_x, player_pos_y, on_ground, player_walks, current_walk_frame, screen)

    # Замена спрайта игрока в прыжке на player_stands
    on_ground, player_shooting, player_image_player_stands_path, player_image, \
            player_size, screen, player_pos_x, player_pos_y =\
        player.set_sprite_while_jumping(on_ground, player_shooting, player_image_player_stands_path, player_image,
                                        player_size, screen, player_pos_x, player_pos_y)

    # Изменение current_walk_frame каждые 100 млс
    last_frame_change_time, player_speed, current_walk_frame, player_walks =\
        player.player_walking(last_frame_change_time, player_speed, current_walk_frame, player_walks, current_time)

    # Анимация стойки игрока
    last_frame_change_time_stands, on_ground, player_image_player_stands_path, player_image, player_size =\
        player.player_staying_and_breating_animation(current_time, last_frame_change_time_stands, on_ground,
                                                     player_image_player_stands_path, player_image, player_size)

    # Обновление экрана после отрисовки объектов
    pygame.display.flip()

    # FPS
    pygame.time.Clock().tick(60)