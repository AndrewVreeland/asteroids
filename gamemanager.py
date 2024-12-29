import pygame

class GameManager:
    def __init__(self, screen_width, screen_height, asteroids_group):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.asteroids = asteroids_group
        # can also track other game elements like score, lives, etc.

    def get_screen_dimensions(self):
        return self.screen_width, self.screen_height
    
    def clear_asteroids(self):
        print(f"Asteroids before clear: {len(self.asteroids)}")
        for asteroid in self.asteroids.sprites():
            asteroid.kill()  
        print(f"Asteroids before clear: {len(self.asteroids)}")

    def wrap_position(self, position):
        screen_width, screen_height = self.get_screen_dimensions()
        buffer = 50
    
        # Create a new wrapped position
        wrapped_x = position.x
        wrapped_y = position.y
    
        # Wrap horizontally
        if position.x < -buffer :
            wrapped_x = screen_width + buffer
        elif position.x > screen_width + buffer:
            wrapped_x = -buffer
        
        # Wrap vertically    
        if position.y < -buffer:
            wrapped_y = screen_height + buffer
        elif position.y > screen_height +buffer:
            wrapped_y = -buffer
        
        return pygame.Vector2(wrapped_x, wrapped_y)