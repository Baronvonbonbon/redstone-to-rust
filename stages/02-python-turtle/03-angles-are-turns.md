# Lesson 2.3: Angles Are Turns

**Time:** 45 min · **You need:** Thonny; paper, pencil, and some open floor
space · **New words:** angle, degree, polygon, regular

## Goal *(read this to the learner)*

> Last time, the roof needed a strange number: 120. Today you'll find out
> why, and discover a secret rule that tells you the turn for **any**
> shape: triangles, hexagons, even shapes with 100 sides.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Clear some floor space for walking shapes.
- [ ] Draw this table on paper, with the last two columns empty:

      | Shape | Sides | Turn each time | Sides × turn |
      |---|---|---|---|
      | square | 4 | | |
      | triangle | 3 | | |
      | hexagon | 6 | | |
      | pentagon | 5 | | |
      | octagon | 8 | | |

## Warm-up (5 min)

"Stand up. Turn all the way round, back to where you started. That's 360
**degrees**, a whole turn. Now turn half way (180). Now a quarter (90).
What's three quarters?" *(270.)*

## Activity

1. **Walk the square.** The learner walks a square on the floor and
   counts the turns: 4 turns of 90. **Say:** "When you got back, which way
   were you facing?" *(The same way as at the start.)* "So all your turns
   together made one whole turn. 4 × 90 = 360!"

   Fill in the square's row of the table.

2. **Walk a triangle.** Now an equal-sided triangle. Most people guess 60
   degrees for each turn, because the corners *inside* a triangle are 60.
   Let them try it in Python, in a new file `triangle.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   t.forward(150)
   t.left(60)
   t.forward(150)
   t.left(60)
   t.forward(150)
   t.left(60)

   turtle.done()
   ```
   **They should see:** half a hexagon, not a triangle!

   **Say:** "Interesting! When you walk round the triangle, you end up
   facing the way you started. So the three turns have to add up to a
   whole turn, 360. What number, three times, makes 360?"
   *(120.)* Change the 60s to 120s and run it again.

3. **The turtle turns the outside angle.** On paper, draw a triangle with
   a line sticking out past one corner. Show that the turtle turns the
   *outside* angle (120), not the inside corner (60). The two together
   make a straight line, 180.

4. **Fill in the table.** For each shape, the learner works out the turn
   with the rule "the turns add up to 360", tries it in Python, and fills
   in the row. Each shape is a new program, or they can edit the same one.

   | Shape | Sides | Turn | Sides × turn |
   |---|---|---|---|
   | square | 4 | 90 | 360 |
   | triangle | 3 | 120 | 360 |
   | hexagon | 6 | 60 | 360 |
   | pentagon | 5 | 72 | 360 |
   | octagon | 8 | 45 | 360 |

   **Say:** "Look at the last column. What do you notice?" Let them say it.

5. **The secret rule.** Write it big on paper:

   > **turn = 360 ÷ number of sides**

   **Say:** "Shapes with equal sides and equal corners are called
   **regular polygons**. This rule works for every one of them. And you
   don't have to do the division yourself. Python can do it right inside
   the brackets:"
   ```python
   t.left(360 / 5)
   ```

6. **A 5-pointed star.** **Say:** "A star is a funny one. The turtle
   turns 144 degrees at each point, and it goes round *twice* before it
   faces the start again. 5 × 144 is...?" *(720, which is 2 × 360.)*
   ```python
   t.forward(200)
   t.right(144)
   ```
   Five times. (Right turns work just as well as left ones.)

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The shape doesn't close up | The turns don't add up to 360 | Check the turn with the rule: 360 ÷ sides. |
| The shape goes off the edge of the window | The sides are too long | Use a smaller number in `forward`. |
| A pentagon with 72 looks slightly open | Usually a typing mistake in one of the five turns | Check every line, or count: are there exactly 5 turns? |
| `SyntaxError` on `t.left(360 ÷ 5)` | `÷` isn't a Python symbol | Use `/`. |

## Talk about it

- Why do all the turns add up to 360? *(The turtle ends up facing the
  way it started: one whole turn.)*
- What's the turn for a 10-sided shape? A 360-sided shape? *(36; 1.)*
- What would a 360-sided shape look like? *(Almost a circle.)*

## Challenge *(if there's time, or for next time)*

- Draw a 9-sided shape (a nonagon). What's the turn? *(40.)*
- Draw a 7-sided shape. 360 ÷ 7 doesn't come out evenly, but let Python
  work it out: `t.left(360 / 7)`. Does it close?
- Can you draw a 7-pointed star? *(Hint: try turning `3 * 360 / 7`.)*
- Writing the same two lines eight times for an octagon is boring. Is
  there a better way? (Next lesson!)

## Checkpoint

The learner can, without help:
- [ ] Explain why a square turns 90 and a triangle turns 120
- [ ] Use "turn = 360 ÷ sides" to draw a regular polygon they haven't
      drawn before
- [ ] Use Python to do the division inside `left()`

## Lab notebook

Copy the finished table and the rule "turn = 360 ÷ number of sides". Draw
the triangle with the inside angle and the outside angle marked. Add
*angle*, *degree*, *polygon* and *regular* to the dictionary.

## Guide's background *(optional reading)*

This lesson is a real piece of geometry, discovered by experiment: the
**exterior angles** of any polygon add up to 360°. It's called the
"total turtle trip theorem" in the book *Turtle Geometry* by Abelson and
diSessa. Children often find it easier this way than through the usual
rule about interior angles, because they can feel the turns with their
own body.

The star works because a "star polygon" visits the points in a
different order, so the turtle makes two whole turns instead of one.
In general, the turns add up to 360 × (how many times the turtle goes
round).
