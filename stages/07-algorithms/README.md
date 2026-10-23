# Stage 7: Algorithms & Data

**Badge:** Algorithm Wizard · **Needs first:** Stage 6; pre-algebra:
exponents, letters standing for numbers, and reading graphs (see the
[math track](../../docs/MATH-TRACK.md)) · **Lessons:** 16

Having built a computer, the learner steps back to ask how to make it
solve problems *cleverly*. They count an algorithm's steps instead of
timing it, and learn Big-O to describe how the count grows. They write
the famous algorithms: linear and binary search, then selection,
insertion, merge and quicksort. They learn recursion, and they prove
programs right with invariants and induction, using blocks and
Numberblocks patterns. Then come the data structures every programmer
leans on: stacks, queues, linked lists (their first classes), hash
tables, trees and heaps. Graphs and mazes finish the stage: they solve
mazes with breadth-first search, find the cheapest path round the water
with Dijkstra's algorithm, and build a maze maker that tunnels through
stone with depth-first search.

Every lesson is fully scripted. Every program in this stage was run, and
the lessons show what really appears. A **checker** (`check.py`) tests
the learner's functions on hundreds of cases, so the guide never has to
judge code by eye. Each lesson's error table quotes the checker's real
messages for the common mistakes, found by running deliberately broken
versions.

## Tools

- **Thonny and Python 3**, as in Stages 2 and 3; the turtle for two
  graphs. Programs live in `~/lab/algo`, in a git repository (Lesson
  7.1).
- **The Algorithms lab**: from your own account,
  `./scripts/give-lab.sh LEARNER algo`, before Lesson 7.1. It gives the
  learner the checker and the practice mazes. The
  [Algorithms lab handbook](../../labs/algo/README.md) explains them;
  working answers for every check are in `labs/algo/answers/`, for you.
- **Things to hold:** a pack of playing cards (Lessons 7.1–7.7), nesting
  dolls or boxes (7.5), about 30 building blocks or cubes (7.8, 7.9),
  dominoes (7.9), sticky notes or index cards, three coins of different
  sizes, squared paper and coloured pencils.
- **Reading for the guide**, all free and in the offline library
  (`/srv/redstone-library/books/`):
  - *Book of Proof*, Richard Hammack (`book-of-proof.pdf`): Chapter 4
    (direct proof) for Lesson 7.8, and Chapter 10 (induction) for 7.9.
  - *Open Data Structures*, Pat Morin, Python edition
    (`open-data-structures-python.pdf`): stacks, queues, linked lists,
    hash tables, trees and heaps, a step further than the lessons.
  - *Algorithms*, Jeff Erickson (`algorithms-erickson.pdf`): Chapter 1
    on recursion is famously good, and later chapters cover graphs.
  - OpenStax *Introduction to Computer Science*, Chapter 3 ("Data
    Structures and Algorithms"), a hand download (see `mirror-library.sh`).
  - *Think Python 2e* (`think-python-2e.pdf`), Chapters 15–18, for more
    on classes.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 7.1 | [Counting Steps](01-counting-steps.md) | The robot game, card hunts, linear search, racing a million numbers | algorithms, best and worst case |
| 7.2 | [Halving: Binary Search and Logarithms](02-halving.md) | A mind-reading program, binary search, tracing, log₂ | binary search, logarithms |
| 7.3 | [How Things Grow: Big-O](03-how-things-grow.md) | Walls, floors and cubes; a growth graph; the doubling experiment; spotting the family | Big-O |
| 7.4 | [Sorting by Hand and by Code](04-sorting-by-hand.md) | Selection and insertion sort with cards and in Python; counting comparisons | O(n²) sorting |
| 7.5 | [Recursion](05-recursion.md) | Nesting dolls, the call stack, factorial, reversing words, a fractal tree | recursion, base case |
| 7.6 | [Merge Sort](06-merge-sort.md) | Merging piles, splitting and merging cards, levels × work | divide and conquer, O(n log n) |
| 7.7 | [Quicksort, and Python's Own Sort](07-quicksort.md) | Pivots, the sorted-input trap and its fix, `sorted` with `key` | worst case input, stability |
| 7.8 | [Why Should I Believe It?](08-why-believe-it.md) | Claims and counterexamples, proofs with blocks and algebra, binary search's invariant | proof, invariants |
| 7.9 | [Dominoes: Proof by Induction](09-dominoes.md) | Odd numbers make squares, Gauss's staircase, the Tower of Hanoi | induction |
| 7.10 | [Stacks and Queues](10-stacks-and-queues.md) | An undo button, a bracket checker, `deque` vs `pop(0)` | LIFO, FIFO |
| 7.11 | [Linked Lists](11-linked-lists.md) | A treasure hunt, nodes in RAM, the first class | classes, pointers |
| 7.12 | [Hash Tables](12-hash-tables.md) | Mobs in buckets, a hash table with methods, why buckets matter | hashing, O(1) lookup |
| 7.13 | [Trees](13-trees.md) | The folder tree, Twenty Questions, a binary search tree, tall and bushy trees | trees, balance |
| 7.14 | [Graphs and Mazes](14-graphs-and-mazes.md) | Flooding a maze by hand, then breadth-first search | graphs, BFS |
| 7.15 | [The Cheapest Way](15-cheapest-paths.md) | Water costs more; a priority queue; Dijkstra's algorithm | weights, heaps, Dijkstra |
| 7.16 | [Project: The Block-World Maze Maker](16-maze-project.md) | Carving mazes with depth-first search, watching the flood, demo day; Stage 7 checkpoint | putting it together |

## Setup notes

- Run `./scripts/give-lab.sh LEARNER algo` before Lesson 7.1. Nothing
  else needs installing.
- Re-run `./scripts/mirror-library.sh` while online, so the two new
  books (*Open Data Structures* and Erickson's *Algorithms*) land in the
  library.
- The math gate matters most for Lessons 7.8 and 7.9, which use simple
  algebra (2a + 2b = 2(a + b)). The lessons do every proof with blocks
  first, so a learner still meeting algebra can follow the idea and
  come back to the letters later.
- Timings in the lessons came from one computer. Yours will differ; the
  comparisons (twice as long, a hundred times faster) won't.

## Free play for this stage

- Project Euler problems (projecteuler.net/archives; reading needs no
  account), checking answers with a second, slower program.
- More mazes from `maker.py`, printed for the family.
- Sorting animations with the turtle: draw a list as bars, and redraw
  after every swap.
- Card magic: many card tricks are algorithms (the 21-card trick is a
  three-way split, done three times).

## Habits to build now

- **Count before you time.** Steps don't depend on the computer.
- **Try the small case by hand.** Cards, cups and paper first; code
  second.
- **Think about the worst case input.** Sorted lists, empty lists, one
  item, things that aren't there.
- **Ask "why is it right?"** Testing finds bugs; a reason shows there
  are none left.
- **Choose the data structure first.** The right one makes the
  algorithm easy.

## Checkpoint

The learner can, without help:
- [ ] Say the Big-O of the main searches and sorts, and of simple loops
- [ ] Explain binary search and logarithms, and merge sort's O(n log n)
- [ ] Write recursive functions with a base case
- [ ] Prove simple facts directly and by induction, and explain a loop
      invariant
- [ ] Choose between a list, stack, queue, linked list, hash table, tree
      and graph for a job, and say why

They can also:
- [ ] Pass every check: search, sorts, recursion, merge, quick,
      brackets, linked, hash, bst, bfs and dijkstra
- [ ] Make a maze with depth-first search, and solve it with BFS and
      Dijkstra (Lesson 7.16)
