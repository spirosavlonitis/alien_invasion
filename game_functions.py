import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet

 # events 

def fire_bullet(ai_settings, screen, ship, bullets):
    """Create and add a new bullet to bullets"""
    if len(bullets) < ai_settings.bullet_limit:
        bullets.add(Bullet(ai_settings, screen, ship))

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == 119:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, play_button, 
    ship, aliens, bullets, mouse_x, mouse_y):
    """Rest game settings and set game to active."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        aliens.empty()
        bullets.empty()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        stats.reset_stats()
        create_fleet(ai_settings, screen, ship, aliens)

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Respond to keyboard and mouse evens"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)

# events end

# bullets

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """
    Remove any bullets and aliens that have collided.
    Redraw the fleet if it has been destroyed.
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """
    Update bullets position and remove out of screen bullets.
    Check if any bullets have collided with any aliens,
        and remove both objects.
    """
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

# bullets end

# aliens

def change_fleet_direction(ai_settings, aliens):
    """Drop the down the fleet and change it's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    """Check if any alien has reached either edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, screen, stats, ship, aliens, bullets):
    """Redraw the fleet and recenter the ship. """
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False

def check_aliens_screen_bottom(ai_settings, screen, stats, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    for alien in aliens.sprites():
        if alien.rect.bottom >= alien.screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats,ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
        and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update(ai_settings)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, ship, aliens, bullets)

    check_aliens_screen_bottom(ai_settings, screen, stats, ship, aliens, bullets)

# aliens end

def update_screen(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Control update screen events and flip to new screen"""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2*alien_width))

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - 
        (3*alien_height) - ship_height)
    return int(available_space_y / (2*alien_height))

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien based on it's alien_number x position and row_number and
    add it to the aliens group"""
    alien = Alien(ai_settings, screen)
    alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.x = float(alien.rect.x)
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a fleet of aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.width)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)