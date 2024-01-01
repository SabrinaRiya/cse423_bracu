import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 1800, 1000
centerX, centerY = W_Width / 2, W_Height / 2
mapClick = False
mapSelect = 0
pause = False
towerSelectMenuClick = False
towerCreate = []
towerList1 = []
towerlist1 = []
towerList2 = []
towerlist2 = []
gameLost = False
gameStart = False
map1Path = [
    (780, 0), (780, 350), (600, 400), (600, 690), (680, 730), (920, 730), (920, 770), (920, 840), (1200, 840),
    (1240, 780), (1240, 640), (1300, 600), (1400, 600), (W_Width + 100, 600)
]
map2Path = [
    (850, 0), (850, 280), (870, 320), (1100, 320), (1100, 530), (1000, 550), 
    (600, 550), (550, 600), (550, 730), (600, 820), (840, 820), (880, 850), 
    (860, 950), (880, 980), (1100, 980), (1150, 900), (1150, 750), (1200, 700), 
    (W_Width + 100, 700)
]
map3_1Path = [
    (-40, 350), (300, 350), (800, 300), (900, 400), (940, 450), (940, 500), (920, 550), 
    (680, 600), (700, 725), (850, 800), (1400, 720), (W_Width + 100, 720)
]
map3_2Path = [
    (-40, 350), (300, 350), (800, 300), (900, 400), (940, 450), (940, 500), (920, 550), 
    (680, 600), (630, 775), (715, 950), (1100, 960), (W_Width + 100, 960)
]
wave_1, wave_2, wave_3 = [], [], []
wave1_time, wave2_time, wave3_time = 0, time.time() + 30, time.time() + 60
dinosaur_spawn_time = time.time() + 5
coin = 200

#===================================================================================================================#
#=================================================Algorithms Start==================================================#
#===================================================================================================================#
# Line Drawing Algorithm

def draw_line(x1, y1, x2, y2, color):
    zone = findZone(x1, x2, y1, y2)
    x1, y1 = convertZone(x1, y1, zone)
    x2, y2 = convertZone(x2, y2, zone)
    glBegin(GL_POINTS)
    midpointLine(x1, x2, y1, y2, zone, color)
    glEnd()

def midpointLine(x1, x2, y1, y2, zone, color):
    dx = x2 - x1
    dy = y2 - y1
    d = (2*dy) - dx
    ne = 2*(dy - dx)
    e = 2*dy
    x, y = x1, y1
    while (x <= x2):
        cx, cy = originalZone(x, y, zone)
        glColor3f(color[0], color[1], color[2])
        glVertex2f(cx, cy)
        x += 1
        if d > 0:
            y += 1
            d += ne
        else:
            d += e

def findZone(x1, x2, y1, y2):
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy > 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy < 0:
            return 7
    else:
        if dx >= 0 and dy > 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy < 0:
            return 6

def convertZone(X, Y, zone):
    x, y = X, Y
    if zone == 1:
        x, y = Y, X
    elif zone == 2:
        x, y = Y, -X
    elif zone == 3:
        x, y = -X, Y
    elif zone == 4:
        x, y = -X, -Y
    elif zone == 5:
        x, y = -Y, -X
    elif zone == 6:
        x, y = -Y, X
    elif zone == 7:
        x, y = X, -Y
    
    return x, y

def originalZone(X, Y, zone):
    x, y = X, Y
    if zone == 1:
        x, y = Y, X
    elif zone == 2:
        x, y = -Y, X
    elif zone == 3:
        x, y = -X, Y
    elif zone == 4:
        x, y = -X, -Y
    elif zone == 5:
        x, y = -Y, -X
    elif zone == 6:
        x, y = Y, -X
    elif zone == 7:
        x, y = X, -Y
    
    return x, y

# Circle Drawing Algorithm

def midpointCircle(xc, yc, r, color, size):
    x, y = 0, r
    d = 1 - r
    drawCircle(xc, yc, x, y, color, size)
    while (y > x):
        if d < 0:
            d += 2*x + 3
        else:
            d += 2*(x - y) + 5
            y -= 1
        x += 1
        drawCircle(xc, yc, x, y, color, size)

def drawCircle(xc, yc, x, y, color, size):
    glColor3f(color[0], color[1], color[2])
    glPointSize(size)
    glBegin(GL_POINTS)

    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)

    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)

    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)

    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)

    glEnd()

#===================================================================================================================#
#=================================================Algorithms End====================================================#
#===================================================================================================================#

#===================================================================================================================#
#==================================================Models Start=====================================================#
#===================================================================================================================#
# House Model

def houseModel1(x, y):
    draw_line(x, y + 30, x + 10, y + 30, [0.55, 0.1, 0])
    draw_line(x - 5, y + 30, x - 5, y + 40, [0.55, 0.1, 0])
    draw_line(x + 15, y + 30, x + 15, y + 40, [0.55, 0.1, 0])
    draw_line(x - 5, y + 40, x + 15, y + 40, [0.55, 0.1, 0])
    draw_line(x - 5, y + 40, x + 5, y + 50, [0.55, 0.1, 0])
    draw_line(x + 15, y + 40, x + 5, y + 50, [0.55, 0.1, 0])
    draw_line(x + 5, y + 50, x + 5, y + 30, [0.55, 0.1, 0])
    midpointCircle(x + 5, y + 50, 2, [0.55, 0.1, 0], 2)

def houseModel2(x, y):
    draw_line(x + 5, y + 5, x - 5, y - 5, [0.55, 0.1, 0])
    draw_line(x + 5, y + 5, x + 15, y - 5, [0.55, 0.1, 0])
    draw_line(x + 5, y + 5, x + 30, y + 5, [0.55, 0.1, 0])
    draw_line(x + 30, y + 5, x + 40, y - 5, [0.55, 0.1, 0])
    draw_line(x - 5, y - 5, x + 40, y - 5, [0.55, 0.1, 0])
    draw_line(x - 1, y - 5, x - 1, y - 20, [0.55, 0.1, 0])
    draw_line(x + 10, y - 5, x + 10, y - 20, [0.55, 0.1, 0])
    draw_line(x + 35, y - 5, x + 35, y - 20, [0.55, 0.1, 0])
    draw_line(x - 1, y - 20, x + 35, y - 20, [0.55, 0.1, 0])
    glPointSize(5)
    draw_line(x + 22, y - 10, x + 22, y - 18, [0.55, 0.1, 0])
    glPointSize(5)

