import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Ставим экран с резолюшином
WIDTH, HEIGHT = 800, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DOOM RUNNER")

# Загрузка фонов
background = pygame.image.load("background.jpg")
background_rect = background.get_rect()

# Параметры фона
background_width = background_rect.width

# Создание двух экземпляров фона для бесконечной прокрутки
background1_rect = background_rect.copy()
background2_rect = background_rect.copy()
background2_rect.x = background_width

# Загрузка спрайтов
player_image_player_stands_path = "player\player_stands_1.png"
player_image = pygame.image.load(player_image_player_stands_path)
player_size = (100, 100)
player_image = pygame.transform.scale(player_image, player_size) # Изменение разрешения спрайта
player_walks = [pygame.image.load(f"player/player_walks_{i}.png") for i in range(1, 5)]
player_size_walks = (70, 100)
player_walks = [pygame.transform.scale(img, player_size_walks) for img in player_walks]

enemy_sprite_path = "enemies/enemy_walks_1.png"
enemy_sprite = pygame.image.load(enemy_sprite_path)
enemy_size = (100, 100)

# weapons_bar (панель выбора оружия)
pistol_icon_on_bar = pygame.image.load("weapons_bar/pistol_selected.png")
pistol_icon_on_bar_size = (80, 70)
pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
pistol_icon_on_bar_rect = pistol_icon_on_bar.get_rect()
pistol_icon_on_bar_rect.x = 0
shotgun_icon_on_bar = pygame.image.load("weapons_bar/shotgun_not_selected.png")
shotgun_icon_on_bar_size = (80, 70)
shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
shotgun_icon_on_bar_rect = shotgun_icon_on_bar.get_rect()
shotgun_icon_on_bar_rect.x = 80

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
speed_val = 5
selected_weapon = 'pistol'
shooting_player_image = pygame.image.load("player\player_pistol_shoots.png")

# Загрузка звуков
player_shoots_sound = pygame.mixer.Sound("player/sounds/weapons/pistol_shoot.wav")
player_jumps_sound = pygame.mixer.Sound("player/sounds/player_jumps.wav")
player_runs_sound = pygame.mixer.Sound("player/sounds/player_runs_1.wav")
enemy_dies_sound = pygame.mixer.Sound("enemies/sounds/enemy_death.wav")
selected_weapon_sound = pygame.mixer.Sound("player/sounds/weapons/select_weapon.mp3")

# Фоновая музыка
pygame.mixer.music.load("back_music.mp3")
# pygame.mixer.music.play(-1)

# Переменная для отслеживания времени смены кадров анимации
last_frame_change_time = pygame.time.get_ticks()
last_frame_change_time_stands = pygame.time.get_ticks()

# Переменная для текущего времени
current_time = pygame.time.get_ticks()

# Класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, background):
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
            self.death_images.append(pygame.image.load(f"enemies/enemy_death_{img_dth + 1}.png"))
        self.death_index = 0  # Индекс текущего изображения анимации смерти
        self.death_timer = 0 # Таймер для анимации смерти
        # Анимация ходьбы
        self.walks_images = []
        for img_wlk in range(4):
            self.walks_images.append(pygame.image.load(f"enemies/enemy_walks_{img_wlk + 1}.png"))
        self.walks_index = 0  # Индекс текущего изображения анимации ходьбы
        self.walks_timer = 0 # Таймер для анимации ходьбы

        self.speed = random.randint(1, 3) # Случайная скорость
        self.health = 3 # Здоровье
        self.is_alive = True # Флаг жив ли противник


    # Функция постоянного обновления состояния противника
    def update(self):
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
            # Запуск анимации уничтожения противника
            if self.death_index < len(self.death_images):
                self.death_timer += 1
                if self.death_timer >= 5:  # Задержка в пол секунды
                    self.image = pygame.transform.scale(self.death_images[self.death_index], enemy_size)
                    self.death_index += 1
                    self.death_timer = 0
                    # enemy_dies_sound.play()
            else:
                self.speed = 0

# Создание группы для противников для отрисовки всех противников одновременно
enemies = pygame.sprite.Group()

