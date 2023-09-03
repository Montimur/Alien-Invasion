import pygame
from pygame.sprite import Group

from settings import Settings
from assets.ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode((
        settings.screen_width, settings.screen_height
    ))

    pygame.display.set_caption("Alien Invasion")

    ship = Ship(settings, screen)

    bullets = Group()

    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets, screen)
        gf.update_screen(settings, screen, ship, bullets)


run_game()
