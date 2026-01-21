import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import sys

# ==============================
# KONFIGURASI AWAL
# ==============================
WIDTH, HEIGHT = 1000, 700
FPS = 60

# ==============================
# CLASS PARTICLE
# ==============================
class Particle:
    def __init__(self):
        self.x = random.uniform(-50, 50)
        self.y = random.uniform(-50, 50)
        self.z = random.uniform(-50, -10)
        self.speed = random.uniform(0.5, 2.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.color = (
            random.uniform(0.6, 1.0),
            random.uniform(0.6, 1.0),
            random.uniform(0.6, 1.0)
        )

# ==============================
# CLASS PLANET
# ==============================
class Planet:
    def __init__(self, distance, size, speed, color):
        self.distance = distance
        self.size = size
        self.speed = speed
        self.color = color

# ==============================
# MAIN CLASS
# ==============================
class SolarSystem:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("UAS Grafika Komputer - Solar System")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glClearColor(0.02, 0.02, 0.05, 1)

        gluPerspective(45, WIDTH / HEIGHT, 0.1, 200.0)
        glTranslatef(0, 0, -60)

        # WAKTU
        self.time = 0

        # QUADRIC (GLOBAL - PENTING)
        self.quadric = gluNewQuadric()

        # MATAHARI
        self.sun_size = 5
        self.sun_color = (1.0, 0.8, 0.2)

        # PLANET
        self.planets = [
            Planet(12, 1.2, 1.5, (0.5, 0.7, 1.0)),
            Planet(18, 1.8, 1.0, (1.0, 0.3, 0.3)),
            Planet(25, 2.5, 0.6, (0.4, 1.0, 0.4))
        ]

        # PARTIKEL
        self.particles = [Particle() for _ in range(300)]

    # ==============================
    # BACKGROUND GALAXY
    # ==============================
    def draw_background(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        glBegin(GL_QUADS)
        glColor3f(0.02, 0.02, 0.08)
        glVertex3f(-100, -100, -90)
        glVertex3f(100, -100, -90)
        glVertex3f(100, 100, -90)
        glVertex3f(-100, 100, -90)
        glEnd()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    # ==============================
    # PARTIKEL BINTANG
    # ==============================
    def draw_particles(self):
        glDisable(GL_LIGHTING)
        glPointSize(2)

        glBegin(GL_POINTS)
        for p in self.particles:
            pulse = math.sin(self.time * p.speed + p.angle) * 0.3 + 0.7
            glColor3f(
                p.color[0] * pulse,
                p.color[1] * pulse,
                p.color[2] * pulse
            )
            glVertex3f(p.x, p.y, p.z)
        glEnd()

        glEnable(GL_LIGHTING)

    # ==============================
    # MATAHARI
    # ==============================
    def draw_sun(self):
        glPushMatrix()

        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))
        glColor3f(*self.sun_color)
        glRotatef(self.time * 5, 0, 1, 0)

        # Inti matahari
        gluSphere(self.quadric, self.sun_size, 32, 32)

        # Corona
        glDisable(GL_LIGHTING)
        glColor4f(1.0, 0.7, 0.2, 0.3)
        glScalef(1.2, 1.2, 1.2)
        gluSphere(self.quadric, self.sun_size, 16, 16)
        glEnable(GL_LIGHTING)

        glPopMatrix()

    # ==============================
    # PLANET
    # ==============================
    def draw_planets(self):
        for planet in self.planets:
            glPushMatrix()

            angle = self.time * planet.speed
            x = math.cos(angle) * planet.distance
            z = math.sin(angle) * planet.distance

            glTranslatef(x, 0, z)
            glColor3f(*planet.color)
            gluSphere(self.quadric, planet.size, 24, 24)

            glPopMatrix()

    # ==============================
    # ORBIT
    # ==============================
    def draw_orbits(self):
        glDisable(GL_LIGHTING)
        glColor3f(0.5, 0.5, 0.5)

        for planet in self.planets:
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                angle = 2 * math.pi * i / 100
                glVertex3f(
                    math.cos(angle) * planet.distance,
                    0,
                    math.sin(angle) * planet.distance
                )
            glEnd()

        glEnable(GL_LIGHTING)

    # ==============================
    # MAIN LOOP
    # ==============================
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)
            self.time += 0.02

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # URUTAN RENDER YANG BENAR
            self.draw_background()
            self.draw_particles()
            self.draw_orbits()
            self.draw_sun()
            self.draw_planets()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

# ==============================
# JALANKAN PROGRAM
# ==============================
if __name__ == "__main__":
    SolarSystem().run()
