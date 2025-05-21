# 🧠 Memory Maze

Memory Maze is a puzzle-style memory game built with Python and Pygame. The goal is to test and improve your memory by uncovering the correct symbols hidden in a dynamically growing maze grid.

---

## 🎮 How to Play

At the start of each level, the game briefly shows you the locations of all hidden symbols in a grid-based maze. After a few seconds, the symbols disappear, and you must use your memory to select the correct cells.

- 🟩 Use the **arrow keys** to move the green selector
- ␣ Press **spacebar** to select a cell
- ✅ Correct selections permanently reveal a symbol
- ❌ Incorrect selections display a red cross and reduce your lives
- ❤️ You start each level with **three lives**

The grid size and the number of symbols increase with each level, making the game more challenging over time. If you lose all your lives, it's game over. Enjoy this unlimited levels of Maze game!

---

## 🧰 Requirements

- Python 3.7 or higher
- Pygame 2.x

---

## 📁 Project Structure
```
memory-maze/
├── main.py
├── game_manager.py
├── maze.py
├── player.py
├── ui_manager.py
├── config.py
├── assets/
│   ├── icons/
│   │   ├── redheart.png
│   │   ├── red_x.png
│   │   └── star.png
│   └── audio/ (optional)
├── README.md
└── requirements.txt
```

---

## ⚙️ Setup Instructions

1. **Clone the repository** (or download and unzip it)

   ```bash
   git clone https://github.com/your-username/memory-maze.git
   cd memory-maze
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   ```
   Activate the environment (choose one based on your OS/System):
    
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install pygame
   ```

4. Run the game
   Make sure you are inside the game folder, run
   ```bash
   python main.py
   ```





   
   
