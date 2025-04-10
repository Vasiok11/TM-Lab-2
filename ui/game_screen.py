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
        self.drawing_mode = None
        self.hover_pos = None

        # UI elements
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.save_manager = SaveLoadManager(self.config)

        # Calculate grid display offset
        self.grid_surface_width = self.config.GRID_WIDTH * self.config.CELL_SIZE
        self.grid_surface_height = self.config.GRID_HEIGHT * self.config.CELL_SIZE
        self.grid_x_offset = (self.config.SCREEN_WIDTH - self.grid_surface_width) // 2
        self.grid_y_offset = (self.config.SCREEN_HEIGHT - self.grid_surface_height) // 2 - 50

        # Initialize UI components
        self._init_buttons()
        self._init_colors()

    def _init_colors(self):
        self.ui_colors = {
            "bg": pygame.Color("#2E1A1A"),
            "button": pygame.Color("#5A2E2E"),
            "button_hover": pygame.Color("#8C4A4A"),
            "text": pygame.Color("#E7D6C4"),
            "border": pygame.Color("#3A2323"),
            "sun": pygame.Color("#FFD700"),
            "moon": pygame.Color("#A0A0A0"),
            "forest": self.config.FOREST_COLOR,
            "bunker": self.config.BUNKER_COLOR
        }

    def _init_buttons(self):
        button_width = 100
        self.button_height = 40
        buttons_y = self.config.SCREEN_HEIGHT - self.button_height - 20

        self.button_areas = {
            "pause": pygame.Rect(20, buttons_y, button_width, self.button_height),
            "step": pygame.Rect(130, buttons_y, button_width, self.button_height),
            "reset": pygame.Rect(240, buttons_y, button_width, self.button_height),
            "save": pygame.Rect(350, buttons_y, button_width, self.button_height),
            "load": pygame.Rect(460, buttons_y, button_width, self.button_height),
            "forest": pygame.Rect(570, buttons_y, button_width, self.button_height),
            "bunker": pygame.Rect(680, buttons_y, button_width, self.button_height),
            "menu": pygame.Rect(self.config.SCREEN_WIDTH - 120, buttons_y, button_width, self.button_height)
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
            elif self.button_areas["forest"].collidepoint(event.pos):
                self.drawing_mode = Cell.FOREST
            elif self.button_areas["bunker"].collidepoint(event.pos):
                self.drawing_mode = Cell.BUNKER
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
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.grid.set_cell(x, y, Cell.FOREST)
                    elif pygame.key.get_mods() & pygame.KMOD_ALT:
                        self.grid.set_cell(x, y, Cell.BUNKER)
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
            elif event.key == pygame.K_f:
                self.drawing_mode = Cell.FOREST
            elif event.key == pygame.K_b:
                self.drawing_mode = Cell.BUNKER
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
        # Draw background
        screen.fill(self.ui_colors["bg"])

        # Draw grid
        self._draw_grid(screen)

        # Draw HUD elements
        self._draw_day_night_indicator(screen)
        self._draw_population_counts(screen)
        self._draw_simulation_speed(screen)
        self._draw_buttons(screen)
        self._draw_tool_indicator(screen)

    def _draw_grid(self, screen):
        grid_surface = pygame.Surface((self.grid_surface_width, self.grid_surface_height), pygame.SRCALPHA)
        # Draw subtle grid pattern
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                rect = pygame.Rect(
                    x * self.config.CELL_SIZE,
                    y * self.config.CELL_SIZE,
                    self.config.CELL_SIZE,
                    self.config.CELL_SIZE
                )
                if (x + y) % 2 == 0:
                    pygame.draw.rect(grid_surface, (*self.config.BG_COLOR, 50), rect)
        # Draw cells with depth effect
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.cells[x][y]
                if not cell.is_empty():
                    rect = pygame.Rect(
                        x * self.config.CELL_SIZE + 2,
                        y * self.config.CELL_SIZE + 2,
                        self.config.CELL_SIZE - 4,
                        self.config.CELL_SIZE - 4
                    )
                    if cell.is_human():
                        base_color = Human.get_color(self.config, self.simulation.is_day, cell.age)
                    elif cell.is_vampire():
                        base_color = Vampire.get_color(self.config, self.simulation.is_day, cell.age)
                    elif cell.is_forest():
                        base_color = self.config.FOREST_COLOR
                    elif cell.is_bunker():
                        base_color = self.config.BUNKER_COLOR

                    # Cell shading
                    pygame.draw.rect(grid_surface, base_color, rect, border_radius=2)
                    pygame.draw.rect(grid_surface, (255, 255, 255, 30), rect.inflate(-2, -2), border_radius=2)
                    pygame.draw.rect(grid_surface, (0, 0, 0, 30), rect.inflate(-4, -4), border_radius=2)
        # Draw grid lines
        for x in range(0, self.grid_surface_width, self.config.CELL_SIZE):
            pygame.draw.line(grid_surface, (*self.config.GRID_COLOR, 100), (x, 0), (x, self.grid_surface_height))
        for y in range(0, self.grid_surface_height, self.config.CELL_SIZE):
            pygame.draw.line(grid_surface, (*self.config.GRID_COLOR, 100), (0, y), (self.grid_surface_width, y))
        screen.blit(grid_surface, (self.grid_x_offset, self.grid_y_offset))
        # Draw hover effect
        if self.hover_pos and (
                self.grid_x_offset <= self.hover_pos[0] <= self.grid_x_offset + self.grid_surface_width and
                self.grid_y_offset <= self.hover_pos[1] <= self.grid_y_offset + self.grid_surface_height):
            x = (self.hover_pos[0] - self.grid_x_offset) // self.config.CELL_SIZE
            y = (self.hover_pos[1] - self.grid_y_offset) // self.config.CELL_SIZE
            rect = pygame.Rect(
                self.grid_x_offset + x * self.config.CELL_SIZE,
                self.grid_y_offset + y * self.config.CELL_SIZE,
                self.config.CELL_SIZE,
                self.config.CELL_SIZE
            )
            pygame.draw.rect(screen, (255, 255, 255, 50), rect, 2)

    def _draw_day_night_indicator(self, screen):
        # Draw sun/moon icon
        icon_size = 32
        center = (self.config.SCREEN_WIDTH // 2 - 40 + icon_size // 2, 10 + icon_size // 2)
        if self.simulation.is_day:
            pygame.draw.circle(screen, self.ui_colors["sun"], center, icon_size // 2)
        else:
            pygame.draw.circle(screen, self.ui_colors["moon"], center, icon_size // 2)
            # Add crescent shape
            pygame.draw.circle(screen, self.ui_colors["bg"], (center[0] - 5, center[1]), icon_size // 2 - 3)

        # Gradient progress bar
        progress = self.simulation.day_time / self.config.DAY_DURATION
        bar_width = 250
        bar_height = 20
        bar_x = self.config.SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 50
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)

        # Ensure the background color is a valid RGBA tuple
        bg_color = self.ui_colors["button"]
        if isinstance(bg_color, pygame.Color):
            bg_color = (bg_color.r, bg_color.g, bg_color.b, 150)  # Convert to RGBA
        else:
            bg_color = (*bg_color, 150)  # Append alpha value

        # Draw unfilled bar background
        pygame.draw.rect(screen, bg_color, bar_rect)  # Background
        pygame.draw.rect(screen, self.ui_colors["border"], bar_rect, 2)  # Border

        # Draw filled portion based on progress
        filled_width = int(bar_width * progress)
        filled_rect = pygame.Rect(bar_x, bar_y, filled_width, bar_height)
        for x in range(filled_width):
            color = self.ui_colors["sun"] if self.simulation.is_day else self.ui_colors["moon"]
            alpha = int(255 * (x / filled_width if self.simulation.is_day else 1 - x / filled_width))
            line_color = (*color[:3], alpha)
            pygame.draw.line(screen, line_color, (bar_rect.x + x, bar_rect.y),
                             (bar_rect.x + x, bar_rect.y + bar_height))

    def _draw_population_counts(self, screen):
        stats = self.grid.get_population_stats()
        # Human counter
        self._draw_counter(screen, 20, 20, Human.get_color(self.config, self.simulation.is_day), stats["human_count"])
        # Vampire counter
        self._draw_counter(screen, 20, 80, Vampire.get_color(self.config, self.simulation.is_day),
                           stats["vampire_count"])
        # Forest counter
        self._draw_counter(screen, 20, 140, self.config.FOREST_COLOR, stats["forest_count"])
        # Bunker counter
        self._draw_counter(screen, 20, 200, self.config.BUNKER_COLOR, stats["bunker_count"])

    def _draw_counter(self, screen, x, y, color, count):
        bg_rect = pygame.Rect(x - 10, y - 10, 160, 50)
        pygame.draw.rect(screen, self.ui_colors["button"], bg_rect, border_radius=8)
        pygame.draw.rect(screen, color, bg_rect, 2, border_radius=8)

        # Draw icon
        pygame.draw.circle(screen, color, (x + 20, y + 20), 12)
        text = self.font.render(f"{count}", True, color)
        screen.blit(text, (x + 50, y + 8))

    def _draw_buttons(self, screen):
        for name, rect in self.button_areas.items():
            # Check if hover position is valid
            if self.hover_pos is not None and rect.collidepoint(self.hover_pos):
                color = self.ui_colors["button_hover"]
            else:
                color = self.ui_colors["button"]

            # Draw button background
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, self.ui_colors["border"], rect, 2, border_radius=6)

            # Draw button text
            text = "▶ Resume" if name == "pause" and self.paused else "⏸ Pause" if name == "pause" else f"{name.capitalize()}"
            text_surface = self.font.render(text, True, self.ui_colors["text"])
            screen.blit(text_surface, (
                rect.x + (rect.width - text_surface.get_width()) // 2,
                rect.y + (rect.height - text_surface.get_height()) // 2
            ))

    def _draw_tool_indicator(self, screen):
        if self.drawing_mode:
            icon_rect = pygame.Rect(self.config.SCREEN_WIDTH - 60, 20, 32, 32)
            color = {
                Cell.HUMAN: Human.get_color(self.config, self.simulation.is_day),
                Cell.VAMPIRE: Vampire.get_color(self.config, self.simulation.is_day),
                Cell.FOREST: self.config.FOREST_COLOR,
                Cell.BUNKER: self.config.BUNKER_COLOR,
                Cell.EMPTY: (200, 200, 200)
            }[self.drawing_mode]

            pygame.draw.rect(screen, color, icon_rect, border_radius=4)
            pygame.draw.rect(screen, self.ui_colors["border"], icon_rect.inflate(4, 4), 2, border_radius=6)

    def _draw_simulation_speed(self, screen):
        speed_text = f"Speed: {self.simulation_speed}x"
        text_surface = self.font.render(speed_text, True, self.ui_colors["text"])
        screen.blit(text_surface, (self.config.SCREEN_WIDTH - text_surface.get_width() - 30, 20))