"""
Samurai Adventure (Pygame)
Run: python game.py
Requirements: pygame
Place optional asset images in an "assets/" folder:
 - assets/player_idle.png
 - assets/player_attack.png
 - assets/enemy.png
 - assets/background.png
If assets aren't present, the program will draw simple shapes instead.

Controls:
 - Arrow keys / WASD: Move
 - Space: Attack (short dash + scale)
 - R: Rotate player 90 degrees (demonstrates rotation)

Transformations used:
 - Translation: movement of player & enemies
 - Reflection: flip player sprite when facing left/right
 - Rotation: rotate player sprite with R key and while attacking
 - Scaling: scale player sprite while attacking

Features:
 - Enemies spawn periodically and move toward the player
 - Basic health and knockback
 - Simple AI and collision

This is a small demo to show transformations and simple gameplay.
"""

import os
import math
import random
import pygame

# Configuration
WIDTH, HEIGHT = 960, 600
FPS = 60
ASSET_DIR = os.path.join(os.path.dirname(__file__), "aset")

# Helper: load image with fallback
def load_image(name, colorkey=None):
    path = os.path.join(ASSET_DIR, name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if colorkey is not None:
            img.set_colorkey(colorkey)
        return img
    return None

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.original_image = load_image(" L1.PNG")
        self.attack_image = load_image("LP4.PNG")
        self.fallback = False
        if self.original_image is None:
            # fallback: simple rectangle graphic
            self.fallback = True
            self.original_image = pygame.Surface((48, 64), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, (200, 30, 30), (0, 0, 48, 64), border_radius=8)
            pygame.draw.circle(self.original_image, (220, 180, 120), (36, 22), 8)  # helmet
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.speed = 220.0
        self.facing_right = True
        self.angle = 0
        self.scale = 1.0
        self.attacking = False
        self.attack_timer = 0.0
        self.max_health = 10
        self.health = self.max_health

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y = 1
        if move.length_squared() > 0:
            move = move.normalize()
            self.vel = move * self.speed
        else:
            self.vel *= 0.8
            if self.vel.length() < 5:
                self.vel = pygame.Vector2(0, 0)

        # Attack (dash)
        for event in pygame.event.get([pygame.KEYDOWN]):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.attacking:
                self.attacking = True
                self.attack_timer = 0.25
                # dash
                dash_dir = pygame.Vector2(1 if self.facing_right else -1, 0)
                self.vel += dash_dir * 420
                # rotate a bit during attack
                self.angle += 30

        # Rotate on R
        if keys[pygame.K_r]:
            self.angle += 180 * dt  # continuous rotate while holding R

    def update(self, dt):
        # apply velocity
        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # clamp to screen
        self.pos.x = max(24, min(WIDTH - 24, self.pos.x))
        self.pos.y = max(24, min(HEIGHT - 24, self.pos.y))
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Attack timing and scaling
        if self.attacking:
            self.attack_timer -= dt
            self.scale = 1.4
            self.angle += 720 * dt  # spin while attacking
            if self.attack_timer <= 0:
                self.attacking = False
                self.scale = 1.0
        else:
            # slow return to 0 angle (normalize to range)
            self.angle *= 0.95

        # Facing
        if self.vel.x > 10:
            self.facing_right = True
        elif self.vel.x < -10:
            self.facing_right = False

        # Build transformed image: reflection, rotation, scale
        base = self.attack_image if (self.attacking and self.attack_image) else self.original_image
        img = base
        # scale
        w, h = img.get_size()
        scaled = pygame.transform.smoothscale(img, (max(1, int(w * self.scale)), max(1, int(h * self.scale))))
        # rotate
        rotated = pygame.transform.rotate(scaled, self.angle)
        # reflect when facing left
        if not self.facing_right:
            rotated = pygame.transform.flip(rotated, True, False)
        self.image = rotated
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def draw_ui(self, surface):
        # health bar
        bar_w = 120
        x = 10
        y = 10
        pygame.draw.rect(surface, (40, 40, 40), (x - 2, y - 2, bar_w + 4, 18), border_radius=6)
        fill = int(bar_w * (self.health / self.max_health))
        pygame.draw.rect(surface, (180, 30, 30), (x, y, fill, 14), border_radius=6)
        font = pygame.font.SysFont(None, 20)
        txt = font.render(f"Health: {self.health}/{self.max_health}", True, (255, 255, 255))
        surface.blit(txt, (x + bar_w + 8, y - 2))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.base_image = load_image("enemy.png")
        if self.base_image is None:
            self.base_image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.base_image, (40, 120, 200), [(0,40),(20,0),(40,40)])
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.speed = random.uniform(60, 120)
        self.angle = 0
        self.scale = 1.0

    def update(self, dt, player_pos):
        # Move toward player (translation)
        dirv = pygame.Vector2(player_pos) - self.pos
        dist = dirv.length()
        if dist > 0:
            dirv = dirv.normalize()
            self.pos += dirv * self.speed * dt

        # rotate slowly to face direction
        self.angle = (self.angle + 60 * dt) % 360
        self.scale = 1.0 + 0.2 * math.sin(pygame.time.get_ticks() * 0.005)

        # apply transforms
        img = pygame.transform.smoothscale(self.base_image, (max(1, int(self.base_image.get_width() * self.scale)), max(1, int(self.base_image.get_height() * self.scale))))
        img = pygame.transform.rotate(img, self.angle)
        self.image = img
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Samurai Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.enemy_spawn_timer = 0.0
        self.background = load_image("background.png")

    def spawn_enemy(self):
        # spawn at random edge
        side = random.choice(["top","bottom","left","right"])
        if side == "top":
            x = random.randint(20, WIDTH-20); y = -40
        elif side == "bottom":
            x = random.randint(20, WIDTH-20); y = HEIGHT + 40
        elif side == "left":
            x = -40; y = random.randint(20, HEIGHT-20)
        else:
            x = WIDTH + 40; y = random.randint(20, HEIGHT-20)
        enemy = Enemy(x, y)  
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def handle_events(self):
        # we already consume some events in player.handle_input for KEYDOWN check; here handle quit and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # pass other events back into event queue for player's input handler to see
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                pygame.event.post(event)

    def update(self, dt):
        self.player.handle_input(dt)
        self.player.update(dt)
        for e in list(self.enemies):
            e.update(dt, self.player.pos)
            # collision with player
            if e.rect.colliderect(self.player.rect):
                # damage player
                self.player.health -= 1
                # knockback enemy
                knock = (e.pos - self.player.pos)
                if knock.length() == 0:
                    knock = pygame.Vector2(random.uniform(-1,1), random.uniform(-1,1))
                knock.scale_to_length(60)
                e.pos += knock
                if self.player.health <= 0:
                    print("Player died")
                    self.running = False

        # spawn logic
        self.enemy_spawn_timer -= dt
        if self.enemy_spawn_timer <= 0:
            self.spawn_enemy()
            self.enemy_spawn_timer = max(0.8, 2.0 - (pygame.time.get_ticks() / 60000.0))  # spawn faster over time

    def draw(self):
        if self.background:
            # tile background
            for x in range(0, WIDTH, self.background.get_width()):
                for y in range(0, HEIGHT, self.background.get_height()):
                    self.screen.blit(self.background, (x,y))
        else:
            self.screen.fill((15, 15, 40))
            # simple parallax hills
            pygame.draw.polygon(self.screen, (20, 60, 30), [(0, HEIGHT), (200, 300), (400, HEIGHT)])
            pygame.draw.polygon(self.screen, (30, 80, 50), [(300, HEIGHT), (600, 250), (960, HEIGHT)])

        # sort sprites by y for pseudo-depth
        sprites_sorted = sorted(self.all_sprites, key=lambda s: s.rect.centery)
        for spr in sprites_sorted:
            self.screen.blit(spr.image, spr.rect)

        # UI
        self.player.draw_ui(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

if __name__ == '__main__':
    Game().run()
