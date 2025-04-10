import pygame
import os
from utils.resources import get_resource_path, load_sound


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
                # Extract just the filename from the path
                filename = os.path.basename(path)
                print(f"Loading sound {name}: {filename}")

                # Use the load_sound function
                self.sounds[name] = load_sound(filename)
                self.sounds[name].set_volume(self.sfx_volume)
            except Exception as e:
                print(f"Could not load sound {name}: {e}")
                self.sounds[name] = None

    def play_menu_music(self):
        """Play the menu music in a loop (WAV format)"""
        if not self.audio_available:
            return

        if self.current_music != "menu":
            try:
                # Extract just the filename from the config path
                music_file = os.path.basename(self.config.MENU_MUSIC)
                music_path = get_resource_path(os.path.join('assets', music_file))

                print(f"Loading menu music: {music_path}")
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume if not self.is_muted else 0)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = "menu"
            except pygame.error as e:
                print(f"Could not play menu music: {e}")

    def play_game_music(self, is_day):
        """Play the appropriate game music based on day/night cycle (WAV format)"""
        if not self.audio_available:
            return

        track = "day" if is_day else "night"
        if self.current_music != track:
            try:
                # Get the appropriate music path based on day/night
                config_path = self.config.GAME_MUSIC_DAY if is_day else self.config.GAME_MUSIC_NIGHT

                # Extract just the filename
                music_file = os.path.basename(config_path)
                music_path = get_resource_path(os.path.join('assets', music_file))

                print(f"Loading game music ({track}): {music_path}")
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume if not self.is_muted else 0)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = track
            except pygame.error as e:
                print(f"Could not play game music: {e}")

    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound(self, name):
        """Play a sound effect by name"""
        if not self.is_muted and name in self.sounds and self.sounds[name]:
            print(f"Playing sound: {name}")
            self.sounds[name].play()
        elif name in self.sounds and self.sounds[name] is None:
            print(f"Cannot play sound {name}: Sound not loaded")
        elif name not in self.sounds:
            print(f"Sound not found: {name}")

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