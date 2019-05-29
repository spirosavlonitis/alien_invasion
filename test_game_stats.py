import unittest
from settings import Settings
from game_stats import GameStats


class TestGameStats(unittest.TestCase):
    def setUp(self):
        self.ai_settings = Settings()
        self.stats = GameStats(self.ai_settings)

    def test_attributes(self):
        attributes = [
            "ai_settings", "reset_stats", "game_active", "ships_left"
        ]
        actual = True
        for attribute in attributes:
            if hasattr(self.stats, attribute) == False:
                actual = False
                break
        self.assertEqual(True, actual)


unittest.main()