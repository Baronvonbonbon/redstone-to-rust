# Lesson 7.3: How Things Grow: Big-O

**Time:** 2 sessions of 45 min · **You need:** Thonny; `~/lab/algo`;
squared paper; building blocks or Minecraft (optional) · **New words:**
Big-O, growth, `__name__`

## Goal *(read this to the learner)*

> Linear search takes twice as long on a list twice as long. Binary
> search takes just one more step. Computer scientists sort algorithms
> into families by *how their steps grow* when the problem gets bigger,
> and they write the families with a big letter O: **Big-O**. Today
> you'll build walls and floors, count their blocks, draw the growth as
> a graph, and learn to spot the families in code.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Optional: in Minecraft creative mode (or with building blocks),
      have the learner build a wall 4 long, a floor 4 by 4, and a cube
      4 by 4 by 4 before the lesson, counting the blocks.

## Warm-up (5 min)

"Linear search on a list of a million: how many looks in the worst
case?" *(A million.)* "Binary search?" *(About 20.)* "And if the list is
two million?" *(Two million, and 21.)*

## Activity

### Session 1: walls, floors and cubes

1. **Count blocks.** On squared paper (or in Minecraft), fill in:

   | Side | Wall (side long) | Floor (side by side) | Cube (side × side × side) |
   |---|---|---|---|
   | 1 | 1 | 1 | 1 |
   | 2 | 2 | 4 | 8 |
   | 4 | 4 | 16 | 64 |
   | 10 | ? | ? | ? |
   | 100 | ? | ? | ? |

   *(10, 100, 1000; then 100, 10,000, a million.)* **Say:** "Double the
   side, and the wall doubles. The floor? *(Four times.)* The cube?
   *(Eight times!)* That's what **growth** means: not how big something
   is, but how fast it gets bigger."

2. **Count steps in code.** New file, `~/lab/algo/growth.py`:
   ```python
   def halvings(n):
       """How many times can n be halved before it gets to 1?"""
       steps = 0
       while n > 1:
           n = n // 2
           steps = steps + 1
       return steps


   def wall(n):
       """One loop: a wall n blocks long."""
       steps = 0
       for x in range(n):
           steps = steps + 1
       return steps


   def floor(n):
       """A loop inside a loop: a floor n blocks by n blocks."""
       steps = 0
       for x in range(n):
           for z in range(n):
               steps = steps + 1
       return steps


   if __name__ == "__main__":
       print("    n  halvings   wall     floor")
       for n in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
           print(f"{n:5} {halvings(n):9} {wall(n):6} {floor(n):9}")
   ```
   **Say:** "In an f-string, `{n:5}` means 'take up 5 spaces', so the
   numbers line up in columns. And `if __name__ == "__main__":` means
   'only do this part when this file is run, not when another file
   imports it'. You'll see why in a minute."

   Run it. **They should see:**
   ```
       n  halvings   wall     floor
       1         0      1         1
       2         1      2         4
       4         2      4        16
       8         3      8        64
      16         4     16       256
      32         5     32      1024
      64         6     64      4096
     128         7    128     16384
     256         8    256     65536
     512         9    512    262144
    1024        10   1024   1048576
   ```
   **Ask:** "Each row doubles `n`. What happens to each column?"
   *(Halvings goes up by one. Wall doubles. Floor goes up four times.)*

3. **Draw it.** New file, `~/lab/algo/growth_graph.py`:
   ```python
   import turtle
   from growth import halvings, wall, floor

   turtle.setup(800, 600)
   turtle.bgcolor("white")


   def draw(count_steps, colour):
       t = turtle.Turtle()
       t.hideturtle()
       t.speed(0)
       t.pencolor(colour)
       t.pensize(3)
       t.penup()
       for n in range(1, 12):
           x = -380 + n * 55
           y = -280 + count_steps(n) * 4
           t.goto(x, y)
           t.pendown()
       t.write(count_steps.__name__, font=("Arial", 16, "bold"))


   draw(halvings, "green")
   draw(wall, "blue")
   draw(floor, "red")
   turtle.done()
   ```
   **Say:** "`draw` gets a *function* to draw. That's how one `draw`
   can draw all three." Run it. **They should see:** three lines from the
   bottom left. The green `halvings` line stays almost flat. The blue
   `wall` line climbs in a straight line. The red `floor` line curves up
   and shoots off towards the top.

   **Say:** "Because of the `if __name__` line, importing `growth` didn't
   print the table. Try taking it away (put everything under it back to
   the left), and run the graph again." *(The table is printed first.
   Put it back after.)*

### Session 2: Big-O

4. **The families.** **Say:** "Computer scientists name these families
   with **Big-O**. You say it 'big oh of n'." Write them on a big sheet,
   slowest-growing first:

   | Big-O | Name | Double the size, and the steps... | Example |
   |---|---|---|---|
   | O(1) | constant | stay the same | looking at `items[0]` |
   | O(log n) | logarithmic | go up by one | binary search, halvings |
   | O(n) | linear | double | linear search, a wall |
   | O(n²) | quadratic | go up 4 times | a loop in a loop, a floor |
   | O(n³) | cubic | go up 8 times | a loop in a loop in a loop, a cube |

   **Say:** "`n` is the size of the problem: how long the list is, or
   how long the wall is."

