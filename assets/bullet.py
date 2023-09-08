import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from game.settings import Settings
from assets.ship import Ship


class Bullet(Sprite):

    def __init__(self, settings: Settings, screen: Surface, ship: Ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top

        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self) -> None:
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect)
