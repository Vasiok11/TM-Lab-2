import pygame
import sys
from utils.config import Config
from ui.main_menu import MainMenu
from ui.game_screen import GameScreen
from ui.settings_menu import SettingsMenu
from utils.audio import AudioManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Vampire City")

        self.config = Config()
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        # Initialize audio manager
        self.audio_manager = AudioManager(self.config)

        # Game states
        self.MAIN_MENU = 0
        self.GAME_SCREEN = 1
        self.SETTINGS = 2

        self.current_state = self.MAIN_MENU

        # Initialize screens
        self.main_menu = MainMenu(self)
        self.game_screen = GameScreen(self)
        self.settings_menu = SettingsMenu(self)

        # Start with menu music
        self.audio_manager.play_menu_music()

    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Pass events to current screen
                if self.current_state == self.MAIN_MENU:
                    self.main_menu.handle_event(event)
                elif self.current_state == self.GAME_SCREEN:
                    self.game_screen.handle_event(event)
                elif self.current_state == self.SETTINGS:
                    self.settings_menu.handle_event(event)

            # Update current screen
            if self.current_state == self.MAIN_MENU:
                self.main_menu.update()
            elif self.current_state == self.GAME_SCREEN:
                self.game_screen.update()
            elif self.current_state == self.SETTINGS:
                self.settings_menu.update()

            # Handle music transitions when state changes
            self._handle_music_transitions()

            # Render current screen
            self.screen.fill(self.config.BG_COLOR)

            if self.current_state == self.MAIN_MENU:
                self.main_menu.draw(self.screen)
            elif self.current_state == self.GAME_SCREEN:
                self.game_screen.draw(self.screen)
            elif self.current_state == self.SETTINGS:
                self.settings_menu.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.config.FPS)

        pygame.quit()
        sys.exit()

    def _handle_music_transitions(self):
        """Handle music changes when switching between game states"""
        # Store previous state to detect changes
        if not hasattr(self, '_previous_state'):
            self._previous_state = None

        # Only change music if state actually changed
        if self._previous_state != self.current_state:
            if self.current_state == self.MAIN_MENU:
                self.audio_manager.play_menu_music()
            elif self.current_state == self.GAME_SCREEN:
                # Start with day music (will be updated in game_screen.update())
                self.audio_manager.play_game_music(is_day=True)
            elif self.current_state == self.SETTINGS:
                # You might want to keep menu music or have different settings music
                self.audio_manager.play_menu_music()

        self._previous_state = self.current_state


if __name__ == "__main__":
    game = Game()
    game.run()