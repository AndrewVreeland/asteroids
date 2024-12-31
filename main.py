import pygame
import sys
import os

from gamemanager import GameManager

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    
    # Create asteroid group
    asteroid_group = pygame.sprite.Group()
    
    # Create game manager with screen dimensions
    game_manager = GameManager(screen_width, screen_height, asteroid_group)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        game_manager.update(dt)
        game_manager.draw(game_manager.screen)
        dt = clock.tick(60) / 1000
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()