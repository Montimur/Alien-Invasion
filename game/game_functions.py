import sys

import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.event import Event

from assets.ship import Ship
from assets.bullet import Bullet
from assets.alien import Alien
from assets.drop import Drop
from game.settings import Settings


def check_events(settings: Settings, screen: Surface, ship: Ship, bullets: Group) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def check_keydown_events(event: Event, settings: Settings, screen: Surface, ship: Ship, bullets: Group) -> None:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event: Event, ship: Ship) -> None:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(settings: Settings, screen: Surface, ship: Ship, bullets: Group) -> None:
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(bullets: Group) -> None:
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def create_fleet(settings: Settings, screen: Surface, ship: Ship, aliens: Group) -> None:
    alien = Alien(settings, screen)
    alien_width = alien.rect.width

    number_of_aliens_x = get_number_of_aliens(settings, alien_width)
    number_of_rows = get_number_of_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_of_rows):
        for alien_number in range(number_of_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def get_number_of_aliens(settings: Settings, alien_width: int) -> int:
    available_space_x = settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x


def create_alien(settings: Settings, screen: Surface, aliens: Group, alien_number: int, row_number: int) -> None:
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_of_rows(settings: Settings, ship_height: int, alien_height: int) -> int:
    available_space_y = (settings.screen_height - (3 * alien_height) - ship_height)
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows


def update_aliens(settings: Settings, aliens: Group) -> None:
    check_fleet_edges(settings, aliens)
    aliens.update()


def check_fleet_edges(settings: Settings, aliens: Group) -> None:
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings: Settings, aliens: Group) -> None:
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def update_screen(settings: Settings, screen: Surface, ship: Ship, aliens: Group, bullets: Group, rain_drops: Group) -> None:
    screen.fill(settings.background_color)

    ship.blit_me()
    aliens.draw(screen)
    rain_drops.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    pygame.display.flip()


def get_number_of_drops(settings: Settings, drop_width: int) -> int:
    available_space_x = settings.screen_width
    number_of_drops = (available_space_x / (1.5 * drop_width))
    return int(number_of_drops)


def get_number_of_drop_rows(settings: Settings, drop_height: int) -> int:
    available_space_y = settings.screen_height
    number_of_rows = (available_space_y / (1.5 * drop_height))
    return int(number_of_rows)


def create_drop(settings: Settings, screen: Surface, rain_drops: Group, drop_number: int, row_number: int) -> None:
    drop = Drop(settings, screen)
    drop_width = drop.rect.width
    drop_height = drop.rect.height

    drop.x = drop_width + 1.5 * drop_width * drop_number
    drop.y = drop_height + 1.5 * drop_height * row_number

    drop.rect.x = drop.x
    drop.rect.y = drop.y

    rain_drops.add(drop)


def create_rain_drops(settings: Settings, screen: Surface, rain_drops: Group) -> None:
    drop = Drop(settings, screen)
    drop_width = drop.rect.width
    drop_height = drop.rect.height

    number_of_drops = get_number_of_drops(settings, drop_width)
    number_of_drop_rows = get_number_of_drop_rows(settings, drop_height)

    for row_number in range(number_of_drop_rows):
        for drop_number in range(number_of_drops):
            create_drop(settings, screen, rain_drops, drop_number, row_number)


def add_one_row_of_rain_drops(settings: Settings, screen: Surface, rain_drops: Group) -> None:
    drop = Drop(settings, screen)
    drop_width = drop.rect.width
    number_of_drops = get_number_of_drops(settings, drop_width)

    for drop_number in range(number_of_drops):
        create_drop(settings, screen, rain_drops, drop_number, 0)


def update_drops(settings: Settings, screen: Surface, rain_drops: Group) -> None:
    deleted_row = False
    for drop in rain_drops.copy():
        if drop.check_bottom():
            rain_drops.remove(drop)
            if not deleted_row:
                deleted_row = True
    if deleted_row:
        add_one_row_of_rain_drops(settings, screen, rain_drops)

    rain_drops.update()
