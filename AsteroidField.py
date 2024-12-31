import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField():
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(1 + ASTEROID_MAX_RADIUS, y),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x, 1 + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self, game_manager):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_timer = 0.0
        self.game_manager = game_manager

    def spawn(self, radius, position, velocity):
        x, y = position
        asteroid = Asteroid(x, y, radius, self.game_manager)
        asteroid.velocity = velocity
        # Adds asteroid to the container groups
        self.game_manager.updatable.add(asteroid)
        self.game_manager.drawable.add(asteroid)
        self.game_manager.asteroids.add(asteroid)
    def update(self, dt):


        self.spawn_timer += dt
        
        # controls spawn rate
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            
            # Get base position and adjust for screen dimensions
            base_position = edge[1](random.uniform(0, 1))
            adjusted_position = pygame.Vector2(
                base_position.x * self.game_manager.SCREEN_WIDTH,
                base_position.y * self.game_manager.SCREEN_HEIGHT
            )
            
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, adjusted_position, velocity)
            