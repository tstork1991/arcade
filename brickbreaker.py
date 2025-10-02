import pygame
import sys
import random

# Game constants
WIDTH, HEIGHT = 600, 400
FPS = 60

#brick constants
BRICK_W, BRICK_H = 50, 20
BRICK_GAP_X, BRICK_GAP_Y = 5, 5
BRICK_COLS = 10


# Level layouts: ' ' = empty, '1' = 1-hit, '2' = 2-hit, '3' = 3-hit
LEVELS = [
    # Level 1 – simple wall of 1-hit bricks
    [
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
    ],
    # Level 2 – tougher core with 3-hit bricks
    [
        "1112222211",
        "1122332211",
        "1233333211",
        "1122332211",
        "1112222211",
    ],
    # Level 3 – not finished yet
    [
        "  222222  ",
        " 21111112 ",
        "2111111112",
        " 21111112 ",
        "  222222  ",
    ],
]


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
    def __init__(self, x, y, hits=1):
        super().__init__()
        self.max_hits = hits
        self.hits = hits
        self.image = pygame.Surface((BRICK_W, BRICK_H))
        self.rect = self.image.get_rect(topleft=(x, y))
        self._refresh_color()

    def _refresh_color(self):
        # Color based on remaining hits
        if self.hits >= 3:
            self.image.fill((160, 80, 200))   # purple for 3-hit full
        elif self.hits == 2:
            self.image.fill((255, 140, 0))    # orange for 2-hit
        else:
            self.image.fill((0, 200, 0))      # green for 1-hit

    def hit(self):
        """Reduce health by 1. Return True if destroyed."""
        self.hits -= 1
        if self.hits <= 0:
            self.kill()
            return True
        else:
            self._refresh_color()
            return False


#build level 
def build_level(level_index, bricks_group, all_sprites_group):
    bricks_group.empty()
    # center the grid horizontally
    total_w = BRICK_COLS * BRICK_W + (BRICK_COLS - 1) * BRICK_GAP_X
    start_x = (WIDTH - total_w) // 2
    rows = LEVELS[level_index]
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == ' ':
                continue
            # map characters to hits: 1 = 1-hit, 2 = 2-hit, 3 = 3-hit
            hits = 3 if ch == '3' else 2 if ch == '2' else 1
            x = start_x + c * (BRICK_W + BRICK_GAP_X)
            y = 40 + r * (BRICK_H + BRICK_GAP_Y)
            b = Brick(x, y, hits=hits)
            bricks_group.add(b)
            all_sprites_group.add(b)


#level selection
def level_select(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 32)
    options = [f"Level {i+1}" for i in range(len(LEVELS))] + ["Back"]
    selected = 0

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Back":
                        return None
                    else:
                        return selected  # return level index

        # Draw menu
        screen.fill(BLACK)
        title = font.render("Choose a Level", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))

        for i, opt in enumerate(options):
            color = GREEN if i == selected else WHITE
            text = font.render(opt, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 140 + i*40))

        pygame.display.flip()
        clock.tick(30)



def run_game(screen, level_index=0):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    # Groups
    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()

    paddle = Paddle()
    ball = Ball()
    all_sprites.add(paddle, ball)
    waiting_to_start = True 

    #build chosen level
    build_level(level_index, bricks, all_sprites)

    score = 0
    lives = 3
    running = True
    cleared = False

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
        hit_list = pygame.sprite.spritecollide(ball, bricks, False)
        if hit_list:
            ball.vel[1] = -ball.vel[1]
            for b in hit_list:
                destroyed = b.hit()
                if destroyed:
                    score += 10
        
        # Level cleared if no bricks remain
        if len(bricks) == 0:
            running = False
            cleared = True
            break

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

    # End screen
    screen.fill(BLACK)
    big_font = pygame.font.SysFont("arial", 32)

    if cleared:
        msg = big_font.render("LEVEL CLEARED!", True, GREEN)
        tip = font.render("Press Enter to play again or Esc to return", True, WHITE)
    else:
        msg = big_font.render("GAME OVER", True, RED)
        tip = font.render("Press Enter to try again or Esc to return", True, WHITE)

    final_score = font.render(f"Final Score: {score}", True, WHITE)

    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
    screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()

    # Wait for input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # restart same level
                    run_game(screen, level_index)
                    return
                elif event.key == pygame.K_ESCAPE:  # back to level select
                    return

