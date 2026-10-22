# Lesson 3.6: Prime Hunters

**Time:** 2 sessions of 45 min · **You need:** Thonny; a printed or drawn
grid of the numbers 1 to 100 (10 rows of 10); two colours of pencil ·
**New words:** prime, factor, algorithm, sieve

## Goal *(read this to the learner)*

> Some numbers can only be built as one long line of blocks, never as a
> rectangle. Remember? They're called **primes**, and mathematicians have
> been hunting them for over 2000 years. Today you'll hunt them by hand,
> then teach Python to hunt them for you, thousands at a time.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Prepare the 1 to 100 grid on paper.

## Warm-up (5 min)

"What are the **factors** of 12: the numbers that divide it exactly?"
*(1, 2, 3, 4, 6, 12.)* "And the factors of 7?" *(Only 1 and 7.)* "A prime
is a number bigger than 1 whose only factors are 1 and itself. Is 1 a
prime?" *(No: mathematicians agreed it isn't, because it only has one
factor.)*

## Activity

### Session 1: hunt by hand, then by Python

1. **The sieve, on paper.** This method is more than 2000 years old, and
   is named after Eratosthenes, a Greek mathematician.
   - Cross out 1.
   - Circle 2 (it's prime). Cross out every multiple of 2: 4, 6, 8...
   - Circle the next number not crossed out (3). Cross out its multiples.
   - Keep going: circle the next uncrossed number, cross out its multiples.
   - When you've done 7, everything left uncrossed is prime. Circle them.

   **They should find** 25 primes. **Say:** "Why could we stop after 7?"
   *(The next prime is 11, and 11 × 11 = 121, which is past 100. Any
   number up to 100 that's a multiple of 11 has a smaller factor too, so
   it's already crossed out.)* Don't worry if this is a stretch; it comes
   back in step 6.

2. **A prime checker.** New file, `~/lab/python/stage3/primes.py`:
   ```python
   def is_prime(n):
       if n < 2:
           return False
       for d in range(2, n):
           if n % d == 0:
               return False
       return True

   assert not is_prime(1)
   assert is_prime(2)
   assert is_prime(7)
   assert not is_prime(12)
   assert is_prime(97)
   print("Tests passed!")
   ```
   **Say:** "The function tries every number `d` from 2 up to just below
   `n`. If any of them divides `n` exactly, it's not prime, and we can
   return `False` straight away. If none of them do, the loop finishes, and
   it's prime."

   A step-by-step plan for solving a problem like this is called an
   **algorithm**.

3. **Collect them in a list.** Add:
   ```python
   primes = []
   for n in range(1, 101):
       if is_prime(n):
           primes.append(n)

   print(primes)
   print(f"There are {len(primes)} primes up to 100.")
   ```
   **They should see:** the same 25 primes as the paper sieve. Check them
   against the paper together.

4. **Check against another program.** In a terminal:
   ```
   primes 1 100
   primes 1 100 | wc -l
   ```
   **Say:** "This `primes` command came with the terminal games. It agrees
   with us: 25. When two programs, written by different people, get the
   same answer, we can be more confident they're both right."

### Session 2: bigger and faster

5. **How many primes up to 1000? Up to 10,000?** Change the `range` and
   try. *(168 up to 1000; 1229 up to 10,000.)* Then try:
   ```python
   print(is_prime(1000003))
   ```
   **Say:** "It took a moment, didn't it? To say yes, the function had to
   try a million numbers. Can we be cleverer?"

6. **The square trick.** **Say:** "Factors come in pairs: 36 is 1 × 36,
   2 × 18, 3 × 12, 4 × 9 and 6 × 6. In every pair, one number is 6 or less.
   So we only need to try numbers up to the one that, times itself, makes
   `n`. If nothing that small divides it, nothing does." Change the
   function:
   ```python
   def is_prime(n):
       if n < 2:
           return False
       d = 2
       while d * d <= n:
           if n % d == 0:
               return False
           d += 1
       return True
   ```
   Run the tests again (they must still pass!), then `is_prime(1000003)`.

   **Say:** "Now it only tries about 1000 numbers instead of a million. Same
   answer, a thousand times less work. Making algorithms faster like this
   is a big part of computer science."

7. **Prime facts to explore.** Pick one or two:
   - **Twin primes:** primes that are 2 apart, like 11 and 13. List them up
     to 1000.
   - **The biggest gap:** what's the biggest gap between two primes up to
     1000?
   - **Prime or not?** A quiz: the program picks a random number from 1 to
     100, you say if it's prime, and it checks you with `is_prime`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Every number is prime | `return True` is indented inside the loop | It must line up with the `for` (or `while`), so it only runs after the loop has tried everything. |
| No numbers are prime | `range(1, n)` instead of `range(2, n)` | Every number can be divided by 1! Start at 2. |
| 1 is in the list | The `n < 2` check is missing | Add it at the top of the function. |
| The `while` version never finishes | `d += 1` is missing | Add it at the end of the loop. |
| `primes: command not found` | bsdgames isn't installed, or `/usr/games` isn't on the path | Try `/usr/games/primes 1 100`; the guide checks that setup ran. |

## Talk about it

- What's a prime? Is 2 a prime? Is it the only even one? Why?
  *(Yes; yes, because every other even number has 2 as a factor.)*
- Why can we stop checking at the square root?
- Two programs gave the same answer. Does that prove they're right?
  *(Not quite, but it makes it much more likely.)*

## Challenge *(if there's time, or for next time)*

- Write the sieve itself in Python, using a list of `True`/`False` values.
  (Ask the guide for help with this one; it's tricky and satisfying.)
- **Goldbach's guess:** every even number bigger than 2 is two primes
  added together (10 = 3 + 7). Check it for every even number up to 1000.
  Nobody has ever proved it's always true!
- Write `factors(n)` that returns a list of all the factors of `n`.

## Checkpoint

The learner can, without help:
- [ ] Explain what a prime number is, with examples
- [ ] Write `is_prime(n)` and test it with `assert`
- [ ] Use it to build a list of primes
- [ ] Explain one way to make it faster

## Lab notebook

Glue in the sieve grid. Write the list of primes up to 100. Write how many
primes there are up to 100, 1000 and 10,000. Add *prime*, *factor*,
*algorithm* and *sieve* to the dictionary.

## Guide's background *(optional reading)*

Primes are the "atoms" of the whole numbers: every whole number bigger
than 1 can be made by multiplying primes together in exactly one way
(12 = 2 × 2 × 3). Euclid proved there are infinitely many of them, around
300 BC, and a proof of that fits on a postcard (it's in *Book of Proof*,
in the offline library, for later).

They matter in computing because modern **cryptography**, the maths that
protects passwords and messages online, depends on the fact that
multiplying two huge primes is easy but splitting the result back into
those primes is extremely hard. That's Stage 11.

The square-root speed-up is the learner's first real optimisation of an
algorithm. Comparing "about a million steps" with "about a thousand steps"
is a preview of **Big-O** thinking from Stage 7.
