import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 700
BLOCK_SIZE = 20
CELL = 20
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (105, 105, 105)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = GREY
BACKGROUND_COLOR = BLACK

def reset_game():
    snake = [(100, 100)]
    direction = (CELL, 0)
    food = (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL),
    )
    score = 0
    return snake, direction, food, score

def draw_grid():
    # Draw vertical lines
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    # Draw horizontal lines
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)


def draw(snake, food, score):
    screen.fill(BLACK)
    draw_grid()
    # Snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # Food
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # Score
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()


def game_loop():
    snake, direction, food, score = reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)

        # Move
        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # Collision
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake
        ):
            return score  # game over

        snake.insert(0, new_head)

        # Food
        if new_head == food:
            score += 1
            food = (
                random.randrange(0, WIDTH, CELL),
                random.randrange(0, HEIGHT, CELL),
            )
        else:
            snake.pop()

        draw(snake, food, score)
        clock.tick(FPS)

def show_game_over(score):
    while True:
        screen.fill(BLACK)
        msg1 = font.render(f"Game Over! Score: {score}", True, WHITE)
        msg2 = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(msg1, (WIDTH // 4, HEIGHT // 3))
        screen.blit(msg2, (WIDTH // 6, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# Main game loop
while True:
    final_score = game_loop()
    show_game_over(final_score)