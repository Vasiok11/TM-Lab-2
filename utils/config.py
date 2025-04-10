class Config:
    def __init__(self):
        # Display settings
        self.SCREEN_WIDTH = 1400
        self.SCREEN_HEIGHT = 800
        self.FPS = 60

        # Colors
        self.BG_COLOR = (25, 25, 35)  # Dark blue-ish background
        self.GRID_COLOR = (50, 50, 60)
        self.HUMAN_COLOR = (65, 105, 225)  # Royal blue for humans
        self.VAMPIRE_COLOR = (139, 0, 0)  # Dark red for vampires
        self.FOREST_COLOR = (34, 139, 34)  # Forest green
        self.BUNKER_COLOR = (139, 137, 137)  # Gray bunker color
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

        # Audio Configuration
        self.MUSIC_VOLUME = 0.5  # Range: 0.0 to 1.0
        self.SOUND_EFFECTS_VOLUME = 0.7  # Range: 0.0 to 1.0

        # Music file paths (using .wav as you mentioned)
        self.MENU_MUSIC = "assets/menu.wav"
        self.GAME_MUSIC_DAY = "assets/game.wav"
        self.GAME_MUSIC_NIGHT = "assets/game.wav"

        self.SOUND_FX = {
            "button_click": "assets/pop.wav",
        }

        # Enhanced simulation rules
        self.rules = {
            "day": {
                "human": {
                    "survive_min": 2,  # Min neighbors to survive
                    "survive_max": 3,  # Max neighbors to survive
                    "reproduce": 3,  # Neighbors needed to reproduce
                    "convert_threshold": 1.0,  # Threshold for vampire conversion (probability-based)
                    "fear_threshold": 1,  # Max vampires nearby for reproduction to occur
                    "defense_threshold": 3,  # Min humans for group defense
                    "group_resistance": 0.5,  # Conversion resistance multiplier in groups
                    "wisdom_age": 10,  # Age at which humans gain wisdom
                    "wisdom_resistance": 0.7,  # Conversion resistance for wise humans
                    "base_vulnerability": 0.4  # Base conversion chance per vampire
                },
                "vampire": {
                    "survive_min": 1,  # Min neighbors to survive
                    "survive_max": 3,  # Max neighbors to survive
                    "reproduce": 3,  # Neighbors needed to reproduce
                    "die_in_sunlight": True,  # Vampires vulnerable during day
                    "sunlight_mortality": 0.8,  # Base chance of dying in sunlight
                    "age_resistance": 30,  # Age divisor for sunlight resistance
                    "hunger_threshold": 3,  # Steps before starving
                    "feeding_converts": True  # Whether feeding converts humans
                }
            },
            "night": {
                "human": {
                    "survive_min": 2,  # Min neighbors to survive
                    "survive_max": 4,  # Max neighbors to survive
                    "reproduce": 3,  # Neighbors needed to reproduce
                    "convert_threshold": 0.6,  # Easier to be converted at night
                    "fear_threshold": 0,  # Terrified of vampires at night
                    "defense_threshold": 4,  # Need more humans for group defense at night
                    "group_resistance": 0.7,  # Group resistance at night
                    "wisdom_age": 8,  # Age at which humans gain wisdom
                    "wisdom_resistance": 0.6,  # Conversion resistance for wise humans
                    "base_vulnerability": 0.6  # Higher base vulnerability at night
                },
                "vampire": {
                    "survive_min": 1,  # Easier to survive at night
                    "survive_max": 4,  # Can have larger groups at night
                    "reproduce": 2,  # Easier to reproduce at night
                    "die_in_sunlight": False,  # No sunlight at night
                    "sunlight_mortality": 0.0,  # No sun, no mortality
                    "age_resistance": 15,  # Age divisor for resistance
                    "hunger_threshold": 5,  # Can go longer without feeding at night
                    "feeding_converts": True  # Whether feeding converts humans
                }
            }
        }

        # Save/load
        self.SAVE_FOLDER = "saves/"