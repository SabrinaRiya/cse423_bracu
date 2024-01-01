
#task1


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


def draw_points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
   
    glEnd()

def draw_points1(x, y):
   
    glPointSize(2)

    glBegin(GL_POINTS)
    coordinate_points = 50
    for i in range(coordinate_points):
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
       
        glVertex2f(x, y)

   
    glVertex2f(x, y)

    glEnd()

def draw_lines():
    glBegin(GL_LINES)

#outer structure

    glVertex2f(100, 200)
    glVertex2f(500, 200)

 
   
    glVertex2f(100, 200)
    glVertex2f(100, 500)

    glVertex2f(500, 200)
    glVertex2f(500, 500)
   
    glVertex2f(100, 500)
    glVertex2f(500, 500)
   
    #door
   
    glVertex2f(200, 200)
    glVertex2f(200, 300)
   
    glVertex2f(200, 200)
    glVertex2f(300, 200)
   
    glVertex2f(300, 200)
    glVertex2f(300, 300)
   
    glVertex2f(200, 300)
    glVertex2f(300, 300)
   
    #window
    glVertex2f(320, 380)
    glVertex2f(400, 380)
   
    glVertex2f(320, 380)
    glVertex2f(320, 440)
   
    glVertex2f(400, 380)
    glVertex2f(400, 440)
   
    glVertex2f(320, 440)
    glVertex2f(400, 440)
   
   


    glEnd()
   

def drawTriangle():
    glBegin(GL_TRIANGLES)
    # The points have to be in anticlockwise order.
    glColor3f(0.0, 8.0, 3.0)
    glVertex2f(100, 500)
    glVertex2f(500, 500)
    glVertex2f(290, 770)
    glEnd()
   


def iterate():
    glViewport(0, 0, 700, 900)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 700, 0.0, 900, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0)
 
    draw_points(290, 240)
    draw_points1(400,850)
   
    draw_lines()
   

    drawTriangle()
   
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(250, 0)
wind = glutCreateWindow(b"Task1:Lab01")
glutDisplayFunc(showScreen)

glutMainLoop()

#task2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


def draw_points():
   
    glPointSize(5)
    glBegin(GL_POINTS)

    coordinate_points = 100
    for i in range(coordinate_points):
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
       
        glVertex2f(x, y)

    glEnd()


def iterate():
    glViewport(0, 0, 700, 900)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 700, 0.0, 900, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

 
    glColor3f(1.0, 1.0, 1.0)


    draw_points()

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)


glutInitWindowSize(500, 500)

glutInitWindowPosition(0, 0)

# window name
wind = glutCreateWindow(b"task2_Lab1")

glutDisplayFunc(showScreen)

glutMainLoop()


 

 




