# Lesson 2.9: Numberblocks Builder

**Time:** 2 sessions of 45 min · **You need:** Thonny; square counting
blocks or LEGO bricks if you have them; squared paper · **New words:**
nested loop, rectangle, square number

## Goal *(read this to the learner)*

> Numberblocks are made of blocks, and so is Minecraft. Today you'll teach
> Python to build with blocks: a single block, a tower for any number,
> and then rectangles that show multiplication. You'll finish with a
> times-table poster drawn by your own program.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Put out some blocks or bricks for building on the table.

## Warm-up (5 min)

With real blocks: "Build 12 as a rectangle. Can you build it a different
way? And another?" *(3 × 4, 4 × 3, 2 × 6, 6 × 2, 1 × 12, 12 × 1.)* "Can you
build 7 as a rectangle that isn't one long line?" *(No! 7 is a prime
number, but that's for the challenge.)*

## Activity

### Session 1: blocks and towers

1. **One block.** New file, `blocks.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.speed(0)

   SIZE = 30

   def block(colour):
       t.color("black", colour)
       t.begin_fill()
       for i in range(4):
           t.forward(SIZE)
           t.left(90)
       t.end_fill()

   block("red")

   turtle.done()
   ```
   **They should see:** one red square with a black outline.

   **Say:** "`SIZE` is in capital letters as a signal to other
   programmers: this box is set once, at the top, and never changed. Try
   changing it to 50, and every block in the whole program will get
   bigger."

2. **A tower.** Add a function that stacks blocks upwards, under `block`:
   ```python
   def tower(n, colour):
       for i in range(n):
           block(colour)
           # step up one block
           t.penup()
           t.left(90)
           t.forward(SIZE)
           t.right(90)
           t.pendown()
       # climb back down to the start
       t.penup()
       t.right(90)
       t.forward(SIZE * n)
       t.left(90)
       t.pendown()
   ```
   Replace `block("red")` with `tower(5, "cyan")`.

   **Say:** "Notice the last part: we bring the turtle back down to where
   it started. Remember the rule from Lesson 2.7? *Leave the turtle where
   you found it.* That makes the next part easy."

3. **A line-up from 1 to 10.**
   ```python
   t.penup()
   t.goto(-300, -150)
   t.pendown()

   for n in range(1, 11):
       tower(n, "gold")
       t.penup()
       t.forward(SIZE + 20)
       t.pendown()
   ```
   **They should see:** ten towers, from 1 block to 10, like a staircase.

   **Say:** "`goto(-300, -150)` moves the turtle to the bottom left so
   there's room. You'll learn exactly how `goto` works in the next
   lesson."

4. **Put numbers under them.** Inside the loop, before the tower:
   ```python
       t.penup()
       t.right(90)
       t.forward(25)
       t.write(n, font=("Arial", 14, "bold"))
       t.backward(25)
       t.left(90)
       t.pendown()
   ```
   `t.write` writes text where the turtle is standing.

5. **Their own colours.** The learner chooses a colour for their
   favourite numbers and draws those towers separately with their own
   calls, like `tower(3, "yellow")`.

### Session 2: multiplication rectangles

6. **A row of blocks.** Add:
   ```python
   def row(n, colour):
       for i in range(n):
           block(colour)
           t.penup()
           t.forward(SIZE)
           t.pendown()
       # back to the start of the row
       t.penup()
       t.backward(SIZE * n)
       t.pendown()
   ```

7. **A rectangle: rows of rows.**
   ```python
   def rectangle(rows, columns, colour):
       for r in range(rows):
           row(columns, colour)
           # step up to the next row
           t.penup()
           t.left(90)
           t.forward(SIZE)
           t.right(90)
           t.pendown()
       # back down to the start
       t.penup()
       t.right(90)
       t.forward(SIZE * rows)
       t.left(90)
       t.pendown()
   ```
   Change the bottom of the program to draw `rectangle(3, 4, "green")`.

   **Say:** "3 rows of 4 blocks. How many blocks altogether? Count them."
   *(12.)* "That's what `3 × 4` *means*: 3 rows of 4."

   **Say:** "This is a **loop inside a loop**. The rectangle's loop goes
   round 3 times, and each time, `row` does its own loop 4 times. The
   inside loop runs 3 × 4 = 12 times in total, once for each block."