5. **The doubling experiment.** New file, `~/lab/algo/doubling.py`:
   ```python
   import time
   from growth import wall, floor

   for n in [1000, 2000, 4000]:
       start = time.perf_counter()
       floor(n)
       seconds = time.perf_counter() - start
       print(f"floor({n}) took {seconds:.2f} seconds")
   ```
   **Ask first:** "If `floor(1000)` takes a twentieth of a second, how
   long for 2000? 4000?" Then run it. **They should see** something like:
   ```
   floor(1000) took 0.05 seconds
   floor(2000) took 0.21 seconds
   floor(4000) took 0.85 seconds
   ```
   *(About 4 times longer each time. Times depend on the computer.)*
   **Ask:** "How long for 40,000?" *(Ten times the side is a hundred
   times the time: about a minute and a half.)* "Don't run it!"

6. **The rules.** **Say:** "Big-O only cares about the shape, so two
   rules make it simple":
   - **Ignore constant multiples.** Two walls is still O(n): double the
     size, and the steps still double.
   - **Keep only the biggest part.** A floor and a wall together is
     n² + n steps. When n is 1000, that's 1,000,000 + 1,000: the wall
     hardly matters. It's O(n²).

7. **Spot the family.** Write each piece of code on a card; the learner
   says its Big-O and why:
   ```python
   for x in range(n):            # A
       print(x)
   ```
   ```python
   print(items[0])               # B
   ```
   ```python
   for x in range(n):            # C
       for y in range(n):
           print(x, y)
   ```
   ```python
   for x in range(n):            # D
       print(x)
   for y in range(n):
       print(y)
   ```
   ```python
   while n > 1:                  # E
       n = n // 2
   ```
   ```python
   for x in range(n):            # F
       for y in range(10):
           print(x, y)
   ```
   *(A: O(n). B: O(1). C: O(n²). D: O(n): two loops one after the
   other, not one inside the other. E: O(log n). F: O(n): the inner loop
   is always 10, a constant. F is the tricky one!)*

8. **Commit.** `git add .` and `git commit -m "Big-O experiments"`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The table prints before the graph | The `if __name__ == "__main__":` line is missing, or the lines under it aren't indented | Put the line back, with the table lines indented under it. |
| `ImportError: cannot import name 'floor' from 'growth'` | `floor` is spelled differently in `growth.py`, or it isn't saved | Check the spelling, and save. |
| The red line goes off the top of the window | The loop goes past 11 | `range(1, 12)`. |
| The graph window closes straight away | `turtle.done()` is missing | Add it at the end. |
| `doubling.py` runs for ages | `n` is too big | Press Ctrl+C (or Thonny's red Stop button), and use the numbers in the lesson. |

## Talk about it

- What does "growth" mean? Why does it matter more than speed on one
  computer?
- Which family is binary search? Linear search?
- A program is O(n²). It takes 1 second for 1000 items. About how long
  for 10,000? *(100 seconds.)*

## Challenge *(if there's time, or for next time)*

- Add `cube(n)` to `growth.py`: three loops, one inside another. Add it
  to the table, but only up to 128. Why not 1024? *(1024 cubed is over a
  billion steps: minutes!)*
- How many handshakes if everyone in a room of *n* people shakes hands
  with everyone else once? Try 2, 3, 4 and 5 people. Is it O(n) or
  O(n²)? *(1, 3, 6, 10: it's n × (n − 1) ÷ 2, which is O(n²). Those are
  triangle numbers: Lesson 7.9 proves the formula.)*
- Some algorithms are O(2ⁿ): add one item, and the steps double. How
  many steps for n = 64? *(Over 18 billion billion. Way too many!)*

## Checkpoint

The learner can, without help:
- [ ] Explain growth with walls, floors and cubes
- [ ] Name O(1), O(log n), O(n) and O(n²), with an example of each
- [ ] Say the Big-O of a simple loop, two loops in a row, and a loop in
      a loop
- [ ] Predict the time for a bigger problem from the Big-O

## Lab notebook

Copy the Big-O table. Sketch the three lines from the graph. Write the
doubling-experiment times and the prediction for 40,000. Commit. Add
*Big-O* and *growth* to `dictionary.md`.

## Guide's background *(optional reading)*

**Big-O notation** describes how an algorithm's running time (or
memory) grows with the size of its input, ignoring constant factors and
smaller terms. It answers "what happens when the problem gets 10 times
bigger?", which matters far more than whether one computer is twice as
fast as another. An O(n²) algorithm that's fine for 1,000 items can be
unusable for a million.

Formally, Big-O is an *upper bound*: saying linear search is O(n) means
its worst case grows no faster than *n*. Computer scientists also use
Ω (omega) for lower bounds and Θ (theta) for "exactly this growth", but
everyday programmers say Big-O for all of them, and so does this
course.

`if __name__ == "__main__":` is a standard Python idiom: a file's
`__name__` is `"__main__"` when it's run directly, and the module's
name when it's imported. It lets one file be both a program and a
library of functions.
