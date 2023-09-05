import pygame
from pygame.sprite import Group

import game_functions as gf
from assets.ship import Ship
from game.game_stats import GameStats
from settings import Settings


def run_game():
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)

    screen = pygame.display.set_mode(settings.screen_dimensions)

    pygame.display.set_caption("Alien Invasion")

    ship = Ship(settings, screen)

    bullets = Group()
    aliens = Group()

    gf.create_fleet(settings, screen, ship, aliens)

    while True:
        gf.check_events(settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, ship, aliens, bullets)
            gf.update_aliens(settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(settings, screen, ship, aliens, bullets)


run_game()
