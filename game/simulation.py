from game.entities import Cell


class Simulation:
    def __init__(self, grid, config):
        self.grid = grid
        self.config = config
        self.is_day = True
        self.day_time = 0
        self.vampire_hunger = [[0 for _ in range(grid.height)] for _ in range(grid.width)]

    def update(self, dt):
        """Update day/night cycle time"""
        self.day_time += dt
        if self.day_time >= self.config.DAY_DURATION:
            self.day_time = 0
            self.is_day = not self.is_day
            return True  # Day/night transition occurred
        return False

    def step(self):
        """Perform one step of the simulation"""
        # Get the appropriate ruleset based on time of day
        ruleset = self.config.rules["day"] if self.is_day else self.config.rules["night"]

        # Calculate next state for each cell
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self._calculate_next_state(x, y, ruleset)

        # Apply the calculated next states
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.cells[x][y]
                old_type = cell.cell_type
                cell.update()

                # Update vampire hunger if vampire survived
                if old_type == Cell.VAMPIRE and cell.cell_type == Cell.VAMPIRE:
                    self.vampire_hunger[x][y] += 1
                elif cell.cell_type == Cell.VAMPIRE and old_type != Cell.VAMPIRE:
                    # New vampire starts with no hunger
                    self.vampire_hunger[x][y] = 0
                elif cell.cell_type != Cell.VAMPIRE:
                    # Reset hunger for non-vampires
                    self.vampire_hunger[x][y] = 0

    def _calculate_next_state(self, x, y, ruleset):
        """Calculate the next state for a single cell"""
        cell = self.grid.cells[x][y]

        # Count neighbors
        human_neighbors = self.grid.count_neighbors(x, y, Cell.HUMAN)
        vampire_neighbors = self.grid.count_neighbors(x, y, Cell.VAMPIRE)
        total_neighbors = human_neighbors + vampire_neighbors

        # Empty cell rules
        if cell.is_empty():
            # Human reproduction - check for fear of vampires
            if human_neighbors == ruleset["human"]["reproduce"]:
                # Humans won't reproduce near vampires if they're afraid
                if vampire_neighbors <= ruleset["human"]["fear_threshold"]:
                    cell.set_next_state(Cell.HUMAN)
            # Vampire reproduction
            elif vampire_neighbors == ruleset["vampire"]["reproduce"]:
                cell.set_next_state(Cell.VAMPIRE)

        # Human cell rules
        elif cell.is_human():
            # Check for human defenses (safety in numbers)
            is_defended = human_neighbors >= ruleset["human"]["defense_threshold"]

            # Conversion to vampire - affected by age and group defense
            vulnerability = ruleset["human"]["base_vulnerability"]

            # Older humans are wiser and more resistant
            if cell.age > ruleset["human"]["wisdom_age"]:
                vulnerability *= ruleset["human"]["wisdom_resistance"]

            # Group defense reduces vulnerability
            if is_defended:
                vulnerability *= ruleset["human"]["group_resistance"]

            # Calculate chance of conversion based on vampire neighbors
            conversion_chance = vulnerability * vampire_neighbors

            if conversion_chance >= ruleset["human"]["convert_threshold"]:
                cell.set_next_state(Cell.VAMPIRE)
            # Check for survival based on human population dynamics
            elif (human_neighbors < ruleset["human"]["survive_min"] or
                  human_neighbors > ruleset["human"]["survive_max"]):
                cell.set_next_state(Cell.EMPTY)

        # Vampire cell rules
        elif cell.is_vampire():
            # Track vampire hunger level
            hunger = self.vampire_hunger[x][y]

            # Vampires need to feed on humans or die
            has_fed = False
            if human_neighbors > 0:
                # Vampire has fed and resets hunger
                has_fed = True
                self.vampire_hunger[x][y] = 0

                # Attempt to feed on a random adjacent human
                if ruleset["vampire"]["feeding_converts"]:
                    # This is handled by human conversion logic already
                    pass

            # Check for death in sunlight - older vampires are more resistant
            if self.is_day and ruleset["vampire"]["die_in_sunlight"]:
                sunlight_resistance = min(cell.age / ruleset["vampire"]["age_resistance"], 1)
                sunlight_death_chance = ruleset["vampire"]["sunlight_mortality"] * (1 - sunlight_resistance)

                if not has_fed and sunlight_death_chance > 0.5:  # Simplified check
                    cell.set_next_state(Cell.EMPTY)
                    return

            # Check for starvation
            if hunger >= ruleset["vampire"]["hunger_threshold"] and not has_fed:
                cell.set_next_state(Cell.EMPTY)
                return

            # Check for survival based on vampire social dynamics
            if (vampire_neighbors < ruleset["vampire"]["survive_min"] or
                    vampire_neighbors > ruleset["vampire"]["survive_max"]):
                cell.set_next_state(Cell.EMPTY)

    def get_statistics(self):
        """Get current statistics about the simulation"""
        human_count = 0
        vampire_count = 0
        empty_count = 0

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell_type = self.grid.cells[x][y].cell_type
                if cell_type == Cell.HUMAN:
                    human_count += 1
                elif cell_type == Cell.VAMPIRE:
                    vampire_count += 1
                else:
                    empty_count += 1

        return {
            "human_count": human_count,
            "vampire_count": vampire_count,
            "empty_count": empty_count,
            "is_day": self.is_day,
            "day_progress": self.day_time / self.config.DAY_DURATION
        }