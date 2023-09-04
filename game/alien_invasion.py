import pygame
from pygame.sprite import Group

import game_functions as gf
from assets.ship import Ship
from settings import Settings


def run_game():
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode((
        settings.screen_width, settings.screen_height
    ))

    pygame.display.set_caption("Alien Invasion")

    ship = Ship(settings, screen)

    bullets = Group()
    aliens = Group()
    rain_drops = Group()

    gf.create_fleet(settings, screen, ship, aliens)
    gf.create_rain_drops(settings, screen, rain_drops)

    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(settings, aliens)
        gf.update_drops(settings, screen, rain_drops)
        gf.update_screen(settings, screen, ship, aliens, bullets, rain_drops)


run_game()
