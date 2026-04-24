
import pygame 
import sys
import random

# Configuration
CELL_SIZE = 20
GRID_W, GRID_H = 30, 20
SCREEN_W, SCREEN_H = GRID_W * CELL_SIZE, GRID_H * CELL_SIZE
FPS = 12
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# Initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

def draw_rect(color, pos):
    r = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, r)

def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_W-1), random.randint(0, GRID_H-1))
        if pos not in snake:
            return pos

def main():
    snake = [(GRID_W//2, GRID_H//2), (GRID_W//2-1, GRID_H//2), (GRID_W//2-2, GRID_H//2)]
    direction = (1, 0)  # moving right
    food = random_food(snake)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    return main()  # restart
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # move snake
            new_head = ((snake[0][0] + direction[0]) % GRID_W,
                        (snake[0][1] + direction[1]) % GRID_H)
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        # draw
        screen.fill(BLACK)
        # grid (optional)
        for x in range(0, SCREEN_W, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_H))
        for y in range(0, SCREEN_H, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_W, y))

        # draw food and snake
        draw_rect(RED, food)
        for i, seg in enumerate(snake):
            color = GREEN if i == 0 else (0, 160, 0)
            draw_rect(color, seg)

        # HUD
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (5, 5))

        if game_over:
            over_surf = font.render("Game Over! R: Restart  Q: Quit", True, WHITE)
            rect = over_surf.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
            screen.blit(over_surf, rect)

        pygame.display.flip()
        clock.tick(FPS + score // 5)  # speed up slightly with score

if __name__ == "__main__":
    main()
