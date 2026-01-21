import pygame
import math
import sys

# Inisialisasi PyGame
pygame.init()

# Konstanta layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TransformBot: Belajar Transformasi Grafika")

# Warna
BACKGROUND = (20, 25, 45)
PLAYER_COLOR = (65, 105, 225)
PLATFORM_COLOR = (50, 205, 50)
PORTAL_COLOR = (220, 20, 60)
TEXT_COLOR = (240, 240, 240)
UI_BG = (30, 30, 50, 200)
GRID_COLOR = (40, 40, 60)
ROTATION_COLOR = (255, 165, 0)
SCALE_COLOR = (138, 43, 226)
REFLECTION_COLOR = (0, 191, 255)
MIRROR_COLOR = (180, 180, 220)

# Font
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

class Player:
    """Kelas untuk player (PixelBot)"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = -12
        self.on_ground = False
        self.color = PLAYER_COLOR
        self.is_reflected = False
        self.reflection_timer = 0
        self.original_color = PLAYER_COLOR
        
    def draw(self, surface):
        """Menggambar player (robot sederhana)"""
        # Efek visual saat refleksi aktif
        current_color = self.color
        if self.is_reflected:
            if self.reflection_timer % 10 < 5:
                current_color = (255, 255, 100)  # Warna kuning saat refleksi
            else:
                current_color = (180, 180, 255)  # Warna biru muda
        
        # Body utama
        pygame.draw.rect(surface, current_color, (self.x, self.y, self.width, self.height), 0, 5)
        
        # Mata (LED)
        pygame.draw.circle(surface, (255, 255, 100), (self.x + 8, self.y + 15), 4)
        pygame.draw.circle(surface, (255, 255, 100), (self.x + self.width - 8, self.y + 15), 4)
        
        # Kaki roda
        pygame.draw.rect(surface, (40, 40, 40), (self.x - 2, self.y + self.height - 5, self.width + 4, 8), 0, 3)
        
    def update(self, platforms):
        """Update posisi player dengan gravitasi"""
        # Update efek refleksi
        if self.is_reflected:
            self.reflection_timer -= 1
            if self.reflection_timer <= 0:
                self.is_reflected = False
                self.color = self.original_color
        
        # TERAPKAN TRANSLASI: Pindahkan player berdasarkan kecepatan
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Batas layar horizontal
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            self.velocity_x = 0
        
        # Terapkan gravitasi
        self.velocity_y += self.gravity
        
        # Cek tabrakan dengan platform
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            if player_rect.colliderect(platform_rect):
                if self.velocity_y > 0:  # Jatuh ke platform
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Menabrak dari bawah
                    self.y = platform.y + platform.height
                    self.velocity_y = 0
        
        # Batas layar bawah
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True
            
        # Batas layar atas
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
    
    def apply_reflection(self, mirror):
        """Menerapkan REFLEKSI terhadap cermin"""
        if self.is_reflected:
            return
            
        # Posisi pusat player sebelum refleksi
        player_center_x = self.x + self.width/2
        player_center_y = self.y + self.height/2
        
        if mirror.orientation == 'vertical':
            # Refleksi terhadap garis vertikal di tengah cermin
            mirror_center_x = mirror.x + mirror.width/2
            
            # Hitung jarak ke cermin
            distance_to_mirror = player_center_x - mirror_center_x
            
            # TERAPKAN REFLEKSI: x' = 2c - x
            new_center_x = mirror_center_x - distance_to_mirror
            new_x = new_center_x - self.width/2
            
            # Refleksikan kecepatan horizontal
            new_velocity_x = -self.velocity_x * 0.7
            
            # Update posisi dan kecepatan
            self.x = new_x
            self.velocity_x = new_velocity_x
            
        else:  # horizontal
            # Refleksi terhadap garis horizontal di tengah cermin
            mirror_center_y = mirror.y + mirror.height/2
            
            # Hitung jarak ke cermin
            distance_to_mirror = player_center_y - mirror_center_y
            
            # TERAPKAN REFLEKSI: y' = 2c - y
            new_center_y = mirror_center_y - distance_to_mirror
            new_y = new_center_y - self.height/2
            
            # Refleksikan kecepatan vertikal
            new_velocity_y = -self.velocity_y * 0.7
            
            # Update posisi dan kecepatan
            self.y = new_y
            self.velocity_y = new_velocity_y
        
        # Aktifkan efek visual refleksi
        self.is_reflected = True
        self.reflection_timer = 30
        self.original_color = self.color
        self.color = (200, 200, 255)

class Platform:
    """Kelas dasar untuk platform"""
    def __init__(self, x, y, width, height, color=PLATFORM_COLOR):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.original_x = x
        self.original_y = y
        self.original_width = width
        self.original_height = height
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 3)
        
    def reset(self):
        """Reset ke posisi/orientasi awal"""
        self.x = self.original_x
        self.y = self.original_y
        self.width = self.original_width
        self.height = self.original_height

class RotatingPlatform(Platform):
    """Platform yang dapat diputar (ROTASI)"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, ROTATION_COLOR)
        self.angle = 0
        self.rotation_speed = 45
        self.rotation_point_x = x + width/2
        self.rotation_point_y = y + height/2
        self.points = []  # Titik-titik untuk menggambar setelah rotasi
        
    def rotate(self, direction):
        """TERAPKAN ROTASI dengan matriks rotasi 2D"""
        # direction: 1 = searah jarum jam, -1 = berlawanan jarum jam
        self.angle += direction * self.rotation_speed
        
        # Normalisasi angle ke rentang 0-360
        self.angle %= 360
        
        # Konversi ke radian untuk perhitungan trigonometri
        theta = math.radians(self.angle)
        
        # Titik-titik sudut platform relatif terhadap pusat rotasi
        rel_points = [
            (-self.width/2, -self.height/2),
            (self.width/2, -self.height/2),
            (self.width/2, self.height/2),
            (-self.width/2, self.height/2)
        ]
        
        # TERAPKAN MATRIKS ROTASI 2D:
        # [cosθ  -sinθ]
        # [sinθ   cosθ]
        self.points = []
        for px, py in rel_points:
            # Rotasi titik
            rx = px * math.cos(theta) - py * math.sin(theta)
            ry = px * math.sin(theta) + py * math.cos(theta)
            
            # Translasi kembali ke posisi dunia
            self.points.append((rx + self.rotation_point_x, ry + self.rotation_point_y))
        
        # Hitung bounding box baru untuk collision detection
        min_x = min(p[0] for p in self.points)
        max_x = max(p[0] for p in self.points)
        min_y = min(p[1] for p in self.points)
        max_y = max(p[1] for p in self.points)
        
        self.x = min_x
        self.y = min_y
        self.width = max_x - min_x
        self.height = max_y - min_y
        
    def draw(self, surface):
        if self.points:
            pygame.draw.polygon(surface, self.color, self.points)
        else:
            # Gambar tanpa rotasi jika belum dirotasi
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 3)

