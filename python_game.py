import pygame
import sys
import random

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

        # Game Over screen
        screen.fill(BLACK)
        big_font = pygame.font.SysFont("arial", 36)
        msg = big_font.render("Game Over!", True, WHITE)
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        retry_msg = font.render("Press Enter to Play Again", True, WHITE)
        quit_msg = font.render("Press Esc to Return to Menu", True, WHITE)

        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(retry_msg, (WIDTH // 2 - retry_msg.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(quit_msg, (WIDTH // 2 - quit_msg.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        # Wait for player input
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


