# Lesson 7.13: Trees

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/algo`; 15 index cards with a number from 1 to 99 on each; a
big sheet of paper · **New words:** tree, root, branch, leaf, binary
search tree, in-order, height, balanced

## Goal *(read this to the learner)*

> You've walked through a tree since Stage 1: the folders on your
> computer. One folder at the top, folders inside folders, and files at
> the ends. Trees are one of the most useful shapes in computing. Today
> you'll build a **binary search tree**: a tree that keeps numbers so
> well organized that finding one is like binary search, but adding new
> ones is quick too. And you'll find a way to make one grow very badly.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Shuffle the 15 number cards.

## Warm-up (5 min)

"What's in a linked-list node?" *(A value, and a pointer to the next
node.)* "What if a node had *two* pointers?" *(Then the chain could
split in two... like a tree!)*

## Activity

### Session 1: trees everywhere

1. **The folder tree.** In the terminal:
   ```
   tree -L 2 ~/lab
   ```
   **They should see:** `~/lab` at the top, the folders inside it
   (`algo`, `n2t`, `python` and so on) indented under it, and inside
   those, more. **Say:** "Computer scientists draw trees upside down. The
   top is the **root**. Each line down is a **branch**. Things at the
   very ends, with nothing below them, are **leaves**."

   **Ask:** "Where else are there trees?" *(A family tree; a knockout
   tournament; a Minecraft crafting tree, like logs to planks to sticks
   to a pickaxe; the chapters and sections of a book.)*

2. **Twenty Questions.** The guide thinks of a number from 1 to 100. The
   learner asks only "Is it less than ...?" questions. Draw each question
   as a box on the big sheet, with "yes" going down-left and "no" going
   down-right. **Say:** "That's binary search drawn as a tree. Each
   question sends you left or right."

3. **Build a binary search tree with cards.** **Say:** "The rule: every
   number on a node's *left* side is smaller, and everything on its
   *right* is bigger." Turn over the first card: it's the root, at the
   top of the sheet. For each next card, start at the root: smaller, go
   left; bigger, go right; keep going until there's an empty spot, and
   put it there. Do all 15.

   **Ask:** "How do you check if 42 is in the tree?" *(Start at the
   root, go left or right, until you find it or fall off a leaf.)* "How
   many cards did you look at?" *(Only the ones on one path down, not
   all 15.)*

### Session 2: a tree in Python

4. **A tree node.** New file, `~/lab/algo/trees.py`:
   ```python
   class TreeNode:
       """A value, with a smaller tree on the left and a bigger one on the right."""

       def __init__(self, value):
           self.value = value
           self.left = None
           self.right = None


   def insert(root, value):
       """Puts value in the tree. Gives back the root."""
       if root is None:
           return TreeNode(value)
       if value < root.value:
           root.left = insert(root.left, value)
       elif value > root.value:
           root.right = insert(root.right, value)
       return root
   ```
   **Say:** "`insert` is recursive, like the cards: an empty tree becomes
   a single node; otherwise, insert into the left tree or the right tree.
   If the value is already there, nothing changes. `root.left = ...`
   matters: it attaches the new branch."

5. **Show the tree.** Add this, which prints a tree on its side:
   ```python
   def show(root, depth=0):
       """Prints the tree on its side: the right branch at the top."""
       if root is None:
           return
       show(root.right, depth + 1)
       print("    " * depth + str(root.value))
       show(root.left, depth + 1)
   ```
   In the shell:
   ```
   >>> from trees import insert, show
   >>> root = None
   >>> for x in [50, 30, 70, 20, 40, 60, 80]:
   ...     root = insert(root, x)
   ...
   >>> show(root)
   ```
   **They should see:**
   ```
           80
       70
           60
   50
           40
       30
           20
   ```
   **Say:** "Tilt your head to the left: 50 is the root, at the top, with
   30 and 70 under it." *(In Thonny's shell, press Enter on the empty
   `...` line to finish the loop.)*

6. **Your turn: three more.** The learner writes these in `trees.py`,
   all recursive, with hints:
   - `contains(root, value)`: `True` if `value` is in the tree. *(Empty
     tree: `False`. Found it: `True`. Otherwise, look in the left or the
     right, just like the cards.)*
   - `in_order(root)`: a list of all the values, smallest first. *(The
     left tree's values, then this one, then the right tree's:
     `in_order(root.left) + [root.value] + in_order(root.right)`.)*
   - `height(root)`: how many levels the tree has. An empty tree has 0.
     *(1 for this node, plus the height of whichever side is taller:
     `max(...)`.)*

   Then:
   ```
   python3 check.py bst
   ```
   **They should see:**
   ```
   Checking TreeNode and friends, in trees.py...
     insert, contains, in_order and height: right every time.
     1,000 random numbers made a tree 20 levels tall.
     1 to 100, in order, made a tree 100 levels tall.
   ALL GOOD!
   ```
   Commit.

### Session 3: good trees and bad trees

7. **Sorting for free.** **Ask:** "`in_order` gave the numbers smallest
   first. We never sorted them! Why?" *(The left side is always smaller,
   so it comes first, at every node.)* **Say:** "Putting numbers into a
   tree and reading them out in order is a sort, called tree sort."

8. **A very bad tree.** Look at the checker's last line again: 1 to 100,
   in order, made a tree 100 levels tall. **Ask:** "Draw the tree for 1,
   2, 3, 4, 5, in that order." *(Every number goes to the right of the
   last: a straight line, like a linked list!)* Check with `show`.

   New file, `~/lab/algo/tree_heights.py`:
   ```python
   import random
   from trees import insert, height

   numbers = list(range(500))

   root = None
   for x in numbers:
       root = insert(root, x)
   print("500 numbers in order:", height(root), "levels")

   random.shuffle(numbers)
   root = None
   for x in numbers:
       root = insert(root, x)
   print("500 numbers shuffled:", height(root), "levels")
   ```
   **They should see** something like:
   ```
   500 numbers in order: 500 levels
   500 numbers shuffled: 19 levels
   ```
   *(The shuffled height changes each run, usually somewhere from 16 to
   24.)* **Say:** "A shuffled tree is bushy: finding a number takes about
   20 steps, like binary search. A tree built from sorted numbers is a
   stick: 500 steps, like linear search. It's quicksort's weak spot all
   over again!"

   Try changing `500` to `2000`. **They should see:** a `RecursionError`.
   *(2000 levels is more than Python's call stack allows.)* Put it back.

9. **Balanced trees.** **Say:** "A tree whose two sides are about the same
   height everywhere is **balanced**. Clever trees, like red-black trees,
   rebalance themselves as numbers go in, so they never become sticks.
   You'll use one in Rust, called a `BTreeMap`."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: insert should give back the root TreeNode.` | `return root` is missing at the end of `insert` | Add it, lined up with the `if`s. |
