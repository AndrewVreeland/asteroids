import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from score import Score


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, game_manager):
        super().__init__(x, y, radius)
        self.game_manager = game_manager
        self.spawn_time = 2  # Half a second before wrapping starts
        self.can_wrap = False

        # Load and scale the image
        self.image = random.choice(self.game_manager.asteroid_images)
        self.image = pygame.transform.scale(self.image, (int(radius * 2), int(radius * 2)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        


    
    
    def draw(self, screen):
        # Update the rect position to match the asteroid's position
        self.rect.center = (int(self.position.x), int(self.position.y))
        # Draw the sprite instead of a circle
        screen.blit(self.image, self.rect)


    def update(self, dt):
        self.position += ((self.velocity * dt))

        # Wrap around screen edges
        if self.spawn_time > 0:
            self.spawn_time -= dt
            if self.spawn_time <= 0:
                self.can_wrap = True
        
        # Only wrap if we're past the spawn time
        if self.can_wrap:
            self.position = self.game_manager.wrap_position(self.position)
    
    def split(self):


        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            
        else:
            self.kill()

            random_angle = random.uniform(20, 50)

            angle_1 = self.velocity.rotate(random_angle)
            angle_2 = self.velocity.rotate(-random_angle)

            new_rad = self.radius - ASTEROID_MIN_RADIUS 

            asteroid1 = Asteroid(self.position.x, self.position.y, new_rad, self.game_manager)
            asteroid1.velocity = angle_1 * 1.2
            self.game_manager.add_asteroid(asteroid1)

            asteroid2 = Asteroid(self.position.x, self.position.y, new_rad, self.game_manager)
            asteroid2   .velocity = angle_2 * 1.2 
            self.game_manager.add_asteroid(asteroid2)
            

