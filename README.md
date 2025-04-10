# 🧛 Vampire City: A Gothic Game of Life

Vampire City is a dark, atmospheric twist on Conway's Game of Life. Instead of abstract cells, the simulation features **humans and vampires** locked in a supernatural struggle for survival. Built with **Python** and **Pygame**, this haunting sandbox simulation invites players to observe, interfere, and shape an evolving world where nightfall changes everything.

---

## 🎮 Gameplay Overview

- 🧍 **Humans** try to survive and reproduce during daylight. Vulnerable at night.
- 🧛 **Vampires** prowl at night, hunting and converting humans into fellow creatures of the dark.
- 🌗 **Day-Night Cycle** dramatically changes behavior:
  - **Daytime** favors human growth.
  - **Nighttime** awakens vampires and slows human development.
- 🖱 **Interactive Tools**:
  - Place humans, vampires, or erase cells with drawing tools.
  - Use hotkeys (`H`, `V`, `E`, `C`, `Space`, `Arrow Keys`) for control.
- 🕹 **Simulation Control**:
  - Pause/resume, step forward manually, speed up/down the simulation.
- 💾 **Save & Load**:
  - Save your simulation at any time and reload it later.

---

## ✨ Features

- ⚔️ **Humans vs Vampires** mechanics
- 🌗 **Immersive day-night transition with effects**
- 💾 **Save/Load functionality**
- 🛠 **Customizable simulation settings**
- 🔊 **Optional sounds (hover, select, simulation tick)**
- 🧰 **Beautiful UI with gothic themes, glow animations, and tooltips**
- 🖼 **Asset-free fallback** (everything works without external fonts/images)

---

## 🖥 Requirements

- Python 3.8+
- Pygame (`pip install pygame`)

---

## 🚀 How to Run

```bash
python main.py
```

---

## 🧭 Controls

- `Space`: Pause/Resume simulation
- `→` / `←`: Step forward / adjust speed
- `H`, `V`, `E`: Select Human / Vampire / Eraser tools
- `C`: Clear grid
- `ESC`: Deselect tool
- `BACKSPACE`: Return to menu
- Use mouse to draw entities or click UI buttons

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
└── README.md
```

---

## 🧠 Credits & Authors

**Team:** FAF231  
Faculty of Computer Science and Microelectronics, Technical University of Moldova

- 👤 Clima Marin — FAF231  
- 👤 Pascari Vasile — FAF231  
- 👤 Andreea Gurev — FAF231  
- 👤 Andrei Bobeica — FAF231  
- 👤 Darzu Catalin — FAF231  

Supervised and inspired by a passion for systems, design, and game mechanics.

---

## 🛡 License

MIT License. Use, modify, and adapt freely.

---

Made with 💀 and Python.