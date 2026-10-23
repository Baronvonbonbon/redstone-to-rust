# Lesson 7.9: Dominoes: Proof by Induction (Proof, Part 2)

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
dominoes (or books, or cards that stand up); about 30 building blocks or
cubes; three coins or cups of different sizes; squared paper ·
**New words:** induction, step, triangle number, square number

## Goal *(read this to the learner)*

> How do you prove something is true for *every* number: 1, 2, 3, and on
> forever? Line up dominoes. If the first one falls, and every domino
> knocks over the next, then they *all* fall, however many there are.
> That's a proof method called **induction**, and it's recursion's twin.
> Today you'll use it to prove a Numberblocks pattern, find a shortcut
> that a schoolboy used to beat his teacher, and solve an ancient puzzle
> with a recursive program.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Set up a line of dominoes (or books) standing on end.
- [ ] Optional reading for you: *Book of Proof* (in the offline library,
      `books/book-of-proof.pdf`), Chapter 10, "Mathematical Induction".

## Warm-up (5 min)

"What's a counterexample?" *(One case where a claim is wrong.)* "What
are the two parts of a recursive function?" *(A base case, and a step
that uses a smaller problem.)* Remember them: induction has the same two
parts.

## Activity

### Session 1: dominoes and squares

1. **Dominoes.** **Ask:** "What has to be true for *every* domino to
   fall?" Let the learner experiment: take one out of the middle, or
   don't push the first. *(Two things: the first one must fall, and each
   one must be close enough to knock over the next.)*

   **Say:** "That's **induction**:
   - the **base case**: it's true for the first one;
   - the **step**: *if* it's true for one, it's true for the next.

   Then it's true for all of them, even a line of dominoes that goes on
   forever."

2. **Odd numbers make squares.** With cubes, build the odd numbers as
   L-shapes, each wrapping around the one before: 1; then 3 around it
   (making a 2 by 2 square); then 5 around that (3 by 3)... **Ask:**
   "What do the odd numbers add up to?" *(Square numbers: 1, 4, 9, 16.
   Numberblocks fans may know the Square Club!)*

   New file, `~/lab/algo/squares.py`:
   ```python
   total = 0
   for n in range(1, 11):
       odd = 2 * n - 1
       total = total + odd
       print(f"adding {odd:2} makes {total:3}, and {n} × {n} is {n * n}")
   ```
   **They should see:** ten lines, from `adding  1 makes   1, and 1 × 1
   is 1` to `adding 19 makes 100, and 10 × 10 is 100`. Every total is a
   square.

   **Say:** "Ten cases is evidence. Let's prove it for every number."

3. **The proof.** Write it together, with the cubes on the table:

   > **Claim:** the first n odd numbers add up to n × n.
   >
   > **Base case:** the first odd number is 1, and 1 × 1 is 1. ✓
   >
   > **Step:** suppose the first n odd numbers make an n by n square.
   > The next odd number is 2n + 1. Wrap it around the square as an L:
   > n cubes along the top, n down the side, and 1 in the corner. Now
   > it's an (n + 1) by (n + 1) square. ✓
   >
   > So by induction, it's true for every n. ∎

   **Ask:** "Where's the domino knocking over the next one?" *(The step:
   if the square works for n, it works for n + 1.)*

### Session 2: the staircase

4. **Gauss's shortcut.** **Say:** "About 250 years ago, a teacher told
   his class to add up 1 + 2 + 3 + ... + 100, hoping for some peace and
   quiet. A boy called Carl Friedrich Gauss wrote down the answer almost
   straight away." Build a staircase of cubes: 1, 2, 3, 4. Then build a
   second staircase the same, turn it upside down, and fit it on top.
   **They should see:** a rectangle, 4 wide and 5 tall.

   **Ask:** "How many cubes in the rectangle?" *(4 × 5 = 20.)* "And in
   one staircase?" *(Half: 10.)* "So 1 + 2 + ... + 100?" *(Two staircases
   make a rectangle 100 by 101: 10,100 cubes. One staircase is half:
   5050.)*

   **Say:** "Numbers made as staircases (1, 3, 6, 10, 15...) are called
   **triangle numbers**. The shortcut: 1 + 2 + ... + n = n × (n + 1) ÷ 2."

5. **The number from Lesson 7.4.** **Ask:** "Selection sort compared
   999 + 998 + ... + 1 times, for 1000 numbers. Use the shortcut." In
   the shell:
   ```
   >>> 999 * 1000 // 2
   499500
   ```
   **Say:** "That's exactly the number the checker printed! Now we know
   *why*: it's a triangle number. And n × (n + 1) ÷ 2 is about n² ÷ 2,
   which is why selection sort is O(n²)."

6. **Prove it by induction.** The learner tries, with the staircase:
   - Base case: one step has 1 cube, and 1 × 2 ÷ 2 = 1. ✓
   - Step: a staircase of n steps has n(n + 1) ÷ 2 cubes. Adding the
     next step adds n + 1 cubes. *(With algebra: n(n + 1) ÷ 2 + (n + 1)
     = (n + 1)(n + 2) ÷ 2, which is the formula for n + 1. A learner
     who isn't ready for that line can check it for n = 4 and 5 with
     cubes, and the guide can write it.)*

### Session 3: the Tower of Hanoi

