import pygame
import sys
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIDTH = GRID_SIZE * GRID_WIDTH
HEIGHT = GRID_SIZE * GRID_HEIGHT + 50  # Extra space for cost display

# Vibrant Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization with Dynamic Obstacles")

# Create grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Initialize start and goal positions
start = None
goal = None

# Font for displaying cost
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

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def cost(current, next):
    return 1

def draw_path_cost(cost):
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))
    cost_text = font.render(f"Path Cost: {cost}", True, BLACK)
    screen.blit(cost_text, (10, HEIGHT - 40))
    pygame.display.flip()

def astar():
    if not start or not goal:
        return None

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set_hash = {start}

    while not open_set.empty():
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

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal]

        for neighbor in get_neighbors(*current):
            temp_g_score = g_score[current] + cost(current, neighbor)

            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != goal:
                        pygame.draw.rect(screen, ORANGE, (neighbor[1] * GRID_SIZE, neighbor[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        if current != start and current != goal:
            pygame.draw.rect(screen, PURPLE, (current[1] * GRID_SIZE, current[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        draw_path_cost(g_score[current])
        pygame.display.flip()
        pygame.time.wait(50)

    return None, 0

# Main game loop
running = True
drawing_barriers = False
path_cost = 0

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
                result = astar()
                if result:
                    path, path_cost = result
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
                    
                    draw_path_cost(path_cost)
                    pygame.display.flip()

    screen.fill(WHITE)
    draw_grid()
    draw_path_cost(path_cost)
    pygame.display.flip()

pygame.quit()
sys.exit()