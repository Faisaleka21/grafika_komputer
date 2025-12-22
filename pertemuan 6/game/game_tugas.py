import pygame
import sys

pygame.init()

# -----------------------------
# WINDOW SETUP
# -----------------------------
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# -----------------------------
# LOAD ASSETS
# -----------------------------
# Ganti dengan asetmu sendiri!
def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        print("Gambar tidak ditemukan:", path)
        # fallback kotak jika gagal
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 0))
        return surf

background = load_image("assets/bg.png")
player_img = load_image("assets/player.png")
platform_img = load_image("assets/platform.png")

# -----------------------------
# PLAYER CLASS
# -----------------------------
class Player:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.vx = 0
        self.vy = 0
        self.speed = 4
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False
        self.rect = player_img.get_rect(topleft=(self.x, self.y))

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed

        # Apply velocities
        self.x += self.vx

        # Gravity
        self.vy += self.gravity
        self.y += self.vy

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = self.jump_power

        # Update rect
        self.rect.topleft = (self.x, self.y)

        # Collision with platforms
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0:  # falling
                    self.y = p.rect.top - self.rect.height
                    self.vy = 0
                    self.on_ground = True

        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(player_img, self.rect)

# -----------------------------
# PLATFORM CLASS
# -----------------------------
class Platform:
    def __init__(self, x, y):
        self.img = platform_img
        self.rect = self.img.get_rect(topleft=(x, y))

    def draw(self):
        screen.blit(self.img, self.rect)

# -----------------------------
# CREATE OBJECTS
# -----------------------------
player = Player()
platforms = [
    Platform(0, 450),
    Platform(300, 350),
    Platform(600, 280)
]

# -----------------------------
# GAME LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    player.update(platforms)

    # Draw
    screen.fill((0, 0, 0))  # fallback background
    try:
        screen.blit(background, (0, 0))
    except:
        pass

    for p in platforms:
        p.draw()

    player.draw()

    pygame.display.update()
    clock.tick(60)