7. **The puzzle.** Stack three coins, biggest at the bottom, on spot A.
   Mark spots A, B and C on paper. **Say:** "Move the whole tower to C.
   Rules: one coin at a time, and never put a bigger coin on a smaller
   one." Solve it, counting moves. *(7 moves.)* Then try with 2 coins
   *(3 moves)* and 1 *(1 move)*.

8. **The recursive idea.** **Say:** "To move a tower of 3 to C: first
   move the tower of 2 on top out of the way, to B. Then move the big
   coin to C. Then move the tower of 2 from B onto it. Moving a tower of
   2 uses the same idea with a tower of 1!" New file,
   `~/lab/algo/hanoi.py`:
   ```python
   def hanoi(n, start, goal, spare):
       """Moves n discs from start to goal. Gives back how many moves it took."""
       if n == 0:
           return 0
       moves = hanoi(n - 1, start, spare, goal)
       print(f"Move disc {n} from {start} to {goal}")
       moves = moves + 1
       moves = moves + hanoi(n - 1, spare, goal, start)
       return moves


   count = hanoi(3, "A", "C", "B")
   print(f"That took {count} moves.")
   ```
   **They should see:**
   ```
   Move disc 1 from A to C
   Move disc 2 from A to B
   Move disc 1 from C to B
   Move disc 3 from A to C
   Move disc 1 from B to A
   Move disc 2 from B to C
   Move disc 1 from A to C
   That took 7 moves.
   ```
   (Disc 1 is the smallest.) Follow the moves with the coins.

9. **How many moves?** Try 4, 5 and 10 discs (change the 3). Make a
   table: 1 disc, 1 move; 2, 3; 3, 7; 4, 15; 5, 31. **Ask:** "What's the
   pattern?" *(One less than a power of 2: 2ⁿ − 1.)*

   **Say:** "Prove it by induction. Base case: 1 disc, 1 move, and
   2¹ − 1 is 1. ✓ Step: if n discs take 2ⁿ − 1 moves, then n + 1 discs
   take (2ⁿ − 1) to move the small tower away, 1 for the big disc, and
   (2ⁿ − 1) again to move the small tower back. That's 2 × 2ⁿ − 1, which
   is 2ⁿ⁺¹ − 1. ✓ ∎"

   **Say:** "There's a legend of a temple with 64 golden discs. At one
   move a second, how long would it take?" In the shell:
   `(2 ** 64 - 1) / (60 * 60 * 24 * 365)` *(About 585 billion years!
   That's O(2ⁿ) from Lesson 7.3.)* Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `squares.py`'s totals aren't squares | `odd` is worked out wrongly | `odd = 2 * n - 1`: for n = 1, 2, 3 that's 1, 3, 5. |
| `hanoi` prints moves that break the rules | The pegs are in the wrong order in one of the calls | Compare each call with the lesson: the first call moves the small tower to the *spare*, the second from the spare to the *goal*. |
| `That took None moves.` | `return moves` is missing | Add it at the end of `hanoi`. |
| `RecursionError` | The base case `if n == 0:` is missing | Put it back. |
| The algebra in step 6 is too much | The learner hasn't met brackets in algebra yet | Do the step with cubes for a few cases, and come back to the algebra with the math track. |

## Talk about it

- What are the two parts of an induction proof? How are they like a
  recursive function?
- Why do two staircases make a rectangle?
- Why is the Tower of Hanoi O(2ⁿ)?

## Challenge *(if there's time, or for next time)*

- Prove by induction that 1 + 2 + 4 + 8 + ... + 2ⁿ⁻¹ = 2ⁿ − 1. *(It's
  the binary number 111...1 from Stage 4, and the Tower of Hanoi
  count!)*
- How many handshakes in a room of n people (Lesson 7.3's challenge)?
  *(The first shakes n − 1 hands, the next n − 2 new ones... a triangle
  number: n(n − 1) ÷ 2.)*
- A "proof" that all horses are the same colour uses induction and goes
  wrong. Ask the guide for it, and find the broken domino. *(Guide: see
  below.)*

## Checkpoint

The learner can, without help:
- [ ] Explain induction with dominoes: base case and step
- [ ] Prove that odd numbers add up to squares, with cubes
- [ ] Use the triangle number shortcut, and connect it to selection sort
- [ ] Solve the Tower of Hanoi with a recursive program, and explain
      why it takes 2ⁿ − 1 moves

## Lab notebook

Write the odd-squares proof. Draw the two staircases making a
rectangle. Copy the Hanoi moves table. Commit. Add *induction*, *step*,
*triangle number* and *square number* to `dictionary.md`.

## Guide's background *(optional reading)*

**Induction** proves a statement P(n) for every whole number n by
proving P(1) (the base case) and "if P(n), then P(n + 1)" (the step).
It's the natural way to prove things about recursive programs: the
base case of the proof matches the base case of the function, and the
step matches the recursive call. Stage 8's compiler and Stage 12's
interpreters are full of recursion proved correct this way.

The "all horses are the same colour" puzzle: the claim is that in any
group of n horses, all are the same colour. Base case: one horse, true.
"Step": take n + 1 horses; the first n are all the same colour, and so
are the last n; they overlap, so all n + 1 match. The broken domino is
going from 1 horse to 2: the "first one" and the "last one" don't
overlap at all, so the step fails there, and the whole chain never
starts.

The story about Gauss is famous but probably exaggerated over the
years; the staircase picture is the real point. The triangle-number
formula and the 2ⁿ − 1 formula both come back constantly in computer
science, when counting comparisons, pairs, and subsets.
