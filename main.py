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
BLUE = (50, 100, 200)
YELLOW = (240, 200, 0)

# Fonts (try "comicsansms" or "arialblack" for a chunkier style)
title_font = pygame.font.SysFont("arialblack", 48)
menu_font = pygame.font.SysFont("arial", 32)

# Menu options
options = ["Python", "Jumper", "Quit"]
selected = 0


def draw_menu():
    """Draws the arcade menu with visuals."""
    # Background
    screen.fill(BLUE)

    # Title
    title = title_font.render("Mini Arcade", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    # Options
    for i, option in enumerate(options):
        # Highlight box
        if i == selected:
            pygame.draw.rect(
                screen, YELLOW,
                (WIDTH // 2 - 120, 150 + i * 60, 240, 50),
                border_radius=10
            )

        # Text
        color = BLACK if i == selected else WHITE
        text = menu_font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 160 + i * 60))

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
                        print("Python game would start here!")
                    elif options[selected] == "Jumper":
                        print("Jumper game would start here!")
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()

        clock.tick(60)


if __name__ == "__main__":
    main_menu()