# Tree Model

def treeModel1(x, y):
    leaf_color = [0, 0.5, 0]
    draw_line(x, y, x, y + 30, [0.55, 0.1, 0])
    draw_line(x + 10, y, x + 10, y + 30, [0.55, 0.1, 0])
    midpointCircle(x + 5, y + 30, 5, leaf_color, 2)
    draw_line(x - 15, y + 30, x + 25, y + 30, leaf_color)
    draw_line(x + 5, y + 45, x + 5, y + 25, leaf_color)
    draw_line(x - 10, y + 40, x + 15, y + 25, leaf_color)
    draw_line(x + 20, y + 40, x - 5, y + 25, leaf_color)

# Pond Model

def pondModel1(x, y):
    midpointCircle(x, y, 20, [0, 0.6, 1], 2)
    draw_line(x - 10, y + 7, x, y + 7, [0, 0.6, 1])
    draw_line(x + 5, y + 7, x + 6, y + 7, [0, 0.6, 1])
    draw_line(x - 15, y, x - 5, y, [0, 0.6, 1])
    draw_line(x - 10, y - 7, x + 5, y - 7, [0, 0.6, 1])
    draw_line(x, y - 14, x + 8, y - 14, [0, 0.6, 1])

def pondModel2(x, y):
    midpointCircle(x, y, 30, [0, 0.6, 1], 2)
    midpointCircle(x + 15, y + 15, 5, [0, 0.6, 1], 2)
    midpointCircle(x - 15, y - 10, 2, [0, 0.6, 1], 2)
    draw_line(x - 5, y - 10, x + 10, y - 10, [0, 0.6, 1])
    draw_line(x - 10, y - 15, x + 15, y - 15, [0, 0.6, 1])
    draw_line(x - 15, y, x + 20, y, [0, 0.6, 1])
    draw_line(x - 10, y + 15, x, y + 15, [0, 0.6, 1])

#===================================================================================================================#
#===================================================Models End======================================================#
#===================================================================================================================#

#===================================================================================================================#
#===================================================Button Start======================================================#
#===================================================================================================================#

def backButton():
    glPointSize(5)
    draw_line(80, 930, 160, 930, [0, 0, 0])
    draw_line(80, 930, 110, 960, [0, 0, 0])
    draw_line(80, 930, 110, 900, [0, 0, 0])

def cancleButton():
    glPointSize(5)
    draw_line(1720, 960, 1660, 900, [1, 0, 0])
    draw_line(1720, 900, 1660, 960, [1, 0, 0])

def pauseButton():
    glPointSize(5)
    draw_line(875, 900, 875, 960, [1, 1, 1])
    draw_line(915, 900, 915, 960, [1, 1, 1])

def playButton():
    glPointSize(5)
    draw_line(875, 900, 875, 960, [1, 1, 0])
    draw_line(875, 900, 915, 930, [1, 1, 0])
    draw_line(915, 930, 875, 960, [1, 1, 0])

def startButton():
    glPointSize(5)
    midpointCircle(1600, 200, 70, [1, 0, 1], 4)
    draw_line(1580, 150, 1580, 250, [1, 0, 1])
    draw_line(1580, 250, 1640, 200, [1, 0, 1])
    draw_line(1580, 150, 1640, 200, [1, 0, 1])

#===================================================================================================================#
#===================================================Button End======================================================#
#===================================================================================================================#

#===================================================================================================================#
#===================================================Tower Start======================================================#
#===================================================================================================================#

def towerPlace(x, y):
    glPointSize(5)
    draw_line(x + 8, y - 15, x - 2, y, [0.6, 0, 0.1])
    glPointSize(10)
    draw_line(x - 11, y, x + 1, y + 9, [0.2, 0.2, 0.2])
    glPointSize(5)
    midpointCircle(x, y, 30, [0.9, 0.6, 0.1], 2)

def towerSelectMenu(x, y):

        draw_line(x - 30, y - 30, x + 30, y - 30, [0, 1, 0])
        draw_line(x + 30, y - 30, x + 30, y + 30, [1, 1, 1])
        draw_line(x + 30, y + 30, x - 30, y + 30, [1, 0, 0])
        draw_line(x - 30, y + 30, x - 30, y - 30, [1, 1, 1])
        glPointSize(10)
        draw_line(x - 25, y, x + 25, y, [0, 1, 0])
        draw_line(x - 25, y - 5, x + 25, y - 5, [0, 1, 0])
        draw_line(x - 25, y - 10, x + 25, y - 10, [0, 1, 0])
        draw_line(x - 25, y - 15, x + 25, y - 15, [0, 1, 0])
        draw_line(x - 25, y - 20, x + 25, y - 20, [0, 1, 0])
        draw_line(x - 25, y - 25, x + 25, y - 25, [0, 1, 0])
        
        draw_line(x - 25, y + 5, x + 25, y + 5, [1, 0, 0])
        draw_line(x - 25, y + 10, x + 25, y + 10, [1, 0, 0])
        draw_line(x - 25, y + 15, x + 25, y + 15, [1, 0, 0])
        draw_line(x - 25, y + 20, x + 25, y + 20, [1, 0, 0])
        draw_line(x - 25, y + 25, x + 25, y + 25, [1, 0, 0])
        
        glPointSize(2)

class Tower1:
    
    def __init__(self, x, y):
        global coin
        self.x = x
        self.y = y
        self.attack = 50
        self.range = 200
        self.cost = 80
        coin -= self.cost
        print('Coin Left: ', coin)
    def draw(self):
        x, y = self.x, self.y
        # Base (grey color)
        glColor3f(0.5, 0.5, 0.5)  # Base color (grey)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)  # Bottom-left corner
        glVertex2f(x + 40, y)  # Bottom-right corner
        glVertex2f(x + 40, y + 5)  # Top-right corner
        glVertex2f(x, y + 5)  # Top-left corner
        glEnd()

        # Tower body (red color)
        glColor3f(0.8, 0.0, 0.0)  # Tower body color (red)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x + 5, y + 5)  # Bottom-left corner
        glVertex2f(x + 35, y + 5)  # Bottom-right corner
        glVertex2f(x + 35, y + 55)  # Top-right corner
        glVertex2f(x + 5, y + 55)  # Top-left corner
        glEnd()

        # Tower top (grey color)
        glColor3f(0.5, 0.5, 0.5)  # Tower top color (grey)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x + 2.5, y + 55)  # Bottom-left corner
        glVertex2f(x + 37.5, y + 55)  # Bottom-right corner
        glVertex2f(x + 37.5, y + 57.5)  # Top-right corner
        glVertex2f(x + 2.5, y + 57.5)  # Top-left corner
        glEnd()

