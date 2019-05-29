import unittest
import inspect
import pygame
from pygame.sprite import Sprite
from settings import Settings
from alien import Alien

class TestAlien(unittest.TestCase):
    def setUp(self):
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(self.ai_settings.screen_size)
        self.alien = Alien(self.ai_settings, self.screen)

    def test_inheritance(self):
        actual = Alien in Sprite.__subclasses__()
        self.assertEqual(True, actual)

    def test_attributes(self):
        attributes = [
            "ai_settings", "screen", "image", "screen_rect", "rect", "x",
            "blitme", "update", "check_edges"
        ]
        actual = True
        for attribute in attributes:
            if hasattr(self.alien, attribute) == False:
                actual = False
        expected = True
        self.assertEqual(expected, actual)

    def test_move_right(self):
        temp_x = self.alien.rect.x
        self.alien.update(self.ai_settings)
        actual = self.alien.rect.x > temp_x
        expected = True
        self.assertEqual(expected, actual)

    def test_move_left(self):
        temp_x = self.alien.rect.x
        self.ai_settings.fleet_direction = -1
        self.alien.update(self.ai_settings)
        actual = self.alien.rect.x < temp_x
        expected = True
        self.assertEqual(expected, actual)

unittest.main()