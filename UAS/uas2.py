import pygame
from pygame.locals import *
import pygame.image
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys
import os

# =================================================================
# GLOBAL STATE (Kamera, Animasi, & Waktu)
# =================================================================
cam_pos = [0.0, 8.0, 40.0]  # Posisi awal kamera
yaw = -90.0
pitch = -15.0
world_time = 0.0  # Waktu global untuk animasi dan siang/malam

# =================================================================
# 1. INISIALISASI OPENGL (init_opengl)
# =================================================================
def init_opengl(display):
    # Proyeksi perspektif 3D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 300.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Lighting Utama akan diupdate dinamis di main loop
    glEnable(GL_LIGHT0) # Lampu Jalan (Point Light)
    glEnable(GL_LIGHT1) # Matahari/Bulan (Directional Light)

# =================================================================
# 2. HELPER OBJEK (draw_cube & draw_sphere)
# =================================================================
def draw_cube(w, h, d):
    glBegin(GL_QUADS)
    # Depan
    glNormal3f(0, 0, 1); glVertex3f(-w, 0, d); glVertex3f(w, 0, d); glVertex3f(w, h, d); glVertex3f(-w, h, d)
    # Belakang
    glNormal3f(0, 0, -1); glVertex3f(-w, 0, -d); glVertex3f(w, 0, -d); glVertex3f(w, h, -d); glVertex3f(-w, h, -d)
    # Atas
    glNormal3f(0, 1, 0); glVertex3f(-w, h, -d); glVertex3f(w, h, -d); glVertex3f(w, h, d); glVertex3f(-w, h, d)
    # Samping
    glNormal3f(1, 0, 0); glVertex3f(w, 0, -d); glVertex3f(w, h, -d); glVertex3f(w, h, d); glVertex3f(w, 0, d)
    glNormal3f(-1, 0, 0); glVertex3f(-w, 0, -d); glVertex3f(-w, h, -d); glVertex3f(-w, h, d); glVertex3f(-w, 0, d)
    glEnd()

def draw_sphere(radius, color):
    glColor3f(*color)
    quad = gluNewQuadric()
    gluSphere(quad, radius, 16, 16)
    gluDeleteQuadric(quad)

def draw_cylinder(radius, height, slices=16, color=(0.2, 0.2, 0.2)):
    """Menggambar silinder vertikal (sumbu Y)."""
    glDisable(GL_TEXTURE_2D)
    glColor3f(*color)
    quad = gluNewQuadric()
    
    glPushMatrix()
    glTranslatef(0, -height/2, 0) # Center vertically
    
    # Rotasi seluruh objek agar sumbu Z (default GLUT) menjadi Y
    glRotatef(-90, 1, 0, 0)
    
    # Tutup Bawah (Z=0 lokal -> Y=0 global sebelum rotasi)
    gluDisk(quad, 0, radius, slices, 1)
    
    # Selimut (Sepanjang Z lokal -> Y global)
    gluCylinder(quad, radius, radius, height, slices, 1)
    
    # Tutup Atas (Z=height lokal -> Y=height global)
    glTranslatef(0, 0, height)
    gluDisk(quad, 0, radius, slices, 1)
    
    glPopMatrix()
    gluDeleteQuadric(quad)

def load_texture(filename):
    path = os.path.join("assets", filename)
    if not os.path.exists(path):
        print(f"Texture not found: {path}")
        return None
    textureSurface = pygame.image.load(path)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texid

