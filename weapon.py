import pygame
import sys
import random

# weapons_bar (панель выбора оружия)
def weapons_bar_parameters():
    pistol_icon_on_bar = pygame.image.load("assets/weapons_bar/pistol_selected.png")
    pistol_icon_on_bar_size = (80, 70)
    pistol_icon_on_bar = pygame.transform.scale(pistol_icon_on_bar, pistol_icon_on_bar_size)
    pistol_icon_on_bar_rect = pistol_icon_on_bar.get_rect()
    pistol_icon_on_bar_rect.x = 0
    shotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/shotgun_not_selected.png")
    shotgun_icon_on_bar_size = (80, 70)
    shotgun_icon_on_bar = pygame.transform.scale(shotgun_icon_on_bar, shotgun_icon_on_bar_size)
    shotgun_icon_on_bar_rect = shotgun_icon_on_bar.get_rect()
    shotgun_icon_on_bar_rect.x = 80
    mp5_icon_on_bar = pygame.image.load("assets/weapons_bar/mp5_not_selected.png")
    mp5_icon_on_bar_size = (80, 70)
    mp5_icon_on_bar = pygame.transform.scale(mp5_icon_on_bar, shotgun_icon_on_bar_size)
    mp5_icon_on_bar_rect = mp5_icon_on_bar.get_rect()
    mp5_icon_on_bar_rect.x = 160
    supershotgun_icon_on_bar = pygame.image.load("assets/weapons_bar/supershotgun_not_selected.png")
    supershotgun_icon_on_bar_size = (80, 70)
    supershotgun_icon_on_bar = pygame.transform.scale(supershotgun_icon_on_bar, shotgun_icon_on_bar_size)
    supershotgun_icon_on_bar_rect = supershotgun_icon_on_bar.get_rect()
    supershotgun_icon_on_bar_rect.x = 240
    return pistol_icon_on_bar, pistol_icon_on_bar_size, pistol_icon_on_bar_rect,\
        shotgun_icon_on_bar, shotgun_icon_on_bar_size, shotgun_icon_on_bar_rect,\
        mp5_icon_on_bar, mp5_icon_on_bar_size, mp5_icon_on_bar_rect,\
        supershotgun_icon_on_bar, supershotgun_icon_on_bar_size, supershotgun_icon_on_bar_rect

# Установка звука выбора оружия
def set_selected_weapon_sounds():
    selected_weapon_sound = pygame.mixer.Sound("assets/player/sounds/weapons/select_weapon.mp3")
    return selected_weapon_sound