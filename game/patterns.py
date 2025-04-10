from game.entities import Cell

"""
This module contains predefined patterns for the vampire game of life.
These patterns can be used to create interesting scenarios.
"""

# Common Conway's Game of Life patterns for humans
HUMAN_PATTERNS = {
    # Static patterns
    "block": [
        [Cell.HUMAN, Cell.HUMAN],
        [Cell.HUMAN, Cell.HUMAN]
    ],

    "beehive": [
        [0, Cell.HUMAN, Cell.HUMAN, 0],
        [Cell.HUMAN, 0, 0, Cell.HUMAN],
        [0, Cell.HUMAN, Cell.HUMAN, 0]
    ],

    # Oscillators
    "blinker": [
        [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN]
    ],

    "toad": [
        [0, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN],
        [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, 0]
    ],

    # Gliders
    "glider": [
        [0, Cell.HUMAN, 0],
        [0, 0, Cell.HUMAN],
        [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN]
    ],

    # Larger structures
    "human_village": [
        [0, Cell.HUMAN, Cell.HUMAN, 0, 0, Cell.HUMAN, Cell.HUMAN, 0],
        [Cell.HUMAN, 0, 0, Cell.HUMAN, Cell.HUMAN, 0, 0, Cell.HUMAN],
        [0, Cell.HUMAN, Cell.HUMAN, 0, 0, Cell.HUMAN, Cell.HUMAN, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [Cell.HUMAN, Cell.HUMAN, 0, 0, 0, 0, Cell.HUMAN, Cell.HUMAN],
        [Cell.HUMAN, Cell.HUMAN, 0, 0, 0, 0, Cell.HUMAN, Cell.HUMAN]
    ]
}

# Vampire patterns
VAMPIRE_PATTERNS = {
    "single": [
        [Cell.VAMPIRE]
    ],

    "pair": [
        [Cell.VAMPIRE, Cell.VAMPIRE]
    ],

    "triangle": [
        [Cell.VAMPIRE, 0],
        [Cell.VAMPIRE, Cell.VAMPIRE]
    ],

    "vampire_coven": [
        [Cell.VAMPIRE, 0, Cell.VAMPIRE],
        [0, Cell.VAMPIRE, 0],
        [Cell.VAMPIRE, 0, Cell.VAMPIRE]
    ]
}

# Forest patterns
FOREST_PATTERNS = {
    "small": [
        [Cell.FOREST, Cell.FOREST],
        [Cell.FOREST, Cell.FOREST]
    ],
    "medium": [
        [0, Cell.FOREST, 0],
        [Cell.FOREST, Cell.FOREST, Cell.FOREST],
        [0, Cell.FOREST, 0]
    ],
    "large": [
        [Cell.FOREST, Cell.FOREST, Cell.FOREST],
        [Cell.FOREST, 0, Cell.FOREST],
        [Cell.FOREST, Cell.FOREST, Cell.FOREST]
    ]
}

# Bunker patterns
BUNKER_PATTERNS = {
    "small": [
        [Cell.BUNKER]
    ],
    "medium": [
        [Cell.BUNKER, Cell.BUNKER],
        [Cell.BUNKER, Cell.BUNKER]
    ],
    "large": [
        [0, Cell.BUNKER, 0],
        [Cell.BUNKER, Cell.BUNKER, Cell.BUNKER],
        [0, Cell.BUNKER, 0]
    ]
}

# Mixed scenarios
SCENARIOS = {
    "village_raid": {
        "description": "A vampire raid on a human village",
        "patterns": [
            {"pattern": HUMAN_PATTERNS["human_village"], "x": 10, "y": 10},
            {"pattern": VAMPIRE_PATTERNS["pair"], "x": 10, "y": 5},
            {"pattern": VAMPIRE_PATTERNS["pair"], "x": 15, "y": 5}
        ]
    },

    "forest_encounter": {
        "description": "Humans near a vampire spawning forest",
        "patterns": [
            {"pattern": FOREST_PATTERNS["medium"], "x": 10, "y": 10},
            {"pattern": HUMAN_PATTERNS["block"], "x": 15, "y": 15},
            {"pattern": BUNKER_PATTERNS["small"], "x": 20, "y": 20}
        ]
    },

    "bunker_defense": {
        "description": "Humans defending a bunker from vampires",
        "patterns": [
            {"pattern": BUNKER_PATTERNS["medium"], "x": 15, "y": 15},
            {"pattern": HUMAN_PATTERNS["block"], "x": 15, "y": 14},
            {"pattern": HUMAN_PATTERNS["block"], "x": 16, "y": 16},
            {"pattern": VAMPIRE_PATTERNS["triangle"], "x": 12, "y": 12},
            {"pattern": VAMPIRE_PATTERNS["triangle"], "x": 18, "y": 12}
        ]
    },

    "surrounded": {
        "description": "A group of humans surrounded by vampires",
        "patterns": [
            {"pattern": HUMAN_PATTERNS["block"], "x": 10, "y": 10},
            {"pattern": VAMPIRE_PATTERNS["single"], "x": 8, "y": 8},
            {"pattern": VAMPIRE_PATTERNS["single"], "x": 12, "y": 8},
            {"pattern": VAMPIRE_PATTERNS["single"], "x": 8, "y": 12},
            {"pattern": VAMPIRE_PATTERNS["single"], "x": 12, "y": 12}
        ]
    },

    "vampire_attack": {
        "description": "Two vampire covens attacking human gliders",
        "patterns": [
            {"pattern": HUMAN_PATTERNS["glider"], "x": 5, "y": 5},
            {"pattern": HUMAN_PATTERNS["glider"], "x": 15, "y": 5},
            {"pattern": HUMAN_PATTERNS["glider"], "x": 25, "y": 5},
            {"pattern": VAMPIRE_PATTERNS["vampire_coven"], "x": 10, "y": 15},
            {"pattern": VAMPIRE_PATTERNS["vampire_coven"], "x": 20, "y": 15}
        ]
    },

    "sanctuary": {
        "description": "Humans in a protective formation against vampires",
        "patterns": [
            {"pattern": [
                [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN],
                [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN],
                [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN],
                [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN],
                [Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN, Cell.HUMAN]
            ], "x": 10, "y": 10},
            {"pattern": VAMPIRE_PATTERNS["triangle"], "x": 8, "y": 8},
            {"pattern": VAMPIRE_PATTERNS["triangle"], "x": 16, "y": 8},
            {"pattern": VAMPIRE_PATTERNS["triangle"], "x": 8, "y": 16},
            {"pattern": VAMPIRE_PATTERNS["triangle"], "x": 16, "y": 16}
        ]
    },

    "apocalypse": {
        "description": "Vampires everywhere with small pockets of human resistance",
        "patterns": [
            {"pattern": HUMAN_PATTERNS["beehive"], "x": 10, "y": 10},
            {"pattern": HUMAN_PATTERNS["beehive"], "x": 20, "y": 20},
            {"pattern": HUMAN_PATTERNS["beehive"], "x": 30, "y": 15},
            {"pattern": [
                [Cell.VAMPIRE, 0, Cell.VAMPIRE, 0, Cell.VAMPIRE, 0, Cell.VAMPIRE],
                [0, Cell.VAMPIRE, 0, Cell.VAMPIRE, 0, Cell.VAMPIRE, 0],
                [Cell.VAMPIRE, 0, Cell.VAMPIRE, 0, Cell.VAMPIRE, 0, Cell.VAMPIRE],
                [0, Cell.VAMPIRE, 0, Cell.VAMPIRE, 0, Cell.VAMPIRE, 0]
            ], "x": 5, "y": 5},
            {"pattern": VAMPIRE_PATTERNS["vampire_coven"], "x": 25, "y": 5},
            {"pattern": VAMPIRE_PATTERNS["vampire_coven"], "x": 15, "y": 25},
            {"pattern": VAMPIRE_PATTERNS["vampire_coven"], "x": 35, "y": 25}
        ]
    }
}


def apply_scenario(grid, scenario_name):
    """Apply a predefined scenario to the grid"""
    if scenario_name not in SCENARIOS:
        return False

    # Clear the grid first
    grid.reset()

    # Apply all patterns in the scenario
    scenario = SCENARIOS[scenario_name]
    for pattern_info in scenario["patterns"]:
        grid.add_pattern(
            pattern_info["pattern"],
            pattern_info["x"],
            pattern_info["y"]
        )

    return True


def get_scenario_names():
    """Get a list of all available scenario names"""
    return list(SCENARIOS.keys())


def get_scenario_description(scenario_name):
    """Get the description of a scenario"""
    if scenario_name in SCENARIOS:
        return SCENARIOS[scenario_name]["description"]
    return "Unknown scenario"