def draw_sky_dome(tex_day, tex_night, day_factor):
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND) # Pastikan Blend aktif untuk transisi opacity
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 1, 1, 1)
    
    # Simpan state depth buffer agar sky dome dirender *di belakang* segalanya
    glDepthMask(GL_FALSE)
    
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    
    # 1. NIGHT SKY (Base Layer - Always Drawn)
    # Layer Paling Belakang (Radius 200)
    glBindTexture(GL_TEXTURE_2D, tex_night)
    glColor4f(1, 1, 1, 1.0) 
    glPushMatrix()
    glRotatef(90, 1, 0, 0) 
    gluSphere(quad, 200, 32, 32)
    glPopMatrix()
    
    # 2. DAY SKY (Overlay dengan Alpha = day_factor)
    # Layer Depan (Radius 180 - Lebih kecil agar tidak z-fighting sama sekali)
    # Saat day_factor=0, alpha=0 (Invisible). Saat day_factor=1, alpha=1 (Menutupi Malam).
    if day_factor > 0.01:
        glBindTexture(GL_TEXTURE_2D, tex_day)
        glColor4f(1, 1, 1, day_factor) 
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        gluSphere(quad, 180, 32, 32) 
        glPopMatrix()
        
    gluDeleteQuadric(quad)
    glDepthMask(GL_TRUE)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

# =================================================================
# 3. LINGKUNGAN (Water, Sun/Moon)
# =================================================================
def draw_water(texture):
    # ANIMASI TRANSLASI: Efek gelombang sederhana menggunakan world_time
    wave = math.sin(world_time * 2) * 0.1
    glPushMatrix()
    glTranslatef(0, -10 + wave, 0)
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor4f(1, 1, 1, 0.9) # Sedikit transparan dan putih agar tekstur keluar
    
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    # Plane air sangat luas dengan texture tiling
    size = 200
    repeats = 20 # Ulangi tekstur agar detail
    glTexCoord2f(0, 0); glVertex3f(-size, 0, -size)
    glTexCoord2f(repeats, 0); glVertex3f(size, 0, -size)
    glTexCoord2f(repeats, repeats); glVertex3f(size, 0, size)
    glTexCoord2f(0, repeats); glVertex3f(-size, 0, size)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def draw_celestial():
    # KONSEP ROTASI: Matahari dan Bulan mengorbit jembatan (Timur - Barat via Z-Axis)
    # world_time * 10 adalah sudut. Time 0 = Noon.
    orbit_angle = world_time * 10 
    
    # MATAHARI
    glPushMatrix()
    glRotatef(orbit_angle, 0, 0, 1) # Putar di sumbu Z
    glTranslatef(0, 80, 0)          # Posisi awal di Atas (Noon)
    
    # Gambar Matahari (Kuning terang)
    glDisable(GL_LIGHTING) # Agar warna sendiri keluar (emissive look)
    draw_sphere(5, (1, 1, 0.5)) 
    glEnable(GL_LIGHTING)
    
    # Update Posisi Cahaya Matahari (Directional)
    # Posisi light ikut tertransformasi oleh matrix saat ini
    glLightfv(GL_LIGHT1, GL_POSITION, [0, 0, 0, 1]) 
    
    # Setup warna Specular/Diffuse Matahari berdasarkan ketinggian
    # Simplifikasi: Selalu putih kekuningan
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.9, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    glPopMatrix()
    
    # BULAN (Di sisi berlawanan)
    glPushMatrix()
    glRotatef(orbit_angle + 180, 0, 0, 1)
    glTranslatef(0, 80, 0)
    
    glDisable(GL_LIGHTING)
    draw_sphere(3, (0.8, 0.8, 1)) # Putih Kebiruan
    glEnable(GL_LIGHTING)
    
    glPopMatrix()

