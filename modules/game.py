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
