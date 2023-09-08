import sys

import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.sprite import Group

from assets.bullet import Bullet
from assets.ship import Ship
from assets.target import Target
from controls.button import Button
from game.game_stats import GameStats
from game.settings import Settings


def check_events(settings: Settings, screen: Surface, stats: GameStats, ship: Ship, target: Target, bullets: Group,
                 play_button: Button) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_event(stats, ship, target, bullets, play_button)


def check_keydown_events(event: Event, settings: Settings, screen: Surface, ship: Ship, bullets: Group) -> None:
    if event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)


def check_keyup_event(event: Event, ship: Ship) -> None:
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_mouse_event(stats: GameStats, ship: Ship, target: Target, bullets: Group, play_button: Button) -> None:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if not stats.game_active and play_button.rect.collidepoint(mouse_x, mouse_y):
        start_game(stats, ship, target, bullets)


def start_game(stats: GameStats, ship: Ship, target: Target, bullets: Group) -> None:
    stats.game_active = True
    stats.misses = 0
    stats.hits = 0
    ship.center_ship()
    target.center_target()
    bullets.empty()


def end_game(stats: GameStats, bullets: Group):
    stats.game_active = False
    bullets.empty()


def fire_bullet(settings: Settings, screen: Surface, ship: Ship, bullets: Group) -> None:
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(stats: GameStats, bullets: Group, screen: Surface, target: Target) -> None:
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.left >= screen.get_rect().right:
            bullets.remove(bullet)
            stats.misses += 1
        elif bullet.rect.colliderect(target):
            bullets.remove(bullet)
            stats.hits += 1


def check_stats(stats: GameStats, bullets: Group):
    if stats.misses >= 3:
        end_game(stats, bullets)


def update_screen(settings: Settings, stats: GameStats, screen: Surface, ship: Ship, target: Target, bullets: Group,
                  play_button: Button) -> None:
    screen.fill(settings.background_color)

    ship.blit_me()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    target.draw_target()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