class Tower2:

    def __init__(self, x, y):
        global coin
        self.x = x
        self.y = y
        self.attack = 100
        self.range = 150
        self.cost = 100
        coin -= self.cost
        print('Coin Left: ', coin)
    
    def draw(self):
        x, y = self.x, self.y
        # Pipe body (green color)
        glColor3f(0.0, 1.0, 0.0)  # Pipe body color (green)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)  # Bottom-left corner
        glVertex2f(x + 40, y)  # Bottom-right corner
        glVertex2f(x + 40, y + 55)  # Top-right corner
        glVertex2f(x, y + 55)  # Top-left corner
        glEnd()

        # Left cap (red color)
        glColor3f(1.0, 0.0, 0.0)  # Left cap color (red)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x - 5, y)  # Bottom-left corner
        glVertex2f(x, y)  # Bottom-right corner
        glVertex2f(x, y + 55)  # Top-right corner
        glVertex2f(x - 5, y + 55)  # Top-left corner
        glEnd()

        # Right cap (blue color)
        glColor3f(0.0, 0.0, 1.0)  # Right cap color (blue)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x + 40, y)  # Bottom-left corner
        glVertex2f(x + 45, y)  # Bottom-right corner
        glVertex2f(x + 45, y + 55)  # Top-right corner
        glVertex2f(x + 40, y + 55)  # Top-left corner
        glEnd()

        glColor3f(0.5, 0.0, 0.5)  # Triangle color (purple)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y + 55)  # Left corner
        glVertex2f(x + 40, y + 55)  # Right corner
        glVertex2f(x + 20, y + 85) # Top corner
        glEnd()

#===================================================================================================================#
#===================================================Tower End======================================================#
#===================================================================================================================#

#===================================================================================================================#
#===================================================Enemy Start======================================================#
#===================================================================================================================#

class Dinosaur:

    def __init__(self, path, move_x = 0, move_y = 0):
        self.path = path
        self.current_waypoint = 0
        self.x, self.y = self.path[0]
        self.move_x = move_x
        self.move_y = move_y
        self.health = 500

    def move(self):

        global gameLost

        if self.current_waypoint < len(self.path) - 1 and self.move_x > 0 and self.move_y > 0:
            next_x, next_y = self.path[self.current_waypoint + 1]
            dx = next_x - self.x
            dy = next_y - self.y
            speed = 1
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            
            if distance < speed:
                self.current_waypoint += 1
            else:
                self.x += (dx / distance) * speed
                self.y += (dy / distance) * speed
        
        elif self.move_x <= 0 or self.move_y <= 0:
            self.move_x += 1
            self.move_y += 1
        
        if self.x - 50 > W_Width:
            gameLost = True

    def draw(self):
        x, y = self.x, self.y
        dino_color = [0.2, 0.5, 0.5]
        glPointSize(3)

        #head
        draw_line(x, y, x + 15, y, dino_color)
        draw_line(x, y, x, y - 5, dino_color)
        draw_line(x - 5, y - 5, x, y - 5, dino_color)
        draw_line(x - 5, y - 5, x - 5, y - 10, dino_color)
        draw_line(x - 10, y - 10, x - 5, y - 10, dino_color)
        draw_line(x - 10, y - 10, x - 10, y - 90, dino_color)
        draw_line(x + 15, y, x + 15, y - 5, dino_color)
        draw_line(x + 15, y - 5, x + 22, y - 5, dino_color)
        draw_line(x + 22, y - 5, x + 22, y - 10, dino_color)
        draw_line(x + 22, y - 10, x + 27, y - 10, dino_color)
        draw_line(x + 27, y - 10, x + 27, y - 15, dino_color)
        draw_line(x + 27, y - 15, x + 35, y - 15, dino_color)
        draw_line(x + 35, y - 15, x + 35, y - 20, dino_color)
        draw_line(x + 35, y - 20, x + 40, y - 20, dino_color)
        draw_line(x + 40, y - 20, x + 40, y - 40, dino_color)
        draw_line(x + 35, y - 40, x + 40, y - 40, dino_color)
        draw_line(x + 35, y - 40, x + 35, y - 45, dino_color)
        draw_line(x + 15, y - 45, x + 35, y - 45, dino_color)
        
        #eye
        draw_line(x + 5, y - 15, x + 12, y - 15, dino_color)
        draw_line(x + 12, y - 15, x + 12, y - 22, dino_color)
        draw_line(x + 5, y - 22, x + 12, y - 22, dino_color)
        draw_line(x + 5, y - 15, x + 5, y - 22, dino_color)

        #body
        draw_line(x + 15, y - 45, x + 15, y - 85, dino_color)
        draw_line(x + 15, y - 85, x + 20, y - 85, dino_color)
        draw_line(x + 20, y - 85, x + 20, y - 90, dino_color)
        draw_line(x + 20, y - 90, x + 25, y - 90, dino_color)
        draw_line(x + 25, y - 90, x + 25, y - 130, dino_color)
        draw_line(x + 20, y - 130, x + 25, y - 130, dino_color)
        draw_line(x + 20, y - 130, x + 20, y - 135, dino_color)
        draw_line(x + 12, y - 135, x + 20, y - 135, dino_color)
        draw_line(x + 12, y - 135, x + 12, y - 140, dino_color)
        draw_line(x - 43, y - 140, x, y - 140, dino_color)
        draw_line(x - 40, y - 90, x - 10, y - 90, dino_color)
        draw_line(x - 40, y - 90, x - 40, y - 95, dino_color)
        draw_line(x - 45, y - 95, x - 40, y - 95, dino_color)
        draw_line(x - 45, y - 95, x - 45, y - 100, dino_color)
        draw_line(x - 50, y - 100, x - 45, y - 100, dino_color)
        draw_line(x - 50, y - 100, x - 50, y - 105, dino_color)
        draw_line(x - 55, y - 105, x - 50, y - 105, dino_color)
        draw_line(x - 55, y - 105, x - 55, y - 110, dino_color)

        # #tail
        draw_line(x - 75, y - 110, x - 55, y - 110, dino_color)
        draw_line(x - 75, y - 110, x - 75, y - 115, dino_color)
        draw_line(x - 75, y - 115, x - 70, y - 115, dino_color)
        draw_line(x - 70, y - 115, x - 70, y - 120, dino_color)
        draw_line(x - 70, y - 120, x - 65, y - 120, dino_color)
        draw_line(x - 65, y - 120, x - 65, y - 125, dino_color)
        draw_line(x - 65, y - 125, x - 55, y - 125, dino_color)
        draw_line(x - 55, y - 125, x - 55, y - 140, dino_color)
        draw_line(x - 43, y - 140, x - 40, y - 140, dino_color)
        
        #leg front 1   
        draw_line(x + 20, y - 135, x + 20, y - 145, dino_color)
        draw_line(x + 20, y - 145, x + 30, y - 145, dino_color)
        draw_line(x + 30, y - 145, x + 30, y - 155, dino_color)
        draw_line(x + 12, y - 155, x + 30, y - 155, dino_color)
        draw_line(x + 12, y - 140, x + 12, y - 155, dino_color)
        
        #leg front 2 (big one)
        draw_line(x + 12, y - 140, x + 12, y - 155, dino_color)
        draw_line(x + 12, y - 155, x + 20, y - 155, dino_color)
        draw_line(x + 20, y - 155, x + 20, y - 165, dino_color)
        draw_line(x, y - 165, x + 20, y - 165, dino_color)
        draw_line(x, y - 140, x, y - 165, dino_color)

        #leg back 1 (big one)
        draw_line(x - 55, y - 140, x - 55, y - 165, dino_color)
        draw_line(x - 55, y - 165, x - 35, y - 165, dino_color)
        draw_line(x - 35, y - 155, x - 35, y - 165, dino_color)
        draw_line(x - 43, y - 155, x - 35, y - 155, dino_color)
        draw_line(x - 43, y - 140, x - 43, y - 155, dino_color)

        #leg back 2
        draw_line(x - 43, y - 140, x - 43, y - 155, dino_color)
        draw_line(x - 43, y - 155, x - 25, y - 155, dino_color)
        draw_line(x - 25, y - 145, x - 25, y - 155, dino_color)
        draw_line(x - 35, y - 145, x - 25, y - 145, dino_color)
        draw_line(x - 35, y - 140, x - 25, y - 145, dino_color)
        draw_line(x - 35, y - 140, x - 35, y - 145, dino_color)

