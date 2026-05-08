import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


R, C = 10, 10


northWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
eastWall  = [[1 for _ in range(C + 1)] for _ in range(R + 1)]

def draw_grid():
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    
    
    for i in range(1, R + 1):
        for j in range(1, C + 1):
            if northWall[i][j]:
               
                glVertex2f(j - 1, i) 
                glVertex2f(j, i)     
            if eastWall[i][j]:
                # Draw the right side of the cell (East Wall) [cite: 11]
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


def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


    gluOrtho2D(-1, C + 1, -1, R + 1)

    while True:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

     
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

       
        draw_grid()

     
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()