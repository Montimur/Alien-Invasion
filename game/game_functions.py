import sys
from time import sleep

import pygame
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.event import Event

from assets.ship import Ship
from assets.bullet import Bullet
from assets.alien import Alien
from game.game_stats import GameStats
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


def check_alien_bullet_collisions(aliens: Group, bullets: Group) -> dict:
    return pygame.sprite.groupcollide(bullets, aliens, True, True)


def check_for_new_fleet(settings: Settings, screen: Surface, ship: Ship, aliens: Group, bullets: Group) -> None:
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)


def update_bullets(settings: Settings, screen: Surface, ship: Ship, aliens: Group, bullets: Group) -> None:
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_alien_bullet_collisions(aliens, bullets)

    check_for_new_fleet(settings, screen, ship, aliens, bullets)


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


def update_aliens(settings: Settings, stats: GameStats, screen: Surface, ship: Ship, aliens: Group, bullets: Group) -> None:
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens) or check_aliens_hit_bottom(screen, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets)


def check_aliens_hit_bottom(screen: Surface, aliens: Group) -> bool:
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            return True
    return False


def ship_hit(settings: Settings, stats: GameStats, screen: Surface, ship: Ship, aliens: Group, bullets: Group) -> None:
    if stats.ships_left > 0:
        stats.ships_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False


def check_fleet_edges(settings: Settings, aliens: Group) -> None:
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings: Settings, aliens: Group) -> None:
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def update_screen(settings: Settings, screen: Surface, ship: Ship, aliens: Group, bullets: Group) -> None:
    screen.fill(settings.background_color)

    ship.blit_me()
    aliens.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    pygame.display.flip()

