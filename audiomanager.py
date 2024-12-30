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
            self.sounds['explosion_2'] = pygame.mixer.Sound("assets/audio/explosion_2.mp3")
            self.sounds['explosion_2'] = pygame.mixer.Sound("assets/audio/explosion_2.mp3")
            # self.sounds['game_over'] = pygame.mixer.Sound('assets/game_over.wav')
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.sound_enabled = False

    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_explosion(self):
        # Randomly choose between the two explosion sounds
        import random
        explosion_sound = random.choice([self.sounds['explosion_2'], self.sounds['explosion_2']])
        explosion_sound.play()