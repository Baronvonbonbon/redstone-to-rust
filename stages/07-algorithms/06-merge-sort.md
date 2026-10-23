# Lesson 7.6: Merge Sort: Divide and Conquer

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
a pack of cards · **New words:** merge, merge sort, divide and conquer,
O(n log n)

## Goal *(read this to the learner)*

> Back in Stage 0, the guide's notes promised that a sort called **merge
> sort** could sort 1000 cups with about 10,000 comparisons, instead of
> half a million. Today you'll find out how. The trick is recursion:
> split the pile in half, sort each half (with merge sort!), and then
> **merge** the two sorted halves together, which turns out to be easy.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Take 8 cards, ace (1) to 8, of one suit, and shuffle them.

## Warm-up (5 min)

"What are the two parts of a recursive function?" *(A base case, and a
recursive case that uses a smaller problem.)* "What's the smallest list
there is? Is it sorted?" *(The empty list, and yes! A list of one item
is sorted too.)*

## Activity

### Session 1: merging

1. **Merge two piles.** Make two piles, face up, each already sorted with
   the smallest on top: say 2, 5, 7 in one pile, and 1, 3, 4, 8 in the
   other. **Say:** "Make one sorted pile, by only ever looking at the two
   top cards." *(Take the smaller top card, and put it on the new pile.
   Repeat. When one pile runs out, put the rest of the other pile on the
   end.)*

   **Ask:** "How many comparisons did that take?" *(At most one per card
   moved: about 7.)* **Say:** "Merging is fast: O(n). The two piles
   must already be sorted, though."

2. **Merge in Python.** Add to `sorting.py`:
   ```python
   def merge(left, right):
       """Two sorted lists in, one sorted list out."""
       result = []
       i = 0
       j = 0
       while i < len(left) and j < len(right):
           if left[i] <= right[j]:
               result.append(left[i])
               i = i + 1
           else:
               result.append(right[j])
               j = j + 1
       result = result + left[i:] + right[j:]
       return result
   ```
   **Say:** "`i` is our finger on the top card of `left`, and `j` on
   `right`. The loop goes until one pile runs out. Then `left[i:]` and
   `right[j:]` are whatever's left in each pile; one of them is empty,
   so adding both puts the leftovers on the end."

   Try it in the shell (restart it first with the Stop button):
   ```
   >>> from sorting import merge
   >>> merge([2, 5, 9], [1, 3, 4, 10])
   [1, 2, 3, 4, 5, 9, 10]
   ```

### Session 2: merge sort

3. **Merge sort with cards.** Shuffle the 8 cards. **Say:** "Here's
   merge sort. *To sort a pile: if it has one card, it's sorted already.
   Otherwise, split it in half, sort each half (using these same
   instructions), and merge the halves.*"

   Do it on the table: split 8 into 4 and 4, each 4 into 2 and 2, each
   2 into 1 and 1. Then merge back up: pairs, then fours, then all
   eight. Draw it on paper as a picture that splits down and joins back
   up:
   ```
           5 2 7 1 8 3 6 4
          /               \
      5 2 7 1           8 3 6 4
      /     \           /     \
    5 2     7 1       8 3     6 4
    / \     / \       / \     / \
   5   2   7   1     8   3   6   4      (one card each: sorted!)
    \ /     \ /       \ /     \ /
    2 5     1 7       3 8     4 6       (merge pairs)
      \     /           \     /
      1 2 5 7           3 4 6 8         (merge fours)
          \               /
           1 2 3 4 5 6 7 8              (merge all eight)
   ```

4. **Merge sort in Python.** Add to `sorting.py`:
   ```python
   def merge_sort(items):
       """Sort each half, then merge them."""
       if len(items) <= 1:
           return items
       middle = len(items) // 2
       left = merge_sort(items[:middle])
       right = merge_sort(items[middle:])
       return merge(left, right)
   ```
   **Say:** "`items[:middle]` is everything before the middle, and
   `items[middle:]` is everything from the middle on. The base case is a
   list of 0 or 1 items: already sorted."

   **Ask:** "Where's the sorting actually done?" *(In `merge`! Merge sort
   just splits, and lets merging do the work.)*

5. **The checker.**
   ```
   python3 check.py merge
   ```
   **They should see:**
   ```
   Checking merge and merge_sort, in sorting.py...
     merge: right every time.
     merge_sort: 1,000 shuffled numbers took 8,686 comparisons.
     merge_sort: 1,000 already sorted numbers took 4,932 comparisons.
     merge_sort: 100,000 shuffled numbers took 1,536,462 comparisons.
     merge_sort: 100,000 already sorted numbers took 815,024 comparisons.
     merge_sort: right every time.
   ALL GOOD!
   ```
   **Say:** "8,686, against selection sort's 499,500! The guide's notes
   in Stage 0 said about 10,000. They were right." Commit.

