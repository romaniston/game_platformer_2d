import pygame
import sys
import random

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