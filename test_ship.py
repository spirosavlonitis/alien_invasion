import unittest
import pygame
from pygame.sprite import Group
from pygame.event import Event
from game_stats import GameStats
from settings import Settings
from button import Button
from alien import Alien
from bullet import Bullet
from ship import Ship
import game_functions as gf


class TestShip(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(self.ai_settings.screen_size)
        self.stats = GameStats(self.ai_settings)
        self.play_button = Button(self.ai_settings, self.screen, "Play")
        self.ship = Ship(self.ai_settings, self.screen)
        self.aliens, self.bullets = Group(), Group()
        pygame.event.clear()

    def move_left(self, ship):
        """Perform all the steps needed to move the ship left"""
        pygame.event.post(Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        gf.check_events(self.ai_settings, self.screen, self.stats,
            self.play_button, self.ship, self.aliens, self.bullets)
        self.ship.update()

    def move_right(self, ship):
        """Perform all the steps needed to move the ship right"""
        pygame.event.post(Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        gf.check_events(self.ai_settings, self.screen, self.stats,
            self.play_button, self.ship, self.aliens, self.bullets)
        self.ship.update()

    def test_attributes(self):
        attrs = [
            "screen", "image", "rect", "screen_rect", "center",
            "moving_right", "moving_left", "ai_settings",
            "update", "blitme", "center_ship"
        ]
        actual = True
        for attr in attrs:
            if hasattr(self.ship, attr) == False:
                actual = False
        expected = True
        self.assertEqual(expected, actual)

    def test_right_movement(self):
        prev_centerx = self.ship.rect.centerx
        self.move_right(self.ship)
        actual = self.ship.rect.centerx > prev_centerx
        expected = True
        self.assertEqual(expected, actual)

    def test_left_limit(self):
        while self.ship.rect.left > 0:
            self.move_left(self.ship)
        self.move_left(self.ship)
        actual = self.ship.rect.left
        expected = 0
        self.assertEqual(expected, actual)

    def test_right_limit(self):
        while self.ship.rect.right < self.ship.screen_rect.right:
            self.move_right(self.ship)
        self.move_right(self.ship)
        actual = self.ship.rect.right <= self.ship.screen_rect.right
        expected = True
        self.assertEqual(expected, actual)


unittest.main()