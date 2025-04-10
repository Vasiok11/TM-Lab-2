class Cell:
    EMPTY = 0
    HUMAN = 1
    VAMPIRE = 2

    def __init__(self, x, y, cell_type=EMPTY):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.next_state = cell_type
        self.age = 0

    def update(self):
        self.cell_type = self.next_state
        if self.cell_type != Cell.EMPTY:
            self.age += 1
        else:
            self.age = 0

    def set_next_state(self, state):
        self.next_state = state

    def is_human(self):
        return self.cell_type == Cell.HUMAN

    def is_vampire(self):
        return self.cell_type == Cell.VAMPIRE

    def is_empty(self):
        return self.cell_type == Cell.EMPTY


class Human:
    @staticmethod
    def get_color(config, is_day, age=0):
        """Get human cell color based on time and age"""
        base_color = list(config.HUMAN_COLOR)

        # Older humans are slightly lighter
        age_factor = min(age / 20, 1)
        lighten = int(age_factor * 30)

        # Humans are stronger in day
        day_bonus = 20 if is_day else 0

        r = min(base_color[0] + lighten + day_bonus, 255)
        g = min(base_color[1] + lighten, 255)
        b = min(base_color[2] + lighten, 255)

        return (r, g, b)


class Vampire:
    @staticmethod
    def get_color(config, is_day, age=0):
        """Get vampire cell color based on time and age"""
        base_color = list(config.VAMPIRE_COLOR)

        # Older vampires are slightly darker
        age_factor = min(age / 20, 1)
        darken = int(age_factor * 20)

        # Vampires are weaker in day
        day_penalty = 40 if is_day else 0

        r = max(base_color[0] - darken, 0)
        g = max(base_color[1] - darken, 0)
        b = max(base_color[2] - darken, 0)

        # In daylight, vampires have a slightly bluish tint
        if is_day:
            b = min(b + 40, 255)

        return (r, g, b)