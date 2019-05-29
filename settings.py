class Settings():
    """Settings for Alien Invasion"""
    def __init__(self):
        """Initialize static and dynamic settings"""
        # Screen settings
        self.screen_width = 1860
        self.screen_height = 1020
        self.screen_size = self.screen_width, self.screen_height
        self.bg_color = 230, 230, 230

        # Ship static settings
        self.ship_limit = 3

        # Bullet static settings
        self.bullet_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60

        # Alien static settings
        self.fleet_drop_speed = 10

        self.speed_up_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change with in the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase game speed when all Aliens have been destroyed."""
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
