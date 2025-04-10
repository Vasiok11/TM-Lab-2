import pygame


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.config = game.config

        # Load fonts
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 32)

        # Menu options
        self.options = ["New Game", "Load Game", "Settings", "Quit"]
        self.selected_option = 0

        # Calculate button positions
        self.button_height = 50
        self.button_width = 200
        self.button_spacing = 20

        button_x = (self.config.SCREEN_WIDTH - self.button_width) // 2
        button_start_y = self.config.SCREEN_HEIGHT // 2

        self.button_rects = []
        for i in range(len(self.options)):
            button_y = button_start_y + i * (self.button_height + self.button_spacing)
            self.button_rects.append(pygame.Rect(button_x, button_y, self.button_width, self.button_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    self.handle_option_selection(i)
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
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
        # Mouse hover effect
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_option = i
                break

    def draw(self, screen):
        # Draw title
        title_text = "Vampire City"
        title_surface = self.title_font.render(title_text, True, (180, 0, 0))
        title_x = (self.config.SCREEN_WIDTH - title_surface.get_width()) // 2
        title_y = self.config.SCREEN_HEIGHT // 4
        screen.blit(title_surface, (title_x, title_y))

        # Draw subtitle
        subtitle_text = "A Conway's Game of Life Adaptation"
        subtitle_surface = self.menu_font.render(subtitle_text, True, (150, 150, 150))
        subtitle_x = (self.config.SCREEN_WIDTH - subtitle_surface.get_width()) // 2
        subtitle_y = title_y + title_surface.get_height() + 10
        screen.blit(subtitle_surface, (subtitle_x, subtitle_y))

        # Draw menu options
        for i, (option, rect) in enumerate(zip(self.options, self.button_rects)):
            color = self.config.UI_HIGHLIGHT_COLOR if i == self.selected_option else self.config.UI_BG_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, self.config.UI_TEXT_COLOR, rect, 2)

            option_surface = self.menu_font.render(option, True, self.config.UI_TEXT_COLOR)
            option_x = rect.x + (rect.width - option_surface.get_width()) // 2
            option_y = rect.y + (rect.height - option_surface.get_height()) // 2
            screen.blit(option_surface, (option_x, option_y))

        # Draw footer
        footer_text = "Press arrow keys to navigate, Enter to select"
        footer_surface = pygame.font.SysFont("Arial", 16).render(footer_text, True, (150, 150, 150))
        footer_x = (self.config.SCREEN_WIDTH - footer_surface.get_width()) // 2
        footer_y = self.config.SCREEN_HEIGHT - footer_surface.get_height() - 20
        screen.blit(footer_surface, (footer_x, footer_y))