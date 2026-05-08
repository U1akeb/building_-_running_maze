🧩 Maze Builder & Runner
A Python GUI application that generates mazes based in the given Rown and Column inputs from the user and visually solves them step-by-step using a depth-first search backtracking algorithm.
it is built with Tkinter, this project demonstrates maze generation, pathfinding and real-time visualization.

🚀 Features
   - Random maze generation (recursive backtracking algorithm)
   - Animated pathfinding solver
   - Interactive GUI using Tkinter
   - Customizable maze size (rows & columns)
   - Real-time visualization of generation and solving process
   - Start and Exit markers
   - Dead-end tracking visualization

1,  Maze Generation

The maze is created using a depth-first search (DFS) backtracking algorithm
  - it Start from a random cell and randomly explore unvisited neighbors
  - Remove walls between connected cells
  - Backtrack when stuck until full maze is generated

2, Maze Solving

The solver Starts from the entry point
  - Moves through open paths
  - Uses backtracking when hitting dead ends
  - Visually shows the solution process step-by-step

3, Sidebar
   -  Create Maze
Generates a new random maze
   -  Find Path
Solves the generated maze visually


🧩 Technologies Used
   - Python
   - Tkinter (GUI)
   - Random module (maze generation logic)
     
📸 Preview
   Creating Maze
<img width="1062" height="736" alt="image" src="https://github.com/user-attachments/assets/349637a4-2d64-4460-862d-c2bb4d02b02a" />

   Finding Path
<img width="1062" height="736" alt="image" src="https://github.com/user-attachments/assets/a6912df9-467e-42f0-a1bb-5788e94c0f9e" />


 
 📁 Project Structure

building_running_manze
│
│-maze.py
│
└── README.md



maze.py

is the main program file with all the logic and programs


---



README.md

the explanation for the project

I can help you next with:

* 🎥 Adding a **GIF demo to README**
* 🧠 Adding **A* shortest path solver**
* 🧩 Turning it into a **game with player movement**
* 🌐 Packaging it for **PyPI or executable (.exe)**

Just tell me 👍
