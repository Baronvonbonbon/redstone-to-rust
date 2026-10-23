# Lesson 7.2: Halving: Binary Search and Logarithms

**Time:** 2 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
the 20 cards from Lesson 7.1, in order this time; a calculator (or
Python) · **New words:** binary search, sorted, logarithm

## Goal *(read this to the learner)*

> Linear search looks at everything. But if the list is **sorted**, you
> can do something much cleverer: look in the middle, and throw away the
> half that can't have it. Then do it again, and again. It's the
> guessing trick from Lesson 3.2, and it can find one number among a
> million in about 20 looks. Today you'll write it, and meet the maths
> word that counts those looks: the **logarithm**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Put the 20 cards in order, smallest to biggest, ignoring suits
      (ace low, then 2 to 10, jack, queen, king: use two suits if you
      need 20 different ones, with hearts before spades).

## Warm-up (5 min)

Play "guess my number", 1 to 100. The guide thinks of a number; the
learner guesses, and the guide says "higher" or "lower". Play twice.
"What's the best first guess?" *(50: whatever the answer, half the
numbers are gone.)*

## Activity

### Session 1: the computer guesses

1. **Halving on paper.** **Say:** "If every guess halves the numbers that
   are left, how many guesses for 100 numbers?" Write it down together:

   | Numbers left | 100 | 50 | 25 | 13 | 7 | 4 | 2 | 1 |
   |---|---|---|---|---|---|---|---|---|
   | Guesses so far | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

   *(Seven guesses at most. 25 halves to "12 or 13": count the bigger
   one.)*

2. **The mind reader.** Now the computer guesses *your* number. New
   file, `~/lab/algo/mind_reader.py`:
   ```python
   print("Think of a whole number from 1 to 100, and I'll guess it.")
   print("After each guess, type h (too high), l (too low) or y (yes!).")

   low = 1
   high = 100
   guesses = 0
   while True:
       guess = (low + high) // 2
       guesses = guesses + 1
       answer = input(f"Is it {guess}? ")
       if answer == "y":
           print(f"Got it in {guesses} guesses!")
           break
       elif answer == "h":
           high = guess - 1
       elif answer == "l":
           low = guess + 1
       if low > high:
           print("Hmm, that can't be right. Did you change your number?")
           break
   ```
   **Say:** "`low` and `high` are the smallest and biggest numbers it
   could still be. The guess is the middle: `//` divides and throws away
   any remainder. 'Too high' means it's below the guess, so `high` moves
   to just under the guess."

   Run it, thinking of 73. **They should see:** `Is it 50?` (type `l`),
   `Is it 75?` (`h`), then 62, 68, 71, and `Is it 73?` (`y`):
   `Got it in 6 guesses!` Try 100: it takes 7. Try to beat it! *(You
   can't: it never needs more than 7.)*

3. **Binary search with cards.** Lay the sorted cards face down in a
   row. The guide names a card. The learner turns over the *middle* card
   (the 10th), and the guide says nothing: the learner can tell
   themselves whether to go left or right. Then the middle of the half
   that's left... Count the turns. **Say:** "This is **binary search**.
   'Binary' because each look splits the cards into two halves. It only
   works because they're **sorted**."

### Session 2: binary search in Python

4. **The function.** Add this to `searching.py`, under the asserts
   from last time:
   ```python
   def binary_search(items, target):
       """items must be sorted. Halves the part still to search each time."""
       low = 0
       high = len(items) - 1
       while low <= high:
           middle = (low + high) // 2
           if items[middle] == target:
               return middle
           elif items[middle] < target:
               low = middle + 1
           else:
               high = middle - 1
       return None


   assert binary_search([2, 4, 6, 8, 10, 12, 14, 16], 12) == 5
   assert binary_search([2, 4, 6, 8, 10, 12, 14, 16], 7) is None
   ```
   **Say:** "It's the mind reader again, but with positions instead of
   numbers. `low` and `high` are the first and last positions where the
   target could still be."

5. **Trace it.** On paper, write the eight numbers with their positions
   (0 to 7) underneath. Trace looking for 12, one row per time round the
   loop:

   | low | high | middle | `items[middle]` | so... |
   |---|---|---|---|---|
   | 0 | 7 | 3 | 8 | too small: `low = 4` |
   | 4 | 7 | 5 | 12 | found it: give back 5 |

   Then trace 7 *(0 7 3: 8 is too big, `high = 2`; 0 2 1: 4 is too
   small, `low = 2`; 2 2 2: 6 is too small, `low = 3`; now `low` is
   bigger than `high`, so the loop stops and gives back `None`)*.

6. **The checker.** Run it (F5) first to check the asserts, then in the
   terminal:
   ```
   cd ~/lab/algo
   python3 check.py search
   ```
   **They should see:**
   ```
   Checking linear_search and binary_search, in searching.py...
     linear_search: right every time.
     binary_search: right every time.
     linear_search found 999,999 in a million numbers after 1,000,000 looks.
     binary_search found 999,999 in a million numbers after 39 looks.
   ALL GOOD!
   ```
   **Say:** "39 looks against a million! Each time round the loop, it
   looks at `items[middle]` twice (once for `==`, once for `<`), so
   that's about 20 halvings." Commit: `git add .` then
   `git commit -m "Binary search"`.

7. **The race.** New file, `~/lab/algo/race2.py`:
   ```python
   import time
   from searching import linear_search, binary_search

   numbers = list(range(1_000_000))

   for search in [linear_search, binary_search]:
       start = time.perf_counter()
       search(numbers, 999_999)
       seconds = time.perf_counter() - start
       print(f"{search.__name__}: {seconds:.6f} seconds")
   ```
   **Say:** "A function can go in a list, like anything else! The loop
   tries each one, and `__name__` is the function's name." **They should
   see** something like:
   ```
   linear_search: 0.045885 seconds
   binary_search: 0.000009 seconds
   ```
   *(About five thousand times faster. The exact numbers depend on the
   computer.)*

8. **Logarithms.** **Say:** "How many times can you halve a number
   until you get down to 1? Mathematicians call that the **logarithm**,
   base 2, written log₂. It's the opposite of powers of 2 from Stage 4:
   2 to the power 7 is 128, so log₂ of 128 is 7." In Thonny's shell
   (the bottom part):
   ```
   >>> import math
   >>> math.log2(128)
   7.0
   >>> math.log2(100)
   6.643856189774724
   >>> math.log2(1_000_000)
   19.931568569324174
   ```
   **Say:** "100 is between 2⁶ and 2⁷, so its logarithm is between 6
   and 7. Round up, and that's the most guesses the mind reader ever
   needs: 7. A million needs 20."

   **Ask:** "A billion numbers?" *(Try it: about 30.)* "All the grains of
   sand on a beach, about 10²¹?" *(`math.log2(10**21)`: about 70. Seventy
   looks for every grain of sand on a beach!)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT YET: binary_search([5], 5) gave None, but it should be 0.` | The loop says `while low < high`, so it stops before looking at the last possible place | `while low <= high`: when `low` and `high` are equal, there's still one place to look. |
| `NOT YET: that took more than 10 seconds. Is there a loop that never stops?` | `low = middle` or `high = middle`, without the `+ 1` or `- 1`, so the search can get stuck on the same two places | The middle has just been looked at, so skip it: `middle + 1` and `middle - 1`. |
| `TypeError: list indices must be integers or slices, not float` | `/` instead of `//`, so the middle is a number like `3.5` | Use `//`. |
| `IndexError: list index out of range` | `high = len(items)`, one past the end | `high = len(items) - 1`: the last position. |
| The mind reader says "that can't be right" | `h` and `l` were mixed up: `h` means *the guess* was too high | Play again, slowly. |
| `There's no searching.py in this folder` | The checker ran somewhere else | `cd ~/lab/algo`. |

