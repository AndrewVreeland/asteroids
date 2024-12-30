import pygame
import pickle


from constants import *
from player import Player
from asteroid import Asteroid
from AsteroidField import AsteroidField
from shot import Shot
from score import Score
from gamemanager import GameManager
from background import Background


def main():

    pygame.init()
    pygame.font.init()

    #sprite groups
    updatable = pygame.sprite.Group()
    drawable  = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroid_group, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    # delta time and player position
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    #clock and game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    #instansiations
    game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT, asteroid_group)
    player = Player(x,y, game_manager)
    asteroid_field = AsteroidField(game_manager)
    score_display = Score()
    background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
    

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
        # Clear screen
        background.draw(screen)
    
        # Update player
        # player.update(dt)
        for object in updatable:
            object.update(dt)

        # asteroid collisions
        for object in asteroid_group:
            for bullet in shots:
                if object.collision_check(bullet) == True:
                    object.split()
                    bullet.kill()
                    score_display.add_to_score()

        for object in asteroid_group:
            if object.collision_check(player) == True:
                player.lose_life(dt)
                
        
        # update score text
        score_display.update_text()
        screen.blit(score_display.text, (35, 10))

        for object in drawable:
            object.draw(screen)

    
        # Update display
        pygame.display.flip()

        # Manage time
        dt = clock.tick(60) / 1000

        
if __name__ == "__main__":
    main()

