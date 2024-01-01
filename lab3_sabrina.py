from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WIDTH = 500
HEIGHT = 500

circle_radius = 0
is_paused = False
circle_list = []
circle_speed = 0.1

def circle_points(x, y, cx, cy):
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)

    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)

    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)

    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)

def draw_circle(cx, cy, rad):
    d = 1 - rad
    x = 0
    y = rad
    circle_points(x, y, cx, cy)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1
        circle_points(x, y, cx, cy)

def initialization():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.447, 1.0, 0.973)
    glPointSize(10)
    glBegin(GL_POINTS)

    for circle in circle_list:
        cx, cy, rad = circle
        draw_circle(cx, cy, rad)

    glEnd()
    glutSwapBuffers()

def keyboard_ordinary_keys(key, x, y):
    global is_paused
    if key == b' ':
        is_paused = not is_paused
        if is_paused:
            glutIdleFunc(None)
        else:
            glutIdleFunc(animation)
    glutPostRedisplay()

def keyboard_special_keys(key, x, y):
    global circle_speed
    if key == GLUT_KEY_LEFT:
        circle_speed += 0.1
    elif key == GLUT_KEY_RIGHT:
        circle_speed = max(0.1, circle_speed - 0.1)
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global circle_list
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        opengl_x = x
        opengl_y = HEIGHT - y
        print("Mouse Clicked at:", opengl_x, opengl_y)
        circle_list.append((opengl_x, opengl_y, 30))
    glutPostRedisplay()

def animation():
    global circle_list, circle_speed
    circle_list = [(cx, cy, rad + circle_speed) for cx, cy, rad in circle_list]
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"OpenGL Circle")
glutInitWindowPosition(0, 0)
glutDisplayFunc(show_screen)
glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)
glutIdleFunc(animation)
glEnable(GL_DEPTH_TEST)
initialization()
glutMainLoop()
