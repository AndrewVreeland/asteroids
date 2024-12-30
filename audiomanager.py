import pygame

class AudioManager:
    def __init__(self):
        self.sound_enabled = False
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            self.sounds = {}
            self.load_sounds()
        except pygame.error:
            print("Warning: Audio device not available, running without sound")
    
    def load_sounds(self):
        # Load all your sound effects here
        try:
            self.sounds['shoot'] = pygame.mixer.Sound('assets/audio/shoot.mp3')  
            # self.sounds['explosion'] = pygame.mixer.Sound('assets/explosion.wav')
            # self.sounds['game_over'] = pygame.mixer.Sound('assets/game_over.wav')
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.sound_enabled = False

    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()