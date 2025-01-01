import pygame


class Score():
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 74)


    def add_to_score(self):
        self.score += 1
    
    def update_text(self):
        self.text = self.font.render(str(self.score), True, (255, 255, 255, 1))
    
    def reset_score(self):
        # Set the score to its initial value
        self.score_value = 0
        self.update_text()

    def get_score(self):
        return self.score