| `NOT YET: in_order after inserting ... gave [50, 70, 80]...` | The left branch isn't attached: `insert(root.left, value)` without `root.left =` | `root.left = insert(root.left, value)`, and the same on the right. |
| `NOT YET: in_order ... gave [50, 30, 20, 40, ...]` | `root.value` comes first in `in_order`, not in the middle | Left, then this one, then right. |
| `NOT YET: height(None) gave 1, but it should be 0.` | The base case of `height` | An empty tree has no levels: 0. |
| `show` prints nothing | `root` is still `None`: the loop didn't do `root = insert(root, x)` | Keep what `insert` gives back. |
| `RecursionError` in `tree_heights.py` | The in-order tree is too tall for Python's call stack | Use 500, as in the lesson. |

## Talk about it

- What are the root, branches and leaves of the `~/lab` tree?
- What's the binary search tree rule? Why does `in_order` come out
  sorted?
- Why do sorted numbers make a bad tree?

## Challenge *(if there's time, or for next time)*

- Write `smallest(root)`, which follows `left` until it can't. Is it
  recursive, or a loop? (Either works!)
- Write `count_leaves(root)`: nodes with no left and no right.
- Build a perfectly balanced tree from 1 to 15 by hand, choosing the
  insert order carefully. *(Insert 8 first, then 4 and 12, then 2, 6,
  10, 14, then the odd numbers.)* What's its height? *(4: log₂ of 16.)*

## Checkpoint

The learner can, without help:
- [ ] Name the root, branches and leaves of a tree, and give examples
- [ ] Build a binary search tree from cards, and search it
- [ ] Write `contains`, `in_order` and `height`, and pass
      `python3 check.py bst`
- [ ] Explain why sorted input makes a tall, slow tree

## Lab notebook

Draw the 15-card tree. Draw the trees for `50 30 70 20 40 60 80` and
for `1 2 3 4 5`. Write the tree heights. Commit. Add *tree*, *root*,
*branch*, *leaf*, *binary search tree*, *in-order*, *height* and
*balanced* to `dictionary.md`.

## Guide's background *(optional reading)*

A **binary search tree** keeps the rule "smaller on the left, bigger on
the right" at every node, so search, insert and delete take time
proportional to the tree's height. A balanced tree with n items has
height about log₂ n, so all three are O(log n); a degenerate one is
O(n). Self-balancing trees (AVL, red-black, B-trees) guarantee
O(log n). B-trees, with many children per node, are how databases like
SQLite (Stage 5) and file systems store their data on disk.

Trees appear throughout the rest of the course: the file system
(Stage 10), the **parse tree** a compiler builds from source code
(Stage 8's Jack compiler, and Stage 12's interpreters), and the DOM
tree of a web page. The recursive pattern here (handle the empty tree,
then this node, then recurse on the children) is how almost all tree
code is written.
