# Lesson 7.14: Graphs and Mazes: Breadth-First Search

**Time:** 3 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/algo` and its `mazes` folder; squared paper and coloured pencils
· **New words:** graph, vertex, edge, breadth-first search, visited,
tuple

## Goal *(read this to the learner)*

> A **graph** is dots joined by lines: towns and roads, friends and
> friendships, computers and cables, or the squares of a maze and the
> steps between them. Today you'll solve mazes the way water floods a
> Minecraft cave: spreading out one block at a time in every direction,
> until it reaches the diamond. It's called **breadth-first search**, and
> it always finds the shortest way.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Copy `~/lab/algo/mazes/1-tiny.txt` onto squared paper, one
      character per square (or print it with `cat` and copy it by hand).

## Warm-up (5 min)

"What's a queue? What's FIFO?" *(A line: first in, first out.)* "Which
Python thing makes a fast queue?" *(A `deque`, with `append` and
`popleft`.)*

## Activity

### Session 1: graphs, and flooding a maze

1. **Dots and lines.** Draw a map of five Minecraft places (home, the
   mine, the village, the Nether portal, the farm) as dots, with lines
   for paths between some of them. **Say:** "This is a **graph**. The
   dots are called **vertices** (one is a vertex) and the lines are
   **edges**. Graphs are the most general data structure there is:
   lists and trees are just graphs with rules."

   **Ask:** "What's the fewest paths you need to walk from home to the
   portal?" Count by hops.

2. **A maze is a graph.** Look at the maze on squared paper. **Say:**
   "`#` is stone, and `.` is an open square. You start at `P` (the
   player) and the diamond is at `D`. Each open square is a vertex, and
   squares side by side (not diagonal) are joined by an edge."

3. **Flood it.** **Say:** "Water spreads one block at a time. Write 0 in
   `P`. Then write 1 in every open square next to it. Then 2 in every
   empty open square next to a 1. Keep going." Use a different colour
   for each number if you like. Stop when the water reaches `D`.

   **Ask:** "What number is on `D`?" *(10.)* "How do you find the actual
   path?" *(Start at `D` and step backwards to a square one smaller,
   each time: 9, 8, 7... back to 0.)* **Say:** "That's **breadth-first
   search**: it explores everything 1 step away, then everything 2 steps
   away, and so on. The first time it reaches the diamond must be the
   shortest way."

### Session 2: a maze in Python

4. **Read the maze.** In the terminal,
   `cat ~/lab/algo/mazes/2-two-ways.txt`.
   New file, `~/lab/algo/mazes.py`:
   ```python
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
   ```
   **Say:** "`rstrip("\n")` takes the newline off the end of each line.
   `grid[row][col]` is the letter at that row and column: rows count
   down from 0 at the top, columns across from 0 at the left. `(row,
   col)` is a **tuple**: a pair of values that go together, like a
   list that can't be changed. Tuples can be dictionary keys; lists
   can't (Lesson 7.12)."

   In the shell:
   ```
   >>> from mazes import read_maze, find
   >>> grid = read_maze("mazes/1-tiny.txt")
   >>> grid[1]
   '#P..#...#'
   >>> find(grid, "P")
   (1, 1)
   >>> find(grid, "D")
   (5, 7)
   ```
   *(If it says `FileNotFoundError`, Thonny's shell is in a different
   folder: run `mazes.py` once with F5 first, which moves the shell to
   `~/lab/algo`.)*

5. **Neighbours.** Add:
   ```python
   def neighbours(grid, spot):
       """The squares next to spot (up, down, left, right) that aren't walls."""
       row, col = spot
       result = []
       for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
           if grid[r][c] != "#":
               result.append((r, c))
       return result
   ```
   **Say:** "`row, col = spot` unpacks the tuple into two names. The list
   has the four squares around: up, down, left and right." Restart the
   shell (Stop), and try `neighbours(grid, (1, 1))` after reading the
   maze again. **They should see:** `[(2, 1), (1, 2)]`: down and right.
   *(Up and left are stone.)*

6. **Draw a path.** Add a function to show a path:
   ```python
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
   ```

### Session 3: breadth-first search

