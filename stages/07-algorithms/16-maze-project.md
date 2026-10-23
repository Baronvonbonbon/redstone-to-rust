# Lesson 7.16: Project: The Block-World Maze Maker

**Time:** 3–4 sessions of 45 min, plus demo day · **You need:** a
terminal; Thonny; `~/lab/algo`, with `mazes.py` passing both maze
checks; squared paper · **New words:** depth-first search, maze
generation, animation

## Goal *(read this to the learner)*

> Time to put the whole stage together. You'll write a program that
> *makes* mazes: it starts with solid stone and tunnels through it like
> a very determined miner, using a stack and depth-first search. Then
> you'll add water and secret holes, watch breadth-first search flood
> your maze in the terminal, and race your solvers on mazes far too big
> to solve by hand. Then you'll show it off, and take the Stage 7
> checkpoint.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once, and the checkpoint at the end.
- [ ] `python3 check.py bfs` and `python3 check.py dijkstra` should both
      pass (Lessons 7.14 and 7.15).

## Warm-up (5 min)

"In BFS, what happens if we use a stack instead of a queue?" *(It goes
as deep as it can down one tunnel before trying another: depth-first
search. It finds *a* way, but not the shortest.)* "Today, that's
exactly what we want."

## Activity

### Session 1: carving a maze

1. **The miner's plan.** On squared paper, draw a grid of 4 by 4
   "rooms": dots on every other square, with stone everywhere else.
   **Say:** "A miner starts in the top-left room. Each turn: look at the
   rooms two squares away (up, down, left, right) that are still solid.
   Pick one at random, dig through the wall between, and move there. If
   there are none left, step *back* to the room before. When the miner
   has stepped all the way back to the start, every room has been dug,
   and there's exactly one way between any two rooms."

   Do it on paper, rolling a die (or picking a card) to choose. Keep a
   list of the rooms you came through: that's the stack. Stepping back
   is `pop`.

2. **The maze maker.** New file, `~/lab/algo/maker.py`:
   ```python
   import random
   import sys


   def make_maze(rooms_down, rooms_across):
       """A random maze, carved out of solid stone by depth-first search."""
       height = 2 * rooms_down + 1
       width = 2 * rooms_across + 1
       grid = []
       for row in range(height):
           grid.append(["#"] * width)

       grid[1][1] = "."
       stack = [(1, 1)]
       while len(stack) > 0:
           row, col = stack[-1]
           choices = []
           for r, c in [(row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]:
               if 0 < r < height and 0 < c < width and grid[r][c] == "#":
                   choices.append((r, c))
           if choices == []:
               stack.pop()
           else:
               r, c = random.choice(choices)
               grid[(row + r) // 2][(col + c) // 2] = "."
               grid[r][c] = "."
               stack.append((r, c))
       return grid
   ```
   **Say:** "`["#"] * width` makes a list of `width` stones. Each row is a
   list, not a string, so we can change squares. `stack[-1]` is the top
   of the stack: the room the miner is in now. `(row + r) // 2` is the
   wall halfway between two rooms."

3. **Finish it off.** Add the rest:
   ```python
   def add_extras(grid, holes, water):
       """Knocks down some walls to make loops, and floods some squares."""
       height = len(grid)
       width = len(grid[0])
       for i in range(holes):
           row = random.randint(1, height - 2)
           col = random.randint(1, width - 2)
           grid[row][col] = "."
       for i in range(water):
           row = random.randint(1, height - 2)
           col = random.randint(1, width - 2)
           if grid[row][col] == ".":
               grid[row][col] = "~"
       grid[1][1] = "P"
       grid[height - 2][width - 2] = "D"


   def save(grid, filename):
       with open(filename, "w") as f:
           for row in grid:
               f.write("".join(row) + "\n")


   if __name__ == "__main__":
       grid = make_maze(10, 30)
       add_extras(grid, 40, 60)
       save(grid, sys.argv[1])
       for row in grid:
           print("".join(row))
   ```
   **Say:** "A perfect maze has only one way through, which makes BFS
   and Dijkstra boring. So we knock out 40 random squares to make loops,
   and flood up to 60 with water. The holes stay inside the border, so
   the maze is still sealed. `"".join(row)` glues a row's squares back
   into a string."

   In the terminal, in `~/lab/algo`:
   ```
   python3 maker.py mazes/7-mine.txt
   ```
   **They should see:** a maze 61 squares wide and 21 tall, with `P` at
   the top left, `D` at the bottom right, and water scattered through
   it. A different one every time. Commit.

