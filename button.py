import pygame

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        
        # Draw button rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Render and draw text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, mouse_pos, mouse_pressed):
        # Check if mouse is over button and clicked
        if self.rect.collidepoint(mouse_pos):
            return mouse_pressed
        return False