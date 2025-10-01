import pygame
import sys
import random

# Game constants
WIDTH, HEIGHT = 600, 400
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
GREEN = (0, 200, 0)

# Paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        self.speed = 6

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (5, 5), 5)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.vel = [3, -3]

    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vel[0] = -self.vel[0]
        if self.rect.top <= 0:
            self.vel[1] = -self.vel[1]

# Brick
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

def run_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    # Groups
    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()

    paddle = Paddle()
    ball = Ball()
    all_sprites.add(paddle, ball)
    waiting_to_start = True 

    # Create grid of bricks
    for row in range(5):
        for col in range(10):
            brick = Brick(col * 55 + 20, row * 25 + 40)
            all_sprites.add(brick)
            bricks.add(brick)

    score = 0
    lives = 3
    running = True

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if waiting_to_start and event.key == pygame.K_SPACE:
                    waiting_to_start = False 

        # Update
        paddle.update(keys)

        if not waiting_to_start:
            ball.update()

        # Ball hits paddle
        if ball.rect.colliderect(paddle.rect):
            ball.vel[1] = -ball.vel[1]

        # Ball hits brick
        hit_brick = pygame.sprite.spritecollide(ball, bricks, True)
        if hit_brick:
            ball.vel[1] = -ball.vel[1]
            score += len(hit_brick) * 10

        # Ball falls below screen
        if ball.rect.top > HEIGHT:
            lives -= 1
            if lives <= 0:
                running = False
            else:
                # Reset ball + paddle
                ball.rect.center = (WIDTH // 2, HEIGHT // 2)
                ball.vel = [3 * random.choice([-1, 1]), -3]
                paddle.rect.midbottom = (WIDTH // 2, HEIGHT - 20)

                waiting_to_start = True 
                
        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)

        if waiting_to_start:
            start_text = font.render("Press SPACE to Start", True, WHITE)
            screen.blit(start_text, (WIDTH // 2- start_text.get_width() // 2, HEIGHT // 2 - 20))

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # Game Over
    screen.fill(BLACK)
    msg = font.render("Game Over!", True, WHITE)
    final_score = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