## Talk about it

- Why must the list be sorted for binary search?
- If the list doubles in length, how many more looks does binary search
  need? *(Just one more.)* And linear search? *(Twice as many.)*
- What's log₂ of 1024? *(10: 2¹⁰ is 1024, from Stage 4.)*

## Challenge *(if there's time, or for next time)*

- Change the mind reader for 1 to 1000. How many guesses at most?
  Predict first, with `math.log2`. *(10.)*
- Look up a word in a paper dictionary, counting the pages you open. Is
  that binary search? *(Nearly: people jump close to the right letter,
  not to the middle. That's called interpolation search.)*
- Write `binary_search_steps(items, target)`, which gives back how many
  times it went round the loop. Try it for lists of length 1, 2, 4, 8,
  ... 1024, searching for the last item.

## Checkpoint

The learner can, without help:
- [ ] Explain binary search with cards, and why it needs a sorted list
- [ ] Write `binary_search` and pass `python3 check.py search`
- [ ] Trace `low`, `high` and `middle` on paper
- [ ] Explain log₂ as "how many times can I halve this?"

## Lab notebook

Copy the halving table for 100. Write the race times. Write: "log₂ of
a million is about ___, so binary search needs about ___ halvings."
Commit. Add *binary search*, *sorted* and *logarithm* to
`dictionary.md`.

## Guide's background *(optional reading)*

Binary search is famous for being simple to describe and easy to get
wrong. The off-by-one mistakes in the table above are the classic ones;
a bug like these sat in a widely used Java library for years. The trick
is to be exact about what `low` and `high` mean: "the target, if it's
here, is somewhere from `low` to `high`". Lesson 7.8 comes back to that
sentence, and shows how it proves the code is right.

The **logarithm** base 2 of *n* is the power you raise 2 to, to get
*n*. For whole powers of 2, it's exactly the number of halvings. The
MATH-TRACK gate for this stage asks for a first idea of logarithms; this
lesson is that first idea, and it's all the stage needs. Python has
binary search built in, in the `bisect` module, and Lesson 7.12 shows a
way to search that's even faster.
