import tkinter as tk
from tkinter import Canvas, messagebox
import random

CELL_SIZE = 25

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Builder & Runner")
        self.root.configure(bg="#2c3e50")
        
        self.top_panel = tk.Frame(root, bg="#34495e", pady=10)
        self.top_panel.pack(side="top", fill="x")
        
        tk.Label(self.top_panel, text="Rows:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.rows_entry = tk.Entry(self.top_panel, width=5)
        self.rows_entry.insert(0, "20")
        self.rows_entry.pack(side="left", padx=5)
        
        tk.Label(self.top_panel, text="Cols:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.cols_entry = tk.Entry(self.top_panel, width=5)
        self.cols_entry.insert(0, "20")
        self.cols_entry.pack(side="left", padx=5)

        self.sidebar = tk.Frame(root, width=150, bg="#ecf0f1", padx=10, pady=10)
        self.sidebar.pack(side="left", fill="y")
        
        self.btn_create = tk.Button(
            self.sidebar, text="Create Maze", command=self.start_generation,
            bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
            activebackground="#2ecc71", relief="flat", height=2, width=15
        )
        self.btn_create.pack(pady=10)
        
        self.btn_solve = tk.Button(
            self.sidebar, text="Find Path", command=self.start_solving,
            bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
            activebackground="#3498db", relief="flat", height=2, width=15
        )
        self.btn_solve.pack(pady=10)

        self.canvas = Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(side="right", expand=True, fill="both", padx=40, pady=40)

        self.reset_data(20, 20)

    def reset_data(self, r, c):
        self.R, self.C = r, c
        self.northWall = [[1 for _ in range(self.C + 1)] for _ in range(self.R + 1)]
        self.eastWall  = [[1 for _ in range(self.C + 1)] for _ in range(self.R + 1)]
        self.visited = [[False for _ in range(self.C + 1)] for _ in range(self.R + 1)]
        self.gen_stack = []
        self.solve_stack = []
        self.solve_visited = [[False for _ in range(self.C + 1)] for _ in range(self.R + 1)]
        self.dead_ends = set()
        self.generating = False
        self.solving = False
        self.start_row = None
        self.end_row = None
        
        self.canvas.config(width=self.C * CELL_SIZE + 200, height=self.R * CELL_SIZE + 100)

    def start_generation(self):
        try:
            r = int(self.rows_entry.get())
            c = int(self.cols_entry.get())
            if r < 2 or c < 2: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for Rows and Columns.")
            return

        self.reset_data(r, c)
        self.current_cell = (random.randint(1, self.R), random.randint(1, self.C))
        self.visited[self.current_cell[0]][self.current_cell[1]] = True
        self.generating = True
        self.run_generation()

    def run_generation(self):
        if not self.generating: return
        
        i, j = self.current_cell
        neighbors = []
        if i < self.R and not self.visited[i+1][j]: neighbors.append((i+1, j, "N"))
        if i > 1 and not self.visited[i-1][j]: neighbors.append((i-1, j, "S"))
        if j < self.C and not self.visited[i][j+1]: neighbors.append((i, j+1, "E"))
        if j > 1 and not self.visited[i][j-1]: neighbors.append((i, j-1, "W"))

        if neighbors:
            ni, nj, direction = random.choice(neighbors)
            self.gen_stack.append(self.current_cell)
            if direction == "N": self.northWall[i][j] = 0
            if direction == "S": self.northWall[i-1][j] = 0
            if direction == "E": self.eastWall[i][j] = 0
            if direction == "W": self.eastWall[i][j-1] = 0
            self.current_cell = (ni, nj)
            self.visited[ni][nj] = True
        elif self.gen_stack:
            self.current_cell = self.gen_stack.pop()
        else:
            self.generating = False
            self.start_row = random.randint(1, self.R)
            self.end_row = random.randint(1, self.R)
            self.eastWall[self.start_row][0] = 0
            self.eastWall[self.end_row][self.C] = 0
        
        self.draw()
        if self.generating:
            self.root.after(30, self.run_generation)

    def start_solving(self):
        if self.generating or not self.start_row: return
        self.solve_stack = [(self.start_row, 1)]
        self.solve_visited[self.start_row][1] = True
        self.solver_current = (self.start_row, 1)
        self.solving = True
        self.run_solver()

    def run_solver(self):
        if not self.solving: return
        if self.solver_current == (self.end_row, self.C):
            self.solving = False
            self.draw()
            return

        i, j = self.solver_current
        neighbors = []
        if i < self.R and self.northWall[i][j] == 0 and not self.solve_visited[i+1][j]: neighbors.append((i+1, j))
        if i > 1 and self.northWall[i-1][j] == 0 and not self.solve_visited[i-1][j]: neighbors.append((i-1, j))
        if j < self.C and self.eastWall[i][j] == 0 and not self.solve_visited[i][j+1]: neighbors.append((i, j+1))
        if j > 1 and self.eastWall[i][j-1] == 0 and not self.solve_visited[i][j-1]: neighbors.append((i, j-1))

        if neighbors:
            next_cell = random.choice(neighbors)
            self.solve_stack.append(next_cell)
            self.solver_current = next_cell
            self.solve_visited[next_cell[0]][next_cell[1]] = True
        else:
            self.dead_ends.add(self.solver_current)
            self.solve_stack.pop()
            if self.solve_stack:
                self.solver_current = self.solve_stack[-1]

        self.draw()
        if self.solving:
            self.root.after(60, self.run_solver)

    def draw(self):
        self.canvas.delete("all")
        offset_x = 100
        offset_y = 50
        
        for i in range(1, self.R + 1):
            for j in range(1, self.C + 1):
                x1, y1 = (j-1)*CELL_SIZE + offset_x, (self.R-i)*CELL_SIZE + offset_y
                x2, y2 = j*CELL_SIZE + offset_x, (self.R-i+1)*CELL_SIZE + offset_y
                if self.northWall[i][j]: self.canvas.create_line(x1, y1, x2, y1, fill="white", width=2)
                if self.eastWall[i][j]: self.canvas.create_line(x2, y1, x2, y2, fill="white", width=2)

        for j in range(1, self.C + 1):
            if self.northWall[0][j]:
                x1, y1 = (j-1)*CELL_SIZE + offset_x, self.R*CELL_SIZE + offset_y
                x2 = j*CELL_SIZE + offset_x
                self.canvas.create_line(x1, y1, x2, y1, fill="white", width=2)
        for i in range(1, self.R + 1):
            if self.eastWall[i][0]:
                x1, y1 = offset_x, (self.R-i)*CELL_SIZE + offset_y
                y2 = (self.R-i+1)*CELL_SIZE + offset_y
                self.canvas.create_line(x1, y1, x1, y2, fill="white", width=2)

        if self.start_row and self.end_row:
            y_s = (self.R-self.start_row)*CELL_SIZE + offset_y + (CELL_SIZE // 2)
            self.canvas.create_text(offset_x-70, y_s, text="START", fill="#27ae60", font=("Arial", 10, "bold"))
            self.canvas.create_line(offset_x-40, y_s, offset_x-5, y_s, fill="#27ae60", width=5, arrow=tk.LAST)
            
            y_e = (self.R-self.end_row)*CELL_SIZE + offset_y + (CELL_SIZE // 2)
            self.canvas.create_line(self.C*CELL_SIZE+offset_x+5, y_e, self.C*CELL_SIZE+offset_x+40, y_e, fill="#f1c40f", width=5, arrow=tk.LAST)
            self.canvas.create_text(self.C*CELL_SIZE+offset_x+75, y_e, text="EXIT", fill="#f1c40f", font=("Arial", 10, "bold"))

        for (r, c) in self.dead_ends:
            cx, cy = (c-1)*CELL_SIZE + offset_x + (CELL_SIZE//2), (self.R-r)*CELL_SIZE + offset_y + (CELL_SIZE//2)
            self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill="blue", outline="")

        if self.generating:
            r, c = self.current_cell
            cx, cy = (c-1)*CELL_SIZE + offset_x + (CELL_SIZE//2), (self.R-r)*CELL_SIZE + offset_y + (CELL_SIZE//2)
            self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="red", outline="")
        elif len(self.solve_stack) > 0:
            points = []
            for (r, c) in self.solve_stack:
                cx, cy = (c-1)*CELL_SIZE + offset_x + (CELL_SIZE//2), (self.R-r)*CELL_SIZE + offset_y + (CELL_SIZE//2)
                points.extend([cx, cy])
                self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="red", outline="")
            if len(self.solve_stack) > 1:
                self.canvas.create_line(points, fill="red", width=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()