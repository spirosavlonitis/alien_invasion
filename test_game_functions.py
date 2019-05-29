import unittest
import pygame
from pygame.event import Event
from pygame.sprite import Sprite
from pygame.sprite import Group
from settings import Settings
from button import Button
from game_stats import GameStats
from ship import Ship
from alien import Alien
import game_functions as gf

class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(self.ai_settings.screen_size)
        self.play_button = Button(self.ai_settings, self.screen, "Play")
        self.stats = GameStats(self.ai_settings)
        self.ship = Ship(self.ai_settings ,self.screen)
        self.bullets = Group()
        self.aliens = Group()
        pygame.event.clear()
    
    def test_resonds_to_quit(self):
        pygame.event.post(Event(pygame.QUIT,message="I'am outta here"))
        actual = False
        try:
            gf.check_events(self.ai_settings, self.stats, self.screen, 
                self.play_button, self.ship, self.aliens, self.bullets)
        except SystemExit:
            actual = True
        expected = True
        self.assertEqual(expected, actual)

    def test_update_screen(self):
        gf.update_screen(self.ai_settings, self.screen, self.stats, self.play_button,
            self.ship, self.aliens,self.bullets)

    def test_arrow_press_release(self, press=True):
        arrow_event = pygame.KEYDOWN if press else pygame.KEYUP
        pygame.event.post(Event(arrow_event, key=pygame.K_RIGHT))
        pygame.event.post(Event(arrow_event, key=pygame.K_LEFT))
        gf.check_events(self.ai_settings, self.stats, self.screen, self.play_button, 
            self.ship, self.aliens, self.bullets)
        actual = [self.ship.moving_right, self.ship.moving_left]
        expected = [press]*2
        self.assertEqual(expected, actual)
        if press:
            self.test_arrow_press_release(press=False)

    def test_space_press_responce(self):
        """Check if a bullet gets fired when space is pressed"""
        pygame.event.post(Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        gf.check_events(self.ai_settings, self.stats, self.screen, self.play_button, 
            self.ship, self.aliens, self.bullets)
        actual = len(self.bullets)
        expected = 1
        self.assertEqual(expected, actual)

    def get_fleet_size(self):
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.ai_settings.screen_width - 2 * alien_width
        number_aliens_x  = int(available_space_x / (2*alien_width))
        available_space_y = (self.ai_settings.screen_height - 
            (3 * alien_height) - self.ship.rect.height)
        number_rows  = int(available_space_y / (2*alien_height))
        return number_aliens_x * number_rows

    def test_create_fleet(self):
        gf.create_fleet(self.ai_settings, self.screen, self.ship, self.aliens)
        acutal = len(self.aliens)
        expected = self.get_fleet_size()
        self.assertEqual(expected, acutal)

    def get_current_x(self):
        x = 0
        for alien in self.aliens.sprites():
            x = alien.rect.x
            break
        return x

    def test_fleet_move_right(self):
        """Test to see if an alien moves to the right"""
        self.test_create_fleet()
        self.ai_settings.fleet_direction = 1
        temp_x = self.get_current_x()
        gf.update_aliens(self.ai_settings, self.screen, self.stats, self.ship, self.aliens, self.bullets)
        actual = self.get_current_x() > temp_x
        self.assertEqual(True, actual)

    def test_fleet_move_left(self):
        """Test to see if an alien moves to the left"""
        self.test_create_fleet()
        self.ai_settings.fleet_direction = -1
        temp_x = self.get_current_x()
        gf.update_aliens(self.ai_settings, self.screen, self.stats,self.ship, self.aliens, self.bullets)
        actual = self.get_current_x() < temp_x
        self.assertEqual(True, actual)

    def get_current_y(self):
        y = 0
        for alien in self.aliens.sprites():
            y = alien.rect.y
            break
        return y

    def test_fleet_drop_down(self):
        """
        Test if fleet drops down when an alien reaches the right edge
            and that the fleet direction changes to the left
        """
        self.test_create_fleet()
        self.ai_settings.fleet_direction = 1
        temp_y = self.get_current_y()
        while True:
            gf.update_aliens(self.ai_settings, self.screen, self.stats,self.ship, self.aliens, self.bullets)
            if self.ai_settings.fleet_direction == -1:
                y = self.get_current_y()
                break
        actual = y > temp_y and self.ai_settings.fleet_direction == -1
        self.assertEqual(True, actual)

    def test_bullet_allien_collision_detection(self):
        """Check if a bullet alien collision detection gets handled correctly."""
        pygame.event.post(Event(pygame.KEYDOWN, key= pygame.K_SPACE))
        gf.create_fleet(self.ai_settings, self.screen, self.ship, self.aliens)
        gf.check_events(self.ai_settings, self.screen, self.stats,
            self.play_button, self.ship, self.aliens, self.bullets)
        fleet_size = len(self.aliens)
        while fleet_size == len(self.aliens) and len(self.bullets) == 1:
            gf.update_bullets(self.ai_settings, self.screen, self.ship, self.aliens, self.bullets)
        actual = len(self.aliens), len(self.bullets)
        expected = fleet_size - 1, 0
        self.assertEqual(expected, actual)

    def test_fleet_regeneration_and_level_up(self):
        """Fleet should be recreated when it's len reaches zero."""
        self.aliens.empty()
        prev_ship_speed = self.ai_settings.ship_speed_factor
        gf.check_bullet_alien_collisions(self.ai_settings, self.screen, self.ship, self.aliens, self.bullets)
        actual = (self.ai_settings.ship_speed_factor > prev_ship_speed and
            len(self.aliens) > 0)
        self.assertEqual(True, actual)

    def test_play_button_click(self):
        """Test if game is activated and reset when the play button is clicked"""
        pygame.event.post(Event(pygame.KEYDOWN, key= pygame.K_SPACE))
        screen_rect = self.screen.get_rect()
        pygame.event.post(Event(pygame.MOUSEBUTTONDOWN))
        gf.check_events(self.ai_settings, self.screen, self.stats,
            self.play_button, self.ship, self.aliens, self.bullets)
        full_fleet = Group()
        gf.create_fleet(self.ai_settings, self.screen, self.ship, full_fleet)
        actual = self.stats.game_active and (len(self.aliens) == len(full_fleet) and
            len(self.bullets) == 0)
        self.assertEqual(True, actual)



unittest.main()