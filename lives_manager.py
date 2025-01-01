import pygame

class Lives:
    def __init__(self, initial_lives, screen_width):
        self.initial_lives = initial_lives
        self.lives = initial_lives
        self.font = pygame.font.Font(None, 36)
        self.screen_width = screen_width

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def draw(self, screen):
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        x = self.screen_width - lives_text.get_width() - 10
        y = 10
        screen.blit(lives_text, (x, y))

    def is_game_over(self):
        return self.lives <= 0
    
    def reset_lives(self):
        self.lives = self.initial_lives