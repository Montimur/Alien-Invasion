import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centery = ship.rect.centery

        self.x = float(self.rect.x)
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        self.x += self.speed_factor
        self.rect.x = self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
