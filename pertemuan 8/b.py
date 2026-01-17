import cv2
import mediapipe as mp
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# =====================
# GLOBAL VAR
# =====================
rot_y = 0
scale = 1.0
pos_x = 0

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# =====================
# DRAW CUBE
# =====================
def draw_cube():
    glBegin(GL_QUADS)

    glColor3f(0.2, 0.8, 1.0)
    vertices = [
        [1,1,-1], [-1,1,-1], [-1,1,1], [1,1,1],
        [1,-1,1], [-1,-1,1], [-1,-1,-1], [1,-1,-1]
    ]

    faces = [
        [0,1,2,3], [3,2,5,4], [4,5,6,7],
        [7,6,1,0], [1,6,5,2], [7,0,3,4]
    ]

    for face in faces:
        for v in face:
            glVertex3fv(vertices[v])

    glEnd()

# =====================
# DISPLAY
# =====================
def display():
    global rot_y, scale, pos_x

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        index = hand.landmark[8]

        rot_y = index.x * 360
        scale = 0.5 + index.y
        pos_x = (index.x - 0.5) * 4

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 3, 8, 0, 0, 0, 0, 1, 0)

    glTranslatef(pos_x, 0, 0)     # Translasi
    glRotatef(rot_y, 0, 1, 0)     # Rotasi
    glScalef(scale, scale, scale) # Skala

    draw_cube()

    glutSwapBuffers()
    glutPostRedisplay()

# =====================
# INIT
# =====================
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.3, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)

# =====================
# MAIN
# =====================
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Gesture 3D Building")
init()
glutDisplayFunc(display)
glutMainLoop()
