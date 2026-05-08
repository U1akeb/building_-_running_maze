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

   Path found
<img width="1062" height="736" alt="image" src="https://github.com/user-attachments/assets/d84d13ee-8d22-44b5-afca-0066daae5ad9" />



 
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


Video demo
https://www.loom.com/share/5092475e6991432a8bd508a886a63609
