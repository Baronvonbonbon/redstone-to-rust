# Lesson 3.7: Hailstone Numbers

**Time:** 45 min · **You need:** Thonny; paper · **New words:** sequence,
conjecture, graph

## Goal *(read this to the learner)*

> Today's puzzle has a very simple rule, and it's one of the most famous
> unsolved problems in maths. Nobody in the world knows the answer, not
> even the cleverest mathematicians. You'll explore it with Python, and
> draw pictures of numbers bouncing up and down like hailstones in a cloud.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min): the rule, by hand

Write the rule big on paper:

> Pick a number. If it's **even**, halve it. If it's **odd**, times it by
> 3 and add 1. Do the same to the answer, again and again, until you reach 1.

Do 6 together: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1. That took 8 steps.
Then the learner does 7 on their own. *(7 → 22 → 11 → 34 → 17 → 52 → 26 →
13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1: 16 steps, up to 52.)*

## Activity

1. **One step, as a function.** New file, `~/lab/python/stage3/hailstone.py`:
   ```python
   def next_number(n):
       if n % 2 == 0:
           return n // 2
       else:
           return 3 * n + 1

   assert next_number(6) == 3
   assert next_number(3) == 10
   ```
   **Say:** "We use `//` so the answer stays a whole number."

2. **The whole journey.** Add:
   ```python
   def hailstone(n):
       journey = [n]
       while n != 1:
           n = next_number(n)
           journey.append(n)
       return journey

   assert hailstone(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
   print(hailstone(7))
   ```
   **They should see:** the same journey they worked out by hand for 7.

3. **Steps and heights.** Add:
   ```python
   n = int(input("Pick a starting number: "))
   journey = hailstone(n)
   print(journey)
   print(f"{n} took {len(journey) - 1} steps, and went as high as {max(journey)}.")
   ```
   **Say:** "Why `len(journey) - 1`?" *(The list includes the starting
   number, which isn't a step.)*

   Let them try lots of numbers. Then say: "Try 27."

   **They should see:** 27 takes **111** steps and climbs to **9232**
   before falling back to 1. **Say:** "From 27! Nobody would guess that."

4. **The champion.** Which starting number from 1 to 99 takes the most
   steps? Add:
   ```python
   best = 1
   for n in range(1, 100):
       if len(hailstone(n)) > len(hailstone(best)):
           best = n
   print(f"The champion under 100 is {best}, with {len(hailstone(best)) - 1} steps.")
   ```
   **They should see:** 97, with 118 steps.

5. **Draw the hailstone.** Bring back the turtle from Stage 2. New file,
   `hailstone-graph.py`, with `next_number` and `hailstone` copied in, then:
   ```python
   import turtle

   turtle.setup(800, 600)
   t = turtle.Turtle()
   t.speed(0)

   journey = hailstone(27)

   t.penup()
   for step in range(len(journey)):
       x = -380 + step * 6
       y = -280 + journey[step] / 20
       t.goto(x, y)
       t.pendown()

   turtle.done()
   ```
   **They should see:** a jagged line that bounces up and down, shoots up
   to a peak, and crashes down to 1, like a hailstone tossed around in a
   storm cloud before it falls.

   **Say:** "This is a **graph**: the across direction is the step number,
   and the up direction is the size of the number. We divided by 20 so
   9232 fits on the screen."

6. **The unsolved problem.** **Say:** "Here's the amazing part. Every
   number anyone has ever tried ends up at 1. Computers have checked every
   number up to about 300 billion billion. But nobody has ever *proved*
   that every number gets there. Maybe there's a gigantic number somewhere
   that goes on forever. It's called the **Collatz conjecture**, after
   Lothar Collatz, who asked the question in 1937. A **conjecture** is a
   guess that nobody has proved yet. Maybe *you'll* be the one."

   **Say:** "And here's something for a programmer: our `while n != 1`
   loop *might* never stop for some number. Nobody knows!"

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The program never stops | Starting at 0 or a negative number (0 halves to 0 forever) | Only start at 1 or more. Stop it with the red button. |
| Numbers like `5.0` appear | `/` used instead of `//` | Use `//` to keep whole numbers. |
| The graph goes off the top | A number too big for the screen | Divide by a bigger number than 20. |
| `AssertionError` on `hailstone(6)` | The journey doesn't match | Print `hailstone(6)` and compare with the paper. |

## Talk about it

- What does "conjecture" mean? *(A guess nobody has proved yet.)*
- If a computer checks a billion numbers and they all reach 1, does that
  prove it? *(No. There might be a bigger number that doesn't.)*
- Which was harder: doing the steps by hand, or writing the program?

## Challenge *(if there's time, or for next time)*

- Graph the *number of steps* for every start from 1 to 100, as a bar
  chart with the turtle. Does it make a pattern?
- What's the champion under 1000? Under 10,000? (Be patient!)
- Make up your own rule (for example, odd numbers: times 5 and add 1).
  Do the numbers still come down to 1? (Sometimes they don't! Try 5 × n + 1
  starting from 13.)

## Checkpoint

The learner can, without help:
- [ ] Work out a hailstone journey by hand, and with their program
- [ ] Explain why the `while` loop might, in theory, never stop
- [ ] Draw a list of numbers as a graph with the turtle
- [ ] Explain what a conjecture is

## Lab notebook

Copy the journey of 7. Sketch the graph of 27. Write "The Collatz
conjecture: nobody knows if every number reaches 1." Add *sequence*,
*conjecture* and *graph* to the dictionary.

## Guide's background *(optional reading)*

The Collatz conjecture is a favourite of mathematicians because it's so
easy to state and so hard to solve. The famous mathematician Paul Erdős
said "Mathematics may not be ready for such problems." It's a perfect
example for a young learner that maths isn't finished: there are open
questions anyone can understand.

It also touches a deep idea in computer science: in general, you can't
always tell in advance whether a program will stop. That's called the
**halting problem**, proved by Alan Turing in 1936. The hailstone loop is
a friendly first example of a loop whose stopping nobody can guarantee.

The "5n + 1" challenge is a nice surprise: with that rule, some starting
numbers fall into a loop (13 → 66 → 33 → 166 → 83 → 416 → 208 → 104 → 52
→ 26 → 13...) and never reach 1, which shows why the 3n + 1 version is
special.
