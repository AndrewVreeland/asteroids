import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from score import Score
from gamemanager import GameManager

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, game_manager):
        super().__init__(x, y, radius)
        self.game_manager = game_manager
        self.spawn_time = 2  # Half a second before wrapping starts
        self.can_wrap = False

    
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255, 1), self.position, self.radius,2)

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

            asteroid2 = Asteroid(self.position.x, self.position.y, new_rad, self.game_manager)
            asteroid2.velocity = angle_2 * 1.2 
            
            

