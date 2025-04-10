# audio_manager.py
import pygame
import os

# utils/audio.py
import pygame
import os


class AudioManager:
    def __init__(self, config):
        self.config = config
        self.current_music = None
        self.is_muted = False
        self.music_volume = config.MUSIC_VOLUME
        self.sfx_volume = config.SOUND_EFFECTS_VOLUME

        # Initialize mixer with settings optimized for WAV files
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)  # Larger buffer for WAV music
            self.audio_available = True
        except pygame.error as e:
            print(f"Audio initialization failed: {e}")
            self.audio_available = False
            return

        # Preload sound effects
        self.sounds = {}
        for name, path in config.SOUND_FX.items():
            try:
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sfx_volume)
                else:
                    print(f"Sound file not found: {path}")
                    self.sounds[name] = None
            except pygame.error as e:
                print(f"Could not load sound {name}: {e}")
                self.sounds[name] = None

    def play_menu_music(self):
        """Play the menu music in a loop (WAV format)"""
        if not self.audio_available:
            return

        if self.current_music != "menu":
            try:
                if os.path.exists(self.config.MENU_MUSIC):
                    pygame.mixer.music.load(self.config.MENU_MUSIC)
                    pygame.mixer.music.set_volume(self.music_volume if not self.is_muted else 0)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    self.current_music = "menu"
                else:
                    print(f"Menu music file not found: {self.config.MENU_MUSIC}")
            except pygame.error as e:
                print(f"Could not play menu music: {e}")

    def play_game_music(self, is_day):
        """Play the appropriate game music based on day/night cycle (WAV format)"""
        if not self.audio_available:
            return

        track = "day" if is_day else "night"
        if self.current_music != track:
            try:
                music_path = self.config.GAME_MUSIC_DAY if is_day else self.config.GAME_MUSIC_NIGHT
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume if not self.is_muted else 0)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    self.current_music = track
                else:
                    print(f"Game music file not found: {music_path}")
            except pygame.error as e:
                print(f"Could not play game music: {e}")

    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound(self, name):
        """Play a sound effect by name"""
        if not self.is_muted and name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def toggle_mute(self):
        """Toggle audio mute state"""
        self.is_muted = not self.is_muted
        pygame.mixer.music.set_volume(0 if self.is_muted else self.music_volume)
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(0 if self.is_muted else self.sfx_volume)
        return self.is_muted

    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.is_muted:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        if not self.is_muted:
            for sound in self.sounds.values():
                if sound:
                    sound.set_volume(self.sfx_volume)