class Bird:

    def __init__(self, path, move_x = 0, move_y = 0):
        self.path = path
        self.current_waypoint = 0
        self.x, self.y = self.path[0]
        self.move_x = move_x
        self.move_y = move_y
        self.health = 300

    def move(self):

        global gameLost

        if self.current_waypoint < len(self.path) - 1 and self.move_x > 0 and self.move_y > 0:
            next_x, next_y = self.path[self.current_waypoint + 1]
            dx = next_x - self.x
            dy = next_y - self.y
            speed = 2
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            
            if distance < speed:
                self.current_waypoint += 1
            else:
                self.x += (dx / distance) * speed
                self.y += (dy / distance) * speed
        
        elif self.move_x <= 0 or self.move_y <= 0:
            self.move_x += 1
            self.move_y += 1

        if self.x - 50 > W_Width:
            gameLost = True

    def draw(self):
        x, y = self.x - 50, self.y - 150
        birdColor = [0.6, 0.1, 1]

        glPointSize(3)
        draw_line(x, y, x + 6, y + 3, birdColor)
        draw_line(6 + x, y + 3, 18 + x, y + 8, birdColor)
        draw_line(18 + x, y + 8, 22 + x, y - 3, birdColor)
        draw_line(22 + x, y - 3, 28 + x, y - 7, birdColor)
        draw_line(28 + x, y - 7, 31 + x, y - 10, birdColor)
        draw_line(31 + x, y - 10, 34 + x, y - 18, birdColor)
        draw_line(34 + x, y - 18, 39 + x, y - 17, birdColor)
        draw_line(39 + x, y - 17, 35 + x, y - 10, birdColor)
        draw_line(35 + x, y - 10, 51 + x, y + 11, birdColor)
        draw_line(51 + x, y + 11, 77 + x, y + 24, birdColor)
        draw_line(77 + x, y + 24, 56 + x, y + 25, birdColor)
        draw_line(56 + x, y + 25, 45 + x, y + 23, birdColor)
        draw_line(45 + x, y + 23, 37 + x, y + 17, birdColor)
        draw_line(37 + x, y + 17, 33 + x, y + 24, birdColor)
        draw_line(33 + x, y + 24, 26 + x, y + 29, birdColor)
        draw_line(26 + x, y + 29, 12 + x, y + 31, birdColor)
        draw_line(12 + x, y + 31, 18 + x, y + 24, birdColor)
        draw_line(18 + x, y + 24, 21 + x, y + 17, birdColor)
        draw_line(21 + x, y + 17, 6 + x, y + 8, birdColor)
        draw_line(6 + x, y + 8, 1 + x, y + 4, birdColor)
        draw_line(1 + x, y + 4, x, y, birdColor)
        draw_line(37 + x, y + 17, 26 + x, y + 4, birdColor)
        draw_line(26 + x, y + 4, 25 + x, y + 15, birdColor)
        draw_line(25 + x, y + 15, 28 + x, y + 19, birdColor)
        draw_line(28 + x, y + 19, 21 + x, y + 17, birdColor)
        draw_line(18 + x, y + 10, x, y, birdColor)

#===================================================================================================================#
#===================================================Enemy End======================================================#
#===================================================================================================================#

#===================================================================================================================#
#===================================================Menu Start======================================================#
#===================================================================================================================#

