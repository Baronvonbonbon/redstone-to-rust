# Lesson 7.1: Counting Steps

**Time:** 2 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/algo` (see below); a pack of playing cards; Stage 0's lab
notebook page about sorting cups, if it's there · **New words:**
algorithm, linear search, best case, worst case

## Goal *(read this to the learner)*

> You've built a computer from NAND gates. Now for the other half of
> computer science: how to make a computer solve problems *cleverly*. A
> list of steps that solves a problem is called an **algorithm**. Some
> algorithms are fast and some are painfully slow, even on the same
> computer. In this stage you'll learn the most famous ones, measure
> them, and prove they work. First, you'll learn to count their steps.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] From your own account, give the learner the Stage 7 lab:
      `./scripts/give-lab.sh LEARNER algo`. It makes `~/lab/algo` with
      the checker (`check.py`) and a `mazes` folder.
- [ ] Shuffle the cards, and take out 20 of them, all different.

## Warm-up (5 min)

"Back in Stage 0, you sorted cups by weight, comparing two at a time.
What was that way of sorting called?" *(Bubble Sort.)* "Was it fast?"
*(Not for lots of cups.)* "In this stage, you'll find out exactly how
slow, and learn faster ways."

## Activity

### Session 1: an algorithm, and its steps

1. **Exact steps.** **Say:** "An algorithm is a list of steps so exact
   that someone who doesn't understand the problem can still follow
   them. A computer is that someone: it does exactly what the steps say,
   and nothing else." Play the robot game: the learner is a robot, and
   the guide gives instructions to get from the door to a chair and sit
   down. The robot does *exactly* what it hears ("Walk." *Walks into the
   wall.*). Then swap: the learner gives the instructions.

   **Say:** "A crafting recipe is an algorithm too. So is long division."

2. **Find the card.** Lay the 20 cards face down in a row. The guide
   names a card that's there. The learner turns over cards one at a
   time, from the left, until they find it, counting each turn. Play
   three times, writing down the count each time.

   **Say:** "This is called **linear search**: look at every item, in a
   line, until you find it. What's the luckiest count?" *(1: it was the
   first card. That's the **best case**.)* "The unluckiest?" *(20: the
   last one, or not there at all. That's the **worst case**.)* "And
   usually?" *(About half: 10.)*

3. **A new lab folder.** In the terminal:
   ```
   cd ~/lab/algo
   ls
   git init
   echo "__pycache__/" > .gitignore
   git add .
   git commit -m "Stage 7 starts"
   ```
   **They should see:** `check.py` and `mazes` from `ls`, and git's
   usual commit message. **Say:** "All of Stage 7's programs live here,
   with a commit for each one. `check.py` is a checker: like the tests in
   Nand to Tetris, it'll try your functions on lots of cases and tell you
   if they're right. You'll meet it next lesson."

4. **Searching in Python.** New file in Thonny, saved as
   `~/lab/algo/find_mob.py`:
   ```python
   mobs = ["pig", "cow", "sheep", "chicken", "zombie", "skeleton", "creeper",
           "spider", "enderman", "slime", "witch", "ghast", "blaze", "villager",
           "iron golem", "wolf", "cat", "bee", "axolotl", "warden"]

   target = input("Which mob? ")
   looks = 0
   found = False
   for mob in mobs:
       looks = looks + 1
       if mob == target:
           found = True
           break

   if found:
       print(f"Found the {target} after {looks} looks.")
   else:
       print(f"No {target} here. I looked {looks} times.")
   ```
   Run it (F5) four times, with `pig`, `creeper`, `warden` and `dragon`.
   **They should see:**
   ```
   Found the pig after 1 looks.
   Found the creeper after 7 looks.
   Found the warden after 20 looks.
   No dragon here. I looked 20 times.
   ```
   **Say:** "'1 looks' sounds silly. Computers don't care about grammar
   unless you tell them to. Which one was the best case? The worst?"

### Session 2: a function, and a million numbers

5. **A search function.** **Say:** "Let's make linear search a function
   that works on *any* list. It gives back the **position** of the target
   (0 for the first), or `None` if it isn't there." New file,
   `~/lab/algo/searching.py`:
   ```python
   def linear_search(items, target):
       """Looks at every item, from the start. Gives the position, or None."""
       for i in range(len(items)):
           if items[i] == target:
               return i
       return None


   assert linear_search(["pig", "cow", "sheep"], "pig") == 0
   assert linear_search(["pig", "cow", "sheep"], "sheep") == 2
   assert linear_search(["pig", "cow", "sheep"], "ghast") is None
   assert linear_search([], "pig") is None
   ```
   Run it. **They should see:** nothing at all, which is good: every
   `assert` was true (Lesson 3.5). **Say:** "`return` stops the function
   straight away, so the loop doesn't keep looking after it finds the
   target. We use `is None` to check for `None`: it's the usual Python
   way."

6. **A race against a million.** New file, `~/lab/algo/race.py`:
   ```python
   import time
   from searching import linear_search

   numbers = list(range(1_000_000))

   for target in [0, 500_000, 999_999, -1]:
       start = time.perf_counter()
       place = linear_search(numbers, target)
       seconds = time.perf_counter() - start
       print(f"Looking for {target}: found at {place} in {seconds:.4f} seconds")
   ```
   **Say:** "`1_000_000` is just a million: Python lets you put `_` in
   numbers so they're easier to read. `from searching import
   linear_search` borrows the function from your other file. And
   `time.perf_counter()` is a stopwatch: we read it before and after, and
   take away."

   Run it. **They should see** something like this (the times depend on
   the computer):
   ```
   Looking for 0: found at 0 in 0.0000 seconds
   Looking for 500000: found at 500000 in 0.0229 seconds
   Looking for 999999: found at 999999 in 0.0457 seconds
   Looking for -1: found at None in 0.0452 seconds
   ```
   **Say:** "Find 999,999 in a twentieth of a second: fast! But look at
   the pattern. Halfway along took half the time. The end took the whole
   time, and so did a number that wasn't there. The time grows with the
   length of the list."

7. **Predict.** **Ask:** "A list ten million long. Roughly how long
   would the worst case take?" *(Ten times as long: about half a
   second.)* "A billion?" *(A thousand times a million: about 45
   seconds.)* Try ten million if you like: change `1_000_000` and the
   targets. Put them back after.

8. **Commit.** `git add .` then `git commit -m "Linear search"`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'searching'` | `race.py` and `searching.py` aren't in the same folder, or one isn't saved yet | Save both in `~/lab/algo`. |
| `AssertionError`, pointing at the `"sheep"` line | `return None` is inside the loop, so the function gives up after one look | Move `return None` left, so it lines up with `for`. |
| `AssertionError` on another line | `linear_search` gave a wrong answer for that `assert` | Work out by hand what it should give, then trace the loop on paper. |
| `fatal: not a git repository` | The `git` commands ran outside `~/lab/algo` | `cd ~/lab/algo` first. |
| `ls` shows nothing | The lab hasn't been given yet | The guide runs `./scripts/give-lab.sh LEARNER algo`. |

