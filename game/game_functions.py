import sys

import pygame

import random as rd

from assets.bullet import Bullet
from assets.alien import Alien
from assets.star import Star


def check_events(settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def create_stars(settings, screen, stars):
    star = Star(screen)
    star_width = star.rect.width
    star_height = star.rect.height

    number_of_stars_x = get_number_of_stars(settings, star_width)
    number_of_rows = get_number_of_star_rows(settings, star_height)

    for star_row_number in range(number_of_rows):
        for star_number in range(number_of_stars_x):
            create_star(screen, stars, star_number, star_row_number)


def get_number_of_stars(settings, star_width):
    available_space_x = settings.screen_width
    number_of_stars = int(available_space_x / (2 * star_width))
    return number_of_stars


def get_number_of_star_rows(settings, star_height):
    available_space_y = settings.screen_height
    number_of_star_rows = int(available_space_y / (2 * star_height))
    return number_of_star_rows


def create_star(screen, stars, star_number, row_number):
    star = Star(screen)
    star_width = star.rect.width
    star.x = star_width + 3 * star_width * star_number
    star.x += rd.randint(-50, 50)
    star.rect.x = star.x
    star.rect.y = star.rect.height + 3 * star.rect.height * row_number
    star.rect.y += rd.randint(-50, 50)
    stars.add(star)


def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width

    number_of_aliens_x = get_number_of_aliens(settings, alien_width)
    number_of_rows = get_number_of_rows(settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_of_rows):
        for alien_number in range(number_of_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def get_number_of_aliens(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_of_rows(settings, ship_height, alien_height):
    available_space_y = (settings.screen_height - (3 * alien_height) - ship_height)
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows


def update_screen(settings, screen, ship, aliens, bullets, stars):
    screen.fill(settings.background_color)

    ship.blit_me()
    stars.draw(screen)
    aliens.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    pygame.display.flip()

