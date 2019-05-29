import unittest
import pygame
from button import Button
from settings import Settings


class TestButton(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(self.ai_settings.screen_size)
        self.button = Button(self.ai_settings, self.screen, "Play")

    def test_attributes(self):
        attributes = [
            "width", "height", "button_color", "text_color", "font",
            "rect",  "screen_rect", 
            "prep_msg", "msg_image", "msg_image_rect",
            "draw_button"
        ]
        actual = True
        for attribute in attributes:
            if not hasattr(self.button, attribute):
                actual = False
                break
        self.assertEqual(True, actual)

unittest.main()