class ScalingPlatform(Platform):
    """Platform yang dapat diskala (SKALA)"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, SCALE_COLOR)
        self.scale_factor = 1.0
        self.min_scale = 0.5
        self.max_scale = 2.0
        
    def scale(self, factor):
        """TERAPKAN SKALA dengan faktor tertentu"""
        self.scale_factor *= factor
        
        # Batasi skala
        if self.scale_factor < self.min_scale:
            self.scale_factor = self.min_scale
        elif self.scale_factor > self.max_scale:
            self.scale_factor = self.max_scale
            
        # Hitung pusat platform
        center_x = self.x + self.width/2
        center_y = self.y + self.height/2
        
        # TERAPKAN SKALA: kalikan dimensi dengan faktor skala
        self.width = int(self.original_width * self.scale_factor)
        self.height = int(self.original_height * self.scale_factor)
        
        # Pertahankan posisi pusat
        self.x = center_x - self.width/2
        self.y = center_y - self.height/2
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 3)
        
        # Gambar indikator skala
        scale_text = font_small.render(f"Skala: {self.scale_factor:.1f}x", True, TEXT_COLOR)
        screen.blit(scale_text, (self.x, self.y - 20))

class Mirror:
    """Cermin untuk REFLEKSI"""
    def __init__(self, x, y, width, height, orientation='vertical'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self.color = MIRROR_COLOR
        self.glow_timer = 0
        
    def draw(self, surface):
        # Animasi kilau cermin
        self.glow_timer = (self.glow_timer + 2) % 100
        
        # Gambar cermin
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        
        # Gambar efek kilau
        glow_alpha = abs(50 - self.glow_timer) * 5
        if self.orientation == 'vertical':
            glow_surf = pygame.Surface((5, self.height), pygame.SRCALPHA)
            glow_surf.fill((255, 255, 255, glow_alpha))
            surface.blit(glow_surf, (self.x + self.width/2 - 2, self.y))
        else:
            glow_surf = pygame.Surface((self.width, 5), pygame.SRCALPHA)
            glow_surf.fill((255, 255, 255, glow_alpha))
            surface.blit(glow_surf, (self.x, self.y + self.height/2 - 2))
        
        # Gambar label orientasi
        if self.orientation == 'vertical':
            label = font_small.render("Cermin Vertikal", True, TEXT_COLOR)
            surface.blit(label, (self.x - 60, self.y + self.height/2 - 10))
        else:
            label = font_small.render("Cermin Horizontal", True, TEXT_COLOR)
            surface.blit(label, (self.x + self.width/2 - 50, self.y - 25))

class Portal:
    """Portal untuk menyelesaikan level"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.animation_offset = 0
        
    def update(self):
        self.animation_offset = (self.animation_offset + 5) % 360
        
    def draw(self, surface):
        # Animasi portal berdenyut
        pulse = math.sin(math.radians(self.animation_offset)) * 5
        current_radius = self.radius + pulse
        
        # Lingkaran luar
        pygame.draw.circle(surface, PORTAL_COLOR, (self.x, self.y), current_radius)
        
        # Lingkaran dalam
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), current_radius * 0.6)
        
        # Pusat portal
        pygame.draw.circle(surface, (50, 50, 200), (self.x, self.y), current_radius * 0.3)

