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