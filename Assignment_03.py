from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
from math import sin, cos, radians

class GameState:
    def __init__(self):
        self.player_pos = [0, 0, 0]
        self.gun_angle = 0
        self.player_life = 5
        self.score = 0
        self.bullets_missed = 0
        self.game_over = False
        self.last_hit_time = 0

        self.camera_pos = [0, 500, 500]
        self.target_camera_pos = [0, 500, 500]
        self.camera_angle = 0
        self.first_person_mode = False

        self.bullets = []
        self.enemies = []
        self.cheat_mode = False
        self.cheat_vision = False  
        self.circle_angle = 0 
        self.circle_radius = 200 
        self.circle_center = [0, 0] 

        self.GRID_LENGTH = 600
        self.GRID_SPACING = 50
        self.fovY = 120
        self.enemy_speed = 0.1 
        self.MIN_SPAWN_DISTANCE = 400  

game = GameState()

def init_game():
    game.enemies = []

    for _ in range(5):
        enemy = spawn_enemy()
        game.enemies.append(enemy)
    
    game.player_pos = [0, 0, 0]

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()      
    glRasterPos2f(x, y)    
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    glPushMatrix()
    glTranslatef(game.player_pos[0], game.player_pos[1], game.player_pos[2])
    
    if game.game_over:
        glRotatef(90, 1, 0, 0)
    else:
        glRotatef(game.gun_angle, 0, 0, 1)
    
    # Colors
    HEAD_COLOR = (0.8, 0.7, 0.6)  
    BODY_COLOR = (0.4, 0.6, 0.4)  
    LIMB_COLOR = (0.2, 0.2, 0.8) 
    
    # Head (sphere)
    glColor3f(*HEAD_COLOR)
    glPushMatrix()
    glTranslatef(0, 0, 50)  
    glutSolidSphere(10, 20, 20)
    glPopMatrix()
    
    # Body (cuboid)
    glColor3f(*BODY_COLOR)
    glPushMatrix()
    glTranslatef(0, 0, 25) 
    glScalef(20, 15, 30)   
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.5, 0.5, 0.5)  # Gray gun
    glPushMatrix()

    glTranslatef(20, 0, 40) 
    glRotatef(90, 0, 1, 0)   

    gluCylinder(gluNewQuadric(), 5, 5, 25, 10, 1) 
    glPopMatrix()
    
    #flash effect
    current_time = glutGet(GLUT_ELAPSED_TIME)       
    if current_time - game.last_hit_time < 1000:
        flash_intensity = 0.5 + 0.5 * sin(current_time * 0.01)
        glColor3f(0, flash_intensity, 1)  
    else:
        glColor3f(0, 0, 1) 
    
    # Draw player body
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

def draw_enemies():
    current_time = glutGet(GLUT_ELAPSED_TIME)
    pulse_speed = 0.003  # enemy speed faster 
    
    for enemy in game.enemies:
        glPushMatrix()      
        glTranslatef(enemy['pos'][0], enemy['pos'][1], enemy['pos'][2])
        

        scale = 1 + 0.15 * math.sin(current_time * pulse_speed + enemy['pulse_offset'])   
        glScalef(scale, scale, scale)
        
        #enemy body
        glColor3f(1, 0, 0) 
        glutSolidSphere(15, 20, 20)
        
        glPopMatrix()

def draw_bullets():
    glColor3f(1, 1, 0)  
    for bullet in game.bullets:
        glPushMatrix()
        glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
        glutSolidCube(5)
        glPopMatrix()

