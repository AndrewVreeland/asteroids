import pygame
from constants import SHOT_RADIUS

from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, game_manager):
        super().__init__(x, y, SHOT_RADIUS)
        self.game_manager = game_manager
        
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255, 1), self.position, SHOT_RADIUS, 2)

    def update(self, dt):
        self.position += ((self.velocity * dt))

        # Get screen dimensions
        screen_width, screen_height = self.game_manager.get_screen_dimensions()
        
        # Check if bullet is outside screen view (with no buffer wrapping)
        if (self.position.x < 0 or 
            self.position.x > screen_width or 
            self.position.y < 0 or 
            self.position.y > screen_height):
            self.kill()  # Remove the bullet sprite

        # Wrap around screen edges
        self.position = self.game_manager.wrap_position(self.position)