### Session 2: watching the flood

4. **The watcher.** New file, `~/lab/algo/watch.py`:
   ```python
   import os
   import sys
   import time
   from collections import deque
   from mazes import read_maze, find, neighbours, path_back


   def show(grid, explored, path):
       """Clears the screen and draws the maze: , for explored, o for the path."""
       os.system("clear")
       for row in range(len(grid)):
           line = ""
           for col in range(len(grid[row])):
               square = grid[row][col]
               if square in "PD":
                   line = line + square
               elif (row, col) in path:
                   line = line + "o"
               elif (row, col) in explored and square == ".":
                   line = line + ","
               else:
                   line = line + square
           print(line)


   grid = read_maze(sys.argv[1])
   start = find(grid, "P")
   goal = find(grid, "D")

   came_from = {start: None}
   queue = deque([start])
   while len(queue) > 0:
       spot = queue.popleft()
       if spot == goal:
           break
       for next_spot in neighbours(grid, spot):
           if next_spot not in came_from:
               came_from[next_spot] = spot
               queue.append(next_spot)
       show(grid, came_from, [])
       time.sleep(0.02)

   if goal in came_from:
       path = path_back(came_from, goal)
       show(grid, came_from, path)
       print(f"Found the diamond in {len(path) - 1} steps,"
             f" after exploring {len(came_from)} squares.")
   else:
       print("There's no way through!")
   ```
   **Say:** "It's BFS again, but after every square it explores, it
   clears the screen (like the `clear` command from Stage 1) and draws
   the maze, with `,` on every square explored so far. Drawing over and
   over, fast, is **animation**: it's how every game works."

   Make the terminal window big enough for the maze, then:
   ```
   python3 watch.py mazes/7-mine.txt
   ```
   **They should see:** commas spreading out from `P` in every direction
   at once, like water flooding a cave, until they reach `D`. Then the
   path appears as `o`s, and a line like `Found the diamond in 140
   steps, after exploring 617 squares.` (The numbers depend on the
   maze.) It takes about 15 seconds. *(Run it in the terminal, not in
   Thonny: Thonny's shell can't clear the screen.)*

5. **Check your maze.** **Say:** "The checker runs on every maze in the
   `mazes` folder, so it'll check yours too."
   ```
   python3 check.py bfs
   python3 check.py dijkstra
   ```
   **They should see:** `mazes/7-mine.txt` in each list, with `the
   shortest there is` and `the cheapest there is`. *(Big mazes aren't
   drawn: only small ones.)* Commit, including the maze.

### Session 3: make it your own

6. **Choose at least two.** Each one is a small project. Plan on paper
   first; commit after each.
   - **Watch Dijkstra.** Make `watch_cheap.py`, using a heap and costs,
     like `cheapest_path`. Watch how the flood goes around water instead
     of through it.
   - **Watch depth-first.** Make the watcher use `queue.pop()` instead of
     `popleft()`. How is the exploring different? Is the path shorter or
     longer?
   - **Race.** For a maze of 30 by 38 rooms, count how many squares BFS
     explores before it finds the diamond, compared with the length of
     the path.
   - **A bigger world.** Add soul sand (`:`, cost 3) and lava (`!`, which
     can't be crossed) to `maker.py`, `COST` and `neighbours`.
   - **Colour.** In the terminal, `"\033[34m~\033[0m"` prints a blue `~`.
     Colour the water blue, and the path yellow (`33`).
   - **Paper mazes.** Print a maze from `maker.py` (with no water), and
     challenge the family to solve it with a pencil. Time them, and time
     BFS.

### Session 4: demo day and checkpoint

7. **Demo day.** The learner shows the family: making a maze, watching
   it flood, and the cheapest path around the water. They explain one
   thing from the stage in their own words: why BFS finds the shortest
   path, or why merge sort is fast.

8. **Stage 7 checkpoint.** On paper, without the computer unless it
   says so. The guide reads the questions; answers are in italics.
   - *Big-O.* Say the Big-O of: linear search *(O(n))*; binary search
     *(O(log n))*; selection sort *(O(n²))*; merge sort *(O(n log n))*;
     a dictionary lookup *(O(1) on average)*; a loop inside a loop over
     the same list *(O(n²))*.
   - *Growth.* An O(n²) program takes 2 seconds for 1000 items. About how
     long for 3000? *(9 times as long: 18 seconds.)*
   - *Logarithms.* What's log₂ of 1024? *(10.)* How many guesses to find
     a number from 1 to a thousand by halving? *(10.)*
   - *Sorting.* Do merge sort on 6 cards, drawing the splits and
     merges.
   - *Recursion.* Write `count_down(n)`, which gives back a list `[n,
     n - 1, ..., 1]`, recursively. Say its base case. *(Base case:
     `n == 0` gives `[]`; otherwise `[n] + count_down(n - 1)`.)*
   - *Proof.* Prove that even plus odd is odd. *(2a + 2b + 1 = 2(a + b)
     + 1.)* Explain induction with dominoes.
   - *Data structures.* Which would you use, and why? An undo button
     *(a stack)*; people waiting for a ride at a theme park *(a
     queue)*; looking up a mob's health by name *(a dictionary, a hash
     table)*; keeping numbers in order while adding new ones *(a
     balanced tree)*; the fewest hops between friends *(a graph, with
     BFS)*.
   - *At the computer.* Every check passes:
     ```
     for c in search sorts recursion merge quick brackets linked hash bst bfs dijkstra; do python3 check.py $c | tail -1; done
     ```
     **They should see:** eleven lines of `ALL GOOD!`.

   When it's done, the guide signs the passport: **Algorithm Wizard**.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `IndexError: list index out of range` in `maker.py` | `sys.argv[1]` is missing: no filename was given | `python3 maker.py mazes/7-mine.txt`. |
