# 🧛 Vampire City: A Gothic Game of Life

Vampire City is a dark, atmospheric twist on Conway's Game of Life. Instead of abstract cells, the simulation features **humans and vampires** locked in a supernatural struggle for survival. Built with **Python** and **Pygame**, this haunting sandbox simulation invites players to observe, interact with, and shape an evolving world where nightfall transforms destiny.

---

## 🎮 Gameplay Overview

- **Humans:** Struggle to survive and reproduce during the day. They flourish in light but are vulnerable at night.
- **Vampires:** Emerge with the night, hunting humans and converting them into creatures of the dark.
- **Dynamic Day-Night Cycle:** 
  - **Daytime:** Accelerates human growth and resource management.
  - **Nighttime:** Awakens vampires and alters strategic gameplay.
- **Interactive Tools:** 
  - Place humans, vampires, forests, bunkers, or erase cells using intuitive drawing tools.
  - Quick tool selection with hotkeys (`H`, `V`, `F`, `B`, `E`) and mouse inputs.
- **Simulation Control:** 
  - Pause/resume simulation with `Space`.
  - Step forward manually, or adjust simulation speed with arrow keys.
- **Audio Immersion:** 
  - Enjoy atmospheric background music that responds to the day/night cycle.
  - Toggle music and sound effects on/off via a dedicated UI button.
- **Save & Load:** 
  - Save your simulation at any moment and reload it later to resume your gothic saga.

---

## ✨ Features

- ⚔️ **Humans vs Vampires Mechanics:** See how different populations interact and evolve.
- 🌗 **Immersive Day-Night Transitions:** Visual and auditory effects that heighten the gothic mood.
- 💾 **Robust Save/Load System:** Persist your progress and revisit your dark experiments.
- 🛠 **Customizable Simulation Settings:** Fine-tune parameters like simulation speed, population ratios, audio volumes, and more.
- 🔊 **Dynamic Audio Controls:** Seamlessly control background music and sound effects.
- 🧰 **Rich, Gothic UI:** Ethereal visuals with glow animations, tooltips, and asset-free fallbacks ensure the game remains striking even without external resources.

---

## 🖥 Requirements

- **Python 3.8+**
- **Pygame**  
  Install with:  
  ```bash
  pip install pygame
  ```

---

## 🚀 How to Run

Clone the repository and run the main script from your terminal:

```bash
python main.py
```

Ensure the working directory includes the following structure:

```
VampireCity/
├── main.py
├── ui/
│   ├── game_screen.py
│   ├── main_menu.py
│   └── settings_menu.py
├── game/
│   ├── grid.py
│   ├── simulation.py
│   └── entities.py
├── utils/
│   └── save_load.py
├── assets/ (optional)
│   ├── fonts/
│   ├── images/
│   └── sounds/
└── README
```

---

## 🧭 Controls

- **Simulation:**  
  `Space` — Pause/Resume | `→`/`←` — Step/Adjust Speed  
- **Tool Selection:**  
  `H` — Human | `V` — Vampire | `F` — Forest | `B` — Bunker | `E` — Eraser  
- **Navigation:**  
  `Up/Down Arrow Keys` — Navigate UI | `BACKSPACE` — Return to Menu  
- **Mouse:**  
  Click and drag for drawing entities; interact with UI buttons for various functions (including audio toggling).

---

## 📁 Project Structure

```
VampireCity/
├── main.py
├── ui/
│   ├── game_screen.py
│   ├── main_menu.py
│   └── settings_menu.py
├── game/
│   ├── grid.py
│   ├── simulation.py
│   └── entities.py
├── utils/
│   └── save_load.py
├── assets/ (optional)
│   ├── fonts/
│   ├── images/
│   └── sounds/
└── README
```

---

## 🧠 Credits & Authors

**Team:** FAF231  
Faculty of Computer Science and Microelectronics, Technical University of Moldova

- **Clima Marin** — FAF231  
- **Pascari Vasile** — FAF231  
- **Andreea Gurev** — FAF231  
- **Andrei Bobeica** — FAF231  
- **Darzu Catalin** — FAF231  

Supervised by a shared passion for innovative systems, dark design, and experimental gameplay.

---

## 🛡 License

Distributed under the MIT License. Feel free to use, modify, and share.

---

Made with Python and a touch of nocturnal creativity.