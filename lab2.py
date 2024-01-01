from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


class AABB:
    def __init__(self, x1, x2, y1, y2):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2

    def collides_with(self, other):
        # print(f'Self: ({self.x1}, {self.x2}, {self.y1}, {self.y2})')
        # print(f'Other: ({other.x1}, {other.x2}, {other.y1}, {other.y2})')

        return ((self.x1 < other.x2 < self.x2) or (self.x1 < other.x1 < self.x2)) and (self.y1 < other.y2 < self.y2)


def MidPointLine(zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d_init = (2 * dy) - dx
    e = 2 * dy
    ne = 2 * (dy - dx)

    x = x1
    y = y1

    while x <= x2:
        cx, cy = convert_to_original_zone(zone, x, y)
        glPointSize(2)
        glBegin(GL_POINTS)
        glVertex2f(cx, cy)

        glEnd()

        if d_init <= 0:
            x += 1
            d_init += e
        else:
            x += 1
            y += 1
            d_init += ne


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx > 0:
            if dy > 0:
                return 0
            else:
                return 7
        else:
            if dy > 0:
                return 3
            else:
                return 4
    else:
        if dx > 0:
            if dy > 0:
                return 1
            else:
                return 6
        else:
            if dy > 0:
                return 2
            else:
                return 5


def convert_to_original_zone(orginal, x, y):
    if orginal == 0:
        return x, y
    if orginal == 1:
        return y, x
    if orginal == 2:
        return -y, -x
    if orginal == 3:
        return -x, y
    if orginal == 4:
        return -x, -y
    if orginal == 5:
        return -y, -x
    if orginal == 6:
        return y, -x
    if orginal == 7:
        return x, -y


def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:
        return x, -y


def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    one_x, one_y = convert_to_zone0(x1, y1, zone)
    two_x, two_y = convert_to_zone0(x2, y2, zone)

    MidPointLine(zone, one_x, one_y, two_x, two_y)


# ____________________initialize__________________

box_x = 150
box_y = 50
di_x = 150
di_y = 150
box_speed = 10
di_speed = 0.1
chosen_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

# AABB func
box1 = AABB(box_x - 30, box_x + 40, box_y - 49, box_y - 39)
box2 = AABB(di_x - 7, di_x + 7, di_y + 7, di_y - 7)
collision = False
over = False
score = 0
lower_color = (1.0, 1.0, 1.0)
restart_button_pressed = False
play = True


# ... end .....

# ................. drawing ...........

def lower_box():
    global box_x, box_y, collision, box1, box2
    global di_y, score
    count = 1
    glColor3f(*lower_color)

    draw_line(box_x - 20, box_y - 49, box_x + 30, box_y - 49)
    draw_line(box_x - 30, box_y - 39, box_x + 40, box_y - 39)  # upper

    draw_line(box_x - 30, box_y - 39, box_x - 20, box_y - 49)
    draw_line(box_x + 40, box_y - 39, box_x + 30, box_y - 49)


def diamond_box():
    global di_x, di_y

    glColor3f(*chosen_color)

    draw_line(di_x - 7, di_y, di_x, di_y + 7)
    draw_line(di_x, di_y + 7, di_x + 7, di_y)
    draw_line(di_x + 7, di_y, di_x, di_y - 7)
    draw_line(di_x - 7, di_y, di_x, di_y - 7)


def restart_game():
    global score, di_speed, di_x, di_y, chosen_color, lower_color, restart_button_pressed
    score = 0
    di_speed = 0.1
    di_x = random.randint(20, 500)
    di_y = 550
    chosen_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    lower_color = (1.0, 1.0, 1.0)
    restart_button_pressed = False
    print("Starting Over")


def restart_button():
    glColor3f(0.0, 0.5, 0.5)

    draw_line(10, 560, 30, 590)
    draw_line(10, 560, 60, 560)
    draw_line(10, 560, 30, 530)


def exit_button():
    glColor3f(1.0, 0.0, 0.0)

    draw_line(440, 540, 490, 580)
    draw_line(440, 580, 490, 540)


def play_button():
    glColor3f(1.0, 0.65, 0)

    if play:
        draw_line(240, 580, 240, 540)
        draw_line(270, 580, 270, 540)
    else:
        draw_line(220, 580, 220, 540)
        draw_line(220, 580, 270, 560)
        draw_line(220, 540, 270, 560)


# ................end.............

# ......... mouse and keyboard control.............


def mouse_event(button, state, x, y):
    global restart_button_pressed, play, score, over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and 10 < x < 60 and 7 < y < 71:
        # restart_button()
        restart_button_pressed = True
        over = False
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and 220 < x < 270 and 10 < y < 70:
        play = not play
        # print(play)

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and 440 < x < 490 and 20 < y < 60:
        print("Goodbye! Your final score is:", score)
        glutLeaveMainLoop()
    # print(x," ",y,"\n")


def keyboard_special_keys(key, _, __):
    # check against special keys here (e.g. F1..F11, arrow keys, etc.)
    # use GLUT_KEY_* constants while comparing (e.g. GLUT_KEY_F1, GLUT_KEY_LEFT, etc.)
    global box_x, box_y

    if key == GLUT_KEY_LEFT and box_x > 30:
        box_x -= box_speed
    elif key == GLUT_KEY_RIGHT and box_x < 460:
        box_x += box_speed

    glutPostRedisplay()


# ...............end.............


def iterate():
    glViewport(0, 0, 500, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def change_x():
    global di_x, di_y, box2

    # Randomize the initial horizontal position within a range
    di_x = random.randint(20, 500)
    di_y = 550

    global chosen_color
    chosen_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))


