import pygame
import sys

# Инициализация Pygame
pygame.init()

# Ставим экран с резолюшином
WIDTH, HEIGHT = 800, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DOOM")

# Загрузка фонов
background = pygame.image.load("background.jpg")
background_rect = background.get_rect()

# Параметры фона
background_width = background_rect.width

# Создание двух экземпляров фона для бесконечной прокрутки
background1_rect = background_rect.copy()
background2_rect = background_rect.copy()
background2_rect.x = background_width

# Загрузка спрайтов игрока
player_image_player_stands_path = "player\player_stands_1.png"
player_image = pygame.image.load(player_image_player_stands_path)
player_size = (100, 100)
player_image = pygame.transform.scale(player_image, player_size) # Изменение разрешения спрайта
player_walks = [pygame.image.load(f"player/player_walks_{i}.png") for i in range(1, 5)]
player_size_walks = (70, 100)
player_walks = [pygame.transform.scale(img, player_size_walks) for img in player_walks]

# Параметры игрока
player_on_ground_y = 202
player_pos_x = 75
player_pos_y = player_on_ground_y
jump_strength = 18
gravity = 1
jump_speed = jump_strength  # Начальная скорость прыжка
on_ground = True
shoot_start_time = 0
player_speed = 0
current_walk_frame = 0 # Индекс текущего кадра анимации ходьбы
player_shooting = False
is_running_sound_playing = False # Переменная для отслеживания проигрывания звука бега

# Загрузка звуков
shoot_sound = pygame.mixer.Sound("player/sounds/weapons/pistol_shoot.wav")
player_jumps = pygame.mixer.Sound("player/sounds/player_jumps.wav")
player_runs = pygame.mixer.Sound("player/sounds/player_runs_1.wav")

# Фоновая музыка
pygame.mixer.music.load("back_music.mp3")
# pygame.mixer.music.play(-1)

# Переменная для отслеживания времени смены кадров анимации
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed = 5
            elif event.key == pygame.K_RIGHT:
                player_speed = -5
            elif event.key == pygame.K_UP and on_ground:
                player_jumps.play()
                jump_speed = jump_strength  # Восстанавливаем начальную скорость прыжка
                on_ground = False
                player_runs.stop()
            elif event.key == pygame.K_SPACE:
                shoot_sound.play()
                player_shooting = True
                player_image = pygame.image.load("player\player_pistol_shoots.png")
                player_image = pygame.transform.scale(player_image, player_size)
                shoot_start_time = pygame.time.get_ticks()  # Запоминаем время начала выстрела
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_speed = 0
                player_runs.stop()

    # Воспроизведение звука бега, если игрок находится на земле и движется
    if on_ground and (player_speed != 0) and not is_running_sound_playing:
        player_runs.play(-1)
        is_running_sound_playing = True
    elif (player_speed == 0) or (not on_ground):
        player_runs.stop()
        is_running_sound_playing = False

    # Получение обновляемого текущего времени
    current_time = pygame.time.get_ticks()

    # Обработка выстрела. Если после начала выстрела прошло более N млс, то возвращаем спрайт player_stands
    if current_time - shoot_start_time >= 50:
        player_image = pygame.image.load(player_image_player_stands_path)
        player_image = pygame.transform.scale(player_image, player_size)
        player_shooting = False

    # Перемещение фонов для создания иллюзии движения игрока
    background1_rect.x += player_speed
    background2_rect.x += player_speed

    # Применение гравитации и инерции к прыжку
    if not on_ground:
        player_pos_y -= jump_speed
        jump_speed -= gravity
        # Если игрок касается земли, устанавливаем булеву on_ground в True
        if player_pos_y >= player_on_ground_y:
            player_pos_y = player_on_ground_y
            on_ground = True

    # Проверка, чтобы фоны были бесконечными и повторялись друг за другом, когда заканчивается один из них
    if background1_rect.right <= 0:
        background1_rect.x = background2_rect.right
    elif background2_rect.right <= 0:
        background2_rect.x = background1_rect.right
    elif background1_rect.left >= WIDTH:
        background1_rect.x = background2_rect.left - background_width
    elif background2_rect.left >= WIDTH:
        background2_rect.x = background1_rect.left - background_width

    # Отрисовка фонов и объектов
    screen.blit(background, background1_rect)
    screen.blit(background, background2_rect)

    # Анимация player_walks + замена спрайта игрока при выстреле при ходьбе
    if player_speed < 0:
        if player_shooting == True:
            player_image = pygame.image.load("player\player_pistol_shoots.png")
            player_image = pygame.transform.scale(player_image, player_size)
            screen.blit(player_image, (player_pos_x, player_pos_y))
        elif on_ground == True:
            screen.blit(player_walks[current_walk_frame], (player_pos_x, player_pos_y))
        else:
            pass
    elif player_speed > 0:
        if player_shooting == True:
            player_image = pygame.image.load("player\player_pistol_shoots.png")
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
        if player_image_player_stands_path == "player\player_stands_1.png":
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            last_frame_change_time_stands = current_time
            player_image_player_stands_path = "player\player_stands_2.png"
            print('1')
        else:
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            last_frame_change_time_stands = current_time
            player_image_player_stands_path = "player\player_stands_1.png"
            print('2')

    # Обновление экрана после отрисовки объектов
    pygame.display.flip()

    # FPS
    pygame.time.Clock().tick(60)