import pygame
import sys
import random
import game, player, enemy, weapon

# Инициализация Pygame
pygame.init()

# Установка разрешения
screen, WIDTH, HEIGHT = game.set_screen_resolution(800, 360)

# Установка бэкграунда
background, background_rect, background_width, background1_rect, background2_rect = game.set_backrounds("assets/background/background.jpg")

# Установка и запуск фоновой музыки
game.set_background_music("assets/background/background_music.mp3")

# Установка спрайтов игрока
player_image_player_stands_path, player_image, player_size, player_image, player_walks, player_size_walks, player_walks = player.set_player_sprites()

# Установка спрайтов врагов
enemy_sprite_path, enemy_sprite, enemy_size = enemy.set_enemy_sprites()

# Установка параметров игрока
player_on_ground_y, player_pos_x, player_pos_y, jump_strength, gravity, jump_speed, on_ground, \
    shoot_start_time, shoot_last_time, player_speed, current_walk_frame, player_shooting, is_running_sound_playing,\
    speed_val, selected_weapon, shooting_player_image, shoot_button_pressed, ammo_supershotgun_left,\
    supershotgun_reload_ping = player.set_player_parameters()

# Установка параметров панели с оружием
pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect,\
        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect,\
        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect,\
        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect = weapon.weapons_bar_parameters()

# Установка звуковых эффектов
player_shoots_sound, player_jumps_sound, player_runs_sound = player.set_player_sounds()
enemy_dies_sound = enemy.set_enemy_sounds()
selected_weapon_sound = weapon.set_selected_weapon_sounds()

# Переменные для отслеживания времени смены кадров анимации
last_frame_change_time = pygame.time.get_ticks()
last_frame_change_time_stands = pygame.time.get_ticks()

# Переменная для текущего времени
current_time = pygame.time.get_ticks()

# Игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # # Словарь состояния клавиш клавиатуры в нажатом состоянии
        # keys = pygame.key.get_pressed()
        #
        # # Обработка зажатия кнопки выстрела при автоматической стрельбе
        # if keys[pygame.K_SPACE]:
        #     shoot_button_pressed = True
        #     print(shoot_button_pressed)
        # else:
        #     shoot_button_pressed = False

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
                shooting_player_image =pygame.image.load("assets/player/player_pistol_shoots.png")
                pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_selected.png")
                shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_not_selected.png")
                mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_not_selected.png")
                supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_not_selected.png")
                pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
                shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
                mp5_icon_on_bar = pygame.transform.scale(mp5_icon_on_bar, mp5_icon_on_bar_size)
                supershotgun_icon_on_bar = pygame.transform.scale(supershotgun_icon_on_bar,
                                                                  supershotgun_icon_on_bar_size)
                selected_weapon_sound.play()
            elif event.key == pygame.K_2:
                selected_weapon = 'shotgun'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/shotgun_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_shotgun_shoots.png")
                pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_not_selected.png")
                shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_selected.png")
                mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_not_selected.png")
                supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_not_selected.png")
                pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
                shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
                mp5_icon_on_bar = pygame.transform.scale(mp5_icon_on_bar, mp5_icon_on_bar_size)
                supershotgun_icon_on_bar = pygame.transform.scale(supershotgun_icon_on_bar,
                                                                  supershotgun_icon_on_bar_size)
                selected_weapon_sound.play()
            elif event.key == pygame.K_3:
                selected_weapon = 'mp5'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/mp5_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_mp5_shoots.png")
                pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_not_selected.png")
                shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_not_selected.png")
                mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_selected.png")
                supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_not_selected.png")
                pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
                shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
                mp5_icon_on_bar = pygame.transform.scale(mp5_icon_on_bar, mp5_icon_on_bar_size)
                supershotgun_icon_on_bar = pygame.transform.scale(supershotgun_icon_on_bar,
                                                                  supershotgun_icon_on_bar_size)
                selected_weapon_sound.play()
            elif event.key == pygame.K_4:
                selected_weapon = 'supershotgun'
                player_shoots_sound = pygame.mixer.Sound("assets/player/sounds/weapons/supershotgun_shoot.wav")
                shooting_player_image = pygame.image.load("assets/player/player_supershotgun_shoots.png")
                pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_not_selected.png")
                shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_not_selected.png")
                mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_not_selected.png")
                supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_selected.png")
                pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
                shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
                mp5_icon_on_bar = pygame.transform.scale(mp5_icon_on_bar, mp5_icon_on_bar_size)
                supershotgun_icon_on_bar = pygame.transform.scale(supershotgun_icon_on_bar,
                                                                  supershotgun_icon_on_bar_size)
                selected_weapon_sound.play()
            # Выстрел
            elif event.key == pygame.K_SPACE:
                # Обработка если выбран пистолет
                if selected_weapon == 'pistol':
                    if current_time - shoot_start_time >= 150:
                        player_shoots_sound.play()
                        player_shooting = True
                        player_image = shooting_player_image
                        player_image = pygame.transform.scale(player_image, player_size)
                        shoot_start_time = pygame.time.get_ticks() # Запоминаем время начала выстрела

                        # Уменьшение здоровья врага при выстреле и уничтожение
                        closest_enemy = enemy.find_closest_enemy(player_pos_x)
                        if on_ground: # Если игрок на земле, он попадает по противникам
                            if closest_enemy:
                                if closest_enemy.health > 0:
                                    closest_enemy.health -= 1
                                    closest_enemy.rect.x += 10 # Инерция противника от выстрела
                        else:
                            pass
                # Обработка если выбран шотган
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
                # Обработка если выбран MP5
                elif selected_weapon == 'mp5':
                    if current_time - shoot_start_time >= 100:
                        print(shoot_button_pressed)
                        player_shoots_sound.play()
                        player_shooting = True
                        player_image = shooting_player_image
                        player_image = pygame.transform.scale(player_image, player_size)
                        shoot_start_time = current_time # Запоминаем время начала выстрела
                        shoot_last_time = current_time

                        # Уменьшение здоровья врага при выстреле и уничтожение
                        closest_enemy = enemy.find_closest_enemy(player_pos_x)
                        if on_ground: # Если игрок на земле, он попадает по противникам
                            if closest_enemy:
                                if closest_enemy.health > 0:
                                    closest_enemy.health -= 1.5
                                    closest_enemy.rect.x += 20 # Инерция противника от выстрела
                        else:
                            pass
                # Обработка если выбран супершотган (с учетом двух выстрелов с перезарядкой)
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
                                    closest_enemy.health -= 6
                                    closest_enemy.rect.x += 40  # Инерция противника от выстрела

                        if ammo_supershotgun_left == 1:
                            supershotgun_reload_ping = 750
                            ammo_supershotgun_left = 2
                        else:
                            ammo_supershotgun_left -= 1
                        print(ammo_supershotgun_left)

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                player_speed = 0
                player_runs_sound.stop()

    # Воспроизведение звука бега, если игрок находится на земле и движется
    if on_ground and (player_speed != 0) and not is_running_sound_playing:
        player_runs_sound.play(-1)
        is_running_sound_playing = True
    elif (player_speed == 0) or (not on_ground):
        player_runs_sound.stop()
        is_running_sound_playing = False



    # Получение обновляемого текущего времени
    current_time = pygame.time.get_ticks()

    # Увеличение скорости игрока при прыжке
    if not on_ground:
        if player_speed > 0:
            player_speed = speed_val + 5
        if player_speed < 0:
            player_speed = speed_val - 15
    else:
        if player_speed > 0:
            player_speed = speed_val
        if player_speed < 0:
            player_speed = - speed_val

    # Обработка выстрела. Если после начала выстрела прошло более N млс, то возвращаем спрайт player_stands
    if current_time - shoot_start_time >= 100:
        player_image = pygame.image.load(player_image_player_stands_path)
        player_image = pygame.transform.scale(player_image, player_size)
        player_shooting = False

    game.background_movement(background1_rect, background2_rect, background_width, player_speed, WIDTH)

    # Применение гравитации и инерции к прыжку
    if not on_ground:
        player_pos_y -= jump_speed
        jump_speed -= gravity
        # Если игрок касается земли, устанавливаем булеву on_ground в True
        if player_pos_y >= player_on_ground_y:
            player_pos_y = player_on_ground_y
            on_ground = True

    # Создание противника с определенной вероятностью
    enemy.enemy_random_create()

    # Обновление позиций противников
    enemy.enemy_position_update()

    # Отрисовка фонов и объектов
    screen.blit(background, background1_rect)
    screen.blit(background, background2_rect)
    enemy.enemies.draw(screen)
    # weapons_bar
    screen.blit(pistol_icon_on_bar, pistol_icon_on_bar_rect)
    screen.blit(shotgun_icon_on_bar, shotgun_icon_on_bar_rect)
    screen.blit(mp5_icon_on_bar, mp5_icon_on_bar_rect)
    screen.blit(supershotgun_icon_on_bar, supershotgun_icon_on_bar_rect)

    # Анимация player_walks + замена спрайта игрока при выстреле при ходьбе
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

    # Замена спрайта игрока в прыжке на player_stands
    if not on_ground:
        if not player_shooting:
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            screen.blit(player_image, (player_pos_x, player_pos_y))
        else:
            pass

    # Изменение current_walk_frame каждые 100 млс
    if current_time - last_frame_change_time >= 100:  # Переключение кадров player_walks каждые 0.1 секунды
        if player_speed < 0:
            current_walk_frame = (current_walk_frame + 1) % len(player_walks)
            last_frame_change_time = current_time
        if player_speed > 0:
            current_walk_frame = (current_walk_frame - 1) % len(player_walks)
            last_frame_change_time = current_time

    # Анимация стойки игрока
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

    # Обновление экрана после отрисовки объектов
    pygame.display.flip()

    # FPS
    pygame.time.Clock().tick(60)