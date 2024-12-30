import pygame

class GameManager:
    def __init__(self, screen_width, screen_height, asteroids_group):
        pygame.init()
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)

        screen_info = pygame.display.Info()
        
        self.asteroids = asteroids_group
        # can also track other game elements like score, lives, etc.

        # Add the asteroid images loading here
        self.asteroid_images = self.load_asteroid_images("assets/asteroid_sheet.png", num_rows=2, num_cols=4)

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
    
    def load_asteroid_images(self, sprite_sheet_path, num_rows, num_cols):
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        asteroid_width = 232
        asteroid_height = 212
        
        asteroid_images = []
        
        for row in range(num_rows):
            for col in range(num_cols):
                x = col * asteroid_width
                y = row * asteroid_height
                rect = pygame.Rect(x, y, asteroid_width, asteroid_height)
                image = sheet.subsurface(rect)
                asteroid_images.append(image)
                
        return asteroid_images
    
    def get_screen_dimensions(self):
        return self.SCREEN_WIDTH, self.SCREEN_HEIGHT

    def get_screen(self):
        return self.screen