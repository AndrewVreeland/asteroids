import pygame

class Background:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        try:
            self.image = pygame.image.load("assets/space-galaxy-background.jpg").convert()
            self.image = pygame.transform.scale(self.image, 
                (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.image = pygame.Surface((self.screen_width, self.screen_height))
            self.image.fill((0, 0, 0))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))