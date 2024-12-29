import sys

from circleshape import *
from constants import *
from shot import Shot


class Player(CircleShape):

    def __init__(self, x, y, game_manager):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.reload_timer = 0
        self.life_timer = 10
        self.lives = 3
        self.game_manager = game_manager

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255, 1), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        

            # manage timer
        if self.reload_timer > 0:
            self.reload_timer -= dt
            


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    
    def shoot(self):
        if self.reload_timer <= 0:

            bullet = Shot(self.position.x, self.position.y)
            direction = pygame.Vector2(0,1).rotate(self.rotation)
            bullet.velocity = direction * PLAYER_SHOOT_SPEED
            self.reload_timer = PLAYER_SHOOT_COOLDOWN
    

    def lose_life(self, dt):
        
        if self.life_timer > 0:
            self.lives -= 1
            self.life_timer -= dt
            screen_width, screen_height = self.game_manager.get_screen_dimensions()
            self.position.xy = screen_width / 2, screen_height / 2
            self.game_manager.clear_asteroids()
        elif self.life_timer <= 0:
            self.life_timer == 10
        print(self.lives)
        if self.lives <= 0:
            print("Game over!")
            sys.exit()
        