import pygame
import numpy as np

pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Platformer — Asset Version")

# ===============================================================
# LOAD ASSETS
# ===============================================================
def load_img(path, scale=1):
    img = pygame.image.load(path).convert_alpha()
    if scale != 1:
        w, h = img.get_size()
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img

# background & ground
bg = load_img("mountains-background-game-vector.jpg", 1)
ground_img = load_img("assets/ground.png", 2)

# Player animations
player_idle = load_img("assets/player_idle.png", 1.2)
player_run = [
    load_img("assets/player_run1.png", 1.2),
    load_img("assets/player_run2.png", 1.2)
]
player_jump = load_img("assets/player_jump.png", 1.2)
player_punch = load_img("assets/player_punch.png", 1.2)

# ===============================================================
# PLAYER STATE
# ===============================================================
player = {
    "x": 200,
    "y": 340,
    "vx": 0,
    "vy": 0,
    "on_ground": True,
    "facing": 1,            # 1 kanan, -1 kiri
    "scale": 1.0,

    # animasi
    "frame": 0,
    "frame_timer": 0,

    # aksi
    "punch": 0,
    "dash": 0
}

GRAVITY = 0.9
MOVE_SPEED = 4
JUMP_SPEED = -15
DASH_SPEED = 13

mirror_world = 1  # seluruh dunia dicerminkan (flip screen)

# ===============================================================
# DRAW PLAYER
# ===============================================================
def draw_player(p):
    # tentukan sprite
    if p["punch"] > 0:
        sprite = player_punch
    elif not p["on_ground"]:
        sprite = player_jump
    elif abs(p["vx"]) > 0.1:
        sprite = player_run[p["frame"] % len(player_run)]
    else:
        sprite = player_idle

    img = sprite

    # scale (zoom)
    if p["scale"] != 1:
        w, h = img.get_size()
        img = pygame.transform.scale(img, (int(w * p["scale"]), int(h * p["scale"])))

    # flip jika menghadap kiri
    if p["facing"] == -1:
        img = pygame.transform.flip(img, True, False)

    # mirror seluruh dunia
    if mirror_world == -1:
        img = pygame.transform.flip(img, True, False)
        draw_x = WIDTH - p["x"]
    else:
        draw_x = p["x"]

    screen.blit(img, (draw_x, p["y"]))

# ===============================================================
# MAIN LOOP
# ===============================================================
running = True
while running:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()

    # ---------------- EVENTS -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------------- MOVEMENT -----------------
    player["vx"] = 0

    if keys[pygame.K_a]:
        player["vx"] = -MOVE_SPEED
        player["facing"] = -1
    if keys[pygame.K_d]:
        player["vx"] = MOVE_SPEED
        player["facing"] = 1

    if keys[pygame.K_SPACE] and player["on_ground"]:
        player["vy"] = JUMP_SPEED
        player["on_ground"] = False

    if keys[pygame.K_LSHIFT] and player["dash"] == 0:
        player["dash"] = 12
        player["vx"] = player["facing"] * DASH_SPEED

    if keys[pygame.K_j] and player["punch"] == 0:
        player["punch"] = 12

    # hold "K" = big size
    if keys[pygame.K_k]:
        player["scale"] = min(1.6, player["scale"] + 0.03)
    else:
        player["scale"] = max(1.0, player["scale"] - 0.03)

    # toggle mirror world
    if keys[pygame.K_m]:
        mirror_world *= -1
        pygame.time.delay(200)

    # ---------------- PHYSICS -----------------
    player["x"] += player["vx"]

    # dash timer
    if player["dash"] > 0:
        player["dash"] -= 1

    # gravity
    player["y"] += player["vy"]
    if not player["on_ground"]:
        player["vy"] += GRAVITY

    # ground collision
    if player["y"] >= 340:
        player["y"] = 340
        player["vy"] = 0
        player["on_ground"] = True

    # keep in screen
    player["x"] = max(20, min(WIDTH - 20, player["x"]))

    # punch timer
    if player["punch"] > 0:
        player["punch"] -= 1

    # animation frame switching
    if abs(player["vx"]) > 0.1 and player["on_ground"]:
        player["frame_timer"] += 1
        if player["frame_timer"] >= 10:
            player["frame"] += 1
            player["frame_timer"] = 0

    # ---------------- DRAW -----------------
    screen.blit(bg, (0, 0))
    screen.blit(ground_img, (0, 380))

    draw_player(player)

    pygame.display.update()

pygame.quit()
