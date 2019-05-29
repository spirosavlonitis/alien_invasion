import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from button import Button
from game_stats import GameStats
import game_functions as gf
from ship import Ship
from bullet import Bullet
from alien import Alien

def main(argc, argv):
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode(ai_settings.screen_size)
    pygame.display.set_caption("Alien Invasion")

    stats = GameStats(ai_settings)
    play_button = Button(ai_settings, screen, "Play")
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:    
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, play_button, 
            ship, aliens, bullets)

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)