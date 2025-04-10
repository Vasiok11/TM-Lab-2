import pygame


class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.config = game.config

        # Load fonts
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.option_font = pygame.font.SysFont("Arial", 24)

        # Settings options
        self.settings = [
            {"name": "Simulation Speed", "value": self.config.DEFAULT_SIMULATION_SPEED, "min": 1, "max": 20, "step": 1},
            {"name": "Day Duration (seconds)", "value": self.config.DAY_DURATION, "min": 5, "max": 30, "step": 5},
            {"name": "Human Ratio", "value": 0.1, "min": 0.05, "max": 0.3, "step": 0.05},
            {"name": "Vampire Ratio", "value": 0.05, "min": 0.01, "max": 0.2, "step": 0.01}
        ]

        self.selected_setting = 0

        # Button dimensions
        self.slider_width = 300
        self.slider_height = 20
        self.button_width = 150
        self.button_height = 40

        # Calculate positions
        slider_x = (self.config.SCREEN_WIDTH - self.slider_width) // 2
        slider_start_y = 150
        self.slider_spacing = 80

        self.slider_rects = []
        for i in range(len(self.settings)):
            slider_y = slider_start_y + i * self.slider_spacing
            self.slider_rects.append(pygame.Rect(slider_x, slider_y, self.slider_width, self.slider_height))

        # Back button
        self.back_button = pygame.Rect(
            (self.config.SCREEN_WIDTH - self.button_width) // 2,
            slider_start_y + len(self.settings) * self.slider_spacing + 30,
            self.button_width,
            self.button_height
        )

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
                    break

            # Check if clicked on back button
            if self.back_button.collidepoint(event.pos):
                self._save_settings()
                self.game.current_state = self.game.MAIN_MENU

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_setting = (self.selected_setting - 1) % (len(self.settings) + 1)
            elif event.key == pygame.K_DOWN:
                self.selected_setting = (self.selected_setting + 1) % (len(self.settings) + 1)
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
                if self.selected_setting == len(self.settings):  # Back button selected
                    self._save_settings()
                    self.game.current_state = self.game.MAIN_MENU
            elif event.key == pygame.K_ESCAPE:
                self._save_settings()
                self.game.current_state = self.game.MAIN_MENU

    def _apply_settings(self):
        """Apply settings to the game configuration"""
        # Apply simulation speed
        self.config.DEFAULT_SIMULATION_SPEED = self.settings[0]["value"]
        self.game.game_screen.simulation_speed = self.settings[0]["value"]

        # Apply day duration
        self.config.DAY_DURATION = self.settings[1]["value"]

    def _save_settings(self):
        """Save settings and apply them to the game"""
        self._apply_settings()
        # Human and vampire ratios will be used next time the grid is randomized

    def update(self):
        # Mouse hover effect for back button
        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            self.selected_setting = len(self.settings)  # Select back button

    def draw(self, screen):
        # Draw title
        title_text = "Settings"
        title_surface = self.title_font.render(title_text, True, self.config.UI_TEXT_COLOR)
        title_x = (self.config.SCREEN_WIDTH - title_surface.get_width()) // 2
        title_y = 50
        screen.blit(title_surface, (title_x, title_y))

        # Draw sliders
        for i, (setting, rect) in enumerate(zip(self.settings, self.slider_rects)):
            # Draw setting name
            name_surface = self.option_font.render(setting["name"], True, self.config.UI_TEXT_COLOR)
            name_x = rect.x
            name_y = rect.y - 40
            screen.blit(name_surface, (name_x, name_y))

            # Draw slider background
            pygame.draw.rect(screen, self.config.UI_BG_COLOR, rect)
            pygame.draw.rect(screen, self.config.UI_TEXT_COLOR, rect, 1)

            # Draw slider position
            value_ratio = (setting["value"] - setting["min"]) / (setting["max"] - setting["min"])
            slider_pos = rect.x + value_ratio * rect.width
            pygame.draw.rect(screen,
                             self.config.UI_HIGHLIGHT_COLOR if i == self.selected_setting else self.config.UI_TEXT_COLOR,
                             pygame.Rect(rect.x, rect.y, slider_pos - rect.x, rect.height))

            # Draw value
            if i <= 1:  # Integer values
                value_text = str(int(setting["value"]))
            else:  # Float values
                value_text = f"{setting['value']:.2f}"

            value_surface = self.option_font.render(value_text, True, self.config.UI_TEXT_COLOR)
            value_x = rect.x + rect.width + 20
            value_y = rect.y
            screen.blit(value_surface, (value_x, value_y))

        # Draw back button
        color = self.config.UI_HIGHLIGHT_COLOR if self.selected_setting == len(
            self.settings) else self.config.UI_BG_COLOR
        pygame.draw.rect(screen, color, self.back_button)
        pygame.draw.rect(screen, self.config.UI_TEXT_COLOR, self.back_button, 2)

        back_text = "Back"
        back_surface = self.option_font.render(back_text, True, self.config.UI_TEXT_COLOR)
        back_x = self.back_button.x + (self.back_button.width - back_surface.get_width()) // 2
        back_y = self.back_button.y + (self.back_button.height - back_surface.get_height()) // 2
        screen.blit(back_surface, (back_x, back_y))

        # Draw instructions
        instructions = "Use arrow keys to navigate and adjust values"
        instructions_surface = pygame.font.SysFont("Arial", 16).render(instructions, True, (150, 150, 150))
        instructions_x = (self.config.SCREEN_WIDTH - instructions_surface.get_width()) // 2
        instructions_y = self.config.SCREEN_HEIGHT - instructions_surface.get_height() - 20
        screen.blit(instructions_surface, (instructions_x, instructions_y))