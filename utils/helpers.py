import random
from game.entities import Cell


def create_random_cluster(entity_type, size_range=(3, 7)):
    """Create a random cluster of entities of the specified type"""
    # Determine cluster size
    width = random.randint(*size_range)
    height = random.randint(*size_range)

    # Create empty cluster
    cluster = [[0 for _ in range(width)] for _ in range(height)]

    # Fill with random entities, with higher density in the center
    center_x, center_y = width // 2, height // 2
    max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5

    for y in range(height):
        for x in range(width):
            # Calculate distance from center (normalized to 0-1)
            dx, dy = x - center_x, y - center_y
            distance = ((dx ** 2 + dy ** 2) ** 0.5) / max_distance

            # Higher probability of entity near center
            probability = 0.9 - 0.8 * distance

            if random.random() < probability:
                cluster[y][x] = entity_type

    return cluster


def calculate_population_balance(grid):
    """Calculate the balance between human and vampire populations"""
    stats = grid.get_population_stats()

    total_population = stats["human_count"] + stats["vampire_count"]
    if total_population == 0:
        return 0.5  # Neutral if no population

    # Balance ranges from 0.0 (all vampires) to 1.0 (all humans)
    balance = stats["human_count"] / total_population

    return balance


def get_dominant_species(grid):
    """Get the dominant species in the grid, or None if balanced"""
    balance = calculate_population_balance(grid)

    if balance > 0.7:
        return Cell.HUMAN
    elif balance < 0.3:
        return Cell.VAMPIRE
    else:
        return None  # Balanced


def create_balancing_event(grid, simulation):
    """Create a random event to help balance the simulation"""
    dominant = get_dominant_species(grid)

    if dominant is None:
        return False  # No need to balance

    # If humans dominate, add vampire clusters
    if dominant == Cell.HUMAN:
        # Add 1-3 vampire clusters in random locations
        num_clusters = random.randint(1, 3)
        for _ in range(num_clusters):
            cluster = create_random_cluster(Cell.VAMPIRE, (2, 5))
            x = random.randint(0, grid.width - len(cluster[0]))
            y = random.randint(0, grid.height - len(cluster))
            grid.add_pattern(cluster, x, y)
        return True

    # If vampires dominate, add human sanctuaries
    elif dominant == Cell.VAMPIRE:
        # Add 1-2 larger human clusters
        num_clusters = random.randint(1, 2)
        for _ in range(num_clusters):
            cluster = create_random_cluster(Cell.HUMAN, (4, 8))
            x = random.randint(0, grid.width - len(cluster[0]))
            y = random.randint(0, grid.height - len(cluster))
            grid.add_pattern(cluster, x, y)
        return True

    return False


def is_extinct(grid, cell_type):
    """Check if a species is extinct"""
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.cells[x][y].cell_type == cell_type:
                return False
    return True


def is_stagnant(grid, previous_state, threshold=0.98):
    """Check if the simulation is stagnant (not changing much)"""
    if previous_state is None:
        return False

    same_count = 0
    total_count = grid.width * grid.height

    for x in range(grid.width):
        for y in range(grid.height):
            if x < len(previous_state) and y < len(previous_state[0]):
                if grid.cells[x][y].cell_type == previous_state[x][y]:
                    same_count += 1

    return same_count / total_count >= threshold


def introduce_mutation(grid, simulation, is_day):
    """Introduce a random mutation to keep things interesting"""
    # Get appropriate ruleset
    ruleset = simulation.config.rules["day"] if is_day else simulation.config.rules["night"]

    # Choose what to mutate
    mutation_type = random.choice([
        "vampire_cluster",
        "human_sanctuary",
        "vampire_evolution",
        "human_adaptation"
    ])

    if mutation_type == "vampire_cluster":
        # Create a small cluster of vampires with special properties
        cluster = create_random_cluster(Cell.VAMPIRE, (2, 4))
        x = random.randint(0, grid.width - len(cluster[0]))
        y = random.randint(0, grid.height - len(cluster))
        grid.add_pattern(cluster, x, y)

        # Make these vampires older (more resistant)
        for dx in range(len(cluster[0])):
            for dy in range(len(cluster)):
                if cluster[dy][dx] == Cell.VAMPIRE:
                    cell_x, cell_y = (x + dx) % grid.width, (y + dy) % grid.height
                    grid.cells[cell_x][cell_y].age = random.randint(15, 25)

    elif mutation_type == "human_sanctuary":
        # Create a cluster of humans with special properties
        cluster = create_random_cluster(Cell.HUMAN, (3, 6))
        x = random.randint(0, grid.width - len(cluster[0]))
        y = random.randint(0, grid.height - len(cluster))
        grid.add_pattern(cluster, x, y)

        # Make these humans older (wiser)
        for dx in range(len(cluster[0])):
            for dy in range(len(cluster)):
                if cluster[dy][dx] == Cell.HUMAN:
                    cell_x, cell_y = (x + dx) % grid.width, (y + dy) % grid.height
                    grid.cells[cell_x][cell_y].age = random.randint(8, 15)

    elif mutation_type == "vampire_evolution":
        # Find a group of vampires and make them more resistant
        vampire_cells = []
        for x in range(grid.width):
            for y in range(grid.height):
                if grid.cells[x][y].is_vampire():
                    vampire_cells.append((x, y))

        if vampire_cells:
            # Select a random subset to evolve
            subset_size = min(len(vampire_cells) // 4, 10)
            if subset_size > 0:
                evolved_vampires = random.sample(vampire_cells, subset_size)
                for x, y in evolved_vampires:
                    grid.cells[x][y].age += random.randint(5, 10)

    elif mutation_type == "human_adaptation":
        # Find a group of humans and make them wiser
        human_cells = []
        for x in range(grid.width):
            for y in range(grid.height):
                if grid.cells[x][y].is_human():
                    human_cells.append((x, y))

        if human_cells:
            # Select a random subset to evolve
            subset_size = min(len(human_cells) // 4, 15)
            if subset_size > 0:
                evolved_humans = random.sample(human_cells, subset_size)
                for x, y in evolved_humans:
                    grid.cells[x][y].age += random.randint(3, 8)

    return mutation_type