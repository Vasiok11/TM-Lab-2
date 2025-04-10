import pygame


class DayNightCycle:
    def __init__(self, config):
        self.config = config
        self.is_day = True
        self.time = 0

        # Load background images
        self.day_image = pygame.image.load("assets/day.png").convert_alpha()
        self.night_image = pygame.image.load("assets/night.png").convert_alpha()

        # Backup colors in case images fail to load
        self.day_color = (135, 206, 235)  # Light blue
        self.night_color = (25, 25, 60)  # Midnight blue

        # Sun/Moon properties
        self.sun_color = (255, 255, 0)
        self.moon_color = (200, 200, 200)
        self.celestial_radius = 30

        # Current background image
        self.current_background = self.day_image

    def update(self, dt):
        """Update time and check for day/night transitions"""
        self.time += dt

        # Check for day/night transition
        if self.time >= self.config.DAY_DURATION:
            self.time = 0
            self.is_day = not self.is_day
            return True  # Transition occurred

        return False

    def get_background_image(self):
        """Get current background image based on time of day"""
        progress = self.time / self.config.DAY_DURATION

        # Update current background based on day/night cycle progress
        if self.is_day:
            # Dawn transition (first 20% of day)
            if progress < 0.2:
                # Here we return the night image with increasing alpha for day image
                return self.night_image, self.day_image, progress / 0.2
            # Dusk transition (last 20% of day)
            elif progress > 0.8:
                # Here we return the day image with increasing alpha for night image
                return self.day_image, self.night_image, (progress - 0.8) / 0.2
            # Full day
            else:
                return self.day_image, None, 1.0
        else:
            # Night is always the night image
            return self.night_image, None, 1.0

    def get_background_color(self):
        """Legacy method for fallback support"""
        progress = self.time / self.config.DAY_DURATION

        if self.is_day:
            if progress < 0.2:
                factor = progress / 0.2
                return self._blend_colors(self.night_color, self.day_color, factor)
            elif progress > 0.8:
                factor = (progress - 0.8) / 0.2
                return self._blend_colors(self.day_color, self.night_color, factor)
            else:
                return self.day_color
        else:
            return self.night_color

    def draw_celestial_body(self, surface, width, height):
        """Draw sun or moon based on time of day"""
        progress = self.time / self.config.DAY_DURATION

        # Calculate position along arc
        angle_rad = progress * 3.14159  # Half circle (π radians)
        x = int(width / 2 - width / 2 * pygame.math.cos(angle_rad))
        y = int(height - 100 - 300 * pygame.math.sin(angle_rad))

        # Draw sun or moon
        if self.is_day:
            pygame.draw.circle(surface, self.sun_color, (x, y), self.celestial_radius)
        else:
            pygame.draw.circle(surface, self.moon_color, (x, y), self.celestial_radius)
            # Moon crater details
            if self.celestial_radius > 15:
                crater_color = (170, 170, 170)
                pygame.draw.circle(surface, crater_color, (x - 10, y - 5), 7)
                pygame.draw.circle(surface, crater_color, (x + 8, y + 10), 5)
                pygame.draw.circle(surface, crater_color, (x + 5, y - 12), 4)

    def _blend_colors(self, color1, color2, factor):
        """Blend between two colors based on factor (0-1)"""
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        return (r, g, b)

    def draw_background(self, surface, width, height):
        """Draw tiled background with the appropriate day/night image"""
        base_img, transition_img, blend_factor = self.get_background_image()

        # Calculate how many tiles we need to cover the screen
        tile_width = base_img.get_width()
        tile_height = base_img.get_height()
        cols = width // tile_width + 1
        rows = height // tile_height + 1

        # Draw base background
        for row in range(rows):
            for col in range(cols):
                x = col * tile_width
                y = row * tile_height
                surface.blit(base_img, (x, y))

        # If we're in a transition, draw the second image with appropriate alpha
        if transition_img and blend_factor > 0:
            # Create a copy of the transition image with the right alpha
            alpha_img = transition_img.copy()
            alpha_img.set_alpha(int(blend_factor * 255))

            # Draw the transition image over the base
            for row in range(rows):
                for col in range(cols):
                    x = col * tile_width
                    y = row * tile_height
                    surface.blit(alpha_img, (x, y))