import pygame
import math
from utils.resources import get_resource_path
from utils.resources import load_sound


class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.config = game.config

        # Load fonts
        try:
            self.title_font = pygame.font.Font(get_resource_path("assets/fonts/gothic.ttf"), 46)
            self.option_font = pygame.font.Font(get_resource_path("assets/fonts/gothic.ttf"), 24)
            self.info_font = pygame.font.Font(get_resource_path("assets/fonts/gothic.ttf"), 16)
        except:
            self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.option_font = pygame.font.SysFont("Arial", 24)
            self.info_font = pygame.font.SysFont("Arial", 16)

        # Settings definitions
        self.settings = [
            {"name": "Simulation Speed", "value": self.config.DEFAULT_SIMULATION_SPEED, "min": 1, "max": 20, "step": 1,
             "description": "How fast time flows"},
            {"name": "Day Duration (seconds)", "value": self.config.DAY_DURATION, "min": 5, "max": 30, "step": 5,
             "description": "Length of each day/night"},
            {"name": "Human Ratio", "value": 0.1, "min": 0.05, "max": 0.3, "step": 0.05,
             "description": "Initial % of humans"},
            {"name": "Vampire Ratio", "value": 0.05, "min": 0.01, "max": 0.2, "step": 0.01,
             "description": "Initial % of vampires"}
        ]

        self.selected_setting = 0
        self.animation_time = 0
        self.fade_in_complete = False

        self.slider_width = 360
        self.slider_height = 28
        self.slider_spacing = 90
        self.handle_radius = 12
        self.button_width = 170
        self.button_height = 50

        self.slider_x = (self.config.SCREEN_WIDTH - self.slider_width) // 2
        self.slider_start_y = 140
        self.slider_rects = []
        for i in range(len(self.settings)):
            y = self.slider_start_y + i * self.slider_spacing
            self.slider_rects.append(pygame.Rect(self.slider_x, y, self.slider_width, self.slider_height))

        self.back_button = pygame.Rect(self.config.SCREEN_WIDTH // 2 - self.button_width - 20,
                                       self.slider_start_y + len(self.settings) * self.slider_spacing + 30,
                                       self.button_width, self.button_height)

        self.reset_button = pygame.Rect(self.config.SCREEN_WIDTH // 2 + 20,
                                        self.slider_start_y + len(self.settings) * self.slider_spacing + 30,
                                        self.button_width, self.button_height)

        self.bg_gradient = self._create_background()

        # Sounds (optional fallback-safe)
        try:
            self.hover_sound = load_sound("sounds/hover.wav")
            self.select_sound = load_sound("sounds/select.wav")
            self.slider_sound = load_sound("sounds/slider.wav")
            self.has_sound = True
        except:
            self.has_sound = False

        self.slider_sound_played = False

    def _create_background(self):
        surface = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        for y in range(self.config.SCREEN_HEIGHT):
            ratio = y / self.config.SCREEN_HEIGHT
            r = int(20 + 10 * ratio)
            g = 0
            b = int(15 + 10 * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.config.SCREEN_WIDTH, y))
        return surface

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.slider_rects):
                if rect.collidepoint(event.pos):
                    self.selected_setting = i
                    value_ratio = (event.pos[0] - rect.x) / rect.width
                    setting = self.settings[i]
                    setting["value"] = round((setting["min"] + value_ratio * (setting["max"] - setting["min"])) / setting["step"]) * setting["step"]
                    self._apply_settings()
                    if self.has_sound:
                        self.slider_sound.play()
                    break

            if self.back_button.collidepoint(event.pos):
                self._save_settings()
                self.game.current_state = self.game.MAIN_MENU
                if self.has_sound:
                    self.select_sound.play()

            if self.reset_button.collidepoint(event.pos):
                self._reset_to_defaults()
                if self.has_sound:
                    self.select_sound.play()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.slider_sound_played = False

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                for i, rect in enumerate(self.slider_rects):
                    if self.selected_setting == i:
                        x = max(rect.x, min(event.pos[0], rect.x + rect.width))
                        value_ratio = (x - rect.x) / rect.width
                        setting = self.settings[i]
                        new_value = round((setting["min"] + value_ratio * (setting["max"] - setting["min"])) / setting["step"]) * setting["step"]
                        if new_value != setting["value"]:
                            setting["value"] = new_value
                            self._apply_settings()
                            if self.has_sound and not self.slider_sound_played:
                                self.slider_sound.play()
                                self.slider_sound_played = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % (len(self.settings) + 2)
                if self.has_sound:
                    self.hover_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % (len(self.settings) + 2)
                if self.has_sound:
                    self.hover_sound.play()
            elif event.key == pygame.K_LEFT:
                if self.selected_setting < len(self.settings):
                    setting = self.settings[self.selected_setting]
                    setting["value"] = max(setting["min"], setting["value"] - setting["step"])
                    self._apply_settings()
            elif event.key == pygame.K_RIGHT:
                if self.selected_setting < len(self.settings):
                    setting = self.settings[self.selected_setting]
                    setting["value"] = min(setting["max"], setting["value"] + setting["step"])
                    self._apply_settings()
            elif event.key == pygame.K_RETURN:
                if self.selected_setting == len(self.settings):
                    self._save_settings()
                    self.game.current_state = self.game.MAIN_MENU
                elif self.selected_setting == len(self.settings) + 1:
                    self._reset_to_defaults()
            elif event.key == pygame.K_ESCAPE:
                self._save_settings()
                self.game.current_state = self.game.MAIN_MENU

    def update(self):
        self.animation_time += 1 / 60

    def _apply_settings(self):
        self.config.DEFAULT_SIMULATION_SPEED = self.settings[0]["value"]
        self.game.game_screen.simulation_speed = self.settings[0]["value"]
        self.config.DAY_DURATION = self.settings[1]["value"]

    def _reset_to_defaults(self):
        defaults = [10, 15, 0.1, 0.05]
        for i, setting in enumerate(self.settings):
            setting["value"] = defaults[i]
        self._apply_settings()

    def _save_settings(self):
        self._apply_settings()

    def draw(self, screen):
        screen.blit(self.bg_gradient, (0, 0))

        # Title
        title_surface = self.title_font.render("Settings", True, (180, 0, 0))
        title_shadow = self.title_font.render("Settings", True, (0, 0, 0))
        title_x = (self.config.SCREEN_WIDTH - title_surface.get_width()) // 2
        screen.blit(title_shadow, (title_x + 2, 62))
        screen.blit(title_surface, (title_x, 60))

        for i, (setting, rect) in enumerate(zip(self.settings, self.slider_rects)):
            # Background glow
            if i == self.selected_setting:
                glow_strength = (math.sin(pygame.time.get_ticks() / 250) + 1) * 0.5
                glow_color = (int(80 * glow_strength), 0, 0)
                pygame.draw.rect(screen, glow_color, rect.inflate(14, 14), border_radius=12)

            # Name and description
            name_surf = self.option_font.render(setting["name"], True, (255, 255, 255))
            desc_surf = self.info_font.render(setting["description"], True, (160, 160, 160))
            screen.blit(name_surf, (rect.x, rect.y - 45))
            screen.blit(desc_surf, (rect.x, rect.y - 22))

            # Track and fill
            pygame.draw.rect(screen, (40, 10, 10), rect, border_radius=6)
            fill_width = int(((setting["value"] - setting["min"]) / (setting["max"] - setting["min"])) * rect.width)
            pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(rect.x, rect.y, fill_width, rect.height), border_radius=6)

            # Handle
            handle_x = rect.x + fill_width
            handle_y = rect.y + rect.height // 2
            pygame.draw.circle(screen, (200, 50, 50), (handle_x, handle_y), self.handle_radius)
            pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 3)

            # Value text
            if i == 0:
                value_text = f"{int(setting['value'])}x"
            elif i == 1:
                value_text = f"{int(setting['value'])}s"
            else:
                value_text = f"{int(setting['value'] * 100)}%"

            value_surface = self.option_font.render(value_text, True, (230, 230, 230))
            screen.blit(value_surface, (rect.right + 15, rect.y + (rect.height - value_surface.get_height()) // 2))

        # Draw buttons
        self._draw_button(screen, self.back_button, "Back", self.selected_setting == len(self.settings))
        self._draw_button(screen, self.reset_button, "Reset", self.selected_setting == len(self.settings) + 1)

        # Footer instructions
        hint = "← → adjust | ↑ ↓ navigate | Enter = select"
        hint_surface = self.info_font.render(hint, True, (160, 160, 160))
        hint_x = (self.config.SCREEN_WIDTH - hint_surface.get_width()) // 2
        screen.blit(hint_surface, (hint_x, self.config.SCREEN_HEIGHT - 40))

    def _draw_button(self, screen, rect, label, selected):
        if selected:
            glow = (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.5
            glow_color = (int(100 * glow), 0, 0)
            pygame.draw.rect(screen, glow_color, rect.inflate(12, 12), border_radius=10)

        pygame.draw.rect(screen, (30, 0, 0), rect, border_radius=5)
        pygame.draw.rect(screen, (150, 0, 0), rect, 2, border_radius=5)
        label_surf = self.option_font.render(label, True, (255, 100, 100) if selected else (180, 180, 180))
        label_x = rect.x + (rect.width - label_surf.get_width()) // 2
        label_y = rect.y + (rect.height - label_surf.get_height()) // 2
        screen.blit(label_surf, (label_x, label_y))
