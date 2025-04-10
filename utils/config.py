class Config:
    def __init__(self):
        # Display settings
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60

        # Colors
        self.BG_COLOR = (25, 25, 35)  # Dark blue-ish background
        self.GRID_COLOR = (50, 50, 60)
        self.HUMAN_COLOR = (65, 105, 225)  # Royal blue for humans
        self.VAMPIRE_COLOR = (139, 0, 0)  # Dark red for vampires
        self.UI_BG_COLOR = (15, 15, 25)
        self.UI_TEXT_COLOR = (230, 230, 230)
        self.UI_HIGHLIGHT_COLOR = (100, 0, 0)

        # Grid settings
        self.GRID_WIDTH = 100
        self.GRID_HEIGHT = 80
        self.CELL_SIZE = 8

        # Game settings
        self.DEFAULT_SIMULATION_SPEED = 5  # Updates per second
        self.DAY_DURATION = 10  # Seconds per day/night cycle

        # Simulation rules
        self.rules = {
            "day": {
                "human": {
                    "survive_min": 2,  # Min neighbors to survive
                    "survive_max": 3,  # Max neighbors to survive
                    "reproduce": 3,  # Neighbors needed to reproduce
                    "convert_threshold": 2  # Vampire neighbors to be converted
                },
                "vampire": {
                    "survive_min": 2,  # Min neighbors to survive
                    "survive_max": 3,  # Max neighbors to survive
                    "reproduce": 3,  # Neighbors needed to reproduce
                    "die_in_sunlight": True  # Vampires vulnerable during day
                }
            },
            "night": {
                "human": {
                    "survive_min": 3,  # Harder to survive at night
                    "survive_max": 4,
                    "reproduce": 4,  # Harder to reproduce at night
                    "convert_threshold": 1  # Easier to be converted at night
                },
                "vampire": {
                    "survive_min": 1,  # Easier to survive at night
                    "survive_max": 4,
                    "reproduce": 2,  # Easier to reproduce at night
                    "die_in_sunlight": False  # No sunlight at night
                }
            }
        }

        # Save/load
        self.SAVE_FOLDER = "saves/"