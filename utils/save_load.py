import os
import json
import pickle
import datetime
from game.grid import Grid
from game.simulation import Simulation


class SaveLoadManager:
    def __init__(self, config):
        self.config = config

        # Create save directory if it doesn't exist
        os.makedirs(self.config.SAVE_FOLDER, exist_ok=True)

    def save_game(self, grid, simulation):
        """Save the current game state to a file"""
        try:
            # Create save data
            save_data = {
                "grid_state": grid.get_serialized_state(),
                "is_day": simulation.is_day,
                "day_time": simulation.day_time
            }

            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vampire_city_save_{timestamp}.json"
            filepath = os.path.join(self.config.SAVE_FOLDER, filename)

            # Save to file
            with open(filepath, 'w') as f:
                json.dump(save_data, f)

            print(f"Game saved as {filename}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, filename=None):
        """Load a game state from a file"""
        try:
            # If no filename specified, show latest save
            if filename is None:
                save_files = self._get_save_files()
                if not save_files:
                    print("No save files found")
                    return None

                # Use the most recent save file
                filename = save_files[-1]

            filepath = os.path.join(self.config.SAVE_FOLDER, filename)

            # Load save data
            with open(filepath, 'r') as f:
                save_data = json.load(f)

            # Create new grid and load saved state
            grid = Grid(self.config)
            grid.load_from_serialized(save_data["grid_state"])

            # Create new simulation and set state
            simulation = Simulation(grid, self.config)
            simulation.is_day = save_data["is_day"]
            simulation.day_time = save_data["day_time"]

            print(f"Game loaded from {filename}")
            return grid, simulation
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def _get_save_files(self):
        """Get a list of save files, sorted by modification time"""
        save_files = []
        try:
            for f in os.listdir(self.config.SAVE_FOLDER):
                if f.startswith("vampire_city_save_") and f.endswith(".json"):
                    save_files.append(f)

            # Sort by modification time
            save_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.config.SAVE_FOLDER, f)))
            return save_files
        except Exception:
            return []