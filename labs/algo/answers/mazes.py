import heapq
from collections import deque


def read_maze(filename):
    """Gives back the maze as a list of rows, without the newlines."""
    grid = []
    for line in open(filename):
        grid.append(line.rstrip("\n"))
    return grid


def find(grid, letter):
    """Gives back the (row, col) of the first square with that letter."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == letter:
                return (row, col)
    return None


def neighbours(grid, spot):
    """The squares next to spot (up, down, left, right) that aren't walls."""
    row, col = spot
    result = []
    for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if grid[r][c] != "#":
            result.append((r, c))
    return result


def draw(grid, path):
    """Prints the maze with the path marked by o."""
    for row in range(len(grid)):
        line = ""
        for col in range(len(grid[row])):
            if (row, col) in path and grid[row][col] not in "PD":
                line = line + "o"
            else:
                line = line + grid[row][col]
        print(line)


def path_back(came_from, goal):
    """Follows the arrows back from the goal to the start."""
    path = []
    spot = goal
    while spot is not None:
        path.append(spot)
        spot = came_from[spot]
    path.reverse()
    return path


def shortest_path(grid, start, goal):
    """Breadth-first search. Gives back a list of spots, or None."""
    came_from = {start: None}
    queue = deque([start])
    while len(queue) > 0:
        spot = queue.popleft()
        if spot == goal:
            return path_back(came_from, goal)
        for next_spot in neighbours(grid, spot):
            if next_spot not in came_from:
                came_from[next_spot] = spot
                queue.append(next_spot)
    return None


COST = {".": 1, "P": 1, "D": 1, "~": 5}


def cheapest_path(grid, start, goal):
    """Dijkstra's algorithm. Gives back (cost, path), or None."""
    came_from = {start: None}
    todo = [(0, start)]
    while len(todo) > 0:
        cost, spot = heapq.heappop(todo)
        if spot == goal:
            return (cost, path_back(came_from, goal))
        for next_spot in neighbours(grid, spot):
            if next_spot not in came_from:
                came_from[next_spot] = spot
                row, col = next_spot
                heapq.heappush(todo, (cost + COST[grid[row][col]], next_spot))
    return None


if __name__ == "__main__":
    grid = read_maze("mazes/1-tiny.txt")
    start = find(grid, "P")
    goal = find(grid, "D")
    path = shortest_path(grid, start, goal)
    print(f"From {start} to {goal}: {len(path) - 1} steps")
    draw(grid, path)
