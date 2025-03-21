import pygame
import sys

from background import Background
from score import Score
from audiomanager import AudioManager
from button import Button
from player import Player
from AsteroidField import *
from utils import resource_path
from highscore_manager import initialize_high_score, read_high_score, check_and_update_score

class GameManager:
    def __init__(self, screen_width, screen_height, asteroids_group):
        
        # Screen setup
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        
        # Game state and menu setup
        self.game_state = "MENU"
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Space Shooter', True, (255, 255, 255))
        self.game_over_title = self.font.render('Game Over', True, (255, 255, 255))
        self.high_score = initialize_high_score()
        self.score_checked = False

        # Initialize audio and start menu music
        self.audio_manager = AudioManager()
        self.audio_manager.load_music()
        self.audio_manager.play_menu_music()

        self.play_button = Button(
            screen_width/2 - 100, 
            screen_height/2 - 50, 
            200, 
            50, 
            "Play", 
            (0, 100, 0)
        )
        self.play_again_button = Button(
            screen_width/2 - 100, 
            screen_height/2 - 50, 
            200, 
            50, 
            "Play again", 
            (0, 100, 0)
        )
        self.quit_button = Button(
            screen_width/2 - 100, 
            screen_height/2 + 50, 
            200, 
            50, 
            "Exit", 
            (100, 0, 0)
        )

        # Sprite groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = asteroids_group
        self.shots = pygame.sprite.Group()

        # Game objects
        self.initialize_game_objects()



    def initialize_game_objects(self):
        # Initialize background
        self.background = Background(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    
        # Initialize score display
        self.score_display = Score()
    
        # Initialize audio manager
        self.audio_manager = AudioManager()

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()

        # Initialize player at center of screen
        self.player = Player(
        self.SCREEN_WIDTH / 2,
        self.SCREEN_HEIGHT / 2,
        self,  # passing the game_manager
        self.audio_manager
        )
        # preparing game state change
        self.player_lost = False

        # Add player to sprite groups
        self.updatable.add(self.player)
        self.drawable.add(self.player)
    
        # Load asteroid images
        self.asteroid_images = self.load_asteroid_images(resource_path("assets/asteroid_sheet.png"), num_rows=2, num_cols=4)

        # Create asteroid field
        self.asteroid_field = AsteroidField(self)

    def load_asteroid_images(self, path, num_rows, num_cols):
        # Load and split asteroid sprite sheet
        sprite_sheet = pygame.image.load(resource_path(path)).convert_alpha()

        asteroid_width = 232
        asteroid_height = 212
        
        images = []

        for row in range(num_rows):
            for col in range(num_cols):
                x = col * asteroid_width
                y = row * asteroid_height
                surface = pygame.Surface((asteroid_width, asteroid_height), pygame.SRCALPHA)
                surface.blit(sprite_sheet, (0, 0), (x, y, asteroid_width, asteroid_height))
                images.append(surface)
        return images
    
    def update(self, dt):

        self.asteroid_field.update(dt)
        
        if self.player_lost:
            self.game_state = "GAMEOVER"

        if self.game_state == "MENU":

            # Handle menu interactions
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            if self.play_button.is_clicked(mouse_pos, mouse_pressed):
                self.audio_manager.play_click()
                self.game_state = "PLAYING"
            elif self.quit_button.is_clicked(mouse_pos, mouse_pressed):
                self.audio_manager.play_click()
                pygame.quit()
                sys.exit()
                
        elif self.game_state == "PLAYING":
            # Update all game objects
            for object in self.updatable:
                object.update(dt)
            
            # Check asteroid collisions with bullets
            for asteroid in self.asteroids:
                for bullet in self.shots:
                    if asteroid.collision_check(bullet):
                        asteroid.split()
                        bullet.kill()
                        self.score_display.add_to_score()
                        self.audio_manager.play_explosion()
            
            # Check asteroid collisions with player
            for asteroid in self.asteroids:
                if asteroid.collision_check(self.player) and not self.player.is_player_invulnerable():
                    self.player.lose_life(dt)
                    
            
            # Update shots
            for shot in self.shots:
                if (shot.position.x < 0 or shot.position.x > self.SCREEN_WIDTH or 
                    shot.position.y < 0 or shot.position.y > self.SCREEN_HEIGHT):
                    shot.kill()

            self.score_checked = False

        elif self.game_state == "GAMEOVER":

            # updating highscore
            if not self.score_checked:
                check_and_update_score(self.score_display.get_score())
                self.score_checked = True

            # Handle menu interactions
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            if self.play_again_button.is_clicked(mouse_pos, mouse_pressed):
                self.audio_manager.play_click()
                self.reset_game()
                self.game_state = "PLAYING"
            elif self.quit_button.is_clicked(mouse_pos, mouse_pressed):
                self.audio_manager.play_click()

                pygame.quit()
                sys.exit()
            
            
    
    def draw(self, screen):

        if self.game_state == "MENU":
            # Draw menu
            screen.fill((0, 0, 0))  # Black background
            screen.blit(self.title, (self.SCREEN_WIDTH/2 - self.title.get_width()/2, 200))
            self.play_button.draw(screen)
            self.quit_button.draw(screen)
        
        elif self.game_state == "PLAYING":
            # Draw background
            self.background.draw(screen)
            
            # Draw shots first
            for shot in self.shots:
                shot.draw(screen)

            # Draw asteroids
            for asteroid in self.asteroids:
                asteroid.draw(screen)

            # Draw player last so it appears on top
            self.player.draw(screen)
        
            # Draw the player's lives
            self.player.lives_manager.draw(screen)

            # Update and draw score
            self.score_display.update_text()
            screen.blit(self.score_display.text, (35, 10))

        elif self.game_state == "GAMEOVER":
            screen.fill((0, 0, 0))  # Black background

            self.play_again_button.draw(screen)
            self.quit_button.draw(screen)

            # Center the "Game Over" title
            game_over_x = self.SCREEN_WIDTH/2 - self.game_over_title.get_width()/2
            screen.blit(self.game_over_title, (game_over_x, 200))
            
            # Display current score
            current_score = self.score_display.get_score()
            current_score_text = self.font.render(f'Your Score: {current_score}', True, (255, 255, 255))
            current_score_x = self.SCREEN_WIDTH/2 - current_score_text.get_width()/2
            screen.blit(current_score_text, (current_score_x, 300))

            # Dislpay High Score
            high_score_text = self.font.render(f'High Score: {read_high_score()}', True, (255, 255, 255))
            high_score_x = self.SCREEN_WIDTH/2 - high_score_text.get_width()/2
            screen.blit(high_score_text, (high_score_x, 400))


        # Update display
        pygame.display.flip()

    def clear_asteroids(self):
        for asteroid in self.asteroids.sprites():
            asteroid.kill()  

    def wrap_position(self, position):
        screen_width, screen_height = self.get_screen_dimensions()
        buffer = 50
    
        # Create a new wrapped position
        wrapped_x = position.x
        wrapped_y = position.y
    
        # Wrap horizontally
        if position.x < -buffer :
            wrapped_x = screen_width + buffer
        elif position.x > screen_width + buffer:
            wrapped_x = -buffer
        
        # Wrap vertically    
        if position.y < -buffer:
            wrapped_y = screen_height + buffer
        elif position.y > screen_height +buffer:
            wrapped_y = -buffer
        
        return pygame.Vector2(wrapped_x, wrapped_y)
    
    def load_asteroid_images(self, sprite_sheet_path, num_rows, num_cols):
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        asteroid_width = 232
        asteroid_height = 212

        asteroid_images = []
        
        for row in range(num_rows):
            for col in range(num_cols):
                # Calculate position on sprite sheet
                x = col * asteroid_width
                y = row * asteroid_height
                
                # Create subsurface from sprite sheet
                rect = pygame.Rect(x, y, asteroid_width, asteroid_height)
                temp_surface = sheet.subsurface(rect)
                
                # Get the actual bounds of the asteroid in this image
                actual_bounds = temp_surface.get_bounding_rect()
                
                # Create a new square surface
                size = max(actual_bounds.width, actual_bounds.height)
                centered_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                
                # Calculate position to center the asteroid
                center_x = (size - actual_bounds.width) // 2
                center_y = (size - actual_bounds.height) // 2
                
                # Blit the cropped asteroid onto the centered surface
                centered_surface.blit(temp_surface, 
                                    (center_x, center_y), 
                                    actual_bounds)
            
            asteroid_images.append(centered_surface)
                
        return asteroid_images
    
    def get_screen_dimensions(self):
        return self.SCREEN_WIDTH, self.SCREEN_HEIGHT
    
    def add_shot(self, shot):
        self.shots.add(shot)
        self.updatable.add(shot)
        self.drawable.add(shot)

    def add_asteroid(self, asteroid):

        self.asteroids.add(asteroid)
        self.updatable.add(asteroid)
        self.drawable.add(asteroid)
    
    def clear_shots(self):
        # Clear all shots from the list
        self.shots.empty()

    def reset_game(self):
        # Re-initialize game components
        self.initialize_game_objects()
    
        # Reset score or other necessary variables
        self.score_display.reset_score()

        # Reset player life/position if needed
        self.player.reset_position_and_lives()

        # Clear existing bullets and asteroids
        self.shots.empty()
        self.asteroids.empty()

        # Set game state to PLAYING
        self.game_state = "PLAYING"
