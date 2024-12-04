import pygame
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIDTH = GRID_SIZE * GRID_WIDTH
HEIGHT = GRID_SIZE * GRID_HEIGHT + 50  # Extra space for step count display

# Vibrant Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Pathfinding Visualization with Dynamic Obstacles")

# Create grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Initialize start and goal positions
start = None
goal = None

# Font for displaying step count
font = pygame.font.Font(None, 36)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if grid[y][x] == 1:  # Barrier
                pygame.draw.rect(screen, BLACK, rect)
            elif (y, x) == start:
                pygame.draw.rect(screen, RED, rect)
            elif (y, x) == goal:
                pygame.draw.rect(screen, GREEN, rect)

def get_neighbors(y, x):
    neighbors = []
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH and grid[ny][nx] != 1:
            neighbors.append((ny, nx))
    return neighbors

def draw_step_count(steps):
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))
    step_text = font.render(f"Steps: {steps}", True, BLACK)
    screen.blit(step_text, (10, HEIGHT - 40))
    pygame.display.flip()

def bfs():
    if not start or not goal:
        return None

    queue = deque([(start, [start])])
    visited = set()
    steps = 0

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = pygame.mouse.get_pos()
                    grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
                    if y < HEIGHT - 50 and (grid_y, grid_x) != start and (grid_y, grid_x) != goal:
                        grid[grid_y][grid_x] = 1  # Place obstacle
                        draw_grid()
                        pygame.display.flip()

        current, path = queue.popleft()
        steps += 1

        if current not in visited:
            visited.add(current)

            if current == goal:
                return path, steps

            for neighbor in get_neighbors(*current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
                    if neighbor != goal:
                        pygame.draw.rect(screen, YELLOW, (neighbor[1] * GRID_SIZE, neighbor[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        if current != start and current != goal:
            pygame.draw.rect(screen, PURPLE, (current[1] * GRID_SIZE, current[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        draw_step_count(steps)
        pygame.display.flip()
        pygame.time.wait(50)

    return None, steps

# Main game loop
running = True
drawing_barriers = False
steps_taken = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
            if y < HEIGHT - 50:  # Ensure click is within grid
                if event.button == 1:  # Left mouse button
                    if not start:
                        start = (grid_y, grid_x)
                    elif not goal:
                        goal = (grid_y, grid_x)
                    else:
                        drawing_barriers = True
                elif event.button == 3:  # Right mouse button
                    if (grid_y, grid_x) == start:
                        start = None
                    elif (grid_y, grid_x) == goal:
                        goal = None
                    else:
                        grid[grid_y][grid_x] = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing_barriers = False
        elif event.type == pygame.MOUSEMOTION and drawing_barriers:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
            if y < HEIGHT - 50:  # Ensure within grid
                if (grid_y, grid_x) != start and (grid_y, grid_x) != goal:
                    grid[grid_y][grid_x] = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                result = bfs()
                if result:
                    path, steps_taken = result
                    # Redraw the grid to clear previous visualizations
                    screen.fill(WHITE)
                    draw_grid()
                    
                    # Draw the final path
                    for i in range(len(path) - 1):
                        start_pos = path[i]
                        end_pos = path[i + 1]
                        start_center = (start_pos[1] * GRID_SIZE + GRID_SIZE // 2, start_pos[0] * GRID_SIZE + GRID_SIZE // 2)
                        end_center = (end_pos[1] * GRID_SIZE + GRID_SIZE // 2, end_pos[0] * GRID_SIZE + GRID_SIZE // 2)
                        pygame.draw.line(screen, BLUE, start_center, end_center, 4)
                    
                    draw_step_count(steps_taken)
                    pygame.display.flip()

    screen.fill(WHITE)
    draw_grid()
    draw_step_count(steps_taken)
    pygame.display.flip()

pygame.quit()
sys.exit()
