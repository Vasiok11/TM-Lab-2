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
        self.last_fed = 0  # Tracks when vampire last fed

    def update(self):
        """Update cell state"""
        old_type = self.cell_type
        self.cell_type = self.next_state

        # Reset age when type changes
        if old_type != self.cell_type and self.cell_type != Cell.EMPTY:
            self.age = 0
        # Increment age for non-empty cells
        elif self.cell_type != Cell.EMPTY:
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

        # Older humans are slightly lighter (wiser)
        age_factor = min(age / 20, 1)
        lighten = int(age_factor * 30)

        # Very old humans get a slight golden tint (wise elders)
        if age > 15:
            base_color[0] += int(min((age - 15) * 5, 40))  # Add some red

        # Humans are stronger in day
        day_bonus = 20 if is_day else 0

        r = min(base_color[0] + lighten + day_bonus, 255)
        g = min(base_color[1] + lighten, 255)
        b = min(base_color[2] + lighten, 255)

        return (r, g, b)

    @staticmethod
    def is_resistant(config, age, is_day, human_neighbors):
        """Check if human is resistant to vampire conversion"""
        ruleset = config.rules["day"] if is_day else config.rules["night"]

        # Base resistance calculation
        is_wise = age >= ruleset["human"]["wisdom_age"]
        has_group_defense = human_neighbors >= ruleset["human"]["defense_threshold"]

        wisdom_factor = ruleset["human"]["wisdom_resistance"] if is_wise else 1.0
        group_factor = ruleset["human"]["group_resistance"] if has_group_defense else 1.0

        # Combined resistance factors (lower is more resistant)
        resistance = ruleset["human"]["base_vulnerability"] * wisdom_factor * group_factor

        return resistance < 0.3  # Arbitrary threshold for significant resistance


class Vampire:
    @staticmethod
    def get_color(config, is_day, age=0, hunger=0):
        """Get vampire cell color based on time, age and hunger"""
        base_color = list(config.VAMPIRE_COLOR)

        # Older vampires are slightly darker and more red
        age_factor = min(age / 20, 1)
        darken = int(age_factor * 20)

        # Hungry vampires become paler
        hunger_factor = min(hunger / 5, 1)
        hunger_pale = int(hunger_factor * 30)

        # Vampires are weaker in day
        day_penalty = 40 if is_day else 0

        r = max(base_color[0] - darken + hunger_pale, 0)
        g = max(base_color[1] - darken - hunger_pale, 0)
        b = max(base_color[2] - darken - hunger_pale, 0)

        # In daylight, vampires have a slightly bluish tint
        if is_day:
            b = min(b + 40, 255)

        # Ancient vampires (very old) get a more intense red
        if age > 25:
            r = min(r + 40, 255)

        return (r, g, b)

    @staticmethod
    def is_starving(config, hunger, is_day):
        """Check if vampire is starving"""
        ruleset = config.rules["day"] if is_day else config.rules["night"]
        return hunger >= ruleset["vampire"]["hunger_threshold"]

    @staticmethod
    def is_sunlight_resistant(config, age, is_day):
        """Check if vampire is resistant to sunlight"""
        if not is_day:
            return True

        ruleset = config.rules["day"]
        resistance = min(age / ruleset["vampire"]["age_resistance"], 0.9)  # Cap at 90%
        return resistance > 0.5  # Arbitrary threshold for significant resistance