# =================================================================
# 4. OBJEK DINAMIS (Cars, Boat)
# =================================================================
def draw_car(offset_z, speed, color):
    # ANIMASI TRANSLASI: Mobil bergerak di atas jembatan
    z_pos = ((world_time * speed + offset_z) % 100) - 50
    wheel_rot = -(world_time * speed * 360) / (2 * math.pi * 0.4) 

    glPushMatrix()
    glTranslatef(4, 0.5, z_pos) # Naikkan 0.5 agar di atas jalan
    
    # Arah hadap (Jika speed negatif, putar balik)
    if speed < 0:
        glRotatef(180, 0, 1, 0)
        
    # 2. SHADOW (Bayangan Sederhana - Quad Hitam Transparan)
    glEnable(GL_BLEND)
    glDisable(GL_LIGHTING)
    glColor4f(0, 0, 0, 0.4)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-1.5, 0.05, -3.0); glVertex3f(1.5, 0.05, -3.0)
    glVertex3f(1.5, 0.05, 3.0); glVertex3f(-1.5, 0.05, 3.0)
    glEnd()
    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)

    # 3. BODY MOBIL (Hierarki Objek)
    
    # Chassis Utama (Bawah)
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    glColor3f(*color)
    draw_cube(1.4, 0.5, 3.0) # Body utama (Lebar, Tinggi, Panjang)
    glPopMatrix()

    # Cabin (Atas)
    glPushMatrix()
    glTranslatef(0, 1.2, -0.2)
    glColor3f(0.1, 0.1, 0.1) # Kaca Jendela Gelap
    draw_cube(1.3, 0.4, 1.5) 
    # Atap Mobil (Sedikit lebih kecil dari kaca biar ada frame)
    glTranslatef(0, 0.41, 0)
    glColor3f(*color)
    draw_cube(1.3, 0.05, 1.5)
    glPopMatrix()
    
    # Grill Depan
    glPushMatrix()
    glTranslatef(0, 0.5, 3.01)
    glColor3f(0.2, 0.2, 0.2)
    draw_cube(1.2, 0.3, 0.05)
    glPopMatrix()

    # 4. RODA (4 buah) - ANIMASI ROTASI RODA
    wheel_positions = [
        (1.4, 0.5, 1.8), (1.4, 0.5, -1.8), # Kanan Depan, Kanan Belakang
        (-1.4, 0.5, 1.8), (-1.4, 0.5, -1.8) # Kiri Depan, Kiri Belakang
    ]
    
    for wx, wy, wz in wheel_positions:
        glPushMatrix()
        glTranslatef(wx, wy, wz)       # Posisi lokal roda
        glRotatef(wheel_rot, 1, 0, 0) # ROTASI RODA pada sumbu (Axle) X
        
        # Silinder kita sekarang Vertical (Y). Kita mau Horizontal (X).
        # Putar -90 derajat pada sumbu Z (Y -> X).
        glRotatef(-90, 0, 0, 1) 
        
        draw_cylinder(0.5, 0.4, color=(0.1, 0.1, 0.1))
        # Velg / Rim (Warna Abu/Silver - Silinder lebih kecil sedikit)
        draw_cylinder(0.3, 0.42, color=(0.7, 0.7, 0.7)) 
        glPopMatrix()

    # Lampu Depan (Headlights)
    glPushMatrix()
    glTranslatef(1.0, 0.6, 3.0)
    glColor3f(1, 1, 0.8) # Putih Kuning
    draw_cube(0.2, 0.15, 0.1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-1.0, 0.6, 3.0)
    draw_cube(0.2, 0.15, 0.1)
    glPopMatrix()
    
    # Lampu Belakang (Taillights)
    glPushMatrix()
    glTranslatef(1.0, 0.6, -3.0)
    glColor3f(0.8, 0, 0) # Merah
    draw_cube(0.2, 0.15, 0.1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-1.0, 0.6, -3.0)
    draw_cube(0.2, 0.15, 0.1)
    glPopMatrix()

    glPopMatrix()