8. **Turn it round.** Draw `rectangle(4, 3, "orange")` next to it.
   **Say:** "4 rows of 3. Is it the same number of blocks?" *(Yes, 12.
   It's the same rectangle turned on its side. That's why 3 × 4 = 4 × 3.)*

9. **A times-table poster.** Pick the learner's favourite times table
   (the 3s, for example). New file, `poster.py`, with `block`, `row` and
   `rectangle` copied in. Then:
   ```python
   t.hideturtle()
   t.penup()
   t.goto(-350, 200)
   t.pendown()

   for n in range(1, 6):
       rectangle(3, n, "purple")
       t.penup()
       t.right(90)
       t.forward(25)
       t.write("3 x " + str(n) + " = " + str(3 * n), font=("Arial", 12, "normal"))
       t.backward(25)
       t.left(90)
       t.forward(SIZE * n + 30)
       t.pendown()
   ```
   The rectangles go across the top of the screen. If it runs off the
   right edge, make `SIZE` smaller.

   **Say:** "`str(n)` turns a number into words, so we can join it to
   other words with `+`. `"3 x " + "2"` makes `"3 x 2"`."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Towers or rows end up in odd places | A function doesn't bring the turtle back to its start | Check the "back to the start" lines at the end of each function. |
| The blocks have no outline, or no fill | `t.color("black", colour)` is missing, or `begin_fill`/`end_fill` is missing | Check the `block` function against the lesson. |
| `TypeError: can only concatenate str (not "int") to str` | Joining words and a number with `+` | Wrap the number in `str()`: `"3 x " + str(n)`. |
| `NameError: name 'SIZE' is not defined` | Spelled `Size` or `size` somewhere | Capitals must match: `SIZE` everywhere. |
| The poster runs off the screen | Too many blocks for the window | Make `SIZE` smaller, like 15. |

## Talk about it

- What does `3 × 4` look like as blocks? *(3 rows of 4.)*
- Why is `3 × 4` the same as `4 × 3`? *(It's the same rectangle, turned.)*
- How many times does `block` get called to draw `rectangle(5, 6, ...)`?
  *(30.)*
- What's a loop inside a loop?

## Challenge *(if there's time, or for next time)*

- **Square numbers.** Draw `rectangle(1, 1, ...)`, `rectangle(2, 2, ...)`,
  `rectangle(3, 3, ...)` and so on. How many blocks in each? *(1, 4, 9,
  16, 25.)* Why are they called *square* numbers?
- **Primes.** Which numbers from 2 to 20 can *only* be built as one long
  line? *(2, 3, 5, 7, 11, 13, 17, 19.)*
- **A sneak peek at lists.** Python can keep several things in one box,
  in square brackets:
  ```python
  colours = ["red", "orange", "yellow", "green", "cyan",
             "purple", "pink", "magenta", "gray", "white"]
  ```
  Then `colours[0]` is `"red"` and `colours[9]` is `"white"` (counting
  from 0 again!). Use `tower(n, colours[n - 1])` to give every tower its
  own colour. Lists come properly in Stage 3.

## Checkpoint

The learner can, without help:
- [ ] Explain multiplication as rows of blocks, using their program
- [ ] Explain what a loop inside a loop does, and count how many times
      the inside runs
- [ ] Use `str()` to join a number to some words

## Lab notebook

Colour in a times-table rectangle on squared paper. Write next to it:
"3 rows of 4 = 12 blocks, and 4 rows of 3 = 12 blocks." Add *nested loop*,
*square number* and *prime number* to the dictionary.

## Guide's background *(optional reading)*

The **array model** of multiplication (rows and columns) is the one most
maths teachers use, because it makes the facts visible: you can see why
3 × 4 = 4 × 3 by turning the picture, and you can see square numbers as
actual squares. Numberblocks uses exactly this picture.

**Nested loops** are a core programming pattern: anything with rows and
columns (a spreadsheet, a chessboard, a screen of pixels, a Minecraft
world) is handled with a loop inside a loop. Here the inner loop is
hidden inside the `row` function, which makes it easier to think about:
"draw a row" happens `rows` times.

`str()` converts a number into text. Python keeps numbers and text
separate on purpose, which is why `"3" + 4` is an error. Lesson 2.12
goes the other way, from text to a number with `int()`.