def draw_grid():
    glPushMatrix()
    
    glBegin(GL_QUADS)
    rows = 12 
    cols = 8   
    
    grid_length = game.GRID_LENGTH
    width_per_cell = (grid_length * 2) / cols
    length_per_cell = (grid_length * 2) / rows
    
    for i in range(-cols//2, cols//2):
        for j in range(-rows//2, rows//2):
            if (i + j) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)  
            else:
                glColor3f(0.8, 0.6, 1.0)  
            
            x1 = i * width_per_cell
            x2 = (i + 1) * width_per_cell
            y1 = j * length_per_cell
            y2 = (j + 1) * length_per_cell
            
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()

    glBegin(GL_QUADS)

    glColor3f(0, 0, 1)
    glVertex3f(-350, -350, 0)
    glVertex3f(-300, -350, 0)
    glVertex3f(-300, 350, 0)
    glVertex3f(-350, 350, 0)

    glColor3f(0, 1, 0)
    glVertex3f(300, -350, 0)
    glVertex3f(350, -350, 0)
    glVertex3f(350, 350, 0)
    glVertex3f(300, 350, 0)

    glColor3f(0, 1, 1)
    glVertex3f(-350, 300, 0)
    glVertex3f(350, 300, 0)
    glVertex3f(350, 350, 0)
    glVertex3f(-350, 350, 0)
    glEnd()
    
    glPopMatrix()

def spawn_enemy():
    # Spawn enemy
    angle = random.uniform(0, 2 * math.pi)
    min_distance = 200  #spawn distance
    max_distance = game.GRID_LENGTH - 50  #prevent spawning outside 
    
    while True:
        distance = random.uniform(min_distance, max_distance)
        x = game.player_pos[0] + math.cos(angle) * distance
        y = game.player_pos[1] + math.sin(angle) * distance
        

        if (abs(x) <= game.GRID_LENGTH - 50 and 
            abs(y) <= game.GRID_LENGTH - 50):
            return {
                'pos': [x, y, 20],  
                'pulse_offset': random.random() * math.pi * 2, 
                'radius': 15
            }

def update_bullets():
    bullets_to_remove = set() 
    enemies_to_remove = set()
    
    for i, bullet in enumerate(game.bullets):
        angle_rad = math.radians(bullet['angle'])
        bullet_speed = 25 if game.cheat_mode else 15  # Faster bullets 
        
        if game.cheat_mode:
            #  adjust bullet direction 
            nearest_enemy = None
            min_distance = float('inf')
            
            for enemy in game.enemies:
                dx = enemy['pos'][0] - bullet['pos'][0]
                dy = enemy['pos'][1] - bullet['pos'][1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_enemy = enemy
            
            # Adjust bullet direction 
            if nearest_enemy and min_distance < 600:
                dx = nearest_enemy['pos'][0] - bullet['pos'][0]
                dy = nearest_enemy['pos'][1] - bullet['pos'][1]
                target_angle = math.atan2(dy, dx)
                current_angle = angle_rad
                
                #adjust angle
                angle_diff = target_angle - current_angle
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                while angle_diff < -math.pi:
                    angle_diff += 2 * math.pi
                
                # Adjust angle by 15% 
                adjusted_angle = current_angle + angle_diff * 0.15
                bullet['angle'] = math.degrees(adjusted_angle) % 360
                angle_rad = adjusted_angle
        
        # Update bullet position
        bullet['pos'][0] += math.cos(angle_rad) * bullet_speed
        bullet['pos'][1] += math.sin(angle_rad) * bullet_speed
        
        # enemy collisions
        hit_enemy = False
        for j, enemy in enumerate(game.enemies):
            if j in enemies_to_remove:  
                continue
                
            dx = bullet['pos'][0] - enemy['pos'][0]
            dy = bullet['pos'][1] - enemy['pos'][1]

            distance = math.sqrt(dx*dx + dy*dy)

            hit_radius = 150 if game.cheat_mode else 40
            if distance < hit_radius:
                bullets_to_remove.add(i)
                enemies_to_remove.add(j)
                game.score += 10
                hit_enemy = True
                break
        
        if not hit_enemy:
            if (abs(bullet['pos'][0]) > game.GRID_LENGTH or 
                abs(bullet['pos'][1]) > game.GRID_LENGTH):
                bullets_to_remove.add(i)
                if not game.cheat_mode:  # Only count missed bullets in normal mode
                    game.bullets_missed += 1
                    print("\nBullet Missed!")
                    print(f"Total Bullets Missed: {game.bullets_missed}")
                    print(f"Player Life: {game.player_life}")
                    print("-" * 30)
    
    # Remove bullets and enemies
    for i in sorted(bullets_to_remove, reverse=True):
        if i < len(game.bullets):
            game.bullets.pop(i)
    
    for j in sorted(enemies_to_remove, reverse=True):
        if j < len(game.enemies):
            game.enemies.pop(j)
            game.enemies.append(spawn_enemy())

def update_enemies():
    if game.game_over:
        return
    
    while len(game.enemies) < 5:
        game.enemies.append(spawn_enemy())
    
    current_time = glutGet(GLUT_ELAPSED_TIME)
    difficulty_factor = min(game.score / 300, 1.5)
    current_speed = game.enemy_speed * (1 + 0.2 * difficulty_factor)
    
    for enemy in game.enemies:
        # Move to player
        dx = game.player_pos[0] - enemy['pos'][0]
        dy = game.player_pos[1] - enemy['pos'][1]
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            enemy['pos'][0] += (dx/dist) * current_speed
            enemy['pos'][1] += (dy/dist) * current_speed

            enemy['pos'][0] = max(-game.GRID_LENGTH + 20, 
                                min(game.GRID_LENGTH - 20, enemy['pos'][0]))
            enemy['pos'][1] = max(-game.GRID_LENGTH + 20, 
                                min(game.GRID_LENGTH - 20, enemy['pos'][1]))
        
        if dist < 35: 
            if current_time - game.last_hit_time > 1000: 
                game.player_life -= 1
                game.last_hit_time = current_time

                knockback_dist = 100
                if dist > 0:
                    enemy['pos'][0] = game.player_pos[0] + (dx/dist) * knockback_dist
                    enemy['pos'][1] = game.player_pos[1] + (dy/dist) * knockback_dist
                
                if game.player_life <= 0:
                    game.game_over = True
                    print("\nGAME OVER!")
                    print(f"Final Score: {game.score}")
                    print(f"Total Bullets Fired: {len(game.bullets)}")
                    print(f"Total Bullets Missed: {game.bullets_missed}")
                    print("-" * 30)

def fire_bullet():
    if game.game_over:
        return
    
    if not game.cheat_mode and len(game.bullets) >= 10: 
        return

    angle_rad = math.radians(game.gun_angle)
    gun_base_distance = 20  
    gun_length = 25  
    gun_tip_distance = gun_base_distance + gun_length  
    gun_height = 40 
    
    start_x = game.player_pos[0] + math.cos(angle_rad) * gun_tip_distance
    start_y = game.player_pos[1] + math.sin(angle_rad) * gun_tip_distance
    start_z = gun_height 

    game.bullets.append({
        'pos': [start_x, start_y, start_z],
        'angle': game.gun_angle
    })

    print("\nBullet Fired!")
    print(f"Bullets Fired: {len(game.bullets)}")
    print(f"Bullets Missed: {game.bullets_missed}")
    print(f"Player Life: {game.player_life}")
    print("-" * 30)

def keyboardListener(key, x, y):
    if game.game_over:
        if key == b'r':
            reset_game()
        return
    
    key = key.decode('utf-8').lower()
    movement_speed = 15 

    if key == 'w':  # Forward
        move_x = cos(radians(game.gun_angle)) * movement_speed
        move_y = sin(radians(game.gun_angle)) * movement_speed
        game.player_pos[0] = max(-game.GRID_LENGTH+50, min(game.GRID_LENGTH-50, 
                                     game.player_pos[0] + move_x))
        game.player_pos[1] = max(-game.GRID_LENGTH+50, min(game.GRID_LENGTH-50, 
                                     game.player_pos[1] + move_y))
    elif key == 's':  # Backward
        move_x = cos(radians(game.gun_angle)) * movement_speed
        move_y = sin(radians(game.gun_angle)) * movement_speed
        game.player_pos[0] = max(-game.GRID_LENGTH+50, min(game.GRID_LENGTH-50, 
                                     game.player_pos[0] - move_x))
        game.player_pos[1] = max(-game.GRID_LENGTH+50, min(game.GRID_LENGTH-50, 
                                     game.player_pos[1] - move_y))
    elif key == 'a' and not game.cheat_mode:
        game.gun_angle = (game.gun_angle + 5) % 360
    elif key == 'd' and not game.cheat_mode: 
        game.gun_angle = (game.gun_angle - 5) % 360
    elif key == 'c': 
        game.cheat_mode = not game.cheat_mode
        if not game.cheat_mode:
            game.cheat_vision = False  
    elif key == 'v' and game.cheat_mode:
        game.first_person_mode = not game.first_person_mode

        if game.first_person_mode:
            game.cheat_vision = True
        else:
            game.cheat_vision = False


def specialKeyListener(key, x, y):
    if not game.first_person_mode: 
        if key == GLUT_KEY_LEFT:
            game.camera_angle = (game.camera_angle + 5) % 360
        elif key == GLUT_KEY_RIGHT:
            game.camera_angle = (game.camera_angle - 5) % 360
    
    if key == GLUT_KEY_UP:
        game.camera_pos[2] = min(1000, game.camera_pos[2] + 10)  # Add upper limit
    elif key == GLUT_KEY_DOWN:
        game.camera_pos[2] = max(100, game.camera_pos[2] - 10)   # Add lower limit

def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        game.first_person_mode = not game.first_person_mode
        if not game.first_person_mode:
            game.cheat_vision = False

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if game.first_person_mode: 
        angle_rad = radians(game.gun_angle)
        #rotates continuously in cheat mode
        camera_x = game.player_pos[0] - 80 * cos(angle_rad) 
        camera_y = game.player_pos[1] - 80 * sin(angle_rad)
        camera_z = 100  

        look_x = game.player_pos[0] + cos(angle_rad) * 100
        look_y = game.player_pos[1] + sin(angle_rad) * 100
        look_z = 20  
        
        gluLookAt(camera_x, camera_y, camera_z,  
                  look_x, look_y, look_z,        
                  0, 0, 1)                      
    else: 
    
        camera_x = 500 * sin(radians(game.camera_angle))
        camera_y = 500 * cos(radians(game.camera_angle))
        
        gluLookAt(camera_x, camera_y, game.camera_pos[2],  # Camera position
                  0, 0, 0,                                  # Look at center
                  0, 0, 1)                                  # Up vector

def idle():
    if not game.game_over:
        if game.cheat_mode:
            #rotate gun
            game.gun_angle = (game.gun_angle + 2) % 360
           # Auto-fire bullets 
            current_time = glutGet(GLUT_ELAPSED_TIME)
            if current_time % 20 == 0:  
                for enemy in game.enemies:
                    dx = enemy['pos'][0] - game.player_pos[0]
                    dy = enemy['pos'][1] - game.player_pos[1]
                    angle_to_enemy = math.degrees(math.atan2(dy, dx)) % 360
                    angle_diff = min((game.gun_angle - angle_to_enemy) % 360, 
                                   (angle_to_enemy - game.gun_angle) % 360)
                    
                    if angle_diff < 15:  # 15 degree firing
                        fire_bullet()
                        break
        
        update_bullets()
        update_enemies()

        if game.player_life <= 0 or (not game.cheat_mode and game.bullets_missed >= 10):
            game.game_over = True
    
    glutPostRedisplay()

def reset_game():
    game.player_life = 5
    game.score = 0
    game.bullets_missed = 0

    game.player_pos = [0, 0, 0]
    game.gun_angle = 0
    game.game_over = False
    game.last_hit_time = 0
    game.circle_angle = 0 

    game.bullets = []
    game.enemies = []

    game.cheat_mode = False
    game.cheat_vision = False
    game.first_person_mode = False
 
    game.camera_pos = [0, 500, 500]
    game.target_camera_pos = [0, 500, 500]
    game.camera_angle = 0

    game.enemy_speed = 0.1

    init_game()

    print("\nGame Reset!")
    print(f"Player Life: {game.player_life}")
    print(f"Score: {game.score}")
    print(f"Bullets Missed: {game.bullets_missed}")
    print("-" * 30)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    setupCamera()

    draw_grid()
    draw_player()
    draw_enemies()
    draw_bullets()

    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 770, f"Player Life Remaining: {game.player_life}")
    draw_text(10, 740, f"Game Score: {game.score}")
    draw_text(10, 710, f"Player Bullet Missed: {game.bullets_missed}")
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy - 3D Game")
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    
    reset_game()
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()