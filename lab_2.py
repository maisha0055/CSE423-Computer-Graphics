import sys
import os
import random
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global Configurations
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

CATCHER_WIDTH = 80
CATCHER_HEIGHT = 20
CATCHER_Y = 50

DIAMOND_SIZE = 20
INITIAL_DIAMOND_SPEED = 100.0
SPEED_INCREMENT = 5.0

BUTTON_SIZE = 40
BUTTON_PADDING = 10

WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
TEAL = (0.0, 1.0, 1.0)
AMBER = (1.0, 0.6, 0.0)


CHEAT_MODE = False
CATCHER_AUTO_SPEED = 300.0   

catcher_x = float(WINDOW_WIDTH // 2)
catcher_color = WHITE

diamond = None
diamond_speed = INITIAL_DIAMOND_SPEED
score = 0
GAME_OVER = False
PAUSED = False
last_frame_time = time.time()

# Button (x, y, w, h)
back_button_rect = (BUTTON_PADDING, WINDOW_HEIGHT - BUTTON_SIZE - BUTTON_PADDING, BUTTON_SIZE, BUTTON_SIZE)
pause_button_rect = (WINDOW_WIDTH // 2 - BUTTON_SIZE // 2, WINDOW_HEIGHT - BUTTON_SIZE - BUTTON_PADDING, BUTTON_SIZE, BUTTON_SIZE)
exit_button_rect = (WINDOW_WIDTH - BUTTON_SIZE - BUTTON_PADDING, WINDOW_HEIGHT - BUTTON_SIZE - BUTTON_PADDING, BUTTON_SIZE, BUTTON_SIZE)


# Midpoint Line 
def draw_pixel(x, y):
    glVertex2i(int(round(x)), int(round(y)))

def midpoint_line(x1, y1, x2, y2):
    x1 = int(round(x1)); y1 = int(round(y1))
    x2 = int(round(x2)); y2 = int(round(y2))

    zone = find_zone(x1, y1, x2, y2)
    zx1, zy1 = convert_to_zone0(x1, y1, zone)
    zx2, zy2 = convert_to_zone0(x2, y2, zone)

    dx = zx2 - zx1
    dy = zy2 - zy1
    if dx == 0:
        x = zx1
        ys = range(min(zy1, zy2), max(zy1, zy2) + 1)
        for y in ys:
            ox, oy = convert_from_zone0(x, y, zone)
            draw_pixel(ox, oy)
        return

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x = zx1
    y = zy1

    while x <= zx2:
        ox, oy = convert_from_zone0(x, y, zone)
        draw_pixel(ox, oy)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)

    if abs_dx >= abs_dy:
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def convert_to_zone0(x, y, zone):
    if zone == 0:                              # into zone 0
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return -y, x
    if zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    if zone == 0:                                           #from zone0 to original
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y

# Drawing primitives
def draw_diamond(cx, cy):
    half = DIAMOND_SIZE // 2
    glColor3f(*diamond['color'])

    midpoint_line(cx, cy + half, cx + half, cy)   
    midpoint_line(cx + half, cy, cx, cy - half)
    midpoint_line(cx, cy - half, cx - half, cy)
    midpoint_line(cx - half, cy, cx, cy + half)

def draw_catcher():
    top_width = CATCHER_WIDTH + 60     
    bottom_width = CATCHER_WIDTH - 5
    height = CATCHER_HEIGHT

    top_left_x = catcher_x - top_width // 2
    top_right_x = catcher_x + top_width // 2
    bottom_left_x = catcher_x - bottom_width // 2
    bottom_right_x = catcher_x + bottom_width // 2

    top_y = CATCHER_Y + height
    bottom_y = CATCHER_Y

    glColor3f(*catcher_color)
    midpoint_line(top_left_x, top_y, top_right_x, top_y)            
    midpoint_line(top_left_x, top_y, bottom_left_x, bottom_y)         
    midpoint_line(top_right_x, top_y, bottom_right_x, bottom_y)      
    midpoint_line(bottom_left_x, bottom_y, bottom_right_x, bottom_y) 

def draw_button(x, y, w, h, color, icon):
    glColor3f(*color)
    midpoint_line(x, y, x + w, y)      
    midpoint_line(x + w, y, x + w, y + h)      
    midpoint_line(x + w, y + h, x, y + h)       
    midpoint_line(x, y + h, x, y)              

    glColor3f(1, 1, 1)
    if icon == 'arrow':
        midpoint_line(x + 10, y + h // 2, x + 30, y + 10)
        midpoint_line(x + 10, y + h // 2, x + 30, y + h - 10)
    elif icon == 'pause':
        midpoint_line(x + 12, y + 10, x + 12, y + h - 10)
        midpoint_line(x + 22, y + 10, x + 22, y + h - 10)
    elif icon == 'play':
        midpoint_line(x + 12, y + 10, x + 28, y + h // 2)
        midpoint_line(x + 28, y + h // 2, x + 12, y + h - 10)
        midpoint_line(x + 12, y + h - 10, x + 12, y + 10)
    elif icon == 'cross':
        midpoint_line(x + 10, y + 10, x + 30, y + 30)
        midpoint_line(x + 10, y + 30, x + 30, y + 10)


def spawn_diamond():                                    #logic 
    global diamond
    diamond = {
        'x': random.randint(DIAMOND_SIZE // 2, WINDOW_WIDTH - DIAMOND_SIZE // 2),
        'y': WINDOW_HEIGHT - 1,  # start just inside top
        'color': (max(0.2, random.random()), max(0.2, random.random()), max(0.2, random.random()))
    }

def get_aabb(obj):
    if obj == 'catcher':
        return {
            'x': int(round(catcher_x - CATCHER_WIDTH // 2)),
            'y': CATCHER_Y,
            'width': CATCHER_WIDTH,
            'height': CATCHER_HEIGHT
        }
    elif obj == 'diamond':
        return {
            'x': int(round(diamond['x'] - DIAMOND_SIZE // 2)),
            'y': int(round(diamond['y'] - DIAMOND_SIZE // 2)),
            'width': DIAMOND_SIZE,
            'height': DIAMOND_SIZE
        }

def has_collided():
    if not diamond:
        return False
    a = get_aabb('catcher')
    b = get_aabb('diamond')
    return (a['x'] < b['x'] + b['width'] and
            a['x'] + a['width'] > b['x'] and
            a['y'] < b['y'] + b['height'] and
            a['y'] + a['height'] > b['y'])

def update():
    global diamond_speed, score, GAME_OVER, catcher_color, last_frame_time, catcher_x
    current_time = time.time()
    dt = current_time - last_frame_time
    
    if dt > 0.1:
        dt = 0.1
    last_frame_time = current_time

    if not PAUSED and not GAME_OVER:
       
        if CHEAT_MODE and diamond:
           
            dx = diamond['x'] - catcher_x
            if abs(dx) > 1.0:
                move_amount = CATCHER_AUTO_SPEED * dt
                if dx > 0:
                    catcher_x += min(move_amount, dx)
                else:
                    catcher_x -= min(move_amount, -dx)

          
            catcher_x = max(float(CATCHER_WIDTH // 2), min(float(WINDOW_WIDTH - CATCHER_WIDTH // 2), catcher_x))

        if diamond:
            diamond['y'] -= diamond_speed * dt

            if has_collided():
                score += 1
                diamond_speed += SPEED_INCREMENT
                print(f"Diamond caught! Score: {score}")
                spawn_diamond()

            elif diamond['y'] < -DIAMOND_SIZE:
                GAME_OVER = True
                catcher_color = RED
                print(f"Game Over! Final Score: {score}")

    glutPostRedisplay()

def display():                                      #Render
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    if diamond:
        draw_diamond(int(round(diamond['x'])), int(round(diamond['y'])))
    draw_catcher()

    bx, by, bw, bh = back_button_rect
    draw_button(bx, by, bw, bh, TEAL, 'arrow')
    bx, by, bw, bh = pause_button_rect
    draw_button(bx, by, bw, bh, AMBER, 'pause' if not PAUSED else 'play')
    bx, by, bw, bh = exit_button_rect
    draw_button(bx, by, bw, bh, RED, 'cross')

    glEnd()
    glutSwapBuffers()

def keyboard(key, x, y):                                                 # Handlers
    global catcher_x, CHEAT_MODE, PAUSED, GAME_OVER
    if key == b'c':
        CHEAT_MODE = not CHEAT_MODE
        print("Cheat Mode ON" if CHEAT_MODE else "Cheat Mode OFF")
        return

    if key == b' ':
        PAUSED = not PAUSED
        print("Game paused." if PAUSED else "Game resumed.")
        return

    if GAME_OVER or PAUSED or CHEAT_MODE:
        return

    if key == b'a' or key == b'A':
        catcher_x = max(catcher_x - 20, CATCHER_WIDTH // 2)
    elif key == b'd' or key == b'D':
        catcher_x = min(catcher_x + 20, WINDOW_WIDTH - CATCHER_WIDTH // 2)

def mouse(button, state, x, y):
    global GAME_OVER, PAUSED, catcher_color, score, diamond_speed, diamond, CHEAT_MODE
    if state == GLUT_DOWN:
        y = WINDOW_HEIGHT - y
        bx, by, bw, bh = back_button_rect
        if bx <= x <= bx + bw and by <= y <= by + bh:
            score = 0
            diamond_speed = INITIAL_DIAMOND_SPEED
            catcher_color = WHITE
            GAME_OVER = False
            PAUSED = False
            CHEAT_MODE = False
            spawn_diamond()
            print("Starting Over. Score reset.")
            return

        bx, by, bw, bh = pause_button_rect
        if bx <= x <= bx + bw and by <= y <= by + bh:
            PAUSED = not PAUSED
            print("⏸ Game paused." if PAUSED else "▶️ Game resumed.")
            return

        bx, by, bw, bh = exit_button_rect
        if bx <= x <= bx + bw and by <= y <= by + bh:
            print(f"Goodbye! Final Score: {score}")
            try:
                glutLeaveMainLoop()
            except Exception:
                os._exit(0)


def timer(v):                      
    update()
    glutTimerFunc(16, timer, 0)

def main():
    global last_frame_time
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Catch the Diamonds!")
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(0, timer, 0)

    spawn_diamond()
    last_frame_time = time.time()
    print("🎮 Game Started!")
    glutMainLoop()

if __name__ == '__main__':
    main()