def startMenu(x, y):
    # Map 1
    glPointSize(5)
    draw_line(x - 200, y + 125, x + 200, y + 125, [0, 0, 0])             # _
    draw_line(x - 200, y + 125, x - 200, y + 275, [0, 0, 0])             # |
    draw_line(x + 200, y + 125, x + 200, y + 275, [0, 0, 0])             # |
    draw_line(x - 200, y + 275, x + 200, y + 275, [0, 0, 0])             # _
    drawLevel(x, y + 200)
    glPointSize(10)
    draw_line(x + 150, y + 150, x + 150, y + 250, [1, 0.4, 0])
    draw_line(x + 150, y + 250, x + 140, y + 240, [1, 0.4, 0])

    # Map 2
    glPointSize(5)
    draw_line(x - 200, y + 75, x + 200, y + 75, [0, 0, 0])               # _
    draw_line(x - 200, y - 75, x - 200, y + 75, [0, 0, 0])               # |
    draw_line(x + 200, y - 75, x + 200, y + 75, [0, 0, 0])               # |
    draw_line(x - 200, y - 75, x + 200, y - 75, [0, 0, 0])               # _
    drawLevel(x, y)
    glPointSize(10)
    draw_line(x + 140, y - 50, x + 175, y - 50, [1, 0.2, 0])
    glPointSize(9)
    draw_line(x + 140, y - 50, x + 175, y + 30, [1, 0.2, 0])
    glPointSize(10)
    draw_line(x + 175, y + 30, x + 175, y + 40, [1, 0.2, 0])
    draw_line(x + 149, y + 45, x + 171, y + 45, [1, 0.2, 0])
    draw_line(x + 145, y + 40, x + 145, y + 35, [1, 0.2, 0])

    # Map 3
    glPointSize(5)
    draw_line(x - 200, y - 275, x + 200, y - 275, [0, 0, 0])               # _
    draw_line(x - 200, y - 275, x - 200, y - 125, [0, 0, 0])               # |
    draw_line(x + 200, y - 275, x + 200, y - 125, [0, 0, 0])               # |
    draw_line(x - 200, y - 125, x + 200, y - 125, [0, 0, 0])               # _
    drawLevel(x, y - 200)
    glPointSize(10)
    draw_line(x + 175, y - 250, x + 175, y - 150, [1, 0, 0])
    draw_line(x + 140, y - 150, x + 175, y - 150, [1, 0, 0])
    draw_line(x + 140, y - 250, x + 175, y - 250, [1, 0, 0])
    draw_line(x + 155, y - 200, x + 175, y - 200, [1, 0, 0])
    draw_line(x + 140, y - 250, x + 140, y - 240, [1, 0, 0])
    draw_line(x + 140, y - 150, x + 140, y - 160, [1, 0, 0])
    glPointSize(2)

def drawLevel(x, y):
    glPointSize(7)
    #L
    draw_line(x - 180, y - 50, x - 180, y + 50, [1, 0.6, 0])
    draw_line(x - 180, y - 50, x - 140, y - 50, [1, 0.6, 0])
    #E
    draw_line(x - 120, y - 50, x - 120, y + 50, [1, 0.6, 0])
    draw_line(x - 120, y - 50, x - 80, y - 50, [1, 0.6, 0])
    draw_line(x - 120, y, x - 110, y, [1, 0.6, 0])
    draw_line(x - 120, y + 50, x - 80, y + 50, [1, 0.6, 0])
    #V
    draw_line(x - 60, y + 50, x - 40, y - 50, [1, 0.6, 0])
    draw_line(x - 40, y - 50, x - 20, y + 50, [1, 0.6, 0])
    #E
    draw_line(x, y - 50, x, y + 50, [1, 0.6, 0])
    draw_line(x, y - 50, x + 40, y - 50, [1, 0.6, 0])
    draw_line(x, y, x + 10, y, [1, 0.6, 0])
    draw_line(x, y + 50, x + 40, y + 50, [1, 0.6, 0])
    #L
    draw_line(x + 60, y - 50, x + 60, y + 50, [1, 0.6, 0])
    draw_line(x + 60, y - 50, x + 100, y - 50, [1, 0.6, 0])

def gameOver():
    glPointSize(10)
    draw_line(200, 125, 200, 875, [0, 0, 0])
    draw_line(1600, 125, 1600, 875, [0, 0, 0])
    draw_line(200, 125, 1600, 125, [0, 0, 0])
    draw_line(200, 875, 1600, 875, [0, 0, 0])
    #O
    draw_line(400, 450, 400, 650, [1, 0, 0])
    draw_line(400, 450, 600, 450, [1, 0, 0])
    draw_line(600, 450, 600, 650, [1, 0, 0])
    draw_line(400, 650, 600, 650, [1, 0, 0])
    #V
    draw_line(700, 650, 800, 450, [1, 0, 0])
    draw_line(800, 450, 900, 650, [1, 0, 0])
    #E
    draw_line(1000, 450, 1000, 650, [1, 0, 0])
    draw_line(1000, 450, 1200, 450, [1, 0, 0])
    draw_line(1000, 550, 1100, 550, [1, 0, 0])
    draw_line(1000, 650, 1200, 650, [1, 0, 0])
    #R
    draw_line(1300, 450, 1300, 650, [1, 0, 0])
    draw_line(1300, 550, 1400, 550, [1, 0, 0])
    draw_line(1300, 650, 1500, 650, [1, 0, 0])
    draw_line(1400, 550, 1500, 650, [1, 0, 0])
    draw_line(1400, 550, 1500, 450, [1, 0, 0])

#===================================================================================================================#
#===================================================Menu End======================================================#
#===================================================================================================================#

#===================================================================================================================#
#===================================================Map Start======================================================#
#===================================================================================================================#

def map1():

    global gameStart, towerCreate, towerList1, towerList2, dinosaur_spawn_time, wave_1, wave_2, wave_3, wave1_time, wave2_time, wave3_time
    tower_pointsM1 = [[690, 430], [785, 320], [550, 160], [640, 155], [800, 510], [800, 740], [1340, 580], [1070, 615]]
    road_pointM1 = [[850, 0, 850, 200], [850, 200, 700, 350], [700, 0, 700, 150], [700, 150, 650, 200], [650, 350, 700, 350], [530, 200, 650, 200], [530, 200, 500, 230], 
                    [500, 230, 500, 600], [500, 600, 600, 700], [650, 350, 650, 520], [650, 520, 680, 550], [600, 700, 850, 700], [960, 550, 680, 550], [960, 550, 1000, 590], 
                    [850, 700, 850, 790], [850, 790, 860, 800], [1000, 590, 1000, 650], [860, 800, 1200, 800], [1200, 800, 1300, 700], [1000, 650, 1120, 650], [1120, 650, 1150, 620], 
                    [1300, 700, 1300, 530], [1150, 620, 1150, 430], [1150, 430, 1200, 380], [1300, 530, W_Width, 530], [1200, 380, W_Width, 380]]
    road_color = [0.6, 0, 0.1]
    towerList = []
    
    for i in range(0, len(tower_pointsM1)):
        towerPlace(tower_pointsM1[i][0], tower_pointsM1[i][1])
    
    glPointSize(2)
    for i in range(0, len(road_pointM1)):
        draw_line(road_pointM1[i][0], road_pointM1[i][1], road_pointM1[i][2], road_pointM1[i][3], road_color)

    for i in towerCreate:
        x, y = i[0], i[1]
        towerSelectMenu(x, y)

    for i in towerList1:
        i.draw()

    for i in towerList2:
        i.draw()

    houseModel1(950, 10)
    houseModel2(1000, 100)
    if gameStart == True:
        if time.time() >= wave1_time:
            for i in range(0, len(wave_1)):
                wave_1[i].draw()
                if pause == False:
                    wave_1[i].move()

        if time.time() >= wave2_time:
            for i in range(0, len(wave_2)):
                wave_2[i].draw()
                if pause == False:
                    wave_2[i].move()

        if time.time() >= wave3_time:
            for i in range(0, len(wave_3)):
                wave_3[i].draw()
                if pause == False:
                    wave_3[i].move()

