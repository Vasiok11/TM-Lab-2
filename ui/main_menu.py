import pygame
import math
import random
from pygame import gfxdraw


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

        # Blood particles system
        self.particles = []
        self.initialize_particles(50)  # More particles for a richer atmosphere

        # Moon position and properties
        self.moon_x = self.config.SCREEN_WIDTH * 0.85
        self.moon_y = self.config.SCREEN_HEIGHT * 0.2
        self.moon_radius = 60

        # City skyline points
        self.skyline = self.generate_city_skyline()

        # Bats animation
        self.bats = []
        self.initialize_bats(15)

        # Fog effect
        self.fog_particles = []
        self.initialize_fog(100)

        # Calculate button positions - centered with better spacing
        self.button_height = 60
        self.button_width = 280
        self.button_spacing = 20
        button_x = (self.config.SCREEN_WIDTH - self.button_width) // 2
        button_start_y = self.config.SCREEN_HEIGHT * 0.5
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
            self.ambient_sound = pygame.mixer.Sound("assets/sounds/ambient.wav")
            self.has_sound = True
            # Loop ambient sound
            self.ambient_sound.play(-1)
        except:
            self.has_sound = False

        # Pulse effect for buttons
        self.pulse_timer = 0

        # Keep track of previously selected option for sound effects
        self.prev_selected = self.selected_option

        # Create color palette
        self.colors = {
            "background": (10, 2, 15),
            "moon": (240, 240, 200),
            "buildings": (20, 7, 30),
            "accent": (180, 20, 30),
            "blood": (150, 10, 20),
            "text": (220, 220, 220),
            "highlight": (220, 60, 70),
            "fog": (30, 10, 40, 5)  # With alpha
        }

    def initialize_particles(self, count):
        """Initialize blood particle system"""
        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, self.config.SCREEN_WIDTH),
                'y': random.randint(-100, self.config.SCREEN_HEIGHT),
                'size': random.randint(1, 4),
                'speed': random.uniform(0.5, 2.5),
                'opacity': random.randint(100, 220),
                'type': random.choice(['drip', 'drop'])
            })

    def initialize_bats(self, count):
        """Initialize bat animations"""
        for _ in range(count):
            self.bats.append({
                'x': random.randint(-100, self.config.SCREEN_WIDTH + 100),
                'y': random.randint(50, self.config.SCREEN_HEIGHT // 3),
                'size': random.randint(4, 10),
                'speed_x': random.uniform(0.5, 2.0) * random.choice([1, -1]),
                'speed_y': random.uniform(-0.3, 0.3),
                'wing_state': 0,
                'wing_speed': random.uniform(0.1, 0.3)
            })

    def initialize_fog(self, count):
        """Initialize fog particles"""
        for _ in range(count):
            self.fog_particles.append({
                'x': random.randint(0, self.config.SCREEN_WIDTH),
                'y': random.randint(self.config.SCREEN_HEIGHT // 2, self.config.SCREEN_HEIGHT),
                'radius': random.randint(30, 100),
                'speed': random.uniform(0.1, 0.5) * random.choice([1, -1]),
                'opacity': random.randint(5, 20)
            })

    def generate_city_skyline(self):
        """Generate points for the city skyline"""
        points = [(0, self.config.SCREEN_HEIGHT)]
        x = 0
        while x < self.config.SCREEN_WIDTH:
            building_width = random.randint(30, 100)
            building_height = random.randint(100, 250)
            y = self.config.SCREEN_HEIGHT - building_height

            # Church/castle spires occasionally
            if random.random() < 0.2:
                spire_width = building_width // 3
                points.append((x, y + building_height // 2))
                points.append((x + spire_width, y))
                points.append((x + 2 * spire_width, y + building_height // 2))

            points.append((x, y))
            points.append((x + building_width, y))
            x += building_width

        points.append((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        return points

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
            # Stop ambient sound if playing
            if self.has_sound:
                self.ambient_sound.stop()
            pygame.quit()
            quit()

    def update(self):
        self.animation_time += 1 / 60
        self.pulse_timer += 0.05

        # Fade in effect
        if not self.fade_in_complete and self.animation_time > 1.0:
            self.fade_in_complete = True

        # Update particles
        for particle in self.particles:
            particle['y'] += particle['speed']

            # Reset particle if it goes off screen
            if particle['y'] > self.config.SCREEN_HEIGHT:
                particle['y'] = random.randint(-100, -10)
                particle['x'] = random.randint(0, self.config.SCREEN_WIDTH)

        # Update bats
        for bat in self.bats:
            bat['x'] += bat['speed_x']
            bat['y'] += bat['speed_y']
            bat['wing_state'] += bat['wing_speed']

            # Wrap around screen
            if bat['x'] < -50:
                bat['x'] = self.config.SCREEN_WIDTH + 50
            elif bat['x'] > self.config.SCREEN_WIDTH + 50:
                bat['x'] = -50

            # Random y direction changes
            if random.random() < 0.01:
                bat['speed_y'] = random.uniform(-0.3, 0.3)

        # Update fog
        for fog in self.fog_particles:
            fog['x'] += fog['speed']

            # Wrap around screen
            if fog['x'] < -fog['radius'] * 2:
                fog['x'] = self.config.SCREEN_WIDTH + fog['radius']
            elif fog['x'] > self.config.SCREEN_WIDTH + fog['radius'] * 2:
                fog['x'] = -fog['radius']

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

    def draw_moon_glow(self, screen):
        """Draw the moon with a subtle glow effect"""
        # Draw outer glow
        for radius in range(80, 30, -10):
            alpha = 10 - radius // 10
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.colors["moon"][:3], alpha), (radius, radius), radius)
            screen.blit(glow_surface, (self.moon_x - radius, self.moon_y - radius))

        # Draw moon
        pygame.draw.circle(screen, self.colors["moon"], (self.moon_x, self.moon_y), self.moon_radius)

        # Draw craters
        pygame.draw.circle(screen, (200, 200, 170), (self.moon_x - 20, self.moon_y - 15), 10)
        pygame.draw.circle(screen, (210, 210, 180), (self.moon_x + 15, self.moon_y + 20), 8)
        pygame.draw.circle(screen, (195, 195, 165), (self.moon_x + 5, self.moon_y - 25), 6)

    def draw_city_silhouette(self, screen):
        """Draw the city skyline silhouette"""
        # Draw the skyline
        pygame.draw.polygon(screen, self.colors["buildings"], self.skyline)

        # Add windows to buildings
        # for x in range(10, self.config.SCREEN_WIDTH, 20):
        #     for y in range(self.config.SCREEN_HEIGHT - 250, self.config.SCREEN_HEIGHT - 50, 20):
        #         # Only draw windows inside buildings and randomly
        #         if random.random() < 0.3:
        #             point = (x, y)
        #             if self.point_in_polygon(point, self.skyline):
        #                 # Window glow effect
        #                 if random.random() < 0.7:  # 70% of windows are lit
        #                     glow_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
        #                     glow_color = (240, 220, 130, 20)  # Warm window glow
        #                     pygame.draw.rect(glow_surface, glow_color, (0, 0, 10, 10))
        #                     screen.blit(glow_surface, (x - 10, y - 10))
        #
        #                     # Window
        #                     window_color = (random.randint(30, 60), random.randint(20, 40), random.randint(10, 20))
        #                     pygame.draw.rect(screen, window_color, (x, y, 4, 6))

    def point_in_polygon(self, point, polygon):
        """Check if a point is inside a polygon"""
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def draw_bat(self, screen, bat):
        """Draw a bat with wing animation"""
        # Calculate wing position based on sine wave
        wing_angle = math.sin(bat['wing_state']) * 0.8

        # Draw bat body
        size = bat['size']
        pygame.draw.circle(screen, (10, 10, 10), (int(bat['x']), int(bat['y'])), size)

        # Draw wings based on animation state
        wing1_x = bat['x'] + size * math.cos(math.pi / 4 + wing_angle) * 2
        wing1_y = bat['y'] + size * math.sin(math.pi / 4 + wing_angle) * 2
        wing2_x = bat['x'] + size * math.cos(3 * math.pi / 4 - wing_angle) * 2
        wing2_y = bat['y'] + size * math.sin(3 * math.pi / 4 - wing_angle) * 2

        # Wing shapes
        pygame.draw.polygon(screen, (20, 20, 20), [
            (bat['x'], bat['y']),
            (wing1_x, wing1_y),
            (bat['x'] + size, bat['y'] - size)
        ])
        pygame.draw.polygon(screen, (20, 20, 20), [
            (bat['x'], bat['y']),
            (wing2_x, wing2_y),
            (bat['x'] - size, bat['y'] - size)
        ])

    def draw_particles(self, screen):
        """Draw blood particles"""
        for particle in self.particles:
            if particle['type'] == 'drip':
                # Blood drips
                start_y = particle['y'] - random.randint(10, 40)
                color = (*self.colors["blood"], particle['opacity'])

                # Use antialiased line
                gfxdraw.line(
                    screen,
                    int(particle['x']),
                    int(start_y),
                    int(particle['x']),
                    int(particle['y']),
                    color
                )

                # Blood drop
                gfxdraw.filled_circle(
                    screen,
                    int(particle['x']),
                    int(particle['y']),
                    particle['size'],
                    color
                )
            else:
                # Blood drops/spatters
                color = (*self.colors["blood"], particle['opacity'])
                gfxdraw.filled_circle(
                    screen,
                    int(particle['x']),
                    int(particle['y']),
                    particle['size'],
                    color
                )

    def draw_fog(self, screen):
        """Draw atmospheric fog"""
        for fog in self.fog_particles:
            fog_surface = pygame.Surface((fog['radius'] * 2, fog['radius'] * 2), pygame.SRCALPHA)

            # Draw fog circle with alpha
            pygame.draw.circle(
                fog_surface,
                (*self.colors["fog"][:3], fog['opacity']),
                (fog['radius'], fog['radius']),
                fog['radius']
            )

            screen.blit(fog_surface, (fog['x'] - fog['radius'], fog['y'] - fog['radius']))

    def draw(self, screen):
        # Fill with dark background
        screen.fill(self.colors["background"])

        # Draw stars
        # for _ in range(100):
        #     x = random.randint(0, self.config.SCREEN_WIDTH)
        #     y = random.randint(0, self.config.SCREEN_HEIGHT // 2)
        #     size = random.randint(1, 2)
        #     brightness = random.randint(150, 255)
        #     color = (brightness, brightness, brightness)
        #     pygame.draw.circle(screen, color, (x, y), size)

        # Draw moon with glow effect
        self.draw_moon_glow(screen)

        # Draw fog in the background
        self.draw_fog(screen)

        # Draw city silhouette
        self.draw_city_silhouette(screen)

        # Draw bats
        for bat in self.bats:
            self.draw_bat(screen, bat)

        # Draw blood particles system
        self.draw_particles(screen)

        # Apply fade-in effect
        if not self.fade_in_complete:
            alpha = min(255, int(255 * self.animation_time))
            overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - alpha)
            screen.blit(overlay, (0, 0))

        # Draw title with blood drip effect and glow
        title_text = "Vampire City"

        # Title glow effect
        title_glow = self.title_font.render(title_text, True, (80, 0, 0))
        glow_offset = math.sin(pygame.time.get_ticks() / 1000) * 3
        for i in range(3, 0, -1):
            alpha = 40 + (3 - i) * 20
            glow_surface = title_glow.copy()
            glow_surface.set_alpha(alpha)
            title_x = (self.config.SCREEN_WIDTH - title_glow.get_width()) // 2
            title_y = self.config.SCREEN_HEIGHT // 6
            screen.blit(glow_surface, (title_x - i, title_y - i + glow_offset))
            screen.blit(glow_surface, (title_x + i, title_y + i + glow_offset))

        # Main title
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        title_surface = self.title_font.render(title_text, True, self.colors["accent"])
        title_x = (self.config.SCREEN_WIDTH - title_surface.get_width()) // 2
        title_y = self.config.SCREEN_HEIGHT // 6

        # Blood drips from title
        # for i in range(5):
        #     drip_x = title_x + random.randint(0, title_surface.get_width())
        #     drip_y = title_y + title_surface.get_height()
        #     drip_length = random.randint(10, 40)
        #
        #     # Draw drip
        #     pygame.draw.line(screen, self.colors["blood"], (drip_x, drip_y), (drip_x, drip_y + drip_length), 3)
        #     pygame.draw.circle(screen, self.colors["blood"], (drip_x, drip_y + drip_length), 4)

        # Draw shadow first
        screen.blit(title_shadow, (title_x + 3, title_y + 3 + glow_offset))
        screen.blit(title_surface, (title_x, title_y + glow_offset))

        # Draw subtitle with shadow
        subtitle_text = "A Conway's Game of Life Adaptation"
        subtitle_shadow = self.menu_font.render(subtitle_text, True, (0, 0, 0))
        subtitle_surface = self.menu_font.render(subtitle_text, True, self.colors["text"])
        subtitle_x = (self.config.SCREEN_WIDTH - subtitle_surface.get_width()) // 2
        subtitle_y = title_y + title_surface.get_height() + 15
        screen.blit(subtitle_shadow, (subtitle_x + 2, subtitle_y + 2))
        screen.blit(subtitle_surface, (subtitle_x, subtitle_y))

        # Draw menu options with improved styling
        for i, (option, rect) in enumerate(zip(self.options, self.button_rects)):
            # Button glow and pulse effect when selected
            if i == self.selected_option:
                # Pulsing effect
                pulse = (math.sin(self.pulse_timer) + 1) * 0.5
                pulse_width = int(rect.width + pulse * 20)
                pulse_height = int(rect.height + pulse * 10)
                pulse_rect = pygame.Rect(
                    rect.x - (pulse_width - rect.width) // 2,
                    rect.y - (pulse_height - rect.height) // 2,
                    pulse_width,
                    pulse_height
                )

                # Draw glow
                for glow_size in range(20, 0, -5):
                    glow_alpha = 20 - glow_size
                    glow_rect = rect.inflate(glow_size, glow_size)
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    glow_color = (*self.colors["accent"][:3], glow_alpha)
                    pygame.draw.rect(glow_surface, glow_color,
                                     (0, 0, glow_rect.width, glow_rect.height),
                                     border_radius=12)
                    screen.blit(glow_surface, (glow_rect.x, glow_rect.y))

                # Active button
                button_color = (40, 5, 10)
                border_color = self.colors["accent"]
                text_color = self.colors["highlight"]
                border_width = 2
            else:
                # Inactive button with subtle gradient
                button_color = (20, 5, 15)
                border_color = (100, 20, 30)
                text_color = self.colors["text"]
                border_width = 1

            # Draw button
            pygame.draw.rect(screen, button_color, rect, border_radius=8)
            pygame.draw.rect(screen, border_color, rect, border_width, border_radius=8)

            # Button gradient overlay
            gradient_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            for y in range(rect.height):
                alpha = 10 - int(10 * y / rect.height)
                pygame.draw.line(gradient_surface, (255, 255, 255, alpha),
                                 (0, y), (rect.width, y))
            gradient_surface.set_alpha(50)
            screen.blit(gradient_surface, rect)

            # Button text with shadow
            text_shadow = self.menu_font.render(option, True, (0, 0, 0))
            option_surface = self.menu_font.render(option, True, text_color)

            # Button text positioning
            option_x = rect.x + (rect.width - option_surface.get_width()) // 2
            option_y = rect.y + (rect.height - option_surface.get_height()) // 2

            # Draw text shadow and then text
            screen.blit(text_shadow, (option_x + 2, option_y + 2))
            screen.blit(option_surface, (option_x, option_y))

        # Draw footer with improved styling
        footer_text = "Press arrow keys to navigate, Enter to select"
        footer_surface = self.footer_font.render(footer_text, True, (150, 150, 150))
        footer_x = (self.config.SCREEN_WIDTH - footer_surface.get_width()) // 2
        footer_y = self.config.SCREEN_HEIGHT - footer_surface.get_height() - 20
        screen.blit(footer_surface, (footer_x, footer_y))