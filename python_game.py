import pygame
import sys
import random
import os

# Load high scores from file
def load_high_scores():
    if not os.path.exists("highscores.txt"):
        return []
    scores = []
    with open("highscores.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2 and parts[1].isdigit():
                initials, score = parts
                scores.append((initials, int(score)))
    return scores

# Save high scores to file
def save_high_scores(scores):
    with open("highscores.txt", "w") as f:
        for initials, score in scores[:5]:
            f.write(f"{initials} {score}\n")

# Prompt for initials (arcade style)
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
TILE_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)


def run_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    #high score setup
    high_scores = load_high_scores()

    # Snake setup
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (TILE_SIZE, 0)  # moving right

    # Food setup
    food = (WIDTH // 2, HEIGHT // 2)

    # Score
    score = 0

    while True:
        #reset game 
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("arial", 24)

        snake = [(100, 100), (80,100), (60, 100)]
        direction = (TILE_SIZE, 0)
        food = (WIDTH // 2, HEIGHT // 2)
        score = 0
        running = True

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, TILE_SIZE):
                        direction = (0, -TILE_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -TILE_SIZE):
                        direction = (0, TILE_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (TILE_SIZE, 0):
                        direction = (-TILE_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-TILE_SIZE, 0):
                        direction = (TILE_SIZE, 0)

            # Move snake
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)

            # Check collisions
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake[1:]
            ):
                running = False  # game over

            # Check food
            if new_head == food:
                score += 1
                food = (
                    random.randrange(0, WIDTH, TILE_SIZE),
                    random.randrange(0, HEIGHT, TILE_SIZE)
                )
            else:
                snake.pop()  # remove tail

            # Drawing
            screen.fill(BLACK)
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (segment[0], segment[1], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, RED, (food[0], food[1], TILE_SIZE, TILE_SIZE))
        
            # Draw score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            pygame.display.flip()

            clock.tick(FPS)

        # ---------------- GAME OVER SCREEN ----------------
        screen.fill(BLACK)
        big_font = pygame.font.SysFont("arial", 36)
        msg = big_font.render("Game Over!", True, WHITE)
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 60))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 110))
        pygame.display.flip()
        pygame.time.wait(1000)

        # Check if player made top 5
        high_scores.append(("YOU", score))  # placeholder initials
        high_scores = sorted(high_scores, key=lambda x: x[1], reverse=True)[:5]
        
        if any(init == "YOU" and sc == score for init, sc in high_scores):
            rank = [s for s in high_scores].index(("YOU", score)) + 1

            if rank == 1:
                congrats = big_font.render("YOU'RE NUMBER 1!", True, RED)
                screen.blit(congrats, (WIDTH // 2 - congrats.get_width() // 2, 160))
                pygame.display.flip()
                pygame.time.wait(1500)

            initials = get_initials(screen, font)
            # Replace placeholder initials
            for i, (init, sc) in enumerate(high_scores):
                if sc == score and init == "YOU":
                    high_scores[i] = (initials, score)
                    break
            save_high_scores(high_scores)

        # ---------------- SHOW LEADERBOARD ----------------
        screen.fill(BLACK)
        leader_title = big_font.render("TOP 5 SCORES", True, WHITE)
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
            clock.tick(15)  # prevent freeze




