import pygame
import sys

from background import Background
from score import Score
from audiomanager import AudioManager
from button import Button
from player import Player
from AsteroidField import *

class GameManager:
    def __init__(self, screen_width, screen_height, asteroids_group):
        
        # Screen setup
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        
        # Game state and menu setup
        self.game_state = "MENU"
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('ASTEROIDS', True, (255, 255, 255))

        self.play_button = Button(
            screen_width/2 - 100, 
            screen_height/2 - 50, 
            200, 
            50, 
            "Play", 
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

        # Add player to sprite groups
        self.updatable.add(self.player)
        self.drawable.add(self.player)

        print("Number of updatable sprites:", len(self.updatable))
        print("Number of drawable sprites:", len(self.drawable))
        print("Number of asteroids:", len(self.asteroids))
    
        # Load asteroid images
        self.asteroid_images = self.load_asteroid_images("assets/asteroid_sheet.png", num_rows=2, num_cols=4)

        # Create asteroid field
        self.asteroid_field = AsteroidField(self)

    def load_asteroid_images(self, path, num_rows, num_cols):
        # Load and split asteroid sprite sheet
        sprite_sheet = pygame.image.load(path).convert_alpha()

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

        if self.game_state == "MENU":
            # Handle menu interactions
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            if self.play_button.is_clicked(mouse_pos, mouse_pressed):
                self.game_state = "PLAYING"
            elif self.quit_button.is_clicked(mouse_pos, mouse_pressed):
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
                if asteroid.collision_check(self.player):
                    self.player.lose_life(dt)
    
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
            
            # Draw all game objects
            for object in self.drawable:
                object.draw(screen)

            # Update and draw score
            self.score_display.update_text()
            screen.blit(self.score_display.text, (35, 10))
            
        # Update display
        pygame.display.flip()
    def clear_asteroids(self):
        print(f"Asteroids before clear: {len(self.asteroids)}")
        for asteroid in self.asteroids.sprites():
            asteroid.kill()  
        print(f"Asteroids before clear: {len(self.asteroids)}")

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
                x = col * asteroid_width
                y = row * asteroid_height
                rect = pygame.Rect(x, y, asteroid_width, asteroid_height)
                image = sheet.subsurface(rect)
                asteroid_images.append(image)
                
        return asteroid_images
    
    def get_screen_dimensions(self):
        return self.SCREEN_WIDTH, self.SCREEN_HEIGHT