def map2():

    global gameStart, towerCreate, towerList1, towerList2, towerSelected, dinosaur_spawn_time, wave_1, wave_2, wave_3, wave1_time, wave2_time, wave3_time
    road_pointM2 = [[750, 0, 750, 180], [750, 180, 800, 250], [900, 0, 900, 80], [900, 80, 920, 100], [800, 250, 1000, 250], [920, 100, 1080, 100], [1080, 100, 1150, 150], 
                   [1000, 250, 1000, 350], [1150, 150, 1150, 450], [1000, 350, 600, 350], [1150, 450, 1080, 500], [1080, 500, 650, 500], [650, 500, 620, 530], 
                   [600, 350, 470, 460], [620, 530, 620, 600], [470, 460, 470, 670], [620, 600, 650, 630], [470, 670, 600, 780], [650, 630, 900, 630], [900, 630, 930, 660], 
                   [930, 660, 930, 800], [600, 780, 780, 780], [780, 780, 780, 850], [930, 800, 1030, 800], [1030, 800, 1030, 600], [1030, 600, 1180, 500], 
                   [780, 850, 880, 950], [880, 950, 1080, 950], [1080, 950, 1180, 850], [1180, 850, 1180, 680], [1180, 500, W_Width, 500], [1180, 680, 1230, 650], 
                   [1230, 650, W_Width, 650]]
    tower_pointsM2 = [[940, 60], [950, 300], [840, 300], [665, 565], [735, 820], [970, 760], [970, 690]]
    road_color = [0.6, 0, 0.1]

    glPointSize(2)
    for i in range(0, len(road_pointM2)):
        draw_line(road_pointM2[i][0], road_pointM2[i][1], road_pointM2[i][2], road_pointM2[i][3], road_color)

    for i in range(0, len(tower_pointsM2)):
        towerPlace(tower_pointsM2[i][0], tower_pointsM2[i][1])

    for i in towerCreate:
        x, y = i[0], i[1]
        towerSelectMenu(x, y)

    for i in towerList1:
        i.draw()

    for i in towerList2:
        i.draw()

    if gameStart == True:
        if time.time() >= wave1_time:
            for i in range(0, len(wave_1)):
                wave_1[i].draw()
                if pause == False:
                    wave_1[i].move()

        if time.time() >= wave2_time:
            for i in range(0, len(wave_2)):
                wave_2[i].draw()
                if pause == False:
                    wave_2[i].move()

        if time.time() >= wave3_time:
            for i in range(0, len(wave_3)):
                wave_3[i].draw()
                if pause == False:
                    wave_3[i].move()

def map3():

    global gameStart, towerList1, towerList2, towerCreate, towerSelected, dinosaur_spawn_time, wave_1, wave_2, wave_3, wave1_time, wave2_time, wave3_time
    road_pointM3 = [[0, 300, 300, 300], [0, 150, 300, 150], [300, 300, 800, 250], [300, 150, 800, 100], [800, 250, 825, 275], [825, 275, 825, 350], [825, 350, 800, 375],   
                    [800, 375, 600, 400], [600, 400, 550, 550], [550, 550, 550, 750], [550, 750, 700, 870], [700, 870, 1100, 900], [1100, 900, W_Width, 870], 
                    [740, 755, 1100, 780], [1100, 780, W_Width, 750], [800, 100, 900, 150], [900, 150, 1000, 250], [1000, 250, 1000, 350], [1000, 350, 925, 450], [925, 450, 750, 525], 
                    [750, 525, 750, 550], [850, 570, 750, 550], [850, 570, 1400, 530], [1400, 530, W_Width, 530], [W_Width, 650, 1400, 650], [1400, 650, 850, 690], 
                    [850, 690, 770, 675], [770, 675, 725, 685], [725, 685, 725, 730], [725, 730, 740, 755]]
    tower_pointsM3 = [[775, 310], [685, 330], [570, 330], [700, 70], [560, 85], [860, 525], [790, 720], [915, 725], [1050, 735], [500, 600], [510, 700], [1000, 195]]
    road_color = [0.6, 0, 0.1]

    glPointSize(2)
    for i in range(0, len(road_pointM3)):
        draw_line(road_pointM3[i][0], road_pointM3[i][1], road_pointM3[i][2], road_pointM3[i][3], road_color)

    for i in range(0, len(tower_pointsM3)):
        towerPlace(tower_pointsM3[i][0], tower_pointsM3[i][1])

    for i in towerCreate:
        x, y = i[0], i[1]
        towerSelectMenu(x, y)

    for i in towerList1:
        i.draw()

    for i in towerList2:
        i.draw()

    if gameStart == True:
        if time.time() >= wave1_time:
            for i in range(0, len(wave_1)):
                wave_1[i].draw()
                if pause == False:
                    wave_1[i].move()

        if time.time() >= wave2_time:
            for i in range(0, len(wave_2)):
                wave_2[i].draw()
                if pause == False:
                    wave_2[i].move()

        if time.time() >= wave3_time:
            for i in range(0, len(wave_3)):
                wave_3[i].draw()
                if pause == False:
                    wave_3[i].move()

#===================================================================================================================#
#===================================================Map End======================================================#
#===================================================================================================================#

