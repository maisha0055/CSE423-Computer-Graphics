# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random

# # Global Variables
# rain_drops = []
# num_drops = 100  # Number of rain drops
# rain_angle = 0  
# bg_color = [0.96, 0.87, 0.70]  # Day background color
# is_day = True  # Day/Night mode

# # Colors
# day_color = [0.96, 0.87, 0.70]  # Day sky color
# night_color = [0.15, 0.15, 0.18]  # Night sky color
# house_wall_color = [0.9, 0.8, 0.6]  # House wall color
# house_roof_color = [0.7, 0.1, 0.1]  # House roof color
# house_door_color = [0.5, 0.3, 0.1]  # House door color
# house_window_color = [0.8, 0.9, 1.0]  # House window color
# forest_color = [0.1, 0.4, 0.1]  # Forest color

# def init_rain():
#     global rain_drops
#     rain_drops = [[random.randint(0, 500), random.randint(250, 500)] for _ in range(num_drops)]

# def draw_house():
#     # Main house structure
#     glColor3f(*house_wall_color)
#     glBegin(GL_QUADS)
#     glVertex2f(150, 100)
#     glVertex2f(150, 300)
#     glVertex2f(450, 300)
#     glVertex2f(450, 100)
#     glEnd()

#     # Roof
#     glColor3f(*house_roof_color)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(130, 300)
#     glVertex2f(470, 300)
#     glVertex2f(300, 400)
#     glEnd()

#     # Door
#     glColor3f(*house_door_color)
#     glBegin(GL_QUADS)
#     glVertex2f(200, 100)
#     glVertex2f(200, 200)
#     glVertex2f(250, 200)
#     glVertex2f(250, 100)
#     glEnd()

#     # Door handle
#     glColor3f(0.3, 0.2, 0.1)
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     glVertex2f(240, 150)
#     glEnd()

#     # Window
#     glColor3f(*house_window_color)
#     glBegin(GL_QUADS)
#     glVertex2f(350, 220)
#     glVertex2f(390, 220)
#     glVertex2f(390, 260)
#     glVertex2f(350, 260)
#     glEnd()

#     # Window grid
#     glColor3f(0.2, 0.2, 0.2)
#     glBegin(GL_LINES)
#     glVertex2f(370, 220)  # Vertical line
#     glVertex2f(370, 260)
#     glVertex2f(350, 240)  # Horizontal line
#     glVertex2f(390, 240)
#     glEnd()

# def draw_forest():
#     glColor3f(*forest_color)
#     for i in range(0, 500, 30):  # Draw trees at regular intervals


#         # Tree leaves
#         glColor3f(0.1, 0.5, 0.1)
#         glBegin(GL_TRIANGLES)
#         glVertex2f(i - 15, 150)
#         glVertex2f(i + 25, 150)
#         glVertex2f(i + 5, 200)
#         glEnd()

# def draw_rain():
#     rain_color = (0.0, 0.5, 1.0) if is_day else (0.7, 0.7, 1.0)
#     glColor3f(*rain_color)
#     glBegin(GL_LINES)
#     for drop in rain_drops:
#         x, y = drop
#         drop_angle = rain_angle * 0.1
#         glVertex2f(x, y)
#         glVertex2f(x + drop_angle, y - 10)
#     glEnd()

# def update_rain():
#     for drop in rain_drops:
#         drop[0] += rain_angle * 0.1
#         drop[1] -= 5
#         if drop[1] < 0:
#             drop[1] = random.randint(250, 500)
#             drop[0] = random.randint(0, 500)

# def change_bg_color(target_color):
#     global bg_color, is_day
#     for i in range(3):
#         bg_color[i] += (target_color[i] - bg_color[i]) * 0.05

#     if target_color == day_color:
#         is_day = True
#     else:
#         is_day = False

