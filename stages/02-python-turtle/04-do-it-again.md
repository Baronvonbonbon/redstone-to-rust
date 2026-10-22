# Lesson 2.4: Do It Again

**Time:** 45 min · **You need:** Thonny; last lesson's table of turns ·
**New words:** loop, indent, block, range

## Goal *(read this to the learner)*

> Typing `forward` and `left` eight times for an octagon is boring, and
> programmers *hate* boring. Today you'll learn the **loop**: a way to
> tell the computer "do this 8 times" in just one line. Then you'll draw
> a circle using a shape with 36 sides.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Find a tennis ball or similar for the warm-up.

## Warm-up (5 min)

"Bounce the ball 5 times." Then: "How would you write that as
instructions for a robot? Would you write 'bounce' five times, or
'bounce, 5 times'?" Programmers prefer the second one, and Python can do
it too.

## Activity

1. **The first loop.** In a new file, `loop.py`:
   ```python
   for i in range(5):
       print("Bounce!")
   ```
   Run it. **They should see:** `Bounce!` five times.

   **Say:** "`for i in range(5):` means 'do this five times'. The line
   underneath is pushed in, or **indented**, and that's how Python knows
   it's part of the loop. Everything that's indented gets repeated."

2. **Watch the counter.** Change the inside line to:
   ```python
       print("Bounce number", i)
   ```
   **They should see:** `Bounce number 0` up to `Bounce number 4`.

   **Say:** "`i` is a counter that the loop changes each time round. It
   starts at **0**, not 1! Computers love counting from 0. So `range(5)`
   counts 0, 1, 2, 3, 4: that's five numbers."

3. **Inside and outside the loop.**
   ```python
   for i in range(3):
       print("Hip hip...")
   print("HOORAY!")
   ```
   **Ask before running:** "How many HOORAYs?" *(One: it isn't indented,
   so it isn't in the loop. It runs once, after the loop finishes.)*

4. **A square with a loop.** New file, `loop-square.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   for i in range(4):
       t.forward(100)
       t.left(90)

   turtle.done()
   ```
   **Say:** "Both indented lines are in the loop, so they happen four
   times, together, in order: forward, left, forward, left..."

   In Thonny, the Tab key indents a line, and Shift+Tab un-indents it.
   Thonny also indents automatically after a line ending in `:`.

5. **Every shape, short.** Using their table from last lesson, the learner
   rewrites the triangle, hexagon and octagon with loops. For the octagon:
   ```python
   for i in range(8):
       t.forward(60)
       t.left(45)
   ```
   **Say:** "Two numbers to change: how many times, and how far to turn."

6. **A circle?** Make a shape with 36 sides, each one short:
   ```python
   for i in range(36):
       t.forward(10)
       t.left(10)
   ```
   **Say:** "36 turns of 10 is 360, a whole turn. With that many sides,
   it looks just like a circle. What about 360 sides, turning 1 each
   time?" Try it. Add `t.speed(0)` before the loop to make the turtle
   draw at top speed.

7. **The star, short.**
   ```python
   for i in range(5):
       t.forward(200)
       t.right(144)
   ```

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `IndentationError: expected an indented block after 'for' statement on line 5` | The line under the `for` isn't pushed in | Press Tab at the start of that line (or 4 spaces). |
| `IndentationError: unexpected indent` | A line is indented that shouldn't be | Shift+Tab to un-indent it. |
| `SyntaxError: expected ':'` | The colon at the end of the `for` line is missing | Add `:` at the end of the line. |
| Only one side is drawn, then the turtle turns several times | Only one line is indented | Indent both lines, so both are in the loop. |
| The turtle draws the shape, then moves forward once more | An extra line is outside the loop by mistake | Check which lines are indented. |
| `NameError: name 'Range' is not defined` | Capital letter | Python cares about capitals: `range`. |

## Talk about it

- How does Python know which lines are in the loop? *(They're indented.)*
- What numbers does `range(4)` count? *(0, 1, 2, 3.)*
- Our octagon used to be 16 lines. How long is it now? *(3.)* Why is
  shorter better? *(Less typing, fewer mistakes, easier to change.)*

## Challenge *(if there's time, or for next time)*

- A 100-sided shape. What's the turn? How long should each side be so it
  fits in the window?
- Print the 7 times table with a loop: `print(i, "x 7 =", i * 7)`. It
  starts at 0 times 7. Can you make it start at 1? *(Hint:
  `range(1, 13)` counts from 1 to 12.)*
- Draw a row of 5 squares, each next to the last. *(Hint: a loop inside a
  loop. Lesson 2.9 does this properly.)*

## Checkpoint

The learner can, without help:
- [ ] Write a `for` loop that repeats a block of lines a set number of
      times
- [ ] Explain indentation, and fix an `IndentationError`
- [ ] Draw any regular polygon with a loop, using the turn rule

## Lab notebook

Write the loop-square program next to the long square program from
Lesson 2.2. Count the lines of each. Add *loop*, *indent* and *range* to
the dictionary, and write "computers count from 0" somewhere big.

## Guide's background *(optional reading)*

Loops are the first truly powerful idea in programming: one short
instruction that does a huge amount of work. Every language has them.

Python is unusual because the **indentation** (the spaces at the start of
a line) is part of the language: it's how Python knows which lines belong
inside the loop. Most other languages use curly brackets `{ }` instead,
and indentation is just for humans. Python's way forces programs to be
tidy. The usual style is 4 spaces per level, which Thonny does
automatically.

Counting from 0 surprises every beginner. It comes from how computers
find things in memory: the first item is "0 steps from the start". It
comes back in Stage 3 when we use lists.
