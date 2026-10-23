# The Algorithms Lab: the Guide's Handbook

Stage 7 (Algorithms & Data) happens in the learner's `~/lab/algo`
folder. This lab gives them two things to start with:

- `check.py`, **the checker**: it tries the learner's functions on lots
  of cases, and says `ALL GOOD!` or `NOT YET:` with the case that went
  wrong. It's the judge for the stage, like the tests in Nand to Tetris,
  so you never need to read the learner's code to know it works.
- `mazes/`, six practice mazes for Lessons 7.14–7.16.

The `answers/` folder holds working versions of every file the checker
checks, for you. **Don't give it to the learner**: `give-lab.sh` doesn't
copy it.

## Setting it up

Before Lesson 7.1, from your own account:

```
./scripts/give-lab.sh LEARNER algo
```

It makes `~/lab/algo` with `check.py` and `mazes/`. Lesson 7.1 turns the
folder into a git repository. Everything runs offline, with the Python
that setup installed for Stage 2.

## The checks

From `~/lab/algo`, `python3 check.py` lists them:

| Check | Lesson | Checks | In the file |
|---|---|---|---|
| `search` | 7.2 | `linear_search`, `binary_search` | `searching.py` |
| `sorts` | 7.4 | `selection_sort`, `insertion_sort` | `sorting.py` |
| `recursion` | 7.5 | `factorial`, `total`, `reverse` (and that they're recursive) | `recursion.py` |
| `merge` | 7.6 | `merge`, `merge_sort` | `sorting.py` |
| `quick` | 7.7 | `quick_sort` | `sorting.py` |
| `brackets` | 7.10 | `brackets_ok` | `stacks.py` |
| `linked` | 7.11 | `Node`, `length`, `to_list`, `push_front`, `contains` | `linked.py` |
| `hash` | 7.12 | `HashTable` with `put`, `get`, `size` | `hashtable.py` |
| `bst` | 7.13 | `TreeNode`, `insert`, `contains`, `in_order`, `height` | `trees.py` |
| `bfs` | 7.14 | `read_maze`, `find`, `shortest_path` | `mazes.py` |
| `dijkstra` | 7.15 | `cheapest_path` | `mazes.py` |

Besides right or wrong, some checks print measurements that the lessons
talk about: how many items a search looked at, how many comparisons a
sort made, how a hash table's buckets filled up, and how tall a tree
grew. The maze checks run on **every** `.txt` file in `mazes/`,
including the learner's own, and draw the path for small mazes.

## Reading the checker

- `ALL GOOD!` (exit code 0): every case passed.
- `NOT YET: binary_search([5], 5) gave None, but it should be 0.` One
  case went wrong. Try that exact case by hand, or in Thonny's shell.
  Each lesson's "If something goes wrong" table lists the common ones.
- `NOT YET: your code crashed during a check:` followed by Python's
  error, pointing at the line in the learner's file.
- `NOT YET: that took more than 10 seconds.` Almost always a loop that
  never ends.
- `NOT YET: RecursionError.` A recursive function with a missing or
  wrong base case (except in Lesson 7.7, where it's the point of the
  lesson).
- `There's no searching.py in this folder`: run the checker from
  `~/lab/algo`, where the learner's files are.

## Mazes

Each maze is a text file: `#` is stone, `.` is open, `~` is water
(costs 5 to enter in Lesson 7.15; everything else costs 1), `P` is the
start and `D` the diamond. Every maze needs a `#` border all the way
round, because `neighbours` doesn't check the edges.

| Maze | Shows |
|---|---|
| `1-tiny.txt` | the first maze, to flood by hand |
| `2-two-ways.txt` | two routes, one shorter |
| `3-river.txt` | the fewest steps swim (cost 36); the cheapest path walks round (cost 12) |
| `4-swamp.txt` | the same idea, bigger (22 steps costing 46, or 26 costing 26) |
| `5-ford.txt` | here, swimming *is* the cheapest (30 steps, cost 34) |
| `6-sealed.txt` | no way through: the answer should be `None` |

## Things to know

- **Timings vary.** Lessons show times from one computer and say
  "something like". The *ratios* (twice as long, a hundred times
  faster) are what matter, and those are about the same everywhere.
- **Python's hash for words changes every run**, so the `hash` check's
  bucket numbers change too. That's on purpose (Lesson 7.12 explains).
- **Thonny's shell remembers imports.** After changing a file, click
  Stop (which restarts the shell) before importing it again.
- **`watch.py` (Lesson 7.16) must run in the terminal**: it clears the
  screen with `clear`, which Thonny's shell can't do.

## Licences

`check.py`, the mazes and the answers are the course's own (MIT). The
reading for this stage is in [the stage's README](../../stages/07-algorithms/README.md).
