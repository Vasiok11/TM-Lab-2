import pygame
import math  # Import the math module for trigonometric functions

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.config = game.config
        # Load fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/vampire.ttf", 74)
            self.menu_font = pygame.font.Font("assets/fonts/gothic.ttf", 32)
            self.footer_font = pygame.font.Font("assets/fonts/gothic.ttf", 16)
        except:
            # Fallback to system fonts if custom fonts not available
            self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
            self.menu_font = pygame.font.SysFont("Arial", 32)
            self.footer_font = pygame.font.SysFont("Arial", 16)
        # Menu options
        self.options = ["New Game", "Load Game", "Settings", "Quit"]
        self.selected_option = 0
        # Blood drip animation
        self.blood_drips = []
        for _ in range(5):
            self.blood_drips.append({
                'x': pygame.time.get_ticks() % self.config.SCREEN_WIDTH,
                'y': -20,
                'speed': pygame.time.get_ticks() % 3 + 1,
                'length': pygame.time.get_ticks() % 50 + 20
            })
        # Background gradient
        self.bg_gradient = self._create_background()
        # Load background image if available
        try:
            self.bg_image = pygame.image.load("assets/images/vampire_bg.png").convert_alpha()
            self.bg_image = pygame.transform.scale(self.bg_image,
                                                   (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            self.has_bg_image = True
        except:
            self.has_bg_image = False
        # Calculate button positions
        self.button_height = 60
        self.button_width = 250
        self.button_spacing = 25
        button_x = (self.config.SCREEN_WIDTH - self.button_width) // 2
        button_start_y = self.config.SCREEN_HEIGHT // 2
        self.button_rects = []
        for i in range(len(self.options)):
            button_y = button_start_y + i * (self.button_height + self.button_spacing)
            self.button_rects.append(pygame.Rect(button_x, button_y, self.button_width, self.button_height))
        # Animation state
        self.animation_time = 0
        self.fade_in_complete = False
        # Sound effects
        try:
            self.hover_sound = pygame.mixer.Sound("assets/sounds/hover.wav")
            self.select_sound = pygame.mixer.Sound("assets/sounds/select.wav")
            self.has_sound = True
        except:
            self.has_sound = False
        # Keep track of previously selected option for sound effects
        self.prev_selected = self.selected_option

    def _create_background(self):
        """Create a dark gradient background"""
        bg = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        for y in range(self.config.SCREEN_HEIGHT):
            # Calculate gradient color (darker at top, lighter at bottom)
            color_value = int(25 * (y / self.config.SCREEN_HEIGHT))
            color = (max(0, 30 - color_value), 0, max(0, 20 - color_value))
            pygame.draw.line(bg, color, (0, y), (self.config.SCREEN_WIDTH, y))
        return bg

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    if self.has_sound:
                        self.select_sound.play()
                    self.handle_option_selection(i)
                    break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                if self.has_sound and self.prev_selected != self.selected_option:
                    self.hover_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                if self.has_sound and self.prev_selected != self.selected_option:
                    self.hover_sound.play()
            elif event.key == pygame.K_RETURN:
                if self.has_sound:
                    self.select_sound.play()
                self.handle_option_selection(self.selected_option)

    def handle_option_selection(self, index):
        if index == 0:  # New Game
            self.game.current_state = self.game.GAME_SCREEN
            self.game.game_screen.grid.random_populate()
            self.game.game_screen.paused = True
        elif index == 1:  # Load Game
            loaded = self.game.game_screen.save_manager.load_game()
            if loaded:
                self.game.game_screen.grid, self.game.game_screen.simulation = loaded
                self.game.current_state = self.game.GAME_SCREEN
        elif index == 2:  # Settings
            self.game.current_state = self.game.SETTINGS
        elif index == 3:  # Quit
            pygame.quit()
            quit()

    def update(self):
        self.animation_time += 1 / 60
        # Fade in effect
        if not self.fade_in_complete and self.animation_time > 1.0:
            self.fade_in_complete = True
        # Update blood drips
        for drip in self.blood_drips:
            drip['y'] += drip['speed']
            if drip['y'] > self.config.SCREEN_HEIGHT:
                drip['y'] = -20
                drip['x'] = pygame.time.get_ticks() % self.config.SCREEN_WIDTH
                drip['speed'] = pygame.time.get_ticks() % 3 + 1
                drip['length'] = pygame.time.get_ticks() % 50 + 20
        # Mouse hover effect
        mouse_pos = pygame.mouse.get_pos()
        self.prev_selected = self.selected_option
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                if self.selected_option != i:
                    self.selected_option = i
                    if self.has_sound:
                        self.hover_sound.play()
                break

    def draw(self, screen):
        # Draw background
        if self.has_bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.blit(self.bg_gradient, (0, 0))
        # Draw atmospheric blood drips
        for drip in self.blood_drips:
            pygame.draw.line(
                screen,
                (150, 0, 0),
                (drip['x'], drip['y']),
                (drip['x'], drip['y'] - drip['length']),
                3
            )
            # Blood drop at the end
            pygame.draw.circle(screen, (150, 0, 0), (drip['x'], drip['y']), 5)
        # Apply fade-in effect
        if not self.fade_in_complete:
            alpha = min(255, int(255 * self.animation_time))
            overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - alpha)
            screen.blit(overlay, (0, 0))
        # Draw title with shadow effect
        title_text = "Vampire City"
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        title_surface = self.title_font.render(title_text, True, (180, 0, 0))
        # Slight movement to title for eerie effect
        offset_y = 3 * math.sin(pygame.time.get_ticks() / 1000)  # Replaced pygame.math.sin with math.sin
        title_x = (self.config.SCREEN_WIDTH - title_surface.get_width()) // 2
        title_y = self.config.SCREEN_HEIGHT // 5
        # Draw shadow first
        screen.blit(shadow_surface, (title_x + 3, title_y + 3 + offset_y))
        screen.blit(title_surface, (title_x, title_y + offset_y))
        # Draw subtitle with shadow
        subtitle_text = "A Conway's Game of Life Adaptation"
        subtitle_shadow = self.menu_font.render(subtitle_text, True, (0, 0, 0))
        subtitle_surface = self.menu_font.render(subtitle_text, True, (150, 150, 150))
        subtitle_x = (self.config.SCREEN_WIDTH - subtitle_surface.get_width()) // 2
        subtitle_y = title_y + title_surface.get_height() + 10
        screen.blit(subtitle_shadow, (subtitle_x + 2, subtitle_y + 2))
        screen.blit(subtitle_surface, (subtitle_x, subtitle_y))
        # Draw menu options
        for i, (option, rect) in enumerate(zip(self.options, self.button_rects)):
            # Button glow effect when selected
            if i == self.selected_option:
                glow_rect = rect.inflate(10, 10)
                glow_strength = (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.5  # Replaced pygame.math.sin with math.sin
                glow_color = (
                    int(100 * glow_strength),
                    0,
                    0
                )
                pygame.draw.rect(screen, glow_color, glow_rect, border_radius=10)
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
            option_surface = self.menu_font.render(option, True, text_color)
            option_x = rect.x + (rect.width - option_surface.get_width()) // 2
            option_y = rect.y + (rect.height - option_surface.get_height()) // 2
            screen.blit(option_surface, (option_x, option_y))
        # Draw footer
        footer_text = "Press arrow keys to navigate, Enter to select"
        footer_surface = self.footer_font.render(footer_text, True, (120, 120, 120))
        footer_x = (self.config.SCREEN_WIDTH - footer_surface.get_width()) // 2
        footer_y = self.config.SCREEN_HEIGHT - footer_surface.get_height() - 20
        screen.blit(footer_surface, (footer_x, footer_y))