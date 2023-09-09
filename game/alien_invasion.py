import pygame
from pygame.sprite import Group

import game_functions as gf
from assets.scoreboard import Scoreboard
from assets.ship import Ship
from controls.button import Button
from game.game_stats import GameStats
from settings import Settings


def run_game():
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)

    screen = pygame.display.set_mode(settings.screen_dimensions)

    scoreboard = Scoreboard(settings, screen, stats)

    pygame.display.set_caption("Alien Invasion")

    play_button = Button(settings, screen, 'Play')

    ship = Ship(settings, screen)

    bullets = Group()
    aliens = Group()

    gf.create_fleet(settings, screen, ship, aliens)

    while True:
        gf.check_events(settings, screen, stats, play_button, ship, scoreboard, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, scoreboard, ship, aliens, bullets)
            gf.update_aliens(settings, stats, screen, scoreboard, ship, aliens, bullets)
        gf.update_screen(settings, screen, stats, scoreboard, ship, aliens, bullets, play_button)


run_game()
