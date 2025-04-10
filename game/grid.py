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

    def random_populate(self, human_ratio=0.1, vampire_ratio=0.05):
        """Randomly populate the grid with humans and vampires"""
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