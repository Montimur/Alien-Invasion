import pygame
from pygame import Surface
from pygame.sprite import Sprite

from game.settings import Settings


class Drop(Sprite):

    def __init__(self, settings: Settings, screen: Surface):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load('../images/drop-icon.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y += self.settings.rain_drop_rate
        self.rect.y = self.y

    def check_bottom(self) -> bool:
        screen_rect = self.screen.get_rect()

        if self.rect.top >= screen_rect.bottom:
            return True

    def blit_me(self) -> None:
        self.screen.blit(self.image, self.rect)