7. **The search.** **Say:** "The computer floods the maze like we did,
   using a queue: squares wait in line to have their neighbours
   explored. And for each square it reaches, it writes down *which
   square it came from*, like an arrow pointing back. Then it can
   follow the arrows back from the diamond." Add:
   ```python
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


   if __name__ == "__main__":
       grid = read_maze("mazes/1-tiny.txt")
       start = find(grid, "P")
       goal = find(grid, "D")
       path = shortest_path(grid, start, goal)
       print(f"From {start} to {goal}: {len(path) - 1} steps")
       draw(grid, path)
   ```
   **Say:** "`came_from` is a dictionary: for each square reached, the
   square it was reached from. It also remembers which squares have
   been **visited**, so we never explore one twice. The start came from
   nowhere: `None`. When the queue is empty and we never found the
   diamond, there's no way through."

   Run it. **They should see:**
   ```
   From (1, 1) to (5, 7): 10 steps
   #########
   #P..#...#
   #o#.#.#.#
   #o#...#.#
   #o#####.#
   #ooooooD#
   #########
   ```
   **Say:** "10, the same as the flood on paper!"

8. **Every maze.** In the terminal:
   ```
   python3 check.py bfs
   ```
   **They should see:** each maze with its number of steps, `the shortest
   there is`, and the path drawn. `6-sealed.txt` has `no way through, and
   shortest_path knew it.` Then `ALL GOOD!` Commit.

   **Ask:** "Look at `3-river.txt`. What did the path do?" *(Swam
   straight across the water, `~`: 8 steps.)* "Is that what you'd do in
   Minecraft?" *(Maybe not: swimming is slow!)* **Say:** "Next lesson:
   when some steps cost more than others."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: read_maze('mazes/1-tiny.txt') left the newlines on the rows.` | `.rstrip("\n")` is missing | `grid.append(line.rstrip("\n"))`. |
| `NOT YET: in mazes/1-tiny.txt, shortest_path took 14 steps, but it can be done in 10.` | `queue.pop()` instead of `queue.popleft()`: that takes the newest square, not the oldest, so it isn't breadth-first | `popleft()`. |
| `NOT YET: that took more than 10 seconds...` | Squares are explored again and again: the `if next_spot not in came_from:` check is missing | Only add squares that haven't been visited. |
| `NOT YET: shortest_path's path should start at P ... but it goes from (5, 7) to (1, 1).` | The path is backwards | `path.reverse()` in `path_back`. |
| `FileNotFoundError: [Errno 2] No such file or directory: 'mazes/1-tiny.txt'` | The program ran in a different folder | Save `mazes.py` in `~/lab/algo`, and run it from there. |
| `TypeError: cannot unpack non-iterable NoneType object` | `find` gave `None`: there's no `P` or `D` in the maze | Check the maze file has both. |

## Talk about it

- What's a graph? What are vertices and edges? Give three examples.
- Why does breadth-first search find the *shortest* path?
- What two jobs does the `came_from` dictionary do?

## Challenge *(if there's time, or for next time)*

- Make your own maze in `mazes/7-mine.txt`, with a `#` border all the
  way round, one `P` and one `D`. Run the checker on it.
- Change `shortest_path` to count how many squares it visited. How many
  for each maze, compared with the path length?
- Five friends: Alex knows Sam and Jo; Sam knows Kit; Jo knows Kit and
  Max. Write it as a dictionary of lists (`{"Alex": ["Sam", "Jo"],
  ...}`), and change `shortest_path` to use it in place of
  `neighbours`. How many hops from Alex to Max?

## Checkpoint

The learner can, without help:
- [ ] Explain graphs, vertices and edges, with examples
- [ ] Flood a maze by hand, and find the path back
- [ ] Explain breadth-first search with a queue and `came_from`
- [ ] Pass `python3 check.py bfs`

## Lab notebook

Stick in the flooded paper maze. Draw a five-place graph and its
shortest hops. Commit. Add *graph*, *vertex*, *edge*, *breadth-first
search*, *visited* and *tuple* to `dictionary.md`.

## Guide's background *(optional reading)*

A **graph** is a set of vertices (or nodes) and edges between them.
Graphs model maps, social networks, the web, computer networks,
dependencies between tasks, and states of a game. **Breadth-first
search** (BFS) explores a graph in order of distance from the start,
using a queue; on a graph where every edge counts the same, the first
time it reaches a vertex is by a shortest path. It visits each vertex
and edge once, so it's O(V + E).

The `came_from` dictionary is the standard trick for recovering the
path: each vertex records its predecessor, and following predecessors
from the goal gives the path in reverse. Replace the queue with a stack
and the same code becomes **depth-first search**, which goes as deep as
it can before backing up; it finds *a* path but not the shortest, which
is exactly the 14-step bug in the table. Lesson 7.16 uses depth-first
search on purpose, to *make* mazes.
