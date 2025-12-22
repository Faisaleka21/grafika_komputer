import pygame
import sys
import random

pygame.init()

# -----------------------------
# WINDOW
# -----------------------------
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemies")
clock = pygame.time.Clock()

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 120, 255)

# -----------------------------
# PLAYER
# -----------------------------
player_width, player_height = 40, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

# -----------------------------
# ENEMIES
# -----------------------------
enemy_list = []
enemy_size = 40
enemy_speed = 4

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_size)
    y = -enemy_size
    enemy_list.append([x, y])

# -----------------------------
# SCORE
# -----------------------------
score = 0
font = pygame.font.SysFont("consolas", 24)

# -----------------------------
# GAME LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ----- PLAYER MOVEMENT -----
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # batas layar
    player_x = max(0, min(player_x, WIDTH - player_width))

    # ----- ENEMY SPAWN -----
    if random.random() < 0.02:  # probabilitas spawn
        spawn_enemy()

    # ----- MOVE ENEMIES -----
    for enemy in enemy_list:
        enemy[1] += enemy_speed

    # hapus musuh yg lewat bawah
    enemy_list = [e for e in enemy_list if e[1] < HEIGHT]

    # ----- COLLISION -----
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for enemy in enemy_list:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            # GAME OVER
            game_over_text = font.render("GAME OVER - Press R to Restart", True, RED)
            screen.blit(game_over_text, (60, HEIGHT // 2))
            pygame.display.update()

            # Freeze game, wait restart
            waiting = True
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                        # reset semuanya
                        enemy_list = []
                        score = 0
                        player_x = WIDTH // 2
                        waiting = False

    # ----- SCORE -----
    score += 1

    # ----- DRAW -----
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
