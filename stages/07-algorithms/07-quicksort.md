# Lesson 7.7: Quicksort, and Python's Own Sort

**Time:** 2 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
a pack of cards · **New words:** pivot, quicksort, worst case input,
`key`

## Goal *(read this to the learner)*

> There's another famous divide-and-conquer sort, called **quicksort**.
> Pick one card, the **pivot**, and split the rest into "smaller than the
> pivot" and "bigger than the pivot". Sort each pile (with quicksort!),
> and you're done: no merging needed. It's usually very fast. But it has
> a weak spot, and today you'll find it the hard way, then fix it. Then
> you'll meet Python's own sort, which beats them all.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Take 8 cards, ace (1) to 8, of one suit, and shuffle them.

## Warm-up (5 min)

"What's the Big-O of merge sort?" *(O(n log n).)* "Where does merge
sort do its real work: splitting, or merging?" *(Merging.)* "Today's
sort does all its work in the splitting."

## Activity

### Session 1: quicksort

1. **Quicksort with cards.** Lay the 8 shuffled cards in a row. **Say:**
   "Take the first card: it's the pivot. Put every card smaller than it
   in a pile on the left, and every card bigger on the right." Then do
   the same to each pile, again and again, until every pile has one card
   or none. **They should see:** the cards end up in order, reading left
   to right, without any merging.

2. **In Python.** Add to `sorting.py`:
   ```python
   def quick_sort(items):
       """Split around a pivot: the smaller ones, the same ones, the bigger ones."""
       if len(items) <= 1:
           return items
       pivot = items[0]
       smaller = []
       same = []
       bigger = []
       for x in items:
           if x < pivot:
               smaller.append(x)
           elif x == pivot:
               same.append(x)
           else:
               bigger.append(x)
       return quick_sort(smaller) + same + quick_sort(bigger)
   ```
   **Say:** "`same` collects the pivot, and any cards equal to it. They're
   already in the right place: between the smaller and the bigger ones."

3. **The checker finds the weak spot.**
   ```
   python3 check.py quick
   ```
   **They should see:**
   ```
   Checking quick_sort, in sorting.py...
     quick_sort: 1,000 shuffled numbers took 11,224 comparisons.
   NOT YET: quick_sort crashed with a RecursionError on 1,000 numbers that were already sorted. Lesson 7.7 explains why!
   ```
   **Say:** "Shuffled numbers went fine, with about as many comparisons
   as merge sort. But numbers that were *already sorted* crashed it. Let's
   find out why, with cards."

4. **The worst case input.** Lay out the 8 cards *in order*, and do
   quicksort by hand again, taking the first card as the pivot. **Ask:**
   "What happens?" *(The pivot is always the smallest: the left pile is
   empty, and the right pile has every other card. Each split only takes
   one card off.)* "How many levels of splitting?" *(8, not 3.)*

   **Say:** "With 1000 sorted numbers, that's 1000 levels: 1000 calls
   waiting on the call stack, and Python's limit is about 1000. And each
   level compares every card that's left, so it's O(n²) again. Sorted
   numbers are quicksort's **worst case input**, when the first card is
   the pivot."

5. **The fix.** **Ask:** "Which card would make a better pivot for a
   sorted pile?" *(The middle one: it splits the pile in half.)* Change
   one line:
   ```python
       pivot = items[len(items) // 2]
   ```
   Run the checker again. **They should see:**
   ```
   Checking quick_sort, in sorting.py...
     quick_sort: 1,000 shuffled numbers took 11,397 comparisons.
     quick_sort: 1,000 already sorted numbers took 8,498 comparisons.
     quick_sort: right every time.
   ALL GOOD!
   ```
   Commit: `git commit -am "Quicksort, with a middle pivot"`. *(`-a`
   commits every change to files git already knows, without `git add`.
   New files still need `git add`.)*

### Session 2: Python's own sort

6. **The big race.** New file, `~/lab/algo/race4.py`:
   ```python
   import random
   import time
   from sorting import merge_sort, quick_sort

   numbers = list(range(1_000_000))
   random.shuffle(numbers)

   for sort in [merge_sort, quick_sort, sorted]:
       start = time.perf_counter()
       sort(numbers)
       seconds = time.perf_counter() - start
       print(f"{sort.__name__}: {seconds:.2f} seconds")
   ```
   **They should see** something like:
   ```
   merge_sort: 6.90 seconds
   quick_sort: 3.15 seconds
   sorted: 0.47 seconds
   ```
   **Say:** "A million numbers in a few seconds: try that with selection
   sort and you'd wait for days. But Python's `sorted` wins easily. It's
   O(n log n) too, but it's written in C, a language that runs much
   faster than Python, and it uses clever tricks, like insertion sort for
   small pieces. In real programs, use `sorted`. Now you know what it's
   doing."

