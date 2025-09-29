import pygame
import sys
import random
import os


# Load high scores from file
def load_high_scores():
    if not os.path.exists("highscores_jumper.txt"):
        return []
    scores = []
    with open("highscores_jumper.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2 and parts[1].isdigit():
                initials, score = parts
                scores.append((initials, int(score)))
    return scores

# Save high scores to file
def save_high_scores(scores):
    with open("highscores_jumper.txt", "w") as f:
        for initials, score in scores[:5]:
            f.write(f"{initials} {score}\n")

# Prompt for initials
def get_initials(screen, font):
    initials = ""
    big_font = pygame.font.SysFont("arial", 48)

    while True:
        screen.fill(BLACK)
        prompt = font.render("Enter your initials (3 letters):", True, WHITE)
        current = big_font.render(initials, True, WHITE)

        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 60))
        screen.blit(current, (WIDTH//2 - current.get_width()//2, HEIGHT//2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    return initials
                elif event.key == pygame.K_BACKSPACE and len(initials) > 0:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()



# Game constants
WIDTH, HEIGHT = 600, 400
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -15

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
            self.rect.x -= 7
        if keys[pygame.K_RIGHT]:
            self.rect.x += 7

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

class MovingPlatform(Platform):
    def __init__(self, x, y, w=100, h=10, speed=2):
        super().__init__(x, y, w, h)
        self.speed = speed
        self.image.fill((255, 255, 0)) #yellow for moving horizontal platforms

    def update(self, keys=None):  # ignore player input
        self.rect.x += self.speed
        # Bounce at edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed = -self.speed

class BreakablePlatform(Platform):
    def __init__(self, x, y, w=100, h=10):
        super().__init__(x, y, w, h)
        self.image.fill((200, 0, 0))  # red for breakable platforms
        self.broken = False

    def break_platform(self, platforms, all_sprites):
        if not self.broken:
            self.broken = True
            platforms.remove(self)
            all_sprites.remove(self)


def run_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)
    high_scores = load_high_scores()

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
        p = Platform(random.randint(0, WIDTH-100), i * 60)
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

                    #if its a breakable platform, remove it after touching
                    if isinstance(lowest, BreakablePlatform):
                        lowest.break_platform(platforms, all_sprites)

        # Scroll screen when player reaches top third
        if player.rect.top <= HEIGHT // 3:
            player.rect.y += abs(player.vel_y)
            for plat in platforms:
                plat.rect.y += abs(player.vel_y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

        #ensure there are at least 6 platforms above the player    
        while len(platforms) < 6:
            highest_y = min(p.rect.y for p in platforms)  # top-most platform
            new_y = highest_y - random.randint(50, 120)   # spawn above highest
            
            #place new platform not too horizontal from center
            player_x = player.rect.centerx
            new_x = random.randint(max(0, player_x - 150), min(WIDTH-100, player_x +150))
            
            # After score 30
            if score >= 45: 
                roll = random.random()
                if roll < 0.5: #50% chance 
                    new_p = BreakablePlatform(new_x, new_y)
                elif roll < 0.7: #next 20% chance
                    new_p = MovingPlatform(new_x, new_y)
                else:
                    new_p = Platform(new_x, new_y)
            elif score >= 30:
                if random.random() < 0.3:  # 30% chance after 30 points
                    new_p = MovingPlatform(new_x, new_y)
                else:
                    new_p = Platform(new_x, new_y)
            else:
                new_p = Platform(new_x, new_y)

            platforms.add(new_p)
            all_sprites.add(new_p)                

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10,10))
        pygame.display.flip()

        clock.tick(FPS)


        # Game Over if fall
        if player.rect.top > HEIGHT:
            running = False

        
    

    # ---------------- GAME OVER SCREEN ----------------
    screen.fill(BLACK)
    big_font = pygame.font.SysFont("arial", 36)
    final_score = font.render(f"YOU REACHED {score} HEIGHT!", True, WHITE)
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 100))
    pygame.display.flip()
    pygame.time.wait(1000)

    # Check if player made top 5
    high_scores.append(("YOU", score))  # placeholder
    high_scores = sorted(high_scores, key=lambda x: x[1], reverse=True)[:5]
    
    if any(init == "YOU" and sc == score for init, sc in high_scores):
        rank = [s for s in high_scores].index(("YOU", score)) + 1

        if rank == 1:
            congrats = big_font.render("NEW HIGH SCORE!", True, GREEN)
            screen.blit(congrats, (WIDTH // 2 - congrats.get_width() // 2, 150))
            pygame.display.flip()
            pygame.time.wait(1500)

        initials = get_initials(screen, font)
        # Replace placeholder
        for i, (init, sc) in enumerate(high_scores):
            if sc == score and init == "YOU":
                high_scores[i] = (initials, score)
                break
        save_high_scores(high_scores)

    # ---------------- SHOW LEADERBOARD ----------------
    screen.fill(BLACK)
    leader_title = big_font.render("TOP 5 HEIGHTS", True, WHITE)
    screen.blit(leader_title, (WIDTH // 2 - leader_title.get_width() // 2, 40))

    y_offset = 100
    for i, (init, sc) in enumerate(high_scores, start=1):
        hs_text = font.render(f"{i}. {init}  {sc}", True, WHITE)
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, y_offset))
        y_offset += 40

    retry_msg = font.render("Press Enter to Play Again", True, WHITE)
    quit_msg = font.render("Press Esc to Return to Menu", True, WHITE)
    screen.blit(retry_msg, (WIDTH // 2 - retry_msg.get_width() // 2, y_offset + 20))
    screen.blit(quit_msg, (WIDTH // 2 - quit_msg.get_width() // 2, y_offset + 60))
    pygame.display.flip()

    # ---------------- WAIT FOR INPUT ----------------
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # restart
                    waiting = False
                elif event.key == pygame.K_ESCAPE:  # back to menu
                    return
        clock.tick(15)

        
