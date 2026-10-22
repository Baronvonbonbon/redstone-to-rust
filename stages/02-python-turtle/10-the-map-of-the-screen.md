# Lesson 2.10: The Map of the Screen

**Time:** 45 min · **You need:** Thonny; squared paper; a coin or counter ·
**New words:** coordinates, x, y, origin, negative number

## Goal *(read this to the learner)*

> In Minecraft, every block has an address: three numbers called **X, Y
> and Z**. Python's screen has addresses too, but only two numbers, x and
> y. Today you'll learn to send the turtle straight to any spot, draw
> pictures by joining the dots, and play a treasure-hunting game.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] On squared paper, draw two lines crossing in the middle: one across
      (the x line) and one up and down (the y line). Number the across
      line from -5 to 5, and the up line from -5 to 5. Mark the middle
      `(0, 0)`.
- [ ] Write a secret "treasure" spot for step 6 on a hidden slip of paper,
      for example `(150, -100)`.

## Warm-up (5 min)

"In Minecraft, what happens to the Y number when you dig down?" *(It goes
down. Below a certain level, in newer versions, it goes below zero!)*
"Numbers below zero are called **negative numbers**. They're written with
a minus sign: -1, -2, -3. Think of them as the floors below the ground
floor in a lift."

## Activity

1. **Paper first.** Use the squared paper. Put the coin on `(0, 0)`.
   **Say:** "The first number is **x**: how far across. Positive is right,
   negative is left. The second number is **y**: how far up. Positive is
   up, negative is down."

   Call out spots and have them move the coin: `(3, 0)`, `(3, 2)`,
   `(-2, 2)`, `(-2, -4)`, `(0, 0)`. Then switch: they call spots for you.

   **Say:** "Always across first, then up. A way to remember: you walk
   along the corridor before you go up the stairs."

2. **The turtle's map.** New file, `map.py`:
   ```python
   import turtle

   turtle.setup(800, 600)
   t = turtle.Turtle()
   t.shape("turtle")

   print(t.position())
   t.goto(200, 0)
   t.goto(200, 150)
   t.goto(0, 0)

   turtle.done()
   ```
   **They should see:** a triangle, and `(0.00,0.00)` printed in the Shell.

   **Say:** "`turtle.setup(800, 600)` makes the window 800 pixels wide and
   600 tall. The turtle starts in the middle, at `(0, 0)`, called the
   **origin**. `goto` sends it straight to that spot, drawing a line on
   the way, without any turning. The right edge is at x = 400 and the
   left edge at x = -400. What about the top and the bottom?"
   *(y = 300 and y = -300.)*

3. **Draw the map lines.** Add to the program, before the triangle:
   ```python
   t.speed(0)
   t.pencolor("gray")
   t.penup()
   t.goto(-400, 0)
   t.pendown()
   t.goto(400, 0)
   t.penup()
   t.goto(0, -300)
   t.pendown()
   t.goto(0, 300)
   t.penup()
   t.goto(0, 0)
   t.pendown()
   t.pencolor("black")
   ```
   Now there's a cross through the middle, just like on the paper.

4. **Dot-to-dot mystery picture.** Read the learner these spots, one at a
   time. They write a `goto` line for each, in a new file `mystery.py`,
   without knowing what it will be:
   ```python
   import turtle

   turtle.setup(800, 600)
   t = turtle.Turtle()
   t.pensize(3)

   t.penup()
   t.goto(0, 200)
   t.pendown()
   t.goto(50, 120)
   t.goto(50, -100)
   t.goto(100, -150)
   t.goto(-100, -150)
   t.goto(-50, -100)
   t.goto(-50, 120)
   t.goto(0, 200)

   t.penup()
   t.goto(0, 20)
   t.dot(40, "skyblue")

   turtle.done()
   ```
   **They should see:** a rocket, with a round window. `t.dot(40, "skyblue")`
   draws a filled circle 40 pixels across where the turtle is.

5. **Their own mystery picture.** The learner draws a picture on the
   squared paper, using the lines (each square can be worth 50 pixels),
   writes down its corner spots, and reads them to the guide, who types
   the program. Then swap. Did the picture come out right?

6. **Treasure hunt.** The guide has a secret spot written down. In the
   Shell (with `import turtle`, `t = turtle.Turtle()` first), the learner
   guesses:
   ```python
   t.goto(100, 100)
   ```
   After each guess, the guide says "warmer" or "colder", or gives a clue:
   "go further left" (smaller x) or "go further down" (smaller y). Mark
   each guess with `t.dot(10, "red")`. Found it? Mark it with
   `t.dot(30, "gold")`. Then swap roles.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A line is drawn while moving to a new spot | The pen is down | `t.penup()` before the `goto`, then `t.pendown()` after. |
| The picture is mirrored or upside down | x and y swapped, or a minus sign missed | Check: across (x) first, then up (y). |
| `TypeError: turtle.Vec2D() argument after * must be an iterable, not int` | Only one number given | `goto` needs two: `t.goto(x, y)`. |
| The turtle disappears off the screen | A number bigger than the window | Keep x between -400 and 400, and y between -300 and 300. |
| `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | The comma between the numbers is missing | `t.goto(-50, 120)`. |

## Talk about it

- Which number says across, and which says up? *(x across, y up.)*
- Where is `(0, 0)`? *(The middle, the origin.)*
- What's the difference between `goto` and `forward`? *(`goto` goes to an
  exact spot, without turning; `forward` moves in the direction the turtle
  faces.)*
- Minecraft has three numbers, X, Y and Z. Why does it need one more?
  *(It's a 3D world: Z is the other across direction, into the screen.)*

## Challenge *(if there's time, or for next time)*

- `t.write(t.position())` writes the turtle's spot on the screen. Draw a
  dot at each corner of the window and write its spot next to it.
- Draw a grid of dots, every 50 pixels, with a loop inside a loop:
  `t.goto(x * 50, y * 50)` for x and y from -4 to 4. *(Use `range(-4, 5)`.)*
- Plot the points `(x, x * 2)` for x from -5 to 5, times 20 so you can see
  them. They make a straight line! What about `(x, x * x)`?
- In Minecraft (or Luanti), press F3 (or F5 in Luanti, if your version
  shows it) to see your coordinates. Walk around and watch them change.

## Checkpoint

The learner can, without help:
- [ ] Move a counter to a spot like `(-3, 2)` on squared paper
- [ ] Use `goto(x, y)` with positive and negative numbers
- [ ] Use `penup` and `goto` to move without drawing
- [ ] Draw a picture from a list of corner spots

## Lab notebook

Glue in the squared paper with the cross and the mystery picture. Write
"x is across, y is up". Add *coordinates*, *origin*, *x*, *y* and
*negative number* to the dictionary.

## Guide's background *(optional reading)*

These are **Cartesian coordinates**, named after René Descartes, who had
the idea of naming every point on a flat surface with two numbers. They
connect drawing and numbers: every shape can become a list of numbers,
and every list of numbers can become a picture. That's how every game,
map and drawing program works inside.

Negative numbers are often taught late in school, but children grasp them
easily on a number line or in a lift, and coordinates give a real reason
to use them. The challenge about `(x, x * 2)` is a first look at graphing
a function, which school maths covers much later; there's no need to
explain it formally now.

The screen's y goes *up* in Python turtle, like in maths. In many other
graphics systems (including Pygame Zero, in Stage 3), y goes *down* from
the top of the screen. We'll point that out when we get there.
