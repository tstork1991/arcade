import pygame
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Arcade")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Font
font = pygame.font.SysFont("arial", 32)

# Menu options (your chosen names)
options = ["Python", "Jumper", "Quit"]
selected = 0  # track which menu item is highlighted


def draw_menu():
    """Draws the menu options on screen."""
    screen.fill(WHITE)

    # Title
    title = font.render("Choose a Game:", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    # Options
    for i, option in enumerate(options):
        color = RED if i == selected else BLACK
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 50))

    pygame.display.flip()


def main_menu():
    global selected
    clock = pygame.time.Clock()

    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Python":
                        print("Python game would start here!")  # placeholder
                        # later -> import python_game.run_game(screen)
                    elif options[selected] == "Jumper":
                        print("Jumper game would start here!")  # placeholder
                        # later -> import jumper.run_game(screen)
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()

        clock.tick(60)


if __name__ == "__main__":
    main_menu()
