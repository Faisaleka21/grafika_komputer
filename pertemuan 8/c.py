import cv2
import mediapipe as mp
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# =========================
# GLOBAL VARIABLES
# =========================
rot_y = 0.0
pos_x = 0.0
height = 1.0

# =========================
# CAMERA & HAND TRACKING
# =========================
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# =========================
# DRAW BUILDING (EXTRUDED CUBE)
# =========================
def draw_building():
    w = 0.5
    h = 1.0
    d = 0.5

    glBegin(GL_QUADS)
    glColor3f(0.2, 0.8, 1.0)  # blueprint color

    # Front
    glVertex3f(-w, 0, d)
    glVertex3f(w, 0, d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)

    # Back
    glVertex3f(-w, 0, -d)
    glVertex3f(w, 0, -d)
    glVertex3f(w, h, -d)
    glVertex3f(-w, h, -d)

    # Left
    glVertex3f(-w, 0, -d)
    glVertex3f(-w, 0, d)
    glVertex3f(-w, h, d)
    glVertex3f(-w, h, -d)

    # Right
    glVertex3f(w, 0, -d)
    glVertex3f(w, 0, d)
    glVertex3f(w, h, d)
    glVertex3f(w, h, -d)

    # Top
    glVertex3f(-w, h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)

    glEnd()

# =========================
# DISPLAY FUNCTION
# =========================
def display():
    global rot_y, pos_x, height

    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        # distance between thumb & index (pinch)
        dx = index.x - thumb.x
        dy = index.y - thumb.y
        distance = np.sqrt(dx * dx + dy * dy)

        # mapping gesture → transform
        height = max(0.5, distance * 12)
        rot_y = index.x * 360
        pos_x = (index.x - 0.5) * 5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Camera
    gluLookAt(
        0, 4, 8,
        0, 1, 0,
        0, 1, 0
    )

    # Transformations
    glTranslatef(pos_x, 0, 0)        # Translasi
    glRotatef(rot_y, 0, 1, 0)        # Rotasi
    glScalef(1, height, 1)           # Extrusion (tinggi bangunan)

    draw_building()

    glutSwapBuffers()
    glutPostRedisplay()

# =========================
# INITIALIZATION
# =========================
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800 / 600, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)

# =========================
# MAIN PROGRAM
# =========================
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Gesture Based 3D Building - Grafkom")

init()
glutDisplayFunc(display)
glutMainLoop()