def animate():
    # //codes for any changes in Models, Camera
    global restart_button_pressed, play, over
    global restart_button_pressed
    if not over and play:
        check_collision()
        if restart_button_pressed:
            restart_game()

        global di_x, di_y, di_speed, score
        if di_y <= 0:
            change_x()

        di_y = (di_y - di_speed)

    global box2, box1

    box1 = AABB(box_x - 30, box_x + 40, box_y - 49, box_y - 39)

    box2 = AABB(di_x - 7, di_x + 7, di_y + 7, di_y - 7)

    glutPostRedisplay()


def check_collision():
    global box1, box2, collision, score, box_y, di_y, lower_color, di_x, di_speed, over, play

    if box1.collides_with(box2):
        collision = True
        score += 1
        di_x = random.randint(20, 500)
        di_y = 550
        global chosen_color
        chosen_color = (random.uniform(0.3, 1), random.uniform(0.3, 1), random.uniform(0.3, 1))
        box2 = AABB(di_x - 7, di_x + 7, 550 + 7, 550 - 7)

        if score != 0 and score % 2 == 0:
            di_speed += 0.1

        print("Score :", score)
        # collision = False
    else:
        collision = False

        if di_y < box_y - 39:  # If diamond is lower than the lower box without collision
            lower_color = (1, 0, 0)  # Change lower box color to red
            if not over:
                print("Game Over! Score : ", score, "\n")
                print("Click 'Restart' button twice to start again\n")
                score = 0
                over = True

        else:
            over = False
            lower_color = (1, 1, 1)


# print(collision, "\n")


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(1.0, 1.0, 1.0)

    if not over:
        diamond_box()
    lower_box()
    restart_button()
    play_button()
    exit_button()

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)

# Size of the window.
# Manipulating this value will let us change the size of the output widow where the pixel is shown.
glutInitWindowSize(500, 600)

glutInitWindowPosition(0, 0)

# window name
wind = glutCreateWindow(b"LAB02: CATCH THE DIAMOND")

glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_event)
# glutKeyboardFunc(keyboard_regular_keys)
glEnable(GL_DEPTH_TEST)
glutMainLoop()