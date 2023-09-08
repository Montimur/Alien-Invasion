import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite

from game.settings import Settings


class Target(Sprite):

    def __init__(self, settings: Settings, screen: Surface):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = pygame.Rect(0, 0, settings.target_width, settings.target_height)
        self.rect.centerx = (self.screen_rect.right - (settings.target_width // 2))

        self.y = float(self.rect.y)
        self.color = settings.target_color
        self.speed_factor = settings.target_speed_factor

        self.direction = 1

    def update(self):
        if self.rect.top <= 0:
            self.direction = 1
        elif self.rect.bottom >= self.screen_rect.bottom:
            self.direction = -1

        self.y += self.direction * self.speed_factor
        self.rect.y = self.y

    def draw_target(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def center_target(self):
        self.rect.centery = self.screen_rect.centery