def draw_boat():
    # ANIMASI TRANSLASI: Perahu melintas di bawah jembatan
    x_pos = ((world_time * 5) % 300) - 150 
    
    glPushMatrix()
    glTranslatef(x_pos, -9.5, 20)
    
    # --- LAMBUNG (HULL) ---
    # Gunakan GL_TRIANGLE_FAN / STRIP untuk bentuk lambung lebih curve
    glColor3f(0.9, 0.9, 0.9) # Putih
    
    glPushMatrix()
    glScalef(1, 1, 0.8) # Sedikit ramping
    
    # Bagian Tengah - Belakang (Kotak dasar)
    glPushMatrix()
    glTranslatef(-2, 0, 0)
    draw_cube(4, 1.2, 3.0)
    glPopMatrix()
    
    # Bagian Depan (Muncung V-Shape lebih halus)
    glBegin(GL_TRIANGLES)
    # Atas
    glNormal3f(0, 1, 0)
    glVertex3f(2, 1.2, 3.0); glVertex3f(2, 1.2, -3.0); glVertex3f(7, 1.5, 0)
    # Bawah miring kanan
    glNormal3f(1, -1, 1)
    glVertex3f(2, -1.2, 3.0); glVertex3f(7, 1.5, 0); glVertex3f(2, 1.2, 3.0)
    # Bawah miring kiri
    glNormal3f(1, -1, -1)
    glVertex3f(2, -1.2, -3.0); glVertex3f(2, 1.2, -3.0); glVertex3f(7, 1.5, 0)
    # Tutup Bawah Depan
    glNormal3f(0, -1, 0)
    glVertex3f(2, -1.2, 3.0); glVertex3f(7, 0, 0); glVertex3f(2, -1.2, -3.0) # Approx
    glEnd()
    
    glPopMatrix()
    
    # --- DECK (Lantai Kapal) ---
    glPushMatrix()
    glTranslatef(-0.5, 1.3, 0)
    glColor3f(0.6, 0.4, 0.3) # Warna Kayu
    draw_cube(5.5, 0.1, 2.2)
    glPopMatrix()

    # --- CABIN UTAMA ---
    glPushMatrix()
    glTranslatef(-2, 2.5, 0)
    glColor3f(0.1, 0.2, 0.6) # Biru Tua
    draw_cube(1.5, 1.2, 1.8)
    
    # Jendela Cabin
    glColor3f(0.8, 0.9, 1.0) # Kaca Biru Muda
    glPushMatrix(); glTranslatef(0.8, 0.2, 0); draw_cube(0.8, 0.4, 1.85); glPopMatrix()
    glPushMatrix(); glTranslatef(1.51, 0.2, 0); draw_cube(0.1, 0.4, 1.4); glPopMatrix() # Depan
    
    # Atap Cabin
    glTranslatef(0, 1.25, 0)
    glColor3f(1.0, 1.0, 1.0)
    draw_cube(1.7, 0.1, 2.0)
    
    # Radar / Antena simple
    glTranslatef(0, 0.5, 0)
    glColor3f(0.3, 0.3, 0.3)
    draw_cylinder(0.1, 1.0, color=(0.3, 0.3, 0.3))
    
    glPopMatrix()
    
    # --- CEROBONG ASAP ---
    glPushMatrix()
    glTranslatef(-4.5, 2.5, 0)
    glColor3f(0.8, 0.2, 0.2) # Merah
    draw_cylinder(0.6, 1.5, color=(0.8, 0.2, 0.2))
    # Ring hitam
    glTranslatef(0, 0.6, 0)
    draw_cylinder(0.65, 0.3, color=(0.1, 0.1, 0.1))
    
    # Asap
    glEnable(GL_BLEND)
    glTranslatef(0.5, 1.5 + math.sin(world_time*3)*0.5, 0)
    draw_sphere(0.5 + math.sin(world_time)*0.2, (0.9, 0.9, 0.9))
    glTranslatef(0.4, 0.8, 0)
    draw_sphere(0.4, (0.9, 0.9, 0.9))
    glDisable(GL_BLEND)
    glPopMatrix()
    
    # --- PAGAR (RAILING) ---
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)
    # Kanan
    for x in range(-5, 6, 2):
        glVertex3f(x, 1.2, 2.2); glVertex3f(x, 1.8, 2.2)
    glVertex3f(-6, 1.8, 2.2); glVertex3f(5, 1.8, 2.2)
    # Kiri
    for x in range(-5, 6, 2):
        glVertex3f(x, 1.2, -2.2); glVertex3f(x, 1.8, -2.2)
    glVertex3f(-6, 1.8, -2.2); glVertex3f(5, 1.8, -2.2)
    glEnd()

    glPopMatrix()