7. **Sorting things by a key.** **Say:** "`sorted` can sort anything, by
   any rule you choose." New file, `~/lab/algo/mobs.py`:
   ```python
   mobs = [
       {"name": "creeper", "health": 20},
       {"name": "zombie", "health": 20},
       {"name": "iron golem", "health": 100},
       {"name": "chicken", "health": 4},
       {"name": "enderman", "health": 40},
       {"name": "bee", "health": 10},
       {"name": "axolotl", "health": 14},
       {"name": "skeleton", "health": 20},
   ]


   def health(mob):
       return mob["health"]


   def name(mob):
       return mob["name"]


   print("By name:")
   for mob in sorted(mobs, key=name):
       print(f"  {mob['name']:12} {mob['health']:3}")

   print("Toughest first:")
   for mob in sorted(mobs, key=health, reverse=True):
       print(f"  {mob['name']:12} {mob['health']:3}")
   ```
   **Say:** "`key=health` means: to compare two mobs, compare what the
   `health` function gives for each. `reverse=True` puts the biggest
   first." Run it. **They should see:** the mobs from `axolotl` to
   `zombie`, then from `iron golem` (100) down to `chicken` (4), with
   the three 20s (`creeper`, `zombie`, `skeleton`) in the middle.

   **Ask:** "The three mobs with 20 health came out in the same order as
   in the list. Why?" *(`sorted` keeps equal things in the order they
   started. That's called being **stable**.)*

8. **Two more ways.** In the shell:
   ```
   >>> words = ["zombie", "Axolotl", "bee"]
   >>> sorted(words)
   ['Axolotl', 'bee', 'zombie']
   >>> sorted(words, key=len)
   ['bee', 'zombie', 'Axolotl']
   >>> numbers = [3, 1, 2]
   >>> numbers.sort()
   >>> numbers
   [1, 2, 3]
   ```
   **Say:** "`key=len` sorts by length. And `.sort()` sorts a list *in
   place*: it changes the list itself, and gives back nothing."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: quick_sort crashed with a RecursionError on 1,000 numbers that were already sorted...` | The pivot is the first item | Use the middle: `pivot = items[len(items) // 2]`. |
| `NOT YET: RecursionError...` on the very first check | The pivot isn't in `same`, or `same` isn't in the answer, so a pile never gets smaller | Check the `elif x == pivot` line, and `+ same +` at the end. |
| Numbers go missing from the answer | `same` is left out of the `return` line | `quick_sort(smaller) + same + quick_sort(bigger)`. |
| `TypeError: '<' not supported between instances of 'str' and 'int'` | The list mixes words and numbers | Sort lists that are all words, or all numbers. |
| `sorted(mobs)` gives `TypeError: '<' not supported between instances of 'dict' and 'dict'` | Python doesn't know how to compare two mobs | Give it a `key`. |
| `numbers = numbers.sort()` makes `numbers` into `None` | `.sort()` gives back nothing | Just `numbers.sort()` on its own. |

## Talk about it

- How is quicksort like merge sort? How is it different?
- What's quicksort's worst case input, with the first card as the pivot?
  Why is it so bad?
- Which sort should you use in a real program? *(`sorted`, or
  `.sort()`.)*

## Challenge *(if there's time, or for next time)*

- Use `random.choice(items)` as the pivot (and `import random` at the
  top). Now *no* input is reliably bad. Run the checker a few times:
  why do the comparison counts change each time?
- Sort the mobs by health, but with mobs of the same health in
  alphabetical order. *(Sort by name first, then by health: because
  `sorted` is stable, the names stay in order inside each health.)*
- Python can make the three piles in one line each, with a **list
  comprehension**: `smaller = [x for x in items if x < pivot]`. Rewrite
  `quick_sort` that way.

## Checkpoint

The learner can, without help:
- [ ] Do quicksort with cards, and explain the pivot
- [ ] Explain why sorted input breaks a first-card pivot, and fix it
- [ ] Pass `python3 check.py quick`
- [ ] Sort with `sorted`, `key` and `reverse`, and explain "stable"

## Lab notebook

Draw quicksort's piles for 8 shuffled cards, and for 8 sorted cards.
Write the big race times. Commit. Add *pivot*, *quicksort*, *worst case
input*, *stable* and *key* to `dictionary.md`.

## Guide's background *(optional reading)*

**Quicksort** (Tony Hoare, 1959) is O(n log n) on average and O(n²) in
the worst case, when the pivots split the piles badly. Choosing the
middle or a random pivot makes the worst case very unlikely in practice.
Real quicksorts split the list *in place*, swapping items around inside
it, rather than building new lists as this version does; that's why
they're fast and need little extra memory.

Python's `sorted` uses **Timsort** (Tim Peters, 2002): a merge sort that
finds runs that are already in order and uses insertion sort for short
pieces. It's stable, which is why sorting by one key and then another
works. Rust's standard library uses similar algorithms (Stage 9).

Lesson 7.8 asks a new question: how do we *know* an algorithm is
right, for every input, when we can't test them all?
