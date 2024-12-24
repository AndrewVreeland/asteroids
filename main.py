import pygame
from constants import *
from player import Player

def main():

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
        player.update(dt)
        player.draw(screen)
    
        # Update display
        pygame.display.flip()

        # Manage time
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()