## Talk about it

- What's an algorithm? Give an example from real life.
- What are the best and worst cases of linear search?
- If the list doubles in length, what happens to the worst-case time?
  *(It doubles too.)*

## Challenge *(if there's time, or for next time)*

- Change `find_mob.py` so it says "1 look" but "7 looks".
- Write `count_matches(items, target)`, which says how many times the
  target is in the list. Does it have a best case, or does it always
  look at every item? *(Always every item: it can't stop early.)*
- In the cards game, the guide says "higher" or "lower" after each
  turn, and the cards are laid out in order. Does that help? (That's
  next lesson.)

## Checkpoint

The learner can, without help:
- [ ] Explain what an algorithm is
- [ ] Write linear search as a function that returns a position or `None`
- [ ] Time a piece of code with `time.perf_counter()`
- [ ] Explain best case and worst case

## Lab notebook

Write the card-game counts, and the race times. Write: "If the list is
twice as long, linear search takes ___ as long." Commit. Add
*algorithm*, *linear search*, *best case* and *worst case* to
`dictionary.md`.

## Guide's background *(optional reading)*

This stage is about **algorithms** (exact methods for solving problems)
and **data structures** (ways of arranging data so the algorithms can
be fast). It's the heart of a university computer science degree,
taught here with games, cards and Python.

The key skill is **counting steps** instead of timing them. Timings
depend on the computer, but step counts don't: linear search needs up to
*n* looks for a list of *n* items, on any computer. Computer scientists
usually care most about the worst case, because it's a promise: "it
will never take more than this". Lesson 7.3 turns this into Big-O.

`time.perf_counter()` is the right Python clock for timing code: it's
precise, and it can't jump if the computer's clock changes. The
references for this stage are in the stage's README.
