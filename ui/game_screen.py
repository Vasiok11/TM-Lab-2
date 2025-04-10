import pygame
from game.grid import Grid
from game.simulation import Simulation
from game.entities import Cell, Human, Vampire
from utils.save_load import SaveLoadManager


class GameScreen:
    def __init__(self, game):
        self.game = game
        self.config = game.config

        # Initialize grid and simulation
        self.grid = Grid(self.config)
        self.grid.random_populate()
        self.simulation = Simulation(self.grid, self.config)

        # Game state
        self.paused = True
        self.simulation_speed = self.config.DEFAULT_SIMULATION_SPEED
        self.time_since_last_step = 0
        self.drawing_mode = None  # None, "human", or "vampire"

        # UI elements
        self.font = pygame.font.SysFont("Arial", 16)
        self.save_manager = SaveLoadManager(self.config)

        # Calculate grid display offset to center it
        self.grid_surface_width = self.config.GRID_WIDTH * self.config.CELL_SIZE
        self.grid_surface_height = self.config.GRID_HEIGHT * self.config.CELL_SIZE
        self.grid_x_offset = (self.config.SCREEN_WIDTH - self.grid_surface_width) // 2
        self.grid_y_offset = (self.config.SCREEN_HEIGHT - self.grid_surface_height) // 2 - 30  # Leave room for UI

        # Button areas
        self.button_height = 30
        self.button_spacing = 10
        buttons_y = self.config.SCREEN_HEIGHT - self.button_height - self.button_spacing

        self.button_areas = {
            "pause": pygame.Rect(10, buttons_y, 80, self.button_height),
            "step": pygame.Rect(100, buttons_y, 80, self.button_height),
            "reset": pygame.Rect(190, buttons_y, 80, self.button_height),
            "save": pygame.Rect(280, buttons_y, 80, self.button_height),
            "load": pygame.Rect(370, buttons_y, 80, self.button_height),
            "menu": pygame.Rect(self.config.SCREEN_WIDTH - 90, buttons_y, 80, self.button_height)
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks
            if self.button_areas["pause"].collidepoint(event.pos):
                self.paused = not self.paused
            elif self.button_areas["step"].collidepoint(event.pos):
                self.simulation.step()
            elif self.button_areas["reset"].collidepoint(event.pos):
                self.grid.random_populate()
            elif self.button_areas["save"].collidepoint(event.pos):
                self.save_manager.save_game(self.grid, self.simulation)
            elif self.button_areas["load"].collidepoint(event.pos):
                loaded = self.save_manager.load_game()
                if loaded:
                    self.grid, self.simulation = loaded
            elif self.button_areas["menu"].collidepoint(event.pos):
                self.game.current_state = self.game.MAIN_MENU
            # Handle grid cell clicking
            elif (self.grid_x_offset <= event.pos[0] <= self.grid_x_offset + self.grid_surface_width and
                  self.grid_y_offset <= event.pos[1] <= self.grid_y_offset + self.grid_surface_height):
                x = (event.pos[0] - self.grid_x_offset) // self.config.CELL_SIZE
                y = (event.pos[1] - self.grid_y_offset) // self.config.CELL_SIZE

                if event.button == 1:  # Left click
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        self.grid.set_cell(x, y, Cell.VAMPIRE)
                    else:
                        self.grid.set_cell(x, y, Cell.HUMAN)
                elif event.button == 3:  # Right click
                    self.grid.set_cell(x, y, Cell.EMPTY)

        elif event.type == pygame.MOUSEMOTION:
            # Handle drawing by dragging
            if event.buttons[0] and self.drawing_mode is not None:
                if (self.grid_x_offset <= event.pos[0] <= self.grid_x_offset + self.grid_surface_width and
                        self.grid_y_offset <= event.pos[1] <= self.grid_y_offset + self.grid_surface_height):
                    x = (event.pos[0] - self.grid_x_offset) // self.config.CELL_SIZE
                    y = (event.pos[1] - self.grid_y_offset) // self.config.CELL_SIZE
                    self.grid.set_cell(x, y, self.drawing_mode)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_RIGHT:
                self.simulation.step()
            elif event.key == pygame.K_UP:
                self.simulation_speed = min(30, self.simulation_speed + 1)
            elif event.key == pygame.K_DOWN:
                self.simulation_speed = max(1, self.simulation_speed - 1)
            elif event.key == pygame.K_h:
                self.drawing_mode = Cell.HUMAN
            elif event.key == pygame.K_v:
                self.drawing_mode = Cell.VAMPIRE
            elif event.key == pygame.K_e:
                self.drawing_mode = Cell.EMPTY
            elif event.key == pygame.K_ESCAPE:
                self.drawing_mode = None

    def update(self, dt=1 / 60):
        if not self.paused:
            self.time_since_last_step += dt
            if self.time_since_last_step >= 1.0 / self.simulation_speed:
                self.simulation.step()
                self.time_since_last_step = 0

        # Update day/night cycle regardless of pause state
        time_changed = self.simulation.update(dt)

    def draw(self, screen):
        # Draw grid background
        grid_surface = pygame.Surface((self.grid_surface_width, self.grid_surface_height))
        grid_surface.fill(self.config.BG_COLOR)

        # Draw grid lines
        for x in range(0, self.grid_surface_width, self.config.CELL_SIZE):
            pygame.draw.line(grid_surface, self.config.GRID_COLOR,
                             (x, 0), (x, self.grid_surface_height))
        for y in range(0, self.grid_surface_height, self.config.CELL_SIZE):
            pygame.draw.line(grid_surface, self.config.GRID_COLOR,
                             (0, y), (self.grid_surface_width, y))

        # Draw cells
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.cells[x][y]
                if cell.is_human():
                    color = Human.get_color(self.config, self.simulation.is_day, cell.age)
                    pygame.draw.rect(grid_surface, color,
                                     (x * self.config.CELL_SIZE + 1,
                                      y * self.config.CELL_SIZE + 1,
                                      self.config.CELL_SIZE - 1,
                                      self.config.CELL_SIZE - 1))
                elif cell.is_vampire():
                    color = Vampire.get_color(self.config, self.simulation.is_day, cell.age)
                    pygame.draw.rect(grid_surface, color,
                                     (x * self.config.CELL_SIZE + 1,
                                      y * self.config.CELL_SIZE + 1,
                                      self.config.CELL_SIZE - 1,
                                      self.config.CELL_SIZE - 1))

        # Draw grid surface to screen
        screen.blit(grid_surface, (self.grid_x_offset, self.grid_y_offset))

        # Draw day/night indicator
        day_night_text = "DAY" if self.simulation.is_day else "NIGHT"
        day_night_color = (255, 200, 100) if self.simulation.is_day else (100, 100, 200)
        day_night_surface = self.font.render(day_night_text, True, day_night_color)
        screen.blit(day_night_surface, (self.config.SCREEN_WIDTH // 2 - day_night_surface.get_width() // 2, 10))

        # Draw day/night progress bar
        progress = self.simulation.day_time / self.config.DAY_DURATION
        bar_width = 200
        bar_height = 15
        bar_x = self.config.SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 35

        pygame.draw.rect(screen, self.config.UI_BG_COLOR, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, day_night_color, (bar_x, bar_y, int(bar_width * progress), bar_height))
        pygame.draw.rect(screen, self.config.UI_TEXT_COLOR, (bar_x, bar_y, bar_width, bar_height), 1)

        # Draw population counts
        human_count = sum(1 for row in self.grid.cells for cell in row if cell.is_human())
        vampire_count = sum(1 for row in self.grid.cells for cell in row if cell.is_vampire())

        human_text = f"Humans: {human_count}"
        vampire_text = f"Vampires: {vampire_count}"

        human_surface = self.font.render(human_text, True, Human.get_color(self.config, self.simulation.is_day))
        vampire_surface = self.font.render(vampire_text, True, Vampire.get_color(self.config, self.simulation.is_day))

        screen.blit(human_surface, (20, 10))
        screen.blit(vampire_surface, (20, 35))

        # Draw buttons
        for name, rect in self.button_areas.items():
            pygame.draw.rect(screen, self.config.UI_BG_COLOR, rect)
            pygame.draw.rect(screen, self.config.UI_TEXT_COLOR, rect, 1)

            # Special case for pause button
            if name == "pause":
                text = "Resume" if self.paused else "Pause"
            else:
                text = name.capitalize()

            text_surface = self.font.render(text, True, self.config.UI_TEXT_COLOR)
            text_x = rect.x + (rect.width - text_surface.get_width()) // 2
            text_y = rect.y + (rect.height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

        # Draw simulation speed
        speed_text = f"Speed: {self.simulation_speed}x"
        speed_surface = self.font.render(speed_text, True, self.config.UI_TEXT_COLOR)
        screen.blit(speed_surface, (self.config.SCREEN_WIDTH - speed_surface.get_width() - 20, 10))

        # Draw help text
        help_text = "Left click: Place Human | Shift+Left click: Place Vampire | Right click: Erase"
        help_surface = self.font.render(help_text, True, self.config.UI_TEXT_COLOR)
        screen.blit(help_surface, (20, self.config.SCREEN_HEIGHT - 60))