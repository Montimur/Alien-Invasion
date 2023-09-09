import sys
from time import sleep

import pygame
from pygame.event import Event
from pygame.sprite import Group
from pygame.surface import Surface

from assets.alien import Alien
from assets.bullet import Bullet
from assets.scoreboard import Scoreboard
from assets.ship import Ship
from controls.button import Button
from game.game_stats import GameStats
from game.settings import Settings


def check_events(settings: Settings, screen: Surface, stats: GameStats, play_button: Button, ship: Ship,
                 scoreboard: Scoreboard, aliens: Group, bullets: Group) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stats, ship, scoreboard, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, play_button, ship, scoreboard, aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event: Event, settings: Settings, screen: Surface, stats: GameStats, ship: Ship,
                         scoreboard: Scoreboard, aliens: Group, bullets: Group) -> None:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(settings, screen, stats, ship, scoreboard, aliens, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event: Event, ship: Ship) -> None:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(settings: Settings, screen: Surface, stats: GameStats, play_button: Button, ship: Ship,
                      scoreboard: Scoreboard, aliens: Group, bullets: Group, mouse_x: int, mouse_y: int) -> None:
    if not stats.game_active and play_button.rect.collidepoint(mouse_x, mouse_y):
        start_game(settings, screen, stats, ship, scoreboard, aliens, bullets)


def start_game(settings: Settings, screen: Surface, stats: GameStats, ship: Ship, scoreboard: Scoreboard,
               aliens: Group, bullets: Group) -> None:
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()

    settings.initialize_dynamic_settings()

    aliens.empty()
    bullets.empty()

    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()


def fire_bullet(settings: Settings, screen: Surface, ship: Ship, bullets: Group) -> None:
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_alien_bullet_collisions(aliens: Group, bullets: Group) -> dict:
    return pygame.sprite.groupcollide(bullets, aliens, True, True)


def update_bullets(settings: Settings, screen: Surface, stats: GameStats, scoreboard: Scoreboard, ship, aliens: Group,
                   bullets: Group) -> None:
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = check_alien_bullet_collisions(aliens, bullets)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_score * len(aliens)
            scoreboard.prep_score()

        check_high_score(stats, scoreboard)

    check_for_new_fleet(settings, screen, stats, scoreboard, ship, aliens, bullets)


def check_for_new_fleet(settings: Settings, screen: Surface, stats: GameStats, scoreboard: Scoreboard,
                        ship: Ship, aliens: Group, bullets: Group) -> None:
    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()
        stats.level += 1
        scoreboard.prep_level()
        create_fleet(settings, screen, ship, aliens)


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
    stats.ships_left -= 1
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_fleet_edges(settings: Settings, aliens: Group) -> None:
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings: Settings, aliens: Group) -> None:
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_high_score(stats: GameStats, scoreboard: Scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def update_screen(settings: Settings, screen: Surface, stats: GameStats, scoreboard: Scoreboard, ship: Ship,
                  aliens: Group, bullets: Group, play_button: Button) -> None:
    screen.fill(settings.background_color)

    ship.blit_me()
    aliens.draw(screen)

    scoreboard.show_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

