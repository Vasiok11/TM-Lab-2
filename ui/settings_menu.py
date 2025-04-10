import pygame
import math  # Import the math module for trigonometric functions

class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.config = game.config
        # Load fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/gothic.ttf", 46)
            self.option_font = pygame.font.Font("assets/fonts/gothic.ttf", 24)
            self.info_font = pygame.font.Font("assets/fonts/gothic.ttf", 16)
        except:
            # Fallback to system fonts
            self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.option_font = pygame.font.SysFont("Arial", 24)
            self.info_font = pygame.font.SysFont("Arial", 16)
        # Settings options
        self.settings = [
            {"name": "Simulation Speed", "value": self.config.DEFAULT_SIMULATION_SPEED, "min": 1, "max": 20, "step": 1,
             "description": "Controls how fast the simulation runs"},
            {"name": "Day Duration (seconds)", "value": self.config.DAY_DURATION, "min": 5, "max": 30, "step": 5,
             "description": "Length of a day/night cycle"},
            {"name": "Human Ratio", "value": 0.1, "min": 0.05, "max": 0.3, "step": 0.05,
             "description": "Starting percentage of humans in new games"},
            {"name": "Vampire Ratio", "value": 0.05, "min": 0.01, "max": 0.2, "step": 0.01,
             "description": "Starting percentage of vampires in new games"}
        ]
        self.selected_setting = 0
        # Create background effect
        self.bg_gradient = self._create_background()
        # Try to load background image
        try:
            self.bg_image = pygame.image.load("assets/images/settings_bg.png").convert_alpha()
            self.bg_image = pygame.transform.scale(self.bg_image,
                                                   (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            self.has_bg_image = True
        except:
            self.has_bg_image = False
        # Button dimensions
        self.slider_width = 350
        self.slider_height = 30
        self.button_width = 180
        self.button_height = 50
        self.handle_radius = 12
        # Calculate positions
        self.slider_x = (self.config.SCREEN_WIDTH - self.slider_width) // 2
        self.slider_start_y = 170
        self.slider_spacing = 100
        self.slider_rects = []
        for i in range(len(self.settings)):
            slider_y = self.slider_start_y + i * self.slider_spacing
            self.slider_rects.append(pygame.Rect(self.slider_x, slider_y, self.slider_width, self.slider_height))
        # Back button
        self.back_button = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 - self.button_width - 20,
            self.slider_start_y + len(self.settings) * self.slider_spacing + 30,
            self.button_width,
            self.button_height
        )
        # Reset button
        self.reset_button = pygame.Rect(
            self.config.SCREEN_WIDTH // 2 + 20,
            self.slider_start_y + len(self.settings) * self.slider_spacing + 30,
            self.button_width,
            self.button_height
        )
        # Animation state
        self.animation_time = 0
        self.fade_in_complete = False
        # Sound effects
        try:
            self.hover_sound = pygame.mixer.Sound("assets/sounds/hover.wav")
            self.select_sound = pygame.mixer.Sound("assets/sounds/select.wav")
            self.slider_sound = pygame.mixer.Sound("assets/sounds/slider.wav")
            self.has_sound = True
        except:
            self.has_sound = False
        # Track if we've played slider sound
        self.slider_sound_played = False

    def _create_background(self):
        """Create a dark gradient background"""
        bg = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        for y in range(self.config.SCREEN_HEIGHT):
            # Calculate gradient color (darker at top, lighter at bottom)
            color_value = int(20 * (y / self.config.SCREEN_HEIGHT))
            color = (max(0, 20 - color_value), 0, max(0, 15 - color_value))
            pygame.draw.line(bg, color, (0, y), (self.config.SCREEN_WIDTH, y))
        return bg

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked on a slider
            for i, rect in enumerate(self.slider_rects):
                if rect.collidepoint(event.pos):
                    self.selected_setting = i
                    # Update value based on click position
                    value_ratio = (event.pos[0] - rect.x) / rect.width
                    setting = self.settings[i]
                    setting["value"] = setting["min"] + value_ratio * (setting["max"] - setting["min"])
                    # Round to step
                    setting["value"] = round(setting["value"] / setting["step"]) * setting["step"]
                    self._apply_settings()
                    if self.has_sound:
                        self.slider_sound.play()
                    break
            # Check if clicked on back button
            if self.back_button.collidepoint(event.pos):
                if self.has_sound:
                    self.select_sound.play()
                self._save_settings()
                self.game.current_state = self.game.MAIN_MENU
            # Check if clicked on reset button
            if self.reset_button.collidepoint(event.pos):
                if self.has_sound:
                    self.select_sound.play()
                self._reset_to_defaults()
        elif event.type == pygame.MOUSEBUTTONUP:
            # Reset slider sound flag
            self.slider_sound_played = False
        elif event.type == pygame.MOUSEMOTION:
            # Handle dragging sliders
            if event.buttons[0]:  # Left button held
                for i, rect in enumerate(self.slider_rects):
                    if self.selected_setting == i:
                        # Calculate new value based on mouse position
                        x = max(rect.x, min(event.pos[0], rect.x + rect.width))
                        value_ratio = (x - rect.x) / rect.width
                        setting = self.settings[i]
                        new_value = setting["min"] + value_ratio * (setting["max"] - setting["min"])
                        # Round to step
                        new_value = round(new_value / setting["step"]) * setting["step"]
                        # Only update if value changed
                        if new_value != setting["value"]:
                            setting["value"] = new_value
                            self._apply_settings()
                            if self.has_sound and not self.slider_sound_played:
                                self.slider_sound.play()
                                self.slider_sound_played = True
                        break
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
                    if self.has_sound:
                        self.slider_sound.play()
            elif event.key == pygame.K_RIGHT:
                if self.selected_setting < len(self.settings):
                    setting = self.settings[self.selected_setting]
                    setting["value"] = min(setting["max"], setting["value"] + setting["step"])
                    self._apply_settings()
                    if self.has_sound:
                        self.slider_sound.play()
            elif event.key == pygame.K_RETURN:
                if self.selected_setting == len(self.settings):  # Back button selected
                    if self.has_sound:
                        self.select_sound.play()
                    self._save_settings()
                    self.game.current_state = self.game.MAIN_MENU
                elif self.selected_setting == len(self.settings) + 1:  # Reset button selected
                    if self.has_sound:
                        self.select_sound.play()
                    self._reset_to_defaults()
            elif event.key == pygame.K_ESCAPE:
                if self.has_sound:
                    self.select_sound.play()
                self._save_settings()
                self.game.current_state = self.game.MAIN_MENU

    def _apply_settings(self):
        """Apply settings to the game configuration"""
        # Apply simulation speed
        self.config.DEFAULT_SIMULATION_SPEED = self.settings[0]["value"]
        self.game.game_screen.simulation_speed = self.settings[0]["value"]
        # Apply day duration
        self.config.DAY_DURATION = self.settings[1]["value"]

    def _reset_to_defaults(self):
        """Reset all settings to default values"""
        default_values = [10, 15, 0.1, 0.05]  # Defaults for each setting
        for i, setting in enumerate(self.settings):
            setting["value"] = default_values[i]
        self._apply_settings()

    def _save_settings(self):
        """Save settings and apply them to the game"""
        self._apply_settings()
        # Human and vampire ratios will be used next time the grid is randomized

    def update(self):
        self.animation_time += 1 / 60
        # Fade in effect
        if not self.fade_in_complete and self.animation_time > 0.5:
            self.fade_in_complete = True
        # Mouse hover effect for back button and sliders
        mouse_pos = pygame.mouse.get_pos()
        # Check sliders
        for i, rect in enumerate(self.slider_rects):
            if rect.collidepoint(mouse_pos):
                if self.selected_setting != i:
                    self.selected_setting = i
                    if self.has_sound:
                        self.hover_sound.play()
                break
        # Check back button
        if self.back_button.collidepoint(mouse_pos):
            if self.selected_setting != len(self.settings):
                self.selected_setting = len(self.settings)  # Select back button
                if self.has_sound:
                    self.hover_sound.play()
        # Check reset button
        elif self.reset_button.collidepoint(mouse_pos):
            if self.selected_setting != len(self.settings) + 1:
                self.selected_setting = len(self.settings) + 1  # Select reset button
                if self.has_sound:
                    self.hover_sound.play()

    def draw(self, screen):
        # Draw background
        if self.has_bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.blit(self.bg_gradient, (0, 0))
        # Apply fade-in effect
        if not self.fade_in_complete:
            alpha = min(255, int(255 * self.animation_time))
            overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - alpha)
            screen.blit(overlay, (0, 0))
        # Draw title with shadow
        title_text = "Settings"
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        title_surface = self.title_font.render(title_text, True, (180, 0, 0))
        title_x = (self.config.SCREEN_WIDTH - title_surface.get_width()) // 2
        title_y = 60
        screen.blit(shadow_surface, (title_x + 2, title_y + 2))
        screen.blit(title_surface, (title_x, title_y))
        # Draw sliders
        for i, (setting, rect) in enumerate(zip(self.settings, self.slider_rects)):
            # Draw setting name
            name_surface = self.option_font.render(setting["name"], True, (200, 200, 200))
            name_x = rect.x
            name_y = rect.y - 40
            screen.blit(name_surface, (name_x, name_y))
            # Draw description
            desc_surface = self.info_font.render(setting["description"], True, (150, 150, 150))
            desc_x = rect.x
            desc_y = rect.y - 15
            screen.blit(desc_surface, (desc_x, desc_y))
            # Draw slider track
            if i == self.selected_setting:
                track_color = (60, 10, 10)
                fill_color = (150, 0, 0)
                handle_color = (200, 50, 50)
            else:
                track_color = (30, 5, 5)
                fill_color = (100, 0, 0)
                handle_color = (150, 0, 0)
            # Draw slider background (track)
            pygame.draw.rect(screen, track_color, rect, border_radius=5)
            # Draw slider fill
            value_ratio = (setting["value"] - setting["min"]) / (setting["max"] - setting["min"])
            filled_width = value_ratio * rect.width
            filled_rect = pygame.Rect(rect.x, rect.y, filled_width, rect.height)
            pygame.draw.rect(screen, fill_color, filled_rect, border_radius=5)
            # Draw slider handle
            handle_x = rect.x + filled_width
            handle_y = rect.y + rect.height // 2
            pygame.draw.circle(screen, handle_color, (int(handle_x), int(handle_y)), self.handle_radius)
            # Draw highlight on handle
            pygame.draw.circle(screen, (255, 100, 100), (int(handle_x), int(handle_y)), self.handle_radius // 2)
            # Draw value with shadow
            if i == 0:  # Simulation speed (integer)
                value_text = f"{int(setting['value'])}x"
            elif i == 1:  # Day duration (integer seconds)
                value_text = f"{int(setting['value'])}s"
            else:  # Percentage values
                value_text = f"{int(setting['value'] * 100)}%"
            value_shadow = self.option_font.render(value_text, True, (0, 0, 0))
            value_surface = self.option_font.render(value_text, True, (220, 220, 220))
            value_x = rect.x + rect.width + 20
            value_y = rect.y + (rect.height - value_surface.get_height()) // 2
            screen.blit(value_shadow, (value_x + 1, value_y + 1))
            screen.blit(value_surface, (value_x, value_y))
        # Draw back button
        self._draw_button(screen, self.back_button, "Back", self.selected_setting == len(self.settings))
        # Draw reset button
        self._draw_button(screen, self.reset_button, "Reset", self.selected_setting == len(self.settings) + 1)
        # Draw instructions
        instructions = "← → to adjust values | ↑ ↓ to navigate | Enter to select"
        instructions_surface = self.info_font.render(instructions, True, (150, 150, 150))
        instructions_x = (self.config.SCREEN_WIDTH - instructions_surface.get_width()) // 2
        instructions_y = self.config.SCREEN_HEIGHT - instructions_surface.get_height() - 20
        screen.blit(instructions_surface, (instructions_x, instructions_y))

    def _draw_button(self, screen, rect, text, selected):
        # Button glow effect when selected
        if selected:
            glow_rect = rect.inflate(10, 10)
            glow_strength = (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.5  # Replaced pygame.math.sin with math.sin
            glow_color = (
                int(100 * glow_strength),
                0,
                0
            )
            pygame.draw.rect(screen, glow_color, glow_rect, border_radius=8)
            # Active button
            color = (40, 0, 0)
            border_color = (200, 0, 0)
            text_color = (255, 100, 100)
        else:
            # Inactive button
            color = (20, 0, 0)
            border_color = (100, 0, 0)
            text_color = (150, 150, 150)
        # Draw button
        pygame.draw.rect(screen, color, rect, border_radius=5)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=5)
        # Draw text with shadow
        text_shadow = self.option_font.render(text, True, (0, 0, 0))
        text_surface = self.option_font.render(text, True, text_color)
        text_x = rect.x + (rect.width - text_surface.get_width()) // 2
        text_y = rect.y + (rect.height - text_surface.get_height()) // 2
        screen.blit(text_shadow, (text_x + 1, text_y + 1))
        screen.blit(text_surface, (text_x, text_y))