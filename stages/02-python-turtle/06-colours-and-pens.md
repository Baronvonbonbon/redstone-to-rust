# Lesson 2.6: Colours and Pens

**Time:** 45 min · **You need:** Thonny · **New words:** state, fill, pen up,
pen down

## Goal *(read this to the learner)*

> Black lines are a bit boring. Today your turtle gets a whole box of
> felt-tip pens: colours, thick lines, filled-in shapes, a background,
> and the power to lift its pen and move without drawing. You'll make a
> colourful picture of your own.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"What's a variable? What would happen if I changed `sides = 6` to
`sides = 4` in `any-shape.py`?" *(A labelled box; it would draw a square.)*

## Activity

Work in a new file, `colours.py`, adding a few lines at a time and running
it each time. Start with:
```python
import turtle

t = turtle.Turtle()
t.shape("turtle")

turtle.done()
```
All the new lines go between `t.shape("turtle")` and `turtle.done()`.

1. **Pen colour and size.**
   ```python
   t.pencolor("red")
   t.pensize(5)
   t.forward(100)
   ```
   **Say:** "The turtle remembers its pen colour and size until you change
   them. That's its **state**, like the things a Minecraft player is
   holding." Change the colour and draw another line.

   Colour names to try: `red`, `orange`, `yellow`, `gold`, `green`, `blue`,
   `purple`, `pink`, `brown`, `black`, `white`, `gray`, `cyan`, `magenta`,
   `navy`, `turquoise`, `violet`, `skyblue`, `limegreen`.

2. **Speed.**
   ```python
   t.speed(1)
   ```
   **Say:** "`1` is slowest and `10` is fast. `0` is a special one: as fast
   as possible." Try a few.

3. **Background.**
   ```python
   turtle.bgcolor("black")
   ```
   **Say:** "This one starts with `turtle.`, not `t.`, because the
   background belongs to the whole window, not to one turtle."

4. **Filled shapes.**
   ```python
   t.fillcolor("yellow")
   t.begin_fill()
   for i in range(4):
       t.forward(100)
       t.left(90)
   t.end_fill()
   ```
   **They should see:** a square that fills in yellow when it's finished.

   **Say:** "`begin_fill` means 'start remembering the shape', and
   `end_fill` means 'now colour it in'. The shape needs to be closed, or
   the fill looks strange."

   `t.color("red", "yellow")` sets both colours at once: the pen, then the fill.

5. **Pen up, pen down.**
   ```python
   t.penup()
   t.forward(150)
   t.pendown()
   ```
   **Say:** "With the pen up, the turtle moves without drawing, like
   lifting your pencil off the page. Don't forget to put it down again!"

6. **Hide the turtle.** At the end, before `turtle.done()`:
   ```python
   t.hideturtle()
   ```
   Now the picture is finished, without the turtle sitting on it.

7. **Free design.** The learner designs a picture on paper and builds it:
   a flag, a traffic light, a creeper face (a green square with black
   squares for eyes and mouth), a Minecraft block, or anything they like.
   Save it as `~/lab/python/my-picture.py`.

   Encourage them to use loops and variables from earlier lessons, and to
   run the program after every few lines.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `turtle.TurtleGraphicsError: bad color string: redd` | A colour name it doesn't know, often a spelling mistake | Check the spelling against the list above. Write two-word colours as one word: `"darkgreen"`. |
| The fill doesn't appear | `end_fill()` is missing | Add `t.end_fill()` after the shape. |
| The fill looks like a strange triangle | The shape wasn't closed, or there's a `penup` move inside the fill | Finish the whole shape between `begin_fill` and `end_fill`, with no jumps. |
| Nothing is drawn any more | The pen is still up | Add `t.pendown()`. |
| `AttributeError: 'Turtle' object has no attribute 'bgcolor'` | Wrote `t.bgcolor` | Use `turtle.bgcolor(...)`. |
| `turtle.bgcolor("black")` and the lines vanish | Black pen on a black background | Change the pen colour. |

## Talk about it

- What's the turtle's "state"? What can it remember?
  *(Its position, which way it faces, pen up or down, pen colour, pen
  size, fill colour, speed.)*
- Why do we need `begin_fill` *and* `end_fill`? *(The turtle needs to know
  where the shape starts and ends before it can colour it in.)*
- Why would someone use `penup`? *(To move to a new spot without a line.)*

## Challenge *(if there's time, or for next time)*

- Colours can also be made from numbers. `t.pencolor("#FF8800")` is
  orange: red FF, green 88, blue 00. Each pair goes from `00` (none) to
  `FF` (full). This is the same counting system as the pixel pictures,
  called **hexadecimal**. Try making purple.
- Draw a row of 6 filled squares in rainbow colours. *(Hint: penup and
  forward between them.)*

## Checkpoint

The learner can, without help:
- [ ] Change pen colour, pen size, and speed
- [ ] Draw a filled shape with `begin_fill` and `end_fill`
- [ ] Move without drawing using `penup` and `pendown`
- [ ] Plan and build their own coloured picture

## Lab notebook

Glue in or draw the plan for `my-picture.py`. Make a list called "The
turtle's state" with everything the turtle remembers. Add *state*, *fill*,
*pen up* and *pen down* to the dictionary.

## Guide's background *(optional reading)*

The turtle is a small example of an important idea: an **object** with
**state**. The turtle remembers things about itself (where it is, its pen
colour and so on), and every command either changes that state or uses
it. This is how most programs model things: a Minecraft player is an
object with health, a position and an inventory.

Colour names come from an old list used by Unix graphics (the "X11
colour names"); there are several hundred of them. The `#RRGGBB` codes
are used everywhere: in web pages, in drawing apps and in game files.
They're a gentle first look at hexadecimal, which returns properly in
Stage 4.
