import pygame

class Ship():
    """Set and update the ship object"""
    def __init__(self, ai_settings ,screen):
        self.screen = screen
        self.image = pygame.image.load("images/ship.bmp")
        self.ai_settings = ai_settings

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.center = float(self.screen_rect.centerx)
        self.rect.centerx =  self.center
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update ship's position on the screen"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """Draw ship's current position on screen"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center ship's x position."""
        self.center = self.screen_rect.centerx