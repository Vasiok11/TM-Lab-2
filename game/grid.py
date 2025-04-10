import random
from game.entities import Cell


class Grid:
    def __init__(self, config):
        self.config = config
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.cells = [[Cell(x, y) for y in range(self.height)] for x in range(self.width)]

    def reset(self):
        """Reset the grid to all empty cells"""
        for x in range(self.width):
            for y in range(self.height):
                self.cells[x][y] = Cell(x, y)

    def random_populate(self, human_ratio=0.1, vampire_ratio=0.05, forest_ratio=0.05, bunker_ratio=0.03):
        """Randomly populate the grid with humans, vampires, forests and bunkers"""
        self.reset()

        for x in range(self.width):
            for y in range(self.height):
                r = random.random()
                if r < human_ratio:
                    self.cells[x][y].cell_type = Cell.HUMAN
                    self.cells[x][y].next_state = Cell.HUMAN
                elif r < human_ratio + vampire_ratio:
                    self.cells[x][y].cell_type = Cell.VAMPIRE
                    self.cells[x][y].next_state = Cell.VAMPIRE
                elif r < human_ratio + vampire_ratio + forest_ratio:
                    self.cells[x][y].cell_type = Cell.FOREST
                    self.cells[x][y].next_state = Cell.FOREST
                elif r < human_ratio + vampire_ratio + forest_ratio + bunker_ratio:
                    self.cells[x][y].cell_type = Cell.BUNKER
                    self.cells[x][y].next_state = Cell.BUNKER

    def get_cell(self, x, y):
        """Get the cell at the specified position, handling wrap-around"""
        x = x % self.width
        y = y % self.height
        return self.cells[x][y]

    def set_cell(self, x, y, cell_type):
        """Set the cell type at the specified position"""
        x = x % self.width
        y = y % self.height
        self.cells[x][y].cell_type = cell_type
        self.cells[x][y].next_state = cell_type

    def count_neighbors(self, x, y, cell_type):
        """Count neighbors of specified type around the cell at (x, y)"""
        count = 0

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                if self.cells[nx][ny].cell_type == cell_type:
                    count += 1

        return count

    def get_neighbor_cells(self, x, y, cell_type=None):
        """Get list of neighboring cells, optionally filtered by type"""
        neighbors = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                cell = self.cells[nx][ny]

                if cell_type is None or cell.cell_type == cell_type:
                    neighbors.append(cell)

        return neighbors

    def get_serialized_state(self):
        """Convert grid to a serializable format for saving"""
        return [[cell.cell_type for cell in row] for row in self.cells]

    def load_from_serialized(self, state):
        """Load grid from a serialized state"""
        for x in range(min(len(state), self.width)):
            for y in range(min(len(state[0]), self.height)):
                self.cells[x][y].cell_type = state[x][y]
                self.cells[x][y].next_state = state[x][y]
                self.cells[x][y].age = 0  # Reset age when loading

    def get_population_stats(self):
        """Get statistics about the grid population"""
        stats = {
            "human_count": 0,
            "vampire_count": 0,
            "empty_count": 0,
            "forest_count": 0,
            "bunker_count": 0,
            "human_ages": [],
            "vampire_ages": []
        }

        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]

                if cell.is_human():
                    stats["human_count"] += 1
                    stats["human_ages"].append(cell.age)
                elif cell.is_vampire():
                    stats["vampire_count"] += 1
                    stats["vampire_ages"].append(cell.age)
                elif cell.is_forest():
                    stats["forest_count"] += 1
                elif cell.is_bunker():
                    stats["bunker_count"] += 1
                else:
                    stats["empty_count"] += 1

        # Calculate age statistics if populations exist
        if stats["human_count"] > 0:
            stats["avg_human_age"] = sum(stats["human_ages"]) / stats["human_count"]
            stats["max_human_age"] = max(stats["human_ages"]) if stats["human_ages"] else 0
        else:
            stats["avg_human_age"] = 0
            stats["max_human_age"] = 0

        if stats["vampire_count"] > 0:
            stats["avg_vampire_age"] = sum(stats["vampire_ages"]) / stats["vampire_count"]
            stats["max_vampire_age"] = max(stats["vampire_ages"]) if stats["vampire_ages"] else 0
        else:
            stats["avg_vampire_age"] = 0
            stats["max_vampire_age"] = 0

        return stats

    def add_pattern(self, pattern, x_offset, y_offset):
        """Add a predefined pattern to the grid"""
        for y, row in enumerate(pattern):
            for x, cell_value in enumerate(row):
                grid_x = (x + x_offset) % self.width
                grid_y = (y + y_offset) % self.height
                self.cells[grid_x][grid_y].cell_type = cell_value
                self.cells[grid_x][grid_y].next_state = cell_value