
from circleshape import *
from constants import *
from shot import Shot
from utils import resource_path
from lives_manager import Lives

class Player(CircleShape):

    def __init__(self, x, y, game_manager, audio_manager):
        super().__init__(x,y,PLAYER_RADIUS)

        # Load and set up the image
        self.original_image = pygame.image.load(resource_path("assets/ship.png")).convert_alpha()
        # Scale image to match your desired size
        self.original_image = pygame.transform.scale(self.original_image, (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.screen_width, self.screen_height = game_manager.get_screen_dimensions()
        self.lives_manager = Lives(3, self.screen_width)
        self.reload_timer = 0
        self.rotation = 0.0
        self.game_manager = game_manager
        self.audio_manager = audio_manager
        self.velocity = pygame.Vector2(0, 0)
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 2  
        self.flash_interval = 0.2
        self.is_visible = True
        self.alpha = 255
        
    
    def draw(self, screen):
        if self.is_invulnerable:
            self.alpha = 128 if not self.is_visible else 255
        else:
            self.alpha = 255

        # Apply the alpha to the rotated image
        angle = round(-self.rotation + 180)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.image.set_alpha(self.alpha)
        
        # Update rect and draw
        self.rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, self.rect)


    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        # Keep rotation between 0 and 360 degrees
        self.rotation = self.rotation % 360


        # Handle rotation
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)

        # Handle shooting
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Handle movement
        if keys[pygame.K_w]:
            self.accelerate(dt)
        elif keys[pygame.K_s]:
            self.accelerate(-dt)
        else:
            self.decelerate(dt)
        
        # Update position using velocity
        self.position += self.velocity * dt

        if self.is_invulnerable:
            self.invulnerable_timer -= dt

            # Flash effect
            self.is_visible = int(self.invulnerable_timer / self.flash_interval) % 2 == 0

            
        if self.invulnerable_timer <= 0:
            self.is_invulnerable = False
            self.is_visible = True

        # Wrap around screen edges
        self.position = self.game_manager.wrap_position(self.position)

            # manage timer
        if self.reload_timer > 0:
            self.reload_timer -= dt
            


    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # Apply acceleration in the forward direction
        self.velocity += forward * ACCELERATION_RATE * dt
        
        #clamp velocity
        # Get the magnitude of the velocity vector
        speed = self.velocity.length()

        # If speed is greater than max, scale the vector down
        if speed > MAXIMUM_VELOCITY:
        # Normalize the vector (make it length 1) then multiply by max velocity
            self.velocity = self.velocity.normalize() * MAXIMUM_VELOCITY
        


    def decelerate(self, dt):
        # Get the magnitude of the velocity vector
        speed = self.velocity.length()

        # If not moving at all, do nothing
        if speed == 0:
            return
        
        # if we are moving decel
        if speed < 0.01:
            self.velocity = pygame.Vector2(0, 0)
        else:  
            # Slow down in the direction we're moving
            decel_direction = self.velocity.normalize()
            self.velocity -= decel_direction * DECELERATION_RATE * dt

    def shoot(self):
        if self.reload_timer <= 0:

            bullet = Shot(self.position.x, self.position.y, self.game_manager)
            direction = pygame.Vector2(0,1).rotate(self.rotation)
            bullet.velocity = direction * PLAYER_SHOOT_SPEED
            self.game_manager.add_shot(bullet)
            self.reload_timer = PLAYER_SHOOT_COOLDOWN
            self.audio_manager.play_sound('shoot')

    
    def is_in_buffer_zone(self):
        buffer = 50  # Make sure this matches your GameManager's buffer
        return (self.position.x < 0 or 
                self.position.x > self.screen_width or 
                self.position.y < 0 or 
                self.position.y > self.screen_height)

    def lose_life(self, dt):

        if not self.is_in_buffer_zone():
            if not self.is_invulnerable:
                self.audio_manager.play_sound('explosion_1')
                self.lives_manager.lose_life()
                # First reset position
                self.position.xy = self.screen_width / 2, self.screen_height / 2
                # Then set up invulnerability
                self.velocity = pygame.Vector2(0, 0)  # Reset velocity too
                self.is_invulnerable = True
                self.invulnerable_timer = self.invulnerable_duration
                self.is_visible = True  # Make sure player is visible initially
            if self.lives_manager.lives <= 0:
                self.notify_game_manager_game_over()
        
    def notify_game_manager_game_over(self):
        self.game_manager.player_lost = True
    
    def reset_position_and_lives(self):
        # Reset the position to the center of the screen
        self.position.xy = self.screen_width / 2, self.screen_height / 2
        
        # Reset the number of lives
        self.lives_manager.reset_lives()
        
        # Optionally reset timers and velocity
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0.0
        self.reload_timer = 0

        # Update the player's rect to match the reset position
        self.rect.center = self.position

        # Optionally: you might want to clear current shots or play a sound
        self.game_manager.clear_shots()
        self.audio_manager.play_sound('reset')
        
    def is_player_invulnerable(self):
        return self.is_invulnerable