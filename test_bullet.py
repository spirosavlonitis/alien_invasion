import unittest
import pygame
from pygame.event import Event
from pygame.sprite import Sprite
from pygame.sprite import Group
from settings import Settings
import game_functions as gf
from ship import Ship
from bullet import Bullet


class TestBullet(unittest.TestCase):

    def setUp(self):
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(self.ai_settings.screen_size)
        self.ship = Ship(self.ai_settings, self.screen)
        self.bullet = Bullet(self.ai_settings, self.screen, self.ship)
        self.bullets = Group()

    def move_ship_left(self, ship):
        """Perform all the steps needed to move the ship left"""
        pygame.event.post(Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        gf.check_events(self.ai_settings, self.screen, self.ship, self.bullets)
        self.ship.update()

    def add_bullet(self):
        pygame.event.post(Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        gf.check_events(self.ai_settings, self.screen, self.ship, self.bullets)

    def test_inheritance(self):
        actual = Bullet in Sprite.__subclasses__()
        expected = True
        self.assertEqual(expected, actual)

    def test_attributes(self):
        attributes = [
            "screen", "rect", "y", "color", "speed_factor",
            "update", "draw_bullet"
        ]
        actual = True
        for attr in attributes:
            if hasattr(self.bullet, attr) == False:
                actual = False
        expected = True
        self.assertEqual(expected, actual)

    def test_bullet_position(self):
        self.move_ship_left(self.ship)
        bullet = Bullet(self.ai_settings, self.screen, self.ship)
        actual = bullet.rect.centerx == self.ship.rect.centerx and bullet.rect.top == self.ship.rect.top
        expected = True
        self.assertEqual(expected, actual)

    def test_update(self):
        temp_y = self.bullet.rect.y
        self.bullet.update()
        actual = temp_y > self.bullet.rect.y
        expected = True
        self.assertEqual(expected, actual)

    def test_bullet_limit(self):
        for _ in range(0, self.ai_settings.bullet_limit+2):
            self.add_bullet()
        actual = len(self.bullets)
        expected = self.ai_settings.bullet_limit
        self.assertEqual(expected, actual)

    def test_bullet_removal(self):
        for _ in range(0, self.ai_settings.bullet_limit):
            self.add_bullet()

        for bullet in self.bullets:
            while bullet.rect.bottom > -1:
                bullet.update()
        self.bullets.update()
        gf.update_screen(self.ai_settings, self.screen, self.ship, self.bullets)
        actual = len(self.bullets)
        expected = 0
        self.assertEqual(expected, actual)


def main():
    unittest.main()