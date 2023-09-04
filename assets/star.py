import pygame
from pygame.sprite import Sprite


class Star(Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('../images/star-icon.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blit_me(self):
        self.screen.blit(self.image, self.rect)
