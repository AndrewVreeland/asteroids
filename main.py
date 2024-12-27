import pygame
from constants import *
from player import Player

def main():
    
    updatable = pygame.sprite.Group()
    drawable  = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x,y)
    

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    
        # Clear screen
        screen.fill((0, 0, 0,1))
    
        # Update player
        # player.update(dt)
        for object in updatable:
            object.update(dt)
        
        for object in drawable:
            object.draw(screen)
    
        # Update display
        pygame.display.flip()

        # Manage time
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()

