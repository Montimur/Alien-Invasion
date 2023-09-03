import pygame


class Ship:

    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.image = pygame.transform.rotate(pygame.image.load('../images/ship.bmp'), 270)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left

        self.center = float(self.rect.centery)

        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up and self.rect.top > 0:
            self.center -= self.settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center += self.settings.ship_speed_factor

        self.rect.centery = self.center

    def blit_me(self):
        self.screen.blit(self.image, self.rect)
