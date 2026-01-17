import pygame
import numpy as np
from pygame.locals import *

# ========================================
# INISIALISASI PYGAME
# ========================================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animasi 3D Kubus - Grafika Komputer")
clock = pygame.time.Clock()

# ========================================
# KONSTANTA DAN VARIABEL GLOBAL
# ========================================
# Jarak kamera dari layar proyeksi (untuk perspektif)
FOCAL_LENGTH = 400

# Posisi sumber cahaya (untuk shading)
LIGHT_DIRECTION = np.array([0.5, -1, -0.5])
LIGHT_DIRECTION = LIGHT_DIRECTION / np.linalg.norm(LIGHT_DIRECTION)

# Variabel transformasi objek
rotation_x = 0
rotation_y = 0
rotation_z = 0
position = np.array([0.0, 0.0, 5.0])  # Posisi awal kubus (z=5 agar terlihat)
scale_factor = 1.0

# Kecepatan animasi otomatis
auto_rotate_speed = 0.02

# ========================================
# DEFINISI KUBUS 3D
# ========================================
# Vertex kubus (8 titik sudut)
vertices = np.array([
    [-1, -1, -1],  # 0
    [ 1, -1, -1],  # 1
    [ 1,  1, -1],  # 2
    [-1,  1, -1],  # 3
    [-1, -1,  1],  # 4
    [ 1, -1,  1],  # 5
    [ 1,  1,  1],  # 6
    [-1,  1,  1],  # 7
], dtype=float)

# Face kubus (6 sisi, setiap sisi adalah quadrilateral)
# Format: [v0, v1, v2, v3] - urutan berlawanan arah jarum jam (CCW)
faces = [
    [0, 1, 2, 3],  # Depan
    [1, 5, 6, 2],  # Kanan
    [5, 4, 7, 6],  # Belakang
    [4, 0, 3, 7],  # Kiri
    [3, 2, 6, 7],  # Atas
    [4, 5, 1, 0],  # Bawah
]

# Warna dasar setiap face
face_colors = [
    (255, 0, 0),    # Merah
    (0, 255, 0),    # Hijau
    (0, 0, 255),    # Biru
    (255, 255, 0),  # Kuning
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

# ========================================
# FUNGSI TRANSFORMASI GEOMETRIS
# ========================================
def create_rotation_matrix_x(angle):
    """Matriks rotasi sumbu X"""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,  0],
        [0, c, -s],
        [0, s,  c]
    ])

def create_rotation_matrix_y(angle):
    """Matriks rotasi sumbu Y"""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])

def create_rotation_matrix_z(angle):
    """Matriks rotasi sumbu Z"""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

def transform_vertices(verts):
    """
    Menerapkan transformasi geometris ke semua vertex:
    1. Skala
    2. Rotasi (X, Y, Z)
    3. Translasi
    """
    # 1. SKALA
    transformed = verts * scale_factor
    
    # 2. ROTASI (perkalian matriks)
    rotation_mat = (
        create_rotation_matrix_z(rotation_z) @
        create_rotation_matrix_y(rotation_y) @
        create_rotation_matrix_x(rotation_x)
    )
    transformed = transformed @ rotation_mat.T
    
    # 3. TRANSLASI
    transformed += position
    
    return transformed

# ========================================
# PROYEKSI PERSPEKTIF 3D → 2D
# ========================================
def project_perspective(point_3d):
    """
    KONSEP PERSPEKTIF:
    Proyeksi perspektif membuat objek yang lebih jauh terlihat lebih kecil.
    
    Rumus:
    x_2d = (x_3d * focal_length) / z_3d
    y_2d = (y_3d * focal_length) / z_3d
    
    Semakin besar z (jauh dari kamera), semakin kecil hasil proyeksi.
    """
    x, y, z = point_3d
    
    # Hindari pembagian dengan nol
    if z <= 0.1:
        z = 0.1
    
    # Proyeksi perspektif
    factor = FOCAL_LENGTH / z
    x_2d = x * factor + WIDTH / 2
    y_2d = -y * factor + HEIGHT / 2  # Y terbalik di layar
    
    return int(x_2d), int(y_2d)

# ========================================
# KALKULASI NORMAL DAN SHADING
# ========================================
def calculate_face_normal(face_vertices):
    """
    Menghitung vektor normal permukaan menggunakan cross product.
    Normal digunakan untuk menentukan orientasi dan shading face.
    """
    v0, v1, v2 = face_vertices[0], face_vertices[1], face_vertices[2]
    
    # Dua edge dari face
    edge1 = v1 - v0
    edge2 = v2 - v0
    
    # Cross product menghasilkan vektor normal
    normal = np.cross(edge1, edge2)
    
    # Normalisasi vektor
    norm = np.linalg.norm(normal)
    if norm > 0:
        normal = normal / norm
    
    return normal

def calculate_shading(normal):
    """
    KONSEP CAHAYA & BAYANGAN:
    Menggunakan dot product antara normal permukaan dan arah cahaya.
    
    Dot product = cos(θ) dimana θ adalah sudut antara dua vektor.
    - Jika normal searah dengan cahaya (θ=0°): terang (dot=1)
    - Jika normal tegak lurus cahaya (θ=90°): redup (dot=0)
    - Jika normal berlawanan arah (θ=180°): gelap (dot=-1)
    """
    # Dot product antara normal dan arah cahaya
    intensity = np.dot(normal, -LIGHT_DIRECTION)
    
    # Clamp antara 0.2 (ambient) sampai 1.0 (fully lit)
    intensity = max(0.2, min(1.0, intensity))
    
    return intensity