# =================================================================
# 5. STRUKTUR JEMBATAN
# =================================================================
def draw_bridge_structure(road_texture):
    # 1. Jalan (Deck) - TRANSLASI
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, road_texture)
    glColor3f(1, 1, 1) # Putih agar tekstur asli keluar
    
    glPushMatrix()
    glTranslatef(0, -0.5, 0)
    
    # Manual Draw Cube untuk Road agar bisa kasih texture coords di atas
    w, h, d = 10, 0.5, 50
    glBegin(GL_QUADS)
    # Atas (Jalan)
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0); glVertex3f(-w, h, -d)
    glTexCoord2f(1, 0); glVertex3f(w, h, -d)
    glTexCoord2f(1, 5); glVertex3f(w, h, d) # Repeat 5x sepanjang jalan
    glTexCoord2f(0, 5); glVertex3f(-w, h, d)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
    
    # Sisa sisi jalan (tanpa tekstur / warna solid)
    glColor3f(0.2, 0.2, 0.2)
    draw_cube(10, 0.5, 50) # Timpa dengan kubus biasa (akan z-fight sedikit di atas tapi ketutup tekstur) atau gambar manual sisi lain. 
    # Agar rapi dan tidak z-fight, lebih baik gambar sisi lain manual atau biarkan cube menimpa dan berharap Depth Test handle (tapi texture usually needs separate draw).
    # Simplifikasi: Gambar ulang cube tapi sedikit lebih kecil atau matikan sisi atas.
    # Namun karena draw_cube menggambar semua sisi, kita bisa biarkan draw_cube menggambar "beton" di bawah aspal.
    
    glPopMatrix()
    
    # 2. Tiang Pylon & Kabel (Sisi Kanan)
    glPushMatrix()
    glTranslatef(8, 0, 0)
    # Tower (SKALA)
    glColor3f(0.8, 0.8, 0.8); draw_cube(1, 25, 1)
    # Kabel (ROTASI melalui vertex miring)
    glColor4f(0.9, 0.9, 0.9, 0.6)
    glBegin(GL_LINES)
    for z in range(-30, 31, 6): glVertex3f(0, 24, 0); glVertex3f(0, 0, z)
    glEnd()
    glPopMatrix()
    
    # 3. SISI KIRI (KONSEP REFLEKSI)
    glPushMatrix()
    glScalef(-1, 1, 1) # REFLEKSI Sumbu X
    glTranslatef(8, 0, 0)
    glColor3f(0.8, 0.8, 0.8); draw_cube(1, 25, 1)
    glBegin(GL_LINES)
    for z in range(-30, 31, 6): glVertex3f(0, 24, 0); glVertex3f(0, 0, z)
    glEnd()
    glPopMatrix()

def draw_lamps():
    # Lampu Jalan (Sisi Kanan)
    for z in range(-40, 41, 20):
        glPushMatrix()
        glTranslatef(9.5, 0, z)
        glColor3f(0.4, 0.4, 0.4); draw_cube(0.1, 6, 0.1) # Tiang
        glTranslatef(0, 6, 0); glColor3f(1.0, 1.0, 0.8); draw_cube(0.5, 0.3, 0.5) # Kepala
        glPopMatrix()
    
    # REFLEKSI Lampu ke Sisi Kiri
    glPushMatrix()
    glScalef(-1, 1, 1)
    for z in range(-40, 41, 20):
        glPushMatrix()
        glTranslatef(9.5, 0, z); draw_cube(0.1, 6, 0.1); glTranslatef(0, 6, 0); draw_cube(0.5, 0.3, 0.5)
        glPopMatrix()
    glPopMatrix()

