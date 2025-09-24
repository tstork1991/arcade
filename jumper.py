import pygame
import sys
import random

# Game constants
WIDTH, HEIGHT = 600, 400
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (50, 150, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 0

    def update(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Wrap around screen
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=100, h=10):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

def run_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    # Groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    last_platform = None

    # Player
    player = Player(WIDTH//2, HEIGHT-100)
    all_sprites.add(player)

    #starting platform
    start_platform = Platform(WIDTH//2 - 50, HEIGHT - 50, 100, 10)
    all_sprites.add(start_platform)
    platforms.add(start_platform)

    # Initial platforms
    for i in range(6):
        p = Platform(random.randint(0, WIDTH-100), i * 80)
        all_sprites.add(p)
        platforms.add(p)

    score = 0
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        all_sprites.update(keys)

        # Collision: bounce on platform
        if player.vel_y > 0:  # falling
            hits = pygame.sprite.spritecollide(player, platforms, False)
            if hits:
                lowest = hits[0]
                if player.rect.bottom <= lowest.rect.bottom + 10:
                    if last_platform != lowest:
                        score += 1
                        last_platform = lowest
                    player.rect.bottom = lowest.rect.top
                    player.vel_y = JUMP_STRENGTH

        # Scroll screen when player reaches top
        if player.rect.top <= HEIGHT // 3:
            player.rect.y += abs(player.vel_y)
            for plat in platforms:
                plat.rect.y += abs(player.vel_y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    new_y = plat.rect.y - random.randint(50, 120)  # 50–120 px apart
                    new_p = Platform(random.randint(0, WIDTH-100), new_y)
                    platforms.add(new_p)
                    all_sprites.add(new_p)            

        # Game Over if fall
        if player.rect.top > HEIGHT:
            running = False

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # End screen
    screen.fill(BLACK)
    msg = font.render("Game Over! Returning to menu...", True, WHITE)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)
