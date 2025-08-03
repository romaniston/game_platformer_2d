import sys
import random

import pygame


# Ставим экран с резолюшином
def set_screen_resolution(WIDTH, HEIGHT):
    WIDTH, HEIGHT = 800, 360
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DOOM RUNNER")
    return screen, WIDTH, HEIGHT


# Загрузка фонов
def set_backrounds(background_path):
    background = pygame.image.load(background_path)
    background_rect = background.get_rect()
    background_width = background_rect.width
    # Создание двух экземпляров фона для бесконечной прокрутки
    background1_rect = background_rect.copy()
    background2_rect = background_rect.copy()
    background2_rect.x = background_width
    return background, background_rect, background_width, background1_rect, background2_rect


# Фоновая музыка
def set_background_music(background_music_path):
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)


backgrounds = [
    {"name": "background_1", "path": "assets/background/background_1.jpg"},
    {"name": "background_2", "path": "assets/background/background_2.jpg"},
    {"name": "background_3", "path": "assets/background/background_3.jpg"}
]

musics = [
    {"name": "track_1", "path": "assets/soundtrack/track_1.mp3", "demo": "assets/soundtrack/track_1_short.wav"},
    {"name": "track_2", "path": "assets/soundtrack/track_2.mp3", "demo": "assets/soundtrack/track_2_short.wav"},
    {"name": "track_3", "path": "assets/soundtrack/track_3.mp3", "demo": "assets/soundtrack/track_3_short.wav"},
    {"name": "track_4", "path": "assets/soundtrack/track_4.mp3", "demo": "assets/soundtrack/track_4_short.wav"},
    {"name": "track_5", "path": "assets/soundtrack/track_5.mp3", "demo": "assets/soundtrack/track_5_short.wav"},
    {"name": "track_6", "path": "assets/soundtrack/track_6.mp3", "demo": "assets/soundtrack/track_6_short.wav"},
]


def show_start_menu(screen):
    pygame.font.init()
    font = pygame.font.Font("assets/fonts/amazdoomright.ttf", 32)
    big_font = pygame.font.Font("assets/fonts/amazdoomright.ttf", 48)

    selected_category = "background"
    bg_index = 0
    music_index = 0

    clock = pygame.time.Clock()

    pygame.mixer.music.load(musics[music_index]['demo'])
    pygame.mixer.music.play(-1)

    while True:
        screen.fill((0, 0, 0))

        # Отображение выбранного фона
        bg_image = pygame.image.load(backgrounds[bg_index]["path"]).convert()
        bg_image = pygame.transform.scale(bg_image, screen.get_size())
        screen.blit(bg_image, (0, 0))

        # Цвет текста
        bg_color = (255, 255, 0) if selected_category == "background" else (255, 255, 255)
        music_color = (255, 255, 0) if selected_category == "music" else (255, 255, 255)

        # Текст
        bg_text = font.render(f"Фон: {backgrounds[bg_index]['name']}", True, bg_color)
        music_text = font.render(f"Музыка: {musics[music_index]['name']}", True, music_color)
        instruction_text = big_font.render("Нажмите ПРОБЕЛ чтобы начать", True, (255, 0, 0))

        # Отображение текста
        screen.blit(bg_text, (50, 100))
        screen.blit(music_text, (50, 150))
        screen.blit(instruction_text, (
            screen.get_width() // 2 - instruction_text.get_width() // 2,
            screen.get_height() - 150
        ))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_category = "background"
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_category = "music"

                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    if selected_category == "background":
                        bg_index = (bg_index - 1) % len(backgrounds)
                    else:
                        music_index = (music_index - 1) % len(musics)
                        pygame.mixer.music.load(musics[music_index]['demo'])
                        pygame.mixer.music.play(-1)

                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    if selected_category == "background":
                        bg_index = (bg_index + 1) % len(backgrounds)
                    else:
                        music_index = (music_index + 1) % len(musics)
                        pygame.mixer.music.load(musics[music_index]['demo'])
                        pygame.mixer.music.play(-1)

                elif event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(musics[music_index]['demo'])
                    pygame.mixer.music.play(-1)
                    return backgrounds[bg_index]['path'], musics[music_index]['path']

        clock.tick(30)


# VVV Игровой цикл VVV


# Перемещение фонов для создания иллюзии движения игрока
def background_movement(background1_rect, background2_rect, background_width, player_speed, WIDTH):
    background1_rect.x += player_speed
    background2_rect.x += player_speed
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
def drawing_objects(screen, background, background1_rect, background2_rect, pistol_icon_on_bar, pistol_icon_on_bar_rect,
                    shotgun_icon_on_bar, shotgun_icon_on_bar_rect, mp5_icon_on_bar, mp5_icon_on_bar_rect,
                    supershotgun_icon_on_bar, supershotgun_icon_on_bar_rect, machine_gun_icon_on_bar,
                    machine_gun_icon_on_bar_rect, enemy):
    screen.blit(background, background1_rect)
    screen.blit(background, background2_rect)
    enemy.enemies.draw(screen)
    # weapons_bar
    screen.blit(pistol_icon_on_bar, pistol_icon_on_bar_rect)
    screen.blit(shotgun_icon_on_bar, shotgun_icon_on_bar_rect)
    screen.blit(mp5_icon_on_bar, mp5_icon_on_bar_rect)
    screen.blit(supershotgun_icon_on_bar, supershotgun_icon_on_bar_rect)
    screen.blit(machine_gun_icon_on_bar, machine_gun_icon_on_bar_rect)
    return (screen, background, background1_rect, background2_rect, pistol_icon_on_bar, pistol_icon_on_bar_rect,\
                    shotgun_icon_on_bar, shotgun_icon_on_bar_rect, mp5_icon_on_bar, mp5_icon_on_bar_rect,\
                    supershotgun_icon_on_bar, supershotgun_icon_on_bar_rect, machine_gun_icon_on_bar,\
                    machine_gun_icon_on_bar_rect, enemy)


def game_over(player_health_val, screen):
    if player_health_val <= 0:
        screen.fill((255, 0, 0))
        game_over_font = pygame.font.Font("assets/fonts/doom.ttf", 72)
        game_over_text = game_over_font.render("GAME OVER", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
