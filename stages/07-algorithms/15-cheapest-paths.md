# Lesson 7.15: The Cheapest Way: Dijkstra's Algorithm

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
`mazes.py` from Lesson 7.14; squared paper; about 15 small cards or
sticky notes · **New words:** weight, priority queue, heap, Dijkstra's
algorithm

## Goal *(read this to the learner)*

> Breadth-first search finds the path with the fewest *steps*. But in
> Minecraft, swimming is slow: crossing 7 blocks of water takes longer
> than walking 12 blocks of grass. When some steps cost more than
> others, we need the *cheapest* path, not the shortest. Today you'll
> change just a few lines of your maze solver, using a new kind of queue
> that always lets the cheapest go first. It's called **Dijkstra's
> algorithm**, and something like it runs inside every map app.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `python3 check.py bfs` should pass (Lesson 7.14).
- [ ] Copy `mazes/3-river.txt` onto squared paper.

## Warm-up (5 min)

"In `3-river.txt`, what path did breadth-first search take?" *(Straight
across the water.)* "Why does BFS always find the fewest steps?" *(It
explores everything 1 step away, then 2, then 3...)*

## Activity

### Session 1: costs, and a queue that cheats

1. **Costs.** **Say:** "From now on, every square costs something to step
   into. Grass (`.`) costs 1. Water (`~`) costs 5, because swimming is
   slow. The cost of each step is called its **weight**." On the paper
   maze, add up the cost of BFS's path straight across the river. *(7
   water squares at 5, plus 1 for the diamond: 36.)* Then the long way
   round. *(12 steps on grass: 12.)*

   **Ask:** "Which would you take?" *(The long way: it's much cheaper!)*

2. **A queue where the cheapest goes first.** **Say:** "BFS used a queue:
   first in, first out. Now we need a queue where the *cheapest* thing
   always comes out first, wherever it is in the line. That's a
   **priority queue**." Act it out with cards: write "walk 1", "swim 5",
   "climb 3" on cards, put them in a pile in any order, and always take
   out the smallest number.

3. **Python's priority queue.** In the shell:
   ```
   >>> import heapq
   >>> todo = []
   >>> heapq.heappush(todo, (5, "swim"))
   >>> heapq.heappush(todo, (1, "walk"))
   >>> heapq.heappush(todo, (3, "climb"))
   >>> heapq.heappop(todo)
   (1, 'walk')
   >>> heapq.heappop(todo)
   (3, 'climb')
   >>> todo
   [(5, 'swim')]
   ```
   **Say:** "`heapq` keeps the list in a clever half-sorted shape called a
   **heap**, so the smallest is always at the front. Pushing and popping
   are both O(log n). The tuples are compared by their first item: the
   cost."

4. **Dijkstra by hand.** On the paper river maze, with cards. **Say:**
   "The rule: always explore the cheapest square in the pile. When you
   explore a square, add a card for each of its neighbours that doesn't
   have a card yet, with the cost of getting there: this square's cost
   plus the neighbour's weight. And draw an arrow back."

   Start with a card "P: 0". Explore it: the water square to the right
   gets a card saying 5 (0 so far, plus 5 to enter water), and the grass
   square below gets 1. The pile has 5 and 1: take 1 next, not 5! Keep
   going. **They should see:** the grass path around the bottom gets
   explored first, because the grass cards are cheaper than the water
   cards. `D` is reached with cost 12, before the water route can get
   there.

### Session 2: Dijkstra in Python

5. **Change BFS.** **Say:** "Dijkstra's algorithm is BFS with two
   changes: the queue becomes a priority queue, and each square in it
   has a cost." Add `import heapq` as the first line of `mazes.py`.
   Then add, above the `if __name__` line:
   ```python
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
   ```
   **Say:** "`COST` is a dictionary from each kind of square to its
   weight. Compare it with `shortest_path` line by line: `popleft`
   became `heappop`, `append` became `heappush`, and each square in the
   queue carries its cost. Everything else is the same!"

6. **The checker.**
   ```
   python3 check.py dijkstra
   ```
   **They should see:** each maze with its cost and `the cheapest there
   is`, ending with `ALL GOOD!`. In `3-river.txt`, the drawn path goes
   around the bottom, under the river. Commit.

7. **Compare them.** New file, `~/lab/algo/compare.py`:
   ```python
   from mazes import read_maze, find, shortest_path, cheapest_path, COST


   def path_cost(grid, path):
       """What a path costs: every square entered after the start."""
       cost = 0
       for row, col in path[1:]:
           cost = cost + COST[grid[row][col]]
       return cost


   for name in ["3-river", "4-swamp", "5-ford"]:
       grid = read_maze(f"mazes/{name}.txt")
       start = find(grid, "P")
       goal = find(grid, "D")
       fewest = shortest_path(grid, start, goal)
       cost, cheapest = cheapest_path(grid, start, goal)
       print(f"{name}:")
       print(f"  fewest steps: {len(fewest) - 1} steps, costing {path_cost(grid, fewest)}")
       print(f"  cheapest:     {len(cheapest) - 1} steps, costing {cost}")
   ```
   **They should see:**
   ```
   3-river:
     fewest steps: 8 steps, costing 36
     cheapest:     12 steps, costing 12
   4-swamp:
     fewest steps: 22 steps, costing 46
     cheapest:     26 steps, costing 26
   5-ford:
     fewest steps: 30 steps, costing 34
     cheapest:     30 steps, costing 34
   ```
   **Ask:** "In the ford, why does the cheapest path still swim?" Look at
   `cat mazes/5-ford.txt`. *(Going round the water is 8 more steps.
   Swimming one square only costs 4 more than walking it. Dijkstra weighs
   it up exactly.)*

### Session 3 (or the end of Session 2): maps and networks

8. **Dijkstra in the real world.** **Say:** "A map app treats roads as a
   graph, with travel times as the weights, and finds the cheapest path
   with algorithms like this one, from a Dutch computer scientist called
   Edsger Dijkstra. The internet uses it too: routers find the cheapest
   way to send your messages." Draw a small road map: five towns, with
   roads labelled by minutes. Find the fastest route from one to another
   by hand, always exploring the town with the smallest total so far.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: in mazes/3-river.txt, cheapest_path found a path costing 36, but there's one costing only 12.` | The queue isn't a priority queue: it uses `pop(0)` or `popleft`, so it's still breadth-first | `heapq.heappop(todo)` and `heapq.heappush(todo, ...)`. |
| `KeyError: '~'` | `COST` has no weight for water | Add `"~": 5` to `COST`. |
| `NameError: name 'heapq' is not defined` | `import heapq` is missing | Add it at the top of `mazes.py`. |
| `NOT YET: cheapest_path should give (cost, path), but ... it gave [(1, 1), ...` | It gives back just the path | `return (cost, path_back(came_from, goal))`. |
| `TypeError: cannot unpack non-iterable int object` | The tuple in the heap is `(next_spot, cost)`, the wrong way round | Cost first: `(cost + ..., next_spot)`. The heap sorts by the first item. |

## Talk about it

- What's the difference between the shortest path and the cheapest path?
- What does a priority queue do? How is it different from a queue?
- What two things changed to turn BFS into Dijkstra's algorithm?

## Challenge *(if there's time, or for next time)*

- Add soul sand, `:`, costing 3, and lava, `!`, which can't be crossed
  at all. Make a maze with them. *(Lava: treat it like `#` in
  `neighbours`.)*
- What if walking costs 1, but water costs 1 too? Do BFS and Dijkstra
  give paths of the same cost? *(Yes: with all weights equal, Dijkstra
  is BFS.)*
- Ice is fast in Minecraft. What would go wrong with a cost of 0, or
  less than 0? *(0 still works. Negative costs break Dijkstra: going
  round in circles would keep getting cheaper!)*

## Checkpoint

The learner can, without help:
- [ ] Explain weights, and the difference between shortest and cheapest
- [ ] Use `heapq` as a priority queue
- [ ] Change BFS into Dijkstra's algorithm, and pass
      `python3 check.py dijkstra`
- [ ] Find a cheapest route on a small map by hand

## Lab notebook

Stick in the paper river maze with its cards and arrows. Copy the
`compare.py` table. Draw the five-town map and its fastest route.
Commit. Add *weight*, *priority queue*, *heap* and *Dijkstra's
algorithm* to `dictionary.md`.

## Guide's background *(optional reading)*

**Dijkstra's algorithm** (1956) finds the cheapest paths from a start
vertex in a graph whose edge weights are not negative. It always
explores the cheapest vertex not yet explored, using a **priority
queue**; with a binary heap, it runs in O((V + E) log V).

In this lesson, the cost belongs to the *square being entered*, so the
first time a square is reached is always by a cheapest route, and the
code can be exactly BFS with a heap (this was checked against a slower,
always-correct method on thousands of random mazes). On a general road
map, where each *road* has its own weight, a town can first be reached
by an expensive road and later by a cheaper one, so the full algorithm
also keeps a "best cost so far" for each vertex and updates it when it
finds a cheaper way: that's how the hand method in step 8 works. *Open
Data Structures* and Erickson's *Algorithms* (both in the offline
library) cover heaps and the general version.

A **heap** is a tree stored in a list, where every parent is smaller
than its children, so the smallest is always at position 0. Lesson 7.13
showed why trees give O(log n): a heap is always perfectly balanced.
In Stage 11, the learner meets the routing protocols that run versions
of this algorithm across the internet.
