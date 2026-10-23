# Lesson 7.4: Sorting by Hand and by Code

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
a pack of cards; Stage 0's weighing cups, if you still have them ·
**New words:** selection sort, insertion sort, swap, comparison

## Goal *(read this to the learner)*

> Binary search needs a sorted list. So how do you sort one? You'll
> learn two ways that people use without thinking: **selection sort**
> (find the smallest, put it first, repeat) and **insertion sort** (the
> way you sort a hand of cards). You'll write both in Python, and the
> checker will count every comparison they make. One of them has a
> surprise when the list is already sorted.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Take six cards of one suit, ace (1) to 6, and shuffle them.

## Warm-up (5 min)

"What's the Big-O of a loop inside a loop, both going to n?"
*(O(n²).)* "Why can't binary search work on a shuffled list?" *(It
throws away half, guessing the target isn't there, which is only safe
if the list is in order.)*

## Activity

### Session 1: selection sort

1. **By hand.** Lay the six cards face up in a row. **Say:** "Rule: you
   may only compare two cards at a time, and say which is smaller. Find
   the smallest card by comparing, and **swap** it with the first card."
   The learner moves a pencil along: compare the first card with each of
   the others, remembering the smallest so far, and counting comparisons.
   *(5 comparisons.)* Swap. Now do the same for the other five, starting
   from the second place. *(4 comparisons.)* And so on.

   **Ask:** "How many comparisons altogether?" *(5 + 4 + 3 + 2 + 1 =
   15.)* "Does it matter how the cards were shuffled?" *(No: it always
   compares every card that's left.)*

2. **In Python.** New file, `~/lab/algo/sorting.py`:
   ```python
   def selection_sort(items):
       """Finds the smallest, puts it first; then the next smallest..."""
       items = items.copy()
       for i in range(len(items)):
           smallest = i
           for j in range(i + 1, len(items)):
               if items[j] < items[smallest]:
                   smallest = j
           items[i], items[smallest] = items[smallest], items[i]
       return items
   ```
   **Say:** "Three new things:
   - `items.copy()` makes a copy of the list, so we sort the copy and
     don't spoil the list we were given.
   - `i` is the place we're filling. `smallest` remembers the *position*
     of the smallest card found so far.
   - `a, b = b, a` swaps two things in one go. Python works out the
     whole right side first, then puts it in the left."

3. **Watch it work.** Temporarily, add `print(items)` as the last line
   *inside* the `for i` loop (lined up with `items[i], items[smallest]`).
   In Thonny's shell:
   ```
   >>> from sorting import selection_sort
   >>> selection_sort([5, 2, 8, 1, 9, 3])
   ```
   **They should see:**
   ```
   [1, 2, 8, 5, 9, 3]
   [1, 2, 8, 5, 9, 3]
   [1, 2, 3, 5, 9, 8]
   [1, 2, 3, 5, 9, 8]
   [1, 2, 3, 5, 8, 9]
   [1, 2, 3, 5, 8, 9]
   [1, 2, 3, 5, 8, 9]
   ```
   **Say:** "Each line, one more place is right, from the left. The
   second line didn't change: 2 was already the smallest of the rest, so
   it swapped with itself. The last line is what the function gave back."
   Take the `print` out again.

   *(If Thonny says `NameError: name 'selection_sort' is not defined`,
   the `from sorting import` line is missing. If the shell shows the old
   version after a change, click Thonny's Stop button to restart the
   shell, and import again.)*

### Session 2: insertion sort

4. **By hand.** Shuffle the cards, and deal them face down. **Say:**
   "Pick up the cards one at a time, keeping the ones in your hand in
   order. Each new card slides left past every bigger card, until it
   meets a smaller one." Count comparisons: each time the new card is
   compared with a card in the hand.

   Then do it again with the cards dealt *already in order*. **Ask:**
   "How many comparisons this time?" *(5: each new card is compared with
   just one card, which is smaller, and it stays put.)*

5. **In Python.** Add to `sorting.py`:
   ```python
   def insertion_sort(items):
       """Like sorting a hand of cards: each new card slides left into place."""
       items = items.copy()
       for i in range(1, len(items)):
           card = items[i]
           j = i - 1
           while j >= 0 and items[j] > card:
               items[j + 1] = items[j]
               j = j - 1
           items[j + 1] = card
       return items
   ```
   **Say:** "The cards from 0 to `i - 1` are the hand: already sorted.
   `card` is the new one. The `while` loop moves every bigger card one
   place to the right, making a gap, and the new card drops into the
   gap. `j >= 0` stops it falling off the left end of the list."

   Trace `[5, 2, 8, 1]` on paper, writing the list after each new card:
   *([2, 5, 8, 1], then [2, 5, 8, 1], then [1, 2, 5, 8].)*

6. **The checker.** In the terminal, in `~/lab/algo`:
   ```
   python3 check.py sorts
   ```
   **They should see:**
   ```
   Checking selection_sort and insertion_sort, in sorting.py...
     selection_sort: 1,000 shuffled numbers took 499,500 comparisons.
     selection_sort: 1,000 already sorted numbers took 499,500 comparisons.
     selection_sort: right every time.
     insertion_sort: 1,000 shuffled numbers took 247,610 comparisons.
     insertion_sort: 1,000 already sorted numbers took 999 comparisons.
     insertion_sort: right every time.
   ALL GOOD!
   ```
   Commit: `git add .` and `git commit -m "Selection and insertion sort"`.

### Session 3 (or the end of Session 2): what the numbers say

7. **Read the numbers.** **Ask:**
   - "Where have we seen 499,500 before?" *(It's 999 + 998 + ... + 1:
     like the 5 + 4 + 3 + 2 + 1 with six cards. It's about half of
     1000 × 1000: O(n²).)*
   - "Insertion sort on shuffled numbers?" *(About half of that, but
     still O(n²): about a quarter of n × n.)*
   - "And already sorted?" *(999: just one comparison per card. O(n)!
     Insertion sort is quick when the list is nearly in order.)*

   **Say:** "Selection sort always does the full amount of work.
   Insertion sort notices when there's nothing to do. That's why real
   sorting programs use insertion sort for small or nearly-sorted lists."

8. **How slow is O(n²)?** **Ask:** "1,000 numbers took about 250,000
   comparisons with insertion sort. A million numbers?" *(A thousand
   times the size, so a million times the comparisons: 250 billion. In
   Python, that's about seven hours.)* **Say:** "Next we need a cleverer
   idea. It's called recursion, and it's next lesson."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: selection_sort([]) gave None, but it should be [].` | The `return items` line is missing, or indented inside the loop | `return items` lines up with `for`, at the end. |
| `NOT YET: selection_sort([2, 1]) gave [2, 1], but it should be [1, 2].` | The inner loop stops one too early, like `range(i + 1, len(items) - 1)` | `range(i + 1, len(items))`: it must look at every card to the end. |
| `NOT YET: insertion_sort([2, 1]) gave [2, 1], but it should be [1, 2].` | The new card goes into `items[j]` instead of the gap at `items[j + 1]` | `items[j + 1] = card`. |
| `There's no sorting.py in this folder` | The file is saved somewhere else, or the checker ran somewhere else | Save in `~/lab/algo`, and `cd ~/lab/algo`. |
| `sorting.py has no insertion_sort yet.` | The name is spelled differently | The names must be exactly `selection_sort` and `insertion_sort`. |

## Talk about it

- Explain selection sort and insertion sort in your own words, with
  cards.
- Which one is better for a list that's nearly sorted? Why?
- Why is selection sort O(n²)?

## Challenge *(if there's time, or for next time)*

- Write Stage 0's **bubble sort** as `bubble_sort(items)`: go along the
  list swapping any neighbours in the wrong order, and repeat until a
  whole pass makes no swaps. Check it in the shell against `sorted()`,
  with a few lists of your own.
- Sort words: `insertion_sort(["zombie", "axolotl", "creeper"])`. Why
  does it work? *(`<` compares words in dictionary order.)* What about
  `["Zombie", "axolotl"]`? *(Capitals come first: they have smaller
  ASCII codes, from Stage 4.)*

## Checkpoint

The learner can, without help:
- [ ] Sort cards by selection sort and insertion sort, explaining each
      step
- [ ] Write both sorts and pass `python3 check.py sorts`
- [ ] Swap two things with `a, b = b, a`
- [ ] Explain why both are O(n²), and when insertion sort is faster

## Lab notebook

Draw the cards after each step of insertion sort on `[5, 2, 8, 1]`.
Write the checker's comparison counts. Commit. Add *selection sort*,
*insertion sort*, *swap* and *comparison* to `dictionary.md`.

## Guide's background *(optional reading)*

Selection sort and insertion sort are the two simplest sensible sorting
algorithms, and both are O(n²) on average. The checker counts
comparisons by wrapping each number in an object that adds one to a
counter whenever it's compared, which is how computer scientists
measure sorting algorithms: comparisons don't depend on how fast the
computer is.

Insertion sort's best case (already sorted, O(n)) matters in practice:
Python's own `sorted()` (Lesson 7.7) uses insertion sort for short runs
of data. Bubble sort, from Stage 0, is also O(n²) but usually slower
than both; it's mostly famous for being taught.

The `items.copy()` line avoids a subtle trap: in Python, assigning a
list to another name doesn't copy it, so a function that changes its
argument changes the caller's list too. Rust (Stage 9) makes this kind
of sharing explicit with its borrowing rules.