### Session 3: why it's fast

6. **Count the levels.** Look at the card picture. **Ask:**
   - "How many levels of splitting for 8 cards?" *(3: 8 to 4 to 2 to 1.)*
     "That's log₂ of 8!"
   - "On each level of merging, about how many cards get moved?" *(All
     8, each time.)*
   - "So the work is about cards × levels." *(8 × 3 = 24.)*

   **Say:** "For 1000 numbers: log₂ of 1000 is about 10 levels, and each
   level moves 1000 numbers. About 10,000 steps. We write that
   **O(n log n)**: it's a little more than O(n), and far less than
   O(n²)."

   | n | n log₂ n (merge sort) | n² ÷ 2 (selection sort) |
   |---|---|---|
   | 1,000 | about 10,000 | 500,000 |
   | 1,000,000 | about 20,000,000 | 500,000,000,000 |

7. **The race.** New file, `~/lab/algo/race3.py`:
   ```python
   import random
   import time
   from sorting import insertion_sort, merge_sort

   numbers = list(range(10_000))
   random.shuffle(numbers)

   for sort in [insertion_sort, merge_sort, sorted]:
       start = time.perf_counter()
       sort(numbers)
       seconds = time.perf_counter() - start
       print(f"{sort.__name__}: {seconds:.3f} seconds")
   ```
   **They should see** something like:
   ```
   insertion_sort: 2.727 seconds
   merge_sort: 0.033 seconds
   sorted: 0.001 seconds
   ```
   **Say:** "Merge sort is about 80 times faster here, and the gap grows
   as the list grows. `sorted` is Python's own sort. It's even faster:
   Lesson 7.7 explains why." Commit.

8. **Divide and conquer.** **Say:** "Merge sort splits a big problem into
   smaller ones, solves those, and combines the answers. That's called
   **divide and conquer**. Binary search does it too: it splits the list,
   and only needs one half."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: merge([1], []) gave [], but it should be [1].` | The leftovers aren't added at the end of `merge` | `result = result + left[i:] + right[j:]` after the loop. |
| `NOT YET: RecursionError...` | The base case is `len(items) == 1`, so an empty list never stops splitting | `if len(items) <= 1:`. |
| `TypeError: slice indices must be integers or None or have an __index__ method` | `/` instead of `//`, so `middle` is a number like `2.5` | `middle = len(items) // 2`. |
| Merge sort gives back the list unsorted | `merge_sort` gives back `left + right` instead of merging | `return merge(left, right)`. |
| The shell still runs the old `merge` | Thonny's shell remembers the first import | Click Stop to restart the shell, then import again. |

## Talk about it

- What does merging need to be true about the two lists?
- Why is merge sort O(n log n)? Explain with the card picture.
- Why does divide and conquer help so much?

## Challenge *(if there's time, or for next time)*

- Merge sort takes 4,932 comparisons on 1000 numbers that are already
  sorted, about half. Why? *(When merging, the whole left pile is
  smaller than the right one, so it runs out first, and the right pile
  goes on the end without being compared.)*
- Add a `print` to `merge_sort` that shows `items` each time it's
  called, and sort `[5, 2, 7, 1]`. Does it match the card picture?
- Time `merge_sort` on 100,000 and 200,000 numbers. Is it about twice
  as long? *(A little more than twice: that's the "log n".)*

## Checkpoint

The learner can, without help:
- [ ] Merge two sorted piles of cards, and explain why it's O(n)
- [ ] Do merge sort with cards, and draw its picture
- [ ] Write `merge` and `merge_sort`, and pass `python3 check.py merge`
- [ ] Explain O(n log n) with levels and cards

## Lab notebook

Copy the merge sort picture for 8 cards. Write the race times and the
comparison counts for merge sort and selection sort. Commit. Add
*merge*, *merge sort*, *divide and conquer* and *O(n log n)* to
`dictionary.md`.

## Guide's background *(optional reading)*

**Merge sort** was invented by John von Neumann in 1945, for one of the
first stored-program computers. It's O(n log n) in every case, which is
the best any sort that compares two items at a time can do: a famous
result says you can't beat it on average. Its one cost is memory, since
merging builds new lists.

The "levels × work per level" argument in step 6 is the standard way to
analyse divide-and-conquer algorithms. Merge sort is also **stable**:
equal items stay in the order they started in, because `merge` takes
from the left pile when the two top cards are equal (`<=`). That
matters when sorting records by one field after another, as Lesson 7.7
shows.