# =================================================================
# 6. KONTROL & LOGIK VIEW
# =================================================================
def handle_controls(keys, dt):
    global cam_pos, yaw, pitch
    move_speed = 15.0 * dt
    rot_speed = 80.0 * dt
    
    # Rotasi Kamera (Arrows)
    if keys[pygame.K_LEFT]:  yaw -= rot_speed
    if keys[pygame.K_RIGHT]: yaw += rot_speed
    if keys[pygame.K_UP]:    pitch += rot_speed
    if keys[pygame.K_DOWN]:  pitch -= rot_speed
    pitch = max(-89, min(89, pitch))
    
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)
    front = [math.cos(rad_yaw) * math.cos(rad_pitch), math.sin(rad_pitch), math.sin(rad_yaw) * math.cos(rad_pitch)]
    right = [math.sin(rad_yaw), 0, -math.cos(rad_yaw)]
    
    # Pergerakan (WASD QE)
    if keys[pygame.K_w]: cam_pos = [cam_pos[i] + front[i] * move_speed for i in range(3)]
    if keys[pygame.K_s]: cam_pos = [cam_pos[i] - front[i] * move_speed for i in range(3)]
    if keys[pygame.K_d]: cam_pos = [cam_pos[i] - right[i] * move_speed for i in range(3)]
    if keys[pygame.K_a]: cam_pos = [cam_pos[i] + right[i] * move_speed for i in range(3)]
    if keys[pygame.K_q]: cam_pos[1] += move_speed
    if keys[pygame.K_e]: cam_pos[1] -= move_speed
    return front

# =================================================================
# 7. MAIN LOOP
# =================================================================
def main():
    global world_time
    pygame.init()
    display = (1100, 750)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("UAS Grafika Komputer - Jembatan Modern Dynamic Scene")
    init_opengl(display)
    clock = pygame.time.Clock()
    
    # Load Textures
    tex_sky_day = load_texture("sky_day.png")
    tex_sky_night = load_texture("sky_night.png")
    tex_sea = load_texture("sea.png")
    tex_asphalt = load_texture("asphalt.png")
    
    while True:
        dt = clock.tick(60) / 1000.0
        world_time += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        
        front = handle_controls(pygame.key.get_pressed(), dt)
        
        # --- SISTEM SIANG MALAM (Dynamic Lighting & Colors) ---
        # Sinkronisasi dengan draw_celestial yang pakai world_time * 10.
        # Saat angle 0 (Noon), Cos(0)=1 -> day_factor=1.
        # Saat angle 180 (Midnight), Cos(180)=-1 -> day_factor=0.
        day_factor = (math.cos(math.radians(world_time * 10)) + 1) / 2.0
        
        # Sky Dome menggantikan glClearColor untuk atmosfer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        look_target = [cam_pos[i] + front[i] for i in range(3)]
        gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], look_target[0], look_target[1], look_target[2], 0, 1, 0)
        
        # --- RENDER SCENE ---
        if tex_sky_day and tex_sky_night:
            draw_sky_dome(tex_sky_day, tex_sky_night, day_factor)
        else:
             glClearColor(0.1 * day_factor, 0.4 * day_factor, 0.8 * day_factor, 1.0)
             
        # Intensitas Cahaya Ambient
        # Siang: 0.6, Malam: 0.2
        amb = 0.2 + 0.4 * day_factor
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [amb, amb, amb, 1.0])
        
        # Atur Lampu Jalan (GL_LIGHT0) - Nyala hanya saat malam
        if day_factor < 0.3: # Ambang batas malam
             glEnable(GL_LIGHT0)
             # Taruh lampu "ambient malam" atau lampu jalan area tengah
             glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 0, 1]) 
             glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.8, 0.4, 1.0]) # Oranye
             glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
             glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        else:
             glDisable(GL_LIGHT0)

        draw_celestial()      # Matahari & Bulan
        
        if tex_sea:
            draw_water(tex_sea)          # Air Sungai Textured
        else:
            draw_water(0) # Fallback handling needed in draw_water if texture invalid, but simpler to just pass texid
            
        draw_bridge_structure(tex_asphalt) 
        draw_lamps()
        
        # Kendaraan & Perahu (ANIMASI TRANSLASI)
        draw_car(0, 15, (0.8, 0.1, 0.1)) # Mobil Merah
        draw_car(30, 12, (0.1, 0.1, 0.8)) # Mobil Biru
        
        # Lajur sebaliknya (REFLEKSI posisi mobil)
        glPushMatrix()
        glScalef(-1, 1, -1) # Refleksi posisi kendaraan
        draw_car(15, 10, (1, 1, 0)) # Mobil Kuning
        glPopMatrix()
        
        draw_boat()           # Perahu di bawah
        
        pygame.display.flip()

if __name__ == "__main__":
    main()