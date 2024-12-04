# Pathfinding Algorithm Visualizer

A **Pathfinding Algorithm Visualizer** implemented in Python using **Pygame**, featuring **DFS**, **A***, and **Dynamic A*** algorithms. This interactive tool allows users to visualize how these algorithms explore the grid to find the shortest path between two points, even with dynamic obstacles.

## Features

- **Algorithms**:
  - **DFS (Depth-First Search)**: Explores as far as possible along each branch before backtracking.
  - **A***: Finds the shortest path using a heuristic (Manhattan Distance).
  - **Dynamic A***: Adapts A* for real-time obstacle detection and path adjustments.

- **Dynamic Obstacle Placement**:
  - Add or remove obstacles while the algorithm is running, and observe how paths adjust in real-time (Dynamic A*).

- **Interactive Grid**:
  - Set **start** (red) and **goal** (green) points by clicking.
  - Draw **obstacles** (black) by dragging the mouse.
  - Visualize the algorithm’s exploration and final path using vibrant colors.

- **Step Counter**:
  - Track the number of steps taken by the algorithm during the search.

## How to Use

1. **Set Start and Goal Points**:
   - Left-click to place the start and goal points.
   
2. **Add Obstacles**:
   - Left-click and drag to draw obstacles (black cells).
   - Right-click to remove obstacles or reset the start/goal points.

3. **Run an Algorithm**:
   - Press the corresponding key to run the desired algorithm:
     - **D**: Depth-First Search (DFS)
     - **A**: A* Search
     - **S**: Dynamic A*
   - Press **Spacebar** to pause/resume.

4. **Reset the Grid**:
   - Press **R** to reset the grid for a new visualization.

## Color Legend

- **Red**: Start point
- **Green**: Goal point
- **Black**: Obstacles
- **Yellow**: Nodes visited but not in the final path
- **Purple**: Nodes being processed
- **Blue**: Final shortest path

## Requirements

- **Python 3.x**
- **Pygame**

### Install Dependencies

```bash
pip install pygame
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/SyedNazmusSakib-SNS/Pathfinding_visualizer.git
   cd Pathfinding_visualizer
   ```

2. Run the visualizer:
   ```bash
   python A_star.py  # Replace with BFS.py, DFS.py, or Dynamic_A_star.py as needed
   ```