| `TypeError: 'str' object does not support item assignment` | A row is a string, so its squares can't be changed | Make rows as lists, `["#"] * width`, and only join them when saving. |
| The maze has no tunnels, just `P` and `D` | The `while` loop never runs, or `grid[1][1] = "."` is missing | Check both against the lesson. |
| The maze is a mess of tunnels with no walls | `holes` is too big | Try 40 holes for a 10 by 30 maze. |
| `watch.py` scrolls instead of animating | It's running in Thonny | Run it in the terminal. |
| `watch.py` shows `TERM environment variable not set.` | It's running somewhere that isn't a terminal | Run it in the terminal. |
| The maze doesn't fit the terminal | The window is too small | Make the window bigger, or the font smaller (Ctrl+minus), or make a smaller maze. |

## Talk about it

- How does the maze maker use a stack? What does stepping back do?
- Why does the watcher's flood spread evenly, but depth-first search
  dig one long tunnel?
- What was the hardest idea in this stage? The most surprising?

## Challenge *(if there's time, or for next time)*

- Make the maze maker recursive: `carve(row, col)` digs to a random
  neighbour and calls `carve` there. Why does it crash for big mazes?
  *(RecursionError: the call stack is the miner's stack, and it gets
  too deep.)*
- Read about the A\* algorithm (say "A star"): Dijkstra with a guess of
  how far is left. It explores far fewer squares. Can you build it?
- Build one of your mazes in Luanti (Stage 4's world), and walk it.

## Checkpoint

The learner can, without help:
- [ ] Make random mazes with a depth-first search and a stack
- [ ] Animate a search in the terminal
- [ ] Pass every check, on the course's mazes and their own
- [ ] Pass the Stage 7 checkpoint above

## Lab notebook

Stick in a printed maze with the path drawn in. Write which extras were
built, and what was learned. Fill in the stage's dictionary words. Commit.
On the passport: Algorithm Wizard.

## Guide's background *(optional reading)*

The maze maker is the **recursive backtracker**, a depth-first search
that visits every room exactly once; the rooms and the tunnels between
them form a tree (Lesson 7.13), which is why a perfect maze has exactly
one path between any two points. Adding holes adds cycles, turning the
tree into a general graph, which is what makes BFS and Dijkstra
interesting. Other maze algorithms (Prim's, Kruskal's, Wilson's) make
mazes with different "textures", and are themselves graph algorithms.

This stage has covered the core of a first university algorithms
course: Big-O, searching, sorting, recursion, proof by invariant and
induction, stacks, queues, linked lists, hash tables, trees, heaps and
graph search. Stage 8 returns to the Hack computer and climbs the
software half of Nand to Tetris, where these ideas are used for real: a
**stack** machine, a **symbol table** (a hash table), and a compiler
that walks a **tree** with **recursion**.
