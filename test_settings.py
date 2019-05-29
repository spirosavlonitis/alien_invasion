import unittest
from settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def test_attributes(self):
        attributes = [
            "screen_width", "screen_height","screen_size", "bg_color",
            "ship_limit", "bullet_width", "bullet_height", "bullet_color", 
            "bullet_limit", "fleet_drop_speed", "speed_up_scale",
            "initialize_dynamic_settings",
            "ship_speed_factor","bullet_speed_factor", "alien_speed_factor", 
            "fleet_direction",
            "increase_speed"
        ]
        actual = True
        for attr in attributes:
            if hasattr(self.settings, attr) == False:
                actual = False
                break
        expected = True
        self.assertEqual(expected, actual)

unittest.main()