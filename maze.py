import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

R, C = 20, 20

northWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
eastWall  = [[1 for _ in range(C + 1)] for _ in range(R + 1)]

visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]
gen_stack = []
current_cell = (random.randint(1, R), random.randint(1, C))
visited[current_cell[0]][current_cell[1]] = True
generating = True

solve_visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]
solve_stack = []
dead_ends = set()
solver_current = None
solving = False
start_cell = None
end_cell = None

def generate_step():
    global current_cell, generating, solver_current, solving, start_cell, end_cell
    i, j = current_cell
    
    neighbors = []
    if i < R and not visited[i+1][j]: neighbors.append((i+1, j, "N"))
    if i > 1 and not visited[i-1][j]: neighbors.append((i-1, j, "S"))
    if j < C and not visited[i][j+1]: neighbors.append((i, j+1, "E"))
    if j > 1 and not visited[i][j-1]: neighbors.append((i, j-1, "W"))

    if neighbors:
        ni, nj, direction = random.choice(neighbors)
        gen_stack.append(current_cell)
        if direction == "N": northWall[i][j] = 0
        if direction == "S": northWall[i-1][j] = 0
        if direction == "E": eastWall[i][j] = 0
        if direction == "W": eastWall[i][j-1] = 0
        current_cell = (ni, nj)
        visited[ni][nj] = True
    elif gen_stack:
        current_cell = gen_stack.pop()
    else:
        generating = False
        start_row = random.randint(1, R)
        end_row = random.randint(1, R)
        eastWall[start_row][0] = 0
        eastWall[end_row][C] = 0
        start_cell = (start_row, 1)
        end_cell = (end_row, C)
        solver_current = start_cell
        solve_stack.append(start_cell)
        solve_visited[start_row][1] = True
        solving = True

def solve_step():
    global solver_current, solving
    if solver_current == end_cell:
        solving = False
        return

    i, j = solver_current
    neighbors = []
    if i < R and northWall[i][j] == 0 and not solve_visited[i+1][j]: neighbors.append((i+1, j))
    if i > 1 and northWall[i-1][j] == 0 and not solve_visited[i-1][j]: neighbors.append((i-1, j))
    if j < C and eastWall[i][j] == 0 and not solve_visited[i][j+1]: neighbors.append((i, j+1))
    if j > 1 and eastWall[i][j-1] == 0 and not solve_visited[i][j-1]: neighbors.append((i, j-1))

    if neighbors:
        next_cell = random.choice(neighbors)
        solve_stack.append(next_cell)
        solver_current = next_cell
        solve_visited[next_cell[0]][next_cell[1]] = True
    else:
        dead_ends.add(solver_current)
        solve_stack.pop()
        if solve_stack:
            solver_current = solve_stack[-1]

def draw_maze():
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(1, R + 1):
        for j in range(1, C + 1):
            if northWall[i][j]:
                glVertex2f(j - 1, i); glVertex2f(j, i)
            if eastWall[i][j]:
                glVertex2f(j, i); glVertex2f(j, i - 1)
    for j in range(1, C + 1):
        if northWall[0][j]: glVertex2f(j - 1, 0); glVertex2f(j, 0)
    for i in range(1, R + 1):
        if eastWall[i][0]: glVertex2f(0, i); glVertex2f(0, i - 1)
    glEnd()

def draw_entities():
    glPointSize(8)
    glBegin(GL_POINTS)
    
    glColor3f(0, 0, 1)
    for cell in dead_ends:
        glVertex2f(cell[1] - 0.5, cell[0] - 0.5)
    
    glColor3f(1, 0, 0)
    if generating:
        glVertex2f(current_cell[1] - 0.5, current_cell[0] - 0.5)
    else:
        for cell in solve_stack:
            glVertex2f(cell[1] - 0.5, cell[0] - 0.5)
            
    glEnd()

def main():
    pygame.init()
    pygame.display.set_mode((800, 800), DOUBLEBUF | OPENGL)
    gluOrtho2D(-1, C + 1, -1, R + 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return

        glClear(GL_COLOR_BUFFER_BIT)
        
        if generating:
            generate_step()
        elif solving:
            solve_step()

        draw_maze()
        draw_entities()
        
        pygame.display.flip()
        pygame.time.wait(20)

if __name__ == "__main__":
    main()