import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS


class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255, 1), self.position, self.radius,2)

    def update(self, dt):
        self.position += ((self.velocity * dt))
    
    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
        else:
            self.kill()

            random_angle = random.uniform(20, 50)

            angle_1 = self.velocity.rotate(random_angle)
            angle_2 = self.velocity.rotate(-random_angle)

            new_rad = self.radius - ASTEROID_MIN_RADIUS 

            asteroid1 = Asteroid(self.position.x, self.position.y, new_rad)
            asteroid1.velocity = angle_1 * 1.2

            asteroid2 = Asteroid(self.position.x, self.position.y, new_rad)
            asteroid2.velocity = angle_2 * 1.2 
            