# def handle_keys(key, x, y):
#     global rain_angle
#     if key == GLUT_KEY_LEFT: 
#         rain_angle -= 1  
#     elif key == GLUT_KEY_RIGHT:  
#         rain_angle += 1 
#     elif key == b'd':  # Day mode
#         change_bg_color(day_color)
#     elif key == b'n':  # Night mode
#         change_bg_color(night_color)
#     glutPostRedisplay()

# def show_screen():
#     glClearColor(*bg_color, 1.0)  
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
    
#     draw_forest()  # Draw forest behind the house
#     draw_house()   # Draw the house
#     draw_rain()    # Draw rain
    
#     glFlush()
#     glutSwapBuffers()

# def update(value):
#     update_rain()
#     glutPostRedisplay()  
#     glutTimerFunc(33, update, 0)  # 30 FPS

# def setup():
#     glViewport(0, 0, 500, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, -1.0, 1.0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

# # Start and execution
# glutInit()
# glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
# glutInitWindowSize(500, 500)
# glutInitWindowPosition(0, 0)
# glutCreateWindow(b"2D House with Forest and Rain")
# setup()
# init_rain()
# glutDisplayFunc(show_screen)
# glutTimerFunc(0, update, 0)
# glutSpecialFunc(handle_keys)  # Use arrow keys
# glutKeyboardFunc(handle_keys)  # Use 'd' and 'n' keys
# glutMainLoop()

 


#############################################################################


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


# Global variables
points = []
speed = 1.0
freeze = False
blink = False
last_blink_time = time.time()


BOX_SIZE = 500

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-1, 1]) * speed * random.random()
        self.dy = random.choice([-1, 1]) * speed * random.random()
        self.color = [random.random(), random.random(), random.random()]

    def move(self):
        if not freeze:
            # Move point based on speed and direction
            self.x += self.dx
            self.y += self.dy
            
            # boundary collision and bounce
            if self.x <= -BOX_SIZE or self.x >= BOX_SIZE:
                self.dx = -self.dx
            if self.y <= -BOX_SIZE or self.y >= BOX_SIZE:
                self.dy = -self.dy
    
    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

    def toggle_blink(self):
        # Change color to background color or original
        self.color = [0, 0, 0] if self.color != [0, 0, 0] else [random.random(), random.random(), random.random()]

def init():
    # Initialize OpenGL settings
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(5.0)

def display():
    global last_blink_time
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # Draw all points
    for point in points:
        if blink and time.time() - last_blink_time > 0.5:
            point.toggle_blink()
        point.draw()
    
    if blink and time.time() - last_blink_time > 0.5:
        last_blink_time = time.time()  # Reset blink timer
    
    glutSwapBuffers()

def update(value):
    # Move points if not frozen
    if not freeze:
        for point in points:
            point.move()
    
    glutPostRedisplay()
    glutTimerFunc(33, update, 0)

def mouse(button, state, x, y):
    global blink
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Convert screen coordinates to OpenGL coordinates
        x_gl = (x - 250)
        y_gl = (250 - y)
        
        # Generate a new random point at the click position
        new_point = Point(x_gl, y_gl)
        points.append(new_point)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Toggle blink
        blink = not blink

def keyboard(key, x, y):
    global speed, freeze
    if key == b' ':
        # Toggle freeze state
        freeze = not freeze
    glutPostRedisplay()

def special_keys(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        # Increase speed
        speed += 0.1
        for point in points:
            point.dx *= 1.1
            point.dy *= 1.1
    elif key == GLUT_KEY_DOWN:
        # Decrease speed
        speed = max(0.1, speed - 0.1)  # Prevent negative speed
        for point in points:
            point.dx *= 0.9
            point.dy *= 0.9
    glutPostRedisplay()

def setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-BOX_SIZE, BOX_SIZE, -BOX_SIZE, BOX_SIZE, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# Program entry point
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Amazing Box")
glutDisplayFunc(display)
glutTimerFunc(33, update, 0)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
init()
setup()
glutMainLoop()