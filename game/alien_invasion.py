import pygame
from pygame.sprite import Group

from assets.target import Target
from controls.button import Button
from game.game_stats import GameStats
from settings import Settings
from assets.ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    settings = Settings()
    stats = GameStats()

    screen = pygame.display.set_mode((
        settings.screen_width, settings.screen_height
    ))

    pygame.display.set_caption("Target Practice")

    play_button = Button(settings, screen, "Play")

    ship = Ship(settings, screen)

    target = Target(settings, screen)

    bullets = Group()

    while True:
        gf.check_events(settings, screen, stats, ship, target, bullets, play_button)
        if stats.game_active:
            ship.update()
            target.update()
            gf.update_bullets(stats, bullets, screen, target)
            gf.check_stats(stats, bullets)
        gf.update_screen(settings, stats, screen, ship, target, bullets, play_button)


run_game()
