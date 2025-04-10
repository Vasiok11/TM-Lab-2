from game.entities import Cell


class Simulation:
    def __init__(self, grid, config):
        self.grid = grid
        self.config = config
        self.is_day = True
        self.day_time = 0

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
                self.grid.cells[x][y].update()

    def _calculate_next_state(self, x, y, ruleset):
        """Calculate the next state for a single cell"""
        cell = self.grid.cells[x][y]

        # Count neighbors
        human_neighbors = self.grid.count_neighbors(x, y, Cell.HUMAN)
        vampire_neighbors = self.grid.count_neighbors(x, y, Cell.VAMPIRE)

        # Empty cell rules
        if cell.is_empty():
            # Check for reproduction
            if human_neighbors == ruleset["human"]["reproduce"]:
                cell.set_next_state(Cell.HUMAN)
            elif vampire_neighbors == ruleset["vampire"]["reproduce"]:
                cell.set_next_state(Cell.VAMPIRE)

        # Human cell rules
        elif cell.is_human():
            # Check for conversion to vampire
            if vampire_neighbors >= ruleset["human"]["convert_threshold"]:
                cell.set_next_state(Cell.VAMPIRE)
            # Check for survival
            elif (human_neighbors < ruleset["human"]["survive_min"] or
                  human_neighbors > ruleset["human"]["survive_max"]):
                cell.set_next_state(Cell.EMPTY)

        # Vampire cell rules
        elif cell.is_vampire():
            # Check for death in sunlight
            if self.is_day and ruleset["vampire"]["die_in_sunlight"] and human_neighbors > 0:
                cell.set_next_state(Cell.EMPTY)
            # Check for survival
            elif (vampire_neighbors < ruleset["vampire"]["survive_min"] or
                  vampire_neighbors > ruleset["vampire"]["survive_max"]):
                cell.set_next_state(Cell.EMPTY)