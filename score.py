import pygame


class Score():
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 74)


    def add_to_score(self):
        self.score += 1
    
    def update_text(self):
        self.text = self.font.render(str(self.score), True, (255, 255, 255, 1))
    