import pygame
from pygame.sprite import Sprite

from pygame.surface import Surface

from game.settings import Settings


class Ship(Sprite):

    def __init__(self, settings: Settings, screen: Surface):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self) -> None:
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor

        self.rect.centerx = self.center

    def blit_me(self) -> None:
        self.screen.blit(self.image, self.rect)

    def center_ship(self) -> None:
        self.center = self.screen_rect.centerx