def mouseListener(button, state, x, y):

    global mapClick, coin, gameStart, mapSelect, towerCreate, towerlist1, towerlist2, towerList1, towerList2, towerSelectMenuClick, pause, wave_1, wave_2, wave_3, gameLost
    tower_pointsM1 = [[690, 430], [785, 320], [550, 160], [640, 155], [800, 510], [800, 740], [1340, 580], [1070, 615]]
    tower_pointsM2 = [[940, 60], [950, 300], [840, 300], [665, 565], [735, 820], [970, 760], [970, 690]]
    tower_pointsM3 = [[775, 310], [685, 330], [570, 330], [700, 70], [560, 85], [860, 525], [790, 720], [915, 725], [1050, 735], [500, 600], [510, 700], [1000, 195]]
    tower1cost, tower2cost = 80, 100

    if mapClick is False and button==GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = W_Height - y      # because y should starts from bottom but in my computer it starts from top
        if x >= centerX - 200 and x <= centerX + 200 and y >= centerY - 275 and y <= centerY - 125:
            mapClick = True
            mapSelect = 3
            print('Map 3 has been selected')
            dinosaur1_1 = Dinosaur(map3_1Path)
            dinosaur1_2 = Dinosaur(map3_1Path)
            dinosaur1_3 = Dinosaur(map3_2Path)
            dinosaur2_2 = Dinosaur(map3_2Path, 0, -300)
            dinosaur2_3 = Dinosaur(map3_1Path, 0, -300)
            dinosaur3 = Dinosaur(map3_1Path, 0, -600)
            bird1_1 = Bird(map3_2Path, 0, -200)
            bird1_2 = Bird(map3_1Path, 0, -400)
            bird1_3 = Bird(map3_1Path, 0, -200)
            bird2_3 = Bird(map3_1Path, 0, -400)
            wave_1 = [dinosaur1_1, bird1_1]
            wave_2 = [dinosaur1_2, dinosaur2_2, bird1_2]
            wave_3 = [dinosaur1_3, dinosaur2_3, dinosaur3, bird1_3, bird2_3]
        elif x >= centerX - 200 and x <= centerX + 200 and y >= centerY - 75 and y <= centerY + 75:
            mapClick = True
            mapSelect = 2
            print('Map 2 has been selected')
            dinosaur1_1 = Dinosaur(map2Path)
            dinosaur1_2 = Dinosaur(map2Path)
            dinosaur1_3 = Dinosaur(map2Path)
            dinosaur2_2 = Dinosaur(map2Path, 0, -300)
            dinosaur2_3 = Dinosaur(map2Path, 0, -300)
            dinosaur3 = Dinosaur(map2Path, 0, -600)
            bird1_1 = Bird(map2Path, 0, -200)
            bird1_2 = Bird(map2Path, 0, -400)
            bird1_3 = Bird(map2Path, 0, -200)
            bird2_3 = Bird(map2Path, 0, -400)
            wave_1 = [dinosaur1_1, bird1_1]
            wave_2 = [dinosaur1_2, dinosaur2_2, bird1_2]
            wave_3 = [dinosaur1_3, dinosaur2_3, dinosaur3, bird1_3, bird2_3]
        elif x >= centerX - 200 and x <= centerX + 200 and y >= centerY + 125 and y <= centerY + 275:
            mapClick = True
            mapSelect = 1
            print('Map 1 has been selected')
            dinosaur1_1 = Dinosaur(map1Path)
            dinosaur1_2 = Dinosaur(map1Path)
            dinosaur1_3 = Dinosaur(map1Path)
            dinosaur2_2 = Dinosaur(map1Path, 0, -300)
            dinosaur2_3 = Dinosaur(map1Path, 0, -300)
            dinosaur3 = Dinosaur(map1Path, 0, -600)
            bird1_1 = Bird(map1Path, 0, -200)
            bird1_2 = Bird(map1Path, 0, -400)
            bird1_3 = Bird(map1Path, 0, -200)
            bird2_3 = Bird(map1Path, 0, -400)
            wave_1 = [dinosaur1_1, bird1_1]
            wave_2 = [dinosaur1_2, dinosaur2_2, bird1_2]
            wave_3 = [dinosaur1_3, dinosaur2_3, dinosaur3, bird1_3, bird2_3]
        else:
            mapSelect = 0

    elif mapClick is True and button==GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = W_Height - y      # because y should starts from bottom but in my computer it starts from top
        if x >= 80 and x <= 160 and y >= 900 and y <= 960:
            mapClick = False
            mapSelect = 0
            print('Back to Menu')
            towerCreate.clear()
            towerList1.clear()
            towerList2.clear()
            towerlist1.clear()
            towerlist2.clear()
            gameStart = False
            gameLost = False
            pause = False
        if x >= 1660 and x <= 1720 and y >= 900 and y <= 960:
            glutLeaveMainLoop()
            print('Game Cancled')
        if x >= 875 and x <= 915 and y >= 900 and y <= 960:
            if pause == False:
                pause = True
                print('Game Paused')
            else:
                pause = False 
                print('Game Resumed')
        elif mapSelect == 1 and pause == False:
            if towerSelectMenuClick is True:
                for i in range(0, len(towerCreate)):
                    if x >= towerCreate[i][0] - 30 and x <= towerCreate[i][0] + 30 and y >= towerCreate[i][1] and y <= towerCreate[i][1] + 30:
                        if coin - tower1cost >= 0:
                            print('Tower 1 Created')
                            if towerCreate[i] not in towerlist1:
                                towerList1.append(Tower1(towerCreate[i][0], towerCreate[i][1]))
                                towerlist1.append(towerCreate[i])
                            towerCreate.remove(towerCreate[i])
                            towerSelectMenuClick = False
                            exit
                        else:
                            print('Not enough coin')
                    elif x >= towerCreate[i][0] - 30 and x <= towerCreate[i][0] + 30 and y < towerCreate[i][1] and y >= towerCreate[i][1] - 30:
                        if coin - tower2cost >= 0:
                            print('Tower 2 Created')
                            if towerCreate[i] not in towerlist2:
                                towerList2.append(Tower2(towerCreate[i][0], towerCreate[i][1]))
                                towerlist2.append(towerCreate[i])
                            towerCreate.remove(towerCreate[i])
                            towerSelectMenuClick = False
                            exit
                        else:
                            print('Not enough coin')
                    else:
                        towerCreate.pop()
                        towerSelectMenuClick = False
            elif x <= 1670 and x >= 1530 and y >= 130 and y <= 270:
                gameStart = True
                print('Game Started')
            else:
                for i in range(0, len(tower_pointsM1)):
                    if x >= tower_pointsM1[i][0] - 30 and x <= tower_pointsM1[i][0] + 30 and y >= tower_pointsM1[i][1] - 30 and y <= tower_pointsM1[i][1] + 30 and tower_pointsM1[i] not in towerCreate and towerSelectMenuClick is False and tower_pointsM1[i] not in towerlist1 and tower_pointsM1[i] not in towerlist2:
                        towerCreate.append(tower_pointsM1[i])
                        towerSelectMenuClick = True

        elif mapSelect == 2 and pause == False:
            if towerSelectMenuClick is True:
                for i in range(0, len(towerCreate)):
                    if x >= towerCreate[i][0] - 30 and x <= towerCreate[i][0] + 30 and y >= towerCreate[i][1] and y <= towerCreate[i][1] + 30:
                        if coin - tower1cost >= 0:
                            print('Tower 1 Created')
                            if towerCreate[i] not in towerlist1:
                                towerList1.append(Tower1(towerCreate[i][0], towerCreate[i][1]))
                                towerlist1.append(towerCreate[i])
                            towerCreate.remove(towerCreate[i])
                            towerSelectMenuClick = False
                            exit
                        else:
                            print('Not enough coin')
                    elif x >= towerCreate[i][0] - 30 and x <= towerCreate[i][0] + 30 and y < towerCreate[i][1] and y >= towerCreate[i][1] - 30:
                        if coin - tower2cost >= 0:
                            print('Tower 2 Created')
                            if towerCreate[i] not in towerlist2:
                                towerList2.append(Tower2(towerCreate[i][0], towerCreate[i][1]))
                                towerlist2.append(towerCreate[i])
                            towerCreate.remove(towerCreate[i])
                            towerSelectMenuClick = False
                            exit
                        else:
                            print('Not enough coin')
                    else:
                        towerCreate.pop()
                        towerSelectMenuClick = False
            elif x <= 1670 and x >= 1530 and y >= 130 and y <= 270:
                gameStart = True
                print('Game Started')
            else:
                for i in range(0, len(tower_pointsM2)):
                    if x >= tower_pointsM2[i][0] - 30 and x <= tower_pointsM2[i][0] + 30 and y >= tower_pointsM2[i][1] - 30 and y <= tower_pointsM2[i][1] + 30 and tower_pointsM2[i] not in towerCreate and towerSelectMenuClick is False:
                        towerCreate.append(tower_pointsM2[i])
                        towerSelectMenuClick = True
        
        elif mapSelect == 3 and pause == False:
            if towerSelectMenuClick is True:
                for i in range(0, len(towerCreate)):
                    if x >= towerCreate[i][0] - 30 and x <= towerCreate[i][0] + 30 and y >= towerCreate[i][1] and y <= towerCreate[i][1] + 30:
                        if coin - tower1cost >= 0:
                            print('Tower 1 Created')
                            if towerCreate[i] not in towerlist1:
                                towerList1.append(Tower1(towerCreate[i][0], towerCreate[i][1]))
                                towerlist1.append(towerCreate[i])
                            towerCreate.remove(towerCreate[i])
                            towerSelectMenuClick = False
                            exit
                        else:
                            print('Not enough coin')
                    elif x >= towerCreate[i][0] - 30 and x <= towerCreate[i][0] + 30 and y < towerCreate[i][1] and y >= towerCreate[i][1] - 30:
                        if coin - tower2cost >= 0:
                            print('Tower 2 Created')
                            if towerCreate[i] not in towerlist2:
                                towerList2.append(Tower2(towerCreate[i][0], towerCreate[i][1]))
                                towerlist2.append(towerCreate[i])
                            towerCreate.remove(towerCreate[i])
                            towerSelectMenuClick = False
                            exit
                        else:
                            print('Not enough coin')
                    else:
                        towerCreate.pop()
                        towerSelectMenuClick = False
            elif x <= 1670 and x >= 1530 and y >= 130 and y <= 270:
                gameStart = True
                print('Game Started')
            else:
                for i in range(0, len(tower_pointsM3)):
                    if x >= tower_pointsM3[i][0] - 30 and x <= tower_pointsM3[i][0] + 30 and y >= tower_pointsM3[i][1] - 30 and y <= tower_pointsM3[i][1] + 30 and tower_pointsM3[i] not in towerCreate and towerSelectMenuClick is False:
                        towerCreate.append(tower_pointsM3[i])
                        towerSelectMenuClick = True
            
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global pause, mapClick, mapSelect, gameLost, pause, towerCreate
    if key==b' ' and mapClick is True:
        if pause == False:
            pause = True
            print('Game Paused')
        else:
            pause = False 
            print('Game Resumed')
    elif key==b'\x1b' and mapClick is True:
        glutLeaveMainLoop()
        print('Game Cancled')
    elif key == b'\x08' and mapClick is True:
        mapClick = False
        mapSelect = 0
        print('Back to Menu')
        towerCreate.clear()
        towerList1.clear()
        towerList2.clear()
        towerlist1.clear()
        towerlist2.clear()
        gameStart = False
        gameLost = False
        pause = False

def init():
    gluOrtho2D(0, W_Width, 0, W_Height)
    glViewport(0, 0, W_Width, W_Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glClearColor(0.6, 1, 0.3, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if mapClick is False:
        startMenu(centerX, centerY)
    elif mapClick is True and mapSelect == 1:
        if gameLost == True:
            gameOver()
        else:
            map1()
            if pause == False:
                pauseButton()
            else:
                playButton()
        backButton()
        cancleButton()
        if gameStart == False:
            startButton()
    elif mapClick is True and mapSelect == 2:
        if gameLost == True:
            gameOver()
        else:
            map2()
            if pause == False:
                pauseButton()
            else:
                playButton()
        backButton()
        cancleButton()
        if gameStart == False:
            startButton()
    elif mapClick is True and mapSelect == 3:
        if gameLost == True:
            gameOver()
        else:
            map3()
            if pause == False:
                pauseButton()
            else:
                playButton()
        backButton()
        cancleButton()
        if gameStart == False:
            startButton()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Tower Game")
init()
glutDisplayFunc(display)
glutIdleFunc(display)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()