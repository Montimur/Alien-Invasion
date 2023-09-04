import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from game.settings import Settings


class Alien(Sprite):

    def __init__(self, settings: Settings, screen: Surface):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load('../images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self) -> None:
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self) -> bool:
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blit_me(self) -> None:
        self.screen.blit(self.image, self.rect)
