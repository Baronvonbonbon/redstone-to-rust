# Lesson 2.13: Spirals and Patterns

**Time:** 45 min · **You need:** Thonny · **New words:** pattern, spiral

## Goal *(read this to the learner)*

> Today is all about patterns that look amazingly complicated, but are
> made from tiny programs. The trick is a box that **changes every time
> round a loop**. You'll make spirals, flowers and patterns that look like
> they came out of a spirograph.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"What does `score = score + 1` do? What's `7 % 3`? What's `8 % 3`? And
`9 % 3`?" *(Adds one to score; 1; 2; 0.)* "Keep that pattern in mind:
the remainder goes 0, 1, 2, 0, 1, 2..."

## Activity

1. **A growing line.** New file, `spiral.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.speed(0)
   turtle.bgcolor("black")
   t.pencolor("cyan")

   size = 5
   for i in range(60):
       t.forward(size)
       t.left(90)
       size = size + 5

   turtle.done()
   ```
   **They should see:** a square spiral, getting bigger as it goes.

   **Say:** "It's the square loop from Lesson 2.4, with one new line:
   `size = size + 5`. Every time round, the side gets 5 longer. A box
   that changes inside a loop makes patterns grow."

2. **Twist it.** Change `t.left(90)` to `t.left(91)` and run it.
   **They should see:** the spiral twists round.

   **Say:** "One degree more than a square, and every corner is a tiny bit
   off, so the whole thing twists. Try 89, 92, 121, 145, 60. Which do you
   like best?" Let them explore and write down their favourite angles.

3. **Rainbow colours with `%`.** Add a colour list at the top, after
   `t.pencolor`:
   ```python
   colours = ["red", "orange", "yellow", "green", "cyan", "purple"]
   ```
   And as the first line inside the loop:
   ```python
       t.pencolor(colours[i % 6])
   ```
   **They should see:** the spiral in rainbow stripes.

   **Say:** "`colours[0]` is the first colour, `colours[1]` the second, up
   to `colours[5]`. As `i` counts up 0, 1, 2... 59, `i % 6` goes 0, 1, 2,
   3, 4, 5, 0, 1, 2... round and round, like a clock. So it uses each
   colour in turn, forever. That's the leftover trick from Lesson 2.1!"

4. **A flower from squares.** New file, `flower.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.speed(0)

   def square(size):
       for i in range(4):
           t.forward(size)
           t.left(90)

   for i in range(36):
       square(100)
       t.left(10)

   turtle.done()
   ```
   **They should see:** 36 squares, each turned a little, making a circle
   pattern.

   **Say:** "36 squares, turning 10 each time. 36 × 10 is...?" *(360: a
   whole turn, so the pattern closes perfectly.)* "Try 12 squares turning
   30. Or 72 squares turning 5."

5. **Circles.** The turtle has a built-in circle:
   ```python
   t.circle(80)
   ```
   Replace the `square(100)` in the flower with `t.circle(80)`. **They
   should see:** a spirograph-style pattern.

6. **Their own pattern.** Mix the ideas: rotated hexagons with
   `polygon(6, 80)`, a twisting spiral with rainbow colours, rotated stars,
   or circles that get bigger each time. Run, change one number, run
   again. Save the best ones in `~/lab/python/patterns/`
   (`mkdir -p ~/lab/python/patterns` in the terminal first).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `IndexError: list index out of range` | The `%` number is bigger than the list | With 6 colours, use `i % 6`. With 7 colours, `i % 7`. |
| The spiral doesn't grow | `size = size + 5` is outside the loop, or missing | It must be indented, inside the loop. |
| The pattern doesn't close | The number of repeats times the turn isn't 360 | Make them multiply to 360: 36 × 10, 12 × 30, 72 × 5... |
| The pattern takes ages to draw | Lots of lines | `t.speed(0)` at the top, or see the Challenge for turbo mode. |
| The drawing goes off the screen | The spiral grows too big | Fewer loops, or a smaller step. |

## Talk about it

- What makes a spiral different from a square? *(The side gets longer each
  time round.)*
- Why does `i % 6` go 0, 1, 2, 3, 4, 5, 0, 1...? *(It's the leftover after
  sharing between 6.)*
- How can you make sure a flower pattern closes perfectly? *(Repeats ×
  turn = 360.)*

## Challenge *(if there's time, or for next time)*

- **Turbo mode.** Add `turtle.tracer(0)` near the top and `turtle.update()`
  just before `turtle.done()`. The turtle draws everything invisibly, then
  shows it all at once. Try it on a pattern with 1000 lines.
- Make a spiral where the *turn* changes instead of the size:
  `angle = angle + 1` each time round.
- Change the pen size as the spiral grows: `t.pensize(i // 10)`.
- Use `random` to choose the angle, then print it, so you can make it
  again if you like it.

## Checkpoint

The learner can, without help:
- [ ] Make a spiral by changing a variable inside a loop
- [ ] Use `i % n` to cycle through a list of colours
- [ ] Make a rotated pattern that closes, using repeats × turn = 360

## Lab notebook

Draw your favourite pattern, and write the program next to it. Make a
list of "angles I like for spirals". Add *pattern* and *spiral* to the
dictionary.

## Guide's background *(optional reading)*

This lesson combines three earlier ideas: loops, variables that change,
and `%`. The result is out of proportion to the size of the code, which is
one of the joys of programming: a five-line program can draw something
nobody would have the patience to draw by hand.

Using `%` to cycle through a list is a pattern programmers use
constantly: alternating row colours in tables, wrapping round in clocks
and calendars, and taking turns between players in a game.

The 91-degree spiral works because each corner is just slightly more than
a quarter turn, so the extra degree adds up: after 90 corners, the
spiral has twisted a whole extra quarter turn. Small changes repeated
many times make big effects. That idea comes back in maths, physics, and
compound interest.