class Game:
    """Kelas utama game"""
    def __init__(self):
        self.current_level = 1
        self.player = Player(50, HEIGHT - 100)
        self.portal = None
        self.platforms = []
        self.mirrors = []
        self.rotating_platforms = []
        self.scaling_platforms = []
        self.message = ""
        self.message_timer = 0
        self.level_complete = False
        self.setup_level(self.current_level)
        
    def setup_level(self, level_num):
        """Setup level berdasarkan nomor level"""
        self.current_level = level_num
        self.player = Player(50, HEIGHT - 100)
        self.platforms = []
        self.mirrors = []
        self.rotating_platforms = []
        self.scaling_platforms = []
        self.level_complete = False
        
        if level_num == 1:
            # LEVEL 1: TRANSLASI
            print("\n=== LEVEL 1: TRANSLASI ===")
            print("Belajar: Menggerakkan objek dari posisi (x1,y1) ke (x2,y2)")
            print("Konsep: x' = x + dx, y' = y + dy")
            print("Kontrol: A/D = Kiri/Kanan, SPACE = Lompat")
            
            self.portal = Portal(WIDTH - 100, HEIGHT - 100)
            
            # Platform untuk translasi
            self.platforms.append(Platform(100, HEIGHT - 50, 200, 20))
            self.platforms.append(Platform(350, HEIGHT - 150, 150, 20))
            self.platforms.append(Platform(550, HEIGHT - 200, 150, 20))
            self.platforms.append(Platform(650, HEIGHT - 100, 100, 20))
            
            # Platform bergerak (translasi otomatis)
            self.moving_platform = Platform(200, HEIGHT - 250, 100, 20, (255, 140, 0))
            self.platforms.append(self.moving_platform)
            self.moving_direction = 1
            
            self.message = "LEVEL 1: TRANSLASI - A/D = Kiri/Kanan, SPACE = Lompat"
            self.message_timer = 180
            
        elif level_num == 2:
            # LEVEL 2: ROTASI
            print("\n=== LEVEL 2: ROTASI ===")
            print("Belajar: Memutar objek dengan sudut θ")
            print("Matriks Rotasi: [cosθ -sinθ; sinθ cosθ]")
            print("Kontrol: Q = Rotasi -45°, E = Rotasi +45°")
            
            self.portal = Portal(WIDTH - 100, HEIGHT - 150)
            
            # Platform dasar
            self.platforms.append(Platform(0, HEIGHT - 50, WIDTH, 50))
            
            # Platform yang bisa dirotasi
            rotating_plat1 = RotatingPlatform(200, HEIGHT - 150, 120, 20)
            self.platforms.append(rotating_plat1)
            self.rotating_platforms.append(rotating_plat1)
            
            rotating_plat2 = RotatingPlatform(400, HEIGHT - 200, 100, 20)
            self.platforms.append(rotating_plat2)
            self.rotating_platforms.append(rotating_plat2)
            
            rotating_plat3 = RotatingPlatform(600, HEIGHT - 250, 80, 20)
            self.platforms.append(rotating_plat3)
            self.rotating_platforms.append(rotating_plat3)
            
            self.message = "LEVEL 2: ROTASI - Q = Rotasi -45°, E = Rotasi +45°"
            self.message_timer = 180
            
        elif level_num == 3:
            # LEVEL 3: SKALA
            print("\n=== LEVEL 3: SKALA ===")
            print("Belajar: Mengubah ukuran objek dengan faktor s")
            print("Konsep: x' = x * s, y' = y * s")
            print("Kontrol: Z = Perkecil 0.8x, X = Perbesar 1.25x")
            
            self.portal = Portal(WIDTH - 100, 100)
            
            # Platform dasar
            self.platforms.append(Platform(0, HEIGHT - 50, WIDTH, 50))
            
            # Platform yang bisa diskala
            scaling_plat1 = ScalingPlatform(150, HEIGHT - 150, 80, 20)
            self.platforms.append(scaling_plat1)
            self.scaling_platforms.append(scaling_plat1)
            
            scaling_plat2 = ScalingPlatform(350, HEIGHT - 250, 60, 20)
            self.platforms.append(scaling_plat2)
            self.scaling_platforms.append(scaling_plat2)
            
            # Platform tetap untuk mencapai portal
            self.platforms.append(Platform(550, HEIGHT - 300, 80, 20))
            self.platforms.append(Platform(650, HEIGHT - 350, 60, 20))
            self.platforms.append(Platform(700, HEIGHT - 400, 50, 20))
            
            self.message = "LEVEL 3: SKALA - Z = Perkecil 0.8x, X = Perbesar 1.25x"
            self.message_timer = 180
            
        elif level_num == 4:
            # LEVEL 4: REFLEKSI
            print("\n=== LEVEL 4: REFLEKSI ===")
            print("Belajar: Memantulkan objek terhadap garis")
            print("Vertikal: x' = 2c - x, Horizontal: y' = 2c - y")
            print("Kontrol: F = Refleksi terhadap cermin terdekat")
            
            self.portal = Portal(WIDTH - 100, HEIGHT - 100)
            
            # Platform dasar
            self.platforms.append(Platform(0, HEIGHT - 50, WIDTH, 50))
            
            # Cermin vertikal di tengah
            mirror1 = Mirror(400, 150, 10, 300, 'vertical')
            self.mirrors.append(mirror1)
            
            # Cermin horizontal di atas
            mirror2 = Mirror(200, 200, 300, 10, 'horizontal')
            self.mirrors.append(mirror2)
            
            # Platform untuk mencapai portal (harus menggunakan refleksi)
            self.platforms.append(Platform(100, 250, 80, 20, (200, 100, 200)))  # Platform di kiri
            self.platforms.append(Platform(550, 350, 100, 20))  # Platform di kanan
            self.platforms.append(Platform(650, 250, 80, 20))   # Platform untuk melompat
            
            self.message = "LEVEL 4: REFLEKSI - F = Refleksi terhadap cermin terdekat"
            self.message_timer = 180
    
    def update(self):
        """Update logika game"""
        # Update portal animation
        self.portal.update()
        
        # Update pesan timer
        if self.message_timer > 0:
            self.message_timer -= 1
            
        # Update platform bergerak di level 1
        if self.current_level == 1:
            self.moving_platform.x += 2 * self.moving_direction
            if self.moving_platform.x > 500 or self.moving_platform.x < 200:
                self.moving_direction *= -1
                
        # Update player
        self.player.update(self.platforms)
        
        # Update cermin
        for mirror in self.mirrors:
            mirror.glow_timer = (mirror.glow_timer + 1) % 100
        
        # Cek jika player mencapai portal
        player_center_x = self.player.x + self.player.width/2
        player_center_y = self.player.y + self.player.height/2
        distance_to_portal = math.sqrt((player_center_x - self.portal.x)**2 + 
                                      (player_center_y - self.portal.y)**2)
        
        if distance_to_portal < 35 and not self.level_complete:
            self.level_complete = True
            level_names = ["TRANSLASI", "ROTASI", "SKALA", "REFLEKSI"]
            transform_name = level_names[self.current_level - 1]
            print(f"\n✓ Level {self.current_level} ({transform_name}) selesai!")
            self.message = f"Level {self.current_level} selesai! Tekan N untuk lanjut"
            self.message_timer = 300
    
    def draw_grid(self, surface):
        """Menggambar grid koordinat untuk visualisasi translasi"""
        grid_size = 50
        
        # Garis vertikal
        for x in range(0, WIDTH, grid_size):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
            
        # Garis horizontal
        for y in range(0, HEIGHT, grid_size):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y), 1)
        
        # Label koordinat (setiap 100px)
        for x in range(100, WIDTH, 100):
            label = font_small.render(str(x), True, TEXT_COLOR)
            surface.blit(label, (x - 10, 10))
        
        for y in range(100, HEIGHT, 100):
            label = font_small.render(str(y), True, TEXT_COLOR)
            surface.blit(label, (10, y - 10))
    
    def draw_transform_info(self, surface):
        """Menggambar informasi transformasi matematika"""
        info_y = 70
        
        if self.current_level == 1:
            # Info translasi
            info = [
                "TRANSLASI: Menggeser objek",
                "Rumus: x' = x + dx, y' = y + dy",
                f"Posisi Player: ({int(self.player.x)}, {int(self.player.y)})"
            ]
            
        elif self.current_level == 2:
            # Info rotasi
            angle = self.rotating_platforms[0].angle if self.rotating_platforms else 0
            rad = math.radians(angle)
            info = [
                "ROTASI: Memutar objek dengan sudut θ",
                f"Matriks: [cosθ -sinθ; sinθ cosθ]",
                f"θ = {angle}° = {rad:.2f} rad",
                f"cos({angle}°) = {math.cos(rad):.2f}, sin({angle}°) = {math.sin(rad):.2f}"
            ]
            
        elif self.current_level == 3:
            # Info skala
            scale = self.scaling_platforms[0].scale_factor if self.scaling_platforms else 1.0
            info = [
                "SKALA: Mengubah ukuran objek",
                "Rumus: x' = s·x, y' = s·y",
                f"Faktor skala: {scale:.1f}",
                f"Area: {scale**2:.1f}× luas semula"
            ]
            
        elif self.current_level == 4:
            # Info refleksi
            info = [
                "REFLEKSI: Memantulkan objek",
                "Vertikal: x' = 2c - x, y' = y",
                "Horizontal: x' = x, y' = 2c - y",
                "Gunakan F saat dekat cermin"
            ]
        
        # Gambar latar belakang info
        info_height = len(info) * 25 + 10
        info_bg = pygame.Surface((300, info_height), pygame.SRCALPHA)
        info_bg.fill((0, 0, 0, 150))
        surface.blit(info_bg, (WIDTH - 310, info_y))
        
        # Gambar teks info
        for i, line in enumerate(info):
            text = font_small.render(line, True, TEXT_COLOR)
            surface.blit(text, (WIDTH - 300, info_y + 5 + i * 25))
    
    def draw_ui(self, surface):
        """Menggambar UI"""
        # Panel informasi atas
        pygame.draw.rect(surface, UI_BG, (0, 0, WIDTH, 60))
        pygame.draw.line(surface, (100, 100, 200), (0, 60), (WIDTH, 60), 2)
        
        # Judul level
        level_names = ["TRANSLASI", "ROTASI", "SKALA", "REFLEKSI"]
        level_text = font_large.render(f"LEVEL {self.current_level}: {level_names[self.current_level-1]}", 
                                      True, TEXT_COLOR)
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 10))
        
        # Koordinat player
        coord_text = font_small.render(f"Posisi: ({int(self.player.x)}, {int(self.player.y)})", 
                                      True, TEXT_COLOR)
        screen.blit(coord_text, (20, HEIGHT - 40))
        
        # Kecepatan player
        vel_text = font_small.render(f"Kecepatan: ({self.player.velocity_x:.1f}, {self.player.velocity_y:.1f})", 
                                    True, TEXT_COLOR)
        screen.blit(vel_text, (20, HEIGHT - 70))
        
        # Petunjuk kontrol
        controls = ""
        if self.current_level == 1:
            controls = "Kontrol: A/D = Kiri/Kanan, SPACE = Lompat"
        elif self.current_level == 2:
            controls = "Kontrol: Q = Rotasi -45°, E = Rotasi +45°"
        elif self.current_level == 3:
            controls = "Kontrol: Z = Perkecil 0.8x, X = Perbesar 1.25x"
        elif self.current_level == 4:
            controls = "Kontrol: F = Refleksi terhadap cermin terdekat"
            
        if controls:
            controls_text = font_small.render(controls, True, TEXT_COLOR)
            screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT - 40))
        
        # Tampilkan pesan tutorial
        if self.message_timer > 0:
            message_surface = font_medium.render(self.message, True, TEXT_COLOR)
            message_bg = pygame.Surface((message_surface.get_width() + 20, 
                                        message_surface.get_height() + 10), pygame.SRCALPHA)
            message_bg.fill((0, 0, 0, 200))
            screen.blit(message_bg, (WIDTH//2 - message_surface.get_width()//2 - 10, 
                                    HEIGHT//2 - message_surface.get_height()//2 - 5))
            screen.blit(message_surface, (WIDTH//2 - message_surface.get_width()//2, 
                                         HEIGHT//2 - message_surface.get_height()//2))
    
    def draw(self, surface):
        """Menggambar seluruh game"""
        # Latar belakang
        surface.fill(BACKGROUND)
        
        # Grid hanya untuk level 1 (translasi)
        if self.current_level == 1:
            self.draw_grid(surface)
        
        # Gambar semua objek
        for platform in self.platforms:
            platform.draw(surface)
            
        for mirror in self.mirrors:
            mirror.draw(surface)
            
        self.portal.draw(surface)
        self.player.draw(surface)
        
        # Gambar informasi transformasi
        self.draw_transform_info(surface)
        
        # Gambar UI
        self.draw_ui(surface)
        
        # Tampilkan indikator level selesai
        if self.level_complete:
            complete_surface = font_large.render("LEVEL SELESAI!", True, (50, 255, 100))
            screen.blit(complete_surface, (WIDTH//2 - complete_surface.get_width()//2, 100))
            
            next_text = font_medium.render("Tekan N untuk lanjut ke level berikutnya", True, TEXT_COLOR)
            screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, 150))
    
    def handle_input(self, keys):
        """Handle input keyboard"""
        if self.level_complete:
            return
            
        # KONTROL TRANSLASI (Level 1 dan umum)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.velocity_x = -5
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.velocity_x = 5
        else:
            # Reduksi kecepatan horizontal saat tidak ada input
            self.player.velocity_x *= 0.8
            if abs(self.player.velocity_x) < 0.1:
                self.player.velocity_x = 0
    
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.player.on_ground:
            self.player.velocity_y = self.player.jump_power
        
        # KONTROL ROTASI (Level 2)
        if self.current_level == 2:
            if keys[pygame.K_q]:  # Rotasi kiri (-45°)
                for platform in self.rotating_platforms:
                    platform.rotate(-1)
            if keys[pygame.K_e]:  # Rotasi kanan (+45°)
                for platform in self.rotating_platforms:
                    platform.rotate(1)
                    
        # KONTROL SKALA (Level 3)
        elif self.current_level == 3:
            if keys[pygame.K_z]:  # Perkecil
                for platform in self.scaling_platforms:
                    platform.scale(0.8)
            if keys[pygame.K_x]:  # Perbesar
                for platform in self.scaling_platforms:
                    platform.scale(1.25)
                    
        # KONTROL REFLEKSI (Level 4)
        elif self.current_level == 4:
            if keys[pygame.K_f]:  # Refleksi
                if self.mirrors and not self.player.is_reflected:
                    # Cari cermin terdekat
                    player_center_x = self.player.x + self.player.width/2
                    player_center_y = self.player.y + self.player.height/2
                    
                    closest_mirror = None
                    closest_distance = float('inf')
                    
                    for mirror in self.mirrors:
                        mirror_center_x = mirror.x + mirror.width/2
                        mirror_center_y = mirror.y + mirror.height/2
                        distance = math.sqrt((player_center_x - mirror_center_x)**2 + 
                                           (player_center_y - mirror_center_y)**2)
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_mirror = mirror
                    
                    # Lakukan refleksi jika dekat dengan cermin
                    if closest_mirror and closest_distance < 200:
                        self.player.apply_reflection(closest_mirror)
                        print(f"Refleksi diterapkan! Cermin: {closest_mirror.orientation}")

def main():
    """Fungsi utama game"""
    clock = pygame.time.Clock()
    game = Game()
    running = True
    
    print("=" * 60)
    print("TRANSFORMBOT: BELAJAR TRANSFORMASI GRAFIKA KOMPUTER")
    print("=" * 60)
    print("\nTUJUAN PERMAINAN:")
    print("  Belajar 4 transformasi dasar grafika komputer:")
    print("  1. TRANSLASI - Menggeser objek")
    print("  2. ROTASI    - Memutar objek")
    print("  3. SKALA     - Mengubah ukuran objek")
    print("  4. REFLEKSI  - Memantulkan objek")
    print("\nKONTROL UMUM:")
    print("  A/D atau ←/→ : Bergerak kiri/kanan (Translasi)")
    print("  SPACE/W/↑    : Lompat")
    print("  R            : Reset level")
    print("  N            : Level berikutnya (jika level selesai)")
    print("  ESC          : Keluar")
    print("\nKONTROL TRANSFORMASI:")
    print("  Level 2 (ROTASI)    : Q = Rotasi -45°, E = Rotasi +45°")
    print("  Level 3 (SKALA)     : Z = Perkecil 0.8x, X = Perbesar 1.25x")
    print("  Level 4 (REFLEKSI)  : F = Refleksi terhadap cermin terdekat")
    print("=" * 60)
    print("\nMulai Level 1: TRANSLASI...")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                elif event.key == pygame.K_r:  # Reset level
                    print(f"\nMengulang Level {game.current_level}...")
                    game.setup_level(game.current_level)
                    
                elif event.key == pygame.K_n and game.level_complete:  # Next level
                    if game.current_level < 4:
                        game.setup_level(game.current_level + 1)
                    else:
                        print("\n" + "=" * 60)
                        print("SELAMAT! Anda telah menyelesaikan semua level!")
                        print("Anda sekarang menguasai transformasi grafika:")
                        print("  1. Translasi (Pergeseran)")
                        print("  2. Rotasi (Perputaran)")
                        print("  3. Skala (Penskalaan)")
                        print("  4. Refleksi (Pencerminan)")
                        print("=" * 60)
                        
                        # Tampilkan pesan kemenangan
                        game.message = "SELAMAT! Anda telah menguasai semua transformasi!"
                        game.message_timer = 300
                        
                        # Tunggu sebentar sebelum keluar
                        pygame.time.wait(3000)
                        running = False
        
        # Handle input keyboard berkelanjutan
        keys = pygame.key.get_pressed()
        game.handle_input(keys)
        
        # Update dan gambar game
        game.update()
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()