def apply_shading(color, intensity):
    """Mengaplikasikan intensitas cahaya ke warna RGB"""
    return tuple(int(c * intensity) for c in color)

# ========================================
# DEPTH SORTING (PAINTER'S ALGORITHM)
# ========================================
def get_face_depth(face_vertices):
    """
    KONSEP OVERLAPPING:
    Menghitung kedalaman rata-rata face untuk sorting.
    Face dengan z lebih besar (lebih jauh) digambar terlebih dahulu.
    """
    return np.mean([v[2] for v in face_vertices])

# ========================================
# FUNGSI RENDER
# ========================================
def render_cube(transformed_verts):
    """
    Merender kubus dengan:
    1. Backface culling (tidak render face yang membelakangi kamera)
    2. Depth sorting (Painter's Algorithm)
    3. Shading berdasarkan cahaya
    4. Proyeksi perspektif
    """
    face_data = []
    
    for i, face in enumerate(faces):
        # Ambil vertex 3D dari face
        face_verts_3d = transformed_verts[face]
        
        # Hitung normal face
        normal = calculate_face_normal(face_verts_3d)
        
        # BACKFACE CULLING: 
        # Hanya render face yang menghadap kamera (normal.z < 0)
        view_direction = np.array([0, 0, -1])
        if np.dot(normal, view_direction) <= 0:
            continue
        
        # Hitung intensitas cahaya
        intensity = calculate_shading(normal)
        
        # Hitung kedalaman untuk sorting
        depth = get_face_depth(face_verts_3d)
        
        # Proyeksikan vertex ke 2D
        face_verts_2d = [project_perspective(v) for v in face_verts_3d]
        
        # Simpan data face untuk dirender
        face_data.append({
            'depth': depth,
            'vertices_2d': face_verts_2d,
            'color': face_colors[i],
            'intensity': intensity
        })
    
    # OVERLAPPING: Sort berdasarkan depth (jauh ke dekat)
    face_data.sort(key=lambda f: f['depth'], reverse=True)
    
    # Render semua face
    for face in face_data:
        color = apply_shading(face['color'], face['intensity'])
        pygame.draw.polygon(screen, color, face['vertices_2d'])
        # Gambar outline hitam
        pygame.draw.polygon(screen, (0, 0, 0), face['vertices_2d'], 2)

# ========================================
# FUNGSI KONTROL KEYBOARD
# ========================================
def handle_input(keys):
    """
    INTERAKSI KEYBOARD:
    A/D - Translasi kiri/kanan
    W/S - Translasi atas/bawah
    Q/E - Translasi depan/belakang
    X/C - Rotasi sumbu X
    Y/H - Rotasi sumbu Y
    Z/V - Rotasi sumbu Z
    +/- - Skala
    """
    global position, rotation_x, rotation_y, rotation_z, scale_factor
    
    speed = 0.1
    rot_speed = 0.05
    scale_speed = 0.02
    
    # Translasi
    if keys[K_a]:
        position[0] -= speed
    if keys[K_d]:
        position[0] += speed
    if keys[K_w]:
        position[1] += speed
    if keys[K_s]:
        position[1] -= speed
    if keys[K_q]:
        position[2] += speed
    if keys[K_e]:
        position[2] -= speed
    
    # Rotasi
    if keys[K_x]:
        rotation_x += rot_speed
    if keys[K_c]:
        rotation_x -= rot_speed
    if keys[K_y]:
        rotation_y += rot_speed
    if keys[K_h]:
        rotation_y -= rot_speed
    if keys[K_z]:
        rotation_z += rot_speed
    if keys[K_v]:
        rotation_z -= rot_speed
    
    # Skala
    if keys[K_PLUS] or keys[K_EQUALS]:
        scale_factor += scale_speed
    if keys[K_MINUS]:
        scale_factor = max(0.1, scale_factor - scale_speed)

# ========================================
# LOOP UTAMA
# ========================================
def main():
    global rotation_y
    
    running = True
    font = pygame.font.Font(None, 24)
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
        
        # Input keyboard
        keys = pygame.key.get_pressed()
        handle_input(keys)
        
        # Animasi otomatis (rotasi Y)
        rotation_y += auto_rotate_speed
        
        # Clear screen
        screen.fill((30, 30, 40))
        
        # Transformasi dan render
        transformed = transform_vertices(vertices)
        render_cube(transformed)
        
        # Tampilkan kontrol
        instructions = [
            "KONTROL:",
            "A/D: Kiri/Kanan | W/S: Atas/Bawah | Q/E: Jauh/Dekat",
            "X/C: Rotasi X | Y/H: Rotasi Y | Z/V: Rotasi Z",
            "+/-: Skala | ESC: Keluar"
        ]
        
        y_offset = 10
        for text in instructions:
            surface = font.render(text, True, (255, 255, 255))
            screen.blit(surface, (10, y_offset))
            y_offset += 25
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

# ========================================
# JALANKAN PROGRAM
# ========================================
if __name__ == "__main__":
    main()