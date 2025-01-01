import pygame

from utils import resource_path

class AudioManager:
    def __init__(self):
        self.sound_enabled = False
        try:
            pygame.mixer.pre_init(44100, -16, 2, 1024)
            pygame.mixer.init()
            self.sound_enabled = True
            self.sounds = {}
            self.load_sounds()
        except pygame.error:
            print("Warning: Audio device not available, running without sound")
    
    def load_sounds(self):
        # Load all your sound effects here
        try:
            self.sounds['shoot'] = pygame.mixer.Sound(resource_path('assets/audio/shoot.mp3'))
            self.sounds['explosion_2'] = pygame.mixer.Sound(resource_path("assets/audio/explosion_2.mp3"))
            self.sounds['explosion_2'].set_volume(0.5)
            self.sounds['click'] = pygame.mixer.Sound(resource_path('assets/audio/click.mp3'))
            # self.sounds['game_over'] = pygame.mixer.Sound('assets/game_over.wav')
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.sound_enabled = False
    def load_music(self):
        try:
            pygame.mixer.music.load(resource_path('assets/audio/menu_music.mp3'))
            pygame.mixer.music.set_volume(0.3)  # Adjust volume (0.0 to 1.0)
        except Exception as e:
            print(f"Error loading music: {e}")

    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_explosion(self):
        # Randomly choose between the two explosion sounds
        import random
        explosion_sound = random.choice([self.sounds['explosion_2'], self.sounds['explosion_2']])
        explosion_sound.play()

    def play_click(self):
        if self.sound_enabled:
            self.play_sound('click')

    def play_menu_music(self):
        if self.sound_enabled and not pygame.mixer.music.get_busy():  
                pygame.mixer.music.play(-1)
    
    def stop_music(self):
        if self.sound_enabled:
            pygame.mixer.music.stop()