# Функция для определения самого ближайшего живого противника к игроку
def find_closest_enemy(player_pos_x):
    closest_enemy = None
    min_distance = float('inf')  # Для вычесления противника с наименьшей дистанцией к игроку
    # Перебор всех существующих противников
    for enemy in enemies:
        if not enemy.is_alive: # Если противник убит, исключаем его из цикла
            continue
        else:
            distance = abs(enemy.rect.x - player_pos_x) # Вычисление дистанции до игрока текущего противника
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
            if enemy.health <= 0:  # Проверяем, жив ли противник
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
    return closest_enemy

# Игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
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
                player_shoots_sound = pygame.mixer.Sound("player/sounds/weapons/pistol_shoot.wav")
                shooting_player_image =pygame.image.load("player\player_pistol_shoots.png")
                pistol_icon_on_bar = pygame.image.load("weapons_bar/pistol_selected.png")
                shotgun_icon_on_bar = pygame.image.load("weapons_bar/shotgun_not_selected.png")
                pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
                shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
                selected_weapon_sound.play()
            elif event.key == pygame.K_2:
                selected_weapon = 'shotgun'
                player_shoots_sound = pygame.mixer.Sound("player/sounds/weapons/shotgun_shoot.wav")
                shooting_player_image = pygame.image.load("player\player_shotgun_shoots.png")
                pistol_icon_on_bar = pygame.image.load("weapons_bar/pistol_not_selected.png")
                shotgun_icon_on_bar = pygame.image.load("weapons_bar/shotgun_selected.png")
                pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
                shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
                selected_weapon_sound.play()
            # Выстрел
            elif event.key == pygame.K_SPACE:

                # Обработка если выбран пистолет
                if selected_weapon == 'pistol':
                    player_shoots_sound.play()
                    player_shooting = True
                    player_image = shooting_player_image
                    player_image = pygame.transform.scale(player_image, player_size)
                    shoot_start_time = pygame.time.get_ticks() # Запоминаем время начала выстрела

                    # Уменьшение здоровья врага при выстреле и уничтожение
                    clothest_enemy = find_closest_enemy(player_pos_x)
                    if on_ground: # Если игрок на земле, он попадает по противникам
                        if clothest_enemy:
                            if clothest_enemy.health > 0:
                                clothest_enemy.health -= 1
                                clothest_enemy.rect.x += 10 # Инерция противника от выстрела
                    else:
                        pass
                else:
                    pass

                # Обработка если выбран шотган
                if selected_weapon == 'shotgun':
                    player_shoots_sound.play()
                    player_shooting = True
                    player_image = shooting_player_image
                    player_image = pygame.transform.scale(player_image, player_size)
                    shoot_start_time = pygame.time.get_ticks()  # Запоминаем время начала выстрела

                    # Уменьшение здоровья врага при выстреле и уничтожение
                    clothest_enemy = find_closest_enemy(player_pos_x)
                    if on_ground:  # Если игрок на земле, он попадает по противникам
                        if clothest_enemy:
                            if clothest_enemy.health > 0:
                                clothest_enemy.health -= 3
                                clothest_enemy.rect.x += 25  # Инерция противника от выстрела
                    else:
                        pass
                else:
                    pass

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

    # Создание противника с определенной вероятностью
    if random.randint(1, 50) == 1:
        enemy = Enemy(background)
        enemies.add(enemy)

    # Обновление позиций противников
    enemies.update()

    # Отрисовка фонов и объектов
    screen.blit(background, background1_rect)
    screen.blit(background, background2_rect)
    enemies.draw(screen)
    # weapons_bar
    screen.blit(pistol_icon_on_bar, pistol_icon_on_bar_rect)
    screen.blit(shotgun_icon_on_bar, shotgun_icon_on_bar_rect)

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
        if player_image_player_stands_path == "player\player_stands_1.png":
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            last_frame_change_time_stands = current_time
            player_image_player_stands_path = "player\player_stands_2.png"
        else:
            player_image = pygame.image.load(player_image_player_stands_path)
            player_image = pygame.transform.scale(player_image, player_size)
            last_frame_change_time_stands = current_time
            player_image_player_stands_path = "player\player_stands_1.png"

    # Обновление экрана после отрисовки объектов
    pygame.display.flip()

    # FPS
    pygame.time.Clock().tick(60)