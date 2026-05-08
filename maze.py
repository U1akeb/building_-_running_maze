import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

R, C = 20, 20

northWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
eastWall  = [[1 for _ in range(C + 1)] for _ in range(R + 1)]

visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]
stack = []
current_cell = (1, 1)
visited[1][1] = True

generating = True

def generate_step():
    global current_cell, generating
    i, j = current_cell
    
    neighbors = []
    if i < R and not visited[i+1][j]: neighbors.append((i+1, j, "N"))
    if i > 1 and not visited[i-1][j]: neighbors.append((i-1, j, "S"))
    if j < C and not visited[i][j+1]: neighbors.append((i, j+1, "E"))
    if j > 1 and not visited[i][j-1]: neighbors.append((i, j-1, "W"))

    if neighbors:
        ni, nj, direction = random.choice(neighbors)
        stack.append(current_cell)
        
        if direction == "N": northWall[i][j] = 0
        if direction == "S": northWall[i-1][j] = 0
        if direction == "E": eastWall[i][j] = 0
        if direction == "W": eastWall[i][j-1] = 0
        
        current_cell = (ni, nj)
        visited[ni][nj] = True
    elif stack:
        current_cell = stack.pop()
    else:
        generating = False
        entrance_row = random.randint(1, R)
        exit_row = random.randint(1, R)
        eastWall[entrance_row][0] = 0
        eastWall[exit_row][C] = 0

def draw_maze():
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    
    for i in range(1, R + 1):
        for j in range(1, C + 1):
            if northWall[i][j]:
                glVertex2f(j - 1, i) 
                glVertex2f(j, i)     
            if eastWall[i][j]:
                glVertex2f(j, i)     
                glVertex2f(j, i - 1) 

    for j in range(1, C + 1):
        if northWall[0][j]:
            glVertex2f(j - 1, 0)
            glVertex2f(j, 0)

    for i in range(1, R + 1):
        if eastWall[i][0]:
            glVertex2f(0, i)
            glVertex2f(0, i - 1)
            
    glEnd()

def draw_mouse():
    i, j = current_cell
    glColor3f(1, 0, 0)
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(j - 0.5, i - 0.5)
    glEnd()

def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(-1, C + 1, -1, R + 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if generating:
            generate_step()
            draw_mouse()

        draw_maze()
        
        pygame.display.flip()
        pygame.time.wait(20)

if __name__ == "__main__":
    main()