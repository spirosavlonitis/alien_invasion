import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Instantiate  alien objects."""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load("images/alien.bmp")
        self.screen_rect = self.screen.get_rect()
        
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Check if alien has reached left or right edge."""
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self, ai_settings):
        """Move alien left or right."""
        self.x += (self.ai_settings.alien_speed_factor *
                    self.ai_settings.fleet_direction)
        self.rect.x = self.x