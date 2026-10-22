# Lesson 2.5: Labelled Boxes

**Time:** 45 min · **You need:** Thonny; a few small boxes or cups, sticky
notes, and slips of paper · **New words:** variable, value, assign

## Goal *(read this to the learner)*

> What if you want your octagon bigger? You'd have to find every number
> and change it. Today you'll learn **variables**: labelled boxes that
> hold a number. Change what's in the box, and the whole drawing changes
> at once.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Put a sticky-note label on two boxes or cups: `size` and `sides`.

## Warm-up (5 min)

"Write a loop that draws a hexagon. What numbers did you need?"
*(6 for the loop, 60 for the turn, and a length.)*

## Activity

1. **Boxes on the table.** Write `100` on a slip of paper and put it in
   the box labelled `size`. **Say:** "In Python, we'd write this as
   `size = 100`. The `=` doesn't mean 'equals' like in maths. It means
   **put this in the box**." Ask: "What's in `size`?" They look in the
   box: 100.

   Now take the slip out, write `50` on a new one, and put that in.
   **Say:** "`size = 50`. A box only holds one thing at a time, so the
   old 100 is gone."

2. **Boxes in the Shell.**
   ```python
   size = 100
   size
   size * 2
   size = 50
   size
   ```
   **They should see:** `100`, `200`, then `50`.

   **Say:** "Python remembers what's in the box. Whenever you use the
   name, Python looks inside and uses what it finds there."

3. **Boxes can hold words too.**
   ```python
   name = "Steve"
   print("Hello", name)
   ```
   (They pick any name: theirs, a pet's, a Minecraft character's.)

4. **A box that changes itself.**
   ```python
   score = 0
   score = score + 10
   score = score + 10
   score
   ```
   **They should see:** `20`.

   **Say:** "Read `score = score + 10` from the right: 'look in the
   `score` box, add 10, and put the answer back in the `score` box.'"
   Act it out with the real box. In maths, `score = score + 10` would be
   impossible. In Python, it's how you keep score.

5. **A drawing with knobs.** New file, `any-shape.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   sides = 6
   size = 80

   for i in range(sides):
       t.forward(size)
       t.left(360 / sides)

   turtle.done()
   ```
   Run it: a hexagon.

   **Say:** "Now change only the first number, `sides = 6`, to 5. Run
   it." A pentagon. "Change it to 3." A triangle. "One number changes
   everything, because the loop and the turn both look in the same box."

   Let them play: 10 sides with size 40, 20 sides with size 20.

6. **Watch the boxes in Thonny.** Click **View → Variables**. A panel
   opens showing every box and what's inside. Run the program again and
   point out `sides`, `size` and `i`.

   **Say:** "Look, `i` is a box too! The loop puts 0 in it, then 1, then
   2... that's how it counts."

7. **Good names.** **Say:** "Box names can be long, like
   `number_of_sides`, but they can't have spaces, can't start with a
   number, and capitals matter: `Size` and `size` are different boxes.
   Choose names that say what's inside. `x` is a bad name for the number
   of sides; `sides` is a good one."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `NameError: name 'size' is not defined` | Using a box before putting anything in it (or a spelling mismatch) | Make sure `size = ...` comes *before* it's used, and the spelling matches exactly. |
| `NameError: name 'Sides' is not defined. Did you mean: 'sides'?` | Capitals don't match | Use the same capitals everywhere. Python even suggests the fix! |
| `SyntaxError: cannot assign to literal` | Written backwards, like `100 = size` | The box name goes on the left: `size = 100`. |
| `SyntaxError: invalid syntax` on `number of sides = 6` | Spaces in a name | Use `number_of_sides` with underscores. |
| `TypeError: 'float' object cannot be interpreted as an integer` | `range` was given a number with a decimal point, like `range(360 / 60)` | `range` needs a whole number. Use `//` instead of `/`, or put the whole number in. |

## Talk about it

- What does `=` mean in Python? *(Put the value on the right into the
  box on the left.)*
- What does `score = score + 1` do? *(Adds one to the score.)*
- Why is `sides` a better name than `s`?

## Challenge *(if there's time, or for next time)*

- Add a box called `turn` that holds `360 / sides`, and use it in the loop.
- Make `size` depend on `sides`, so big shapes always fit:
  `size = 300 / sides`.
- In the Shell: `a = 5`, `b = a`, `a = 7`. What's in `b` now? Guess first.
  *(5: `b` got a copy of what was in `a` at the time.)*
- Swap two boxes: start with `a = 1` and `b = 2`, and end with `a`
  holding 2 and `b` holding 1. *(Hint: you need a third box.)*

## Checkpoint

The learner can, without help:
- [ ] Explain a variable as a labelled box, and `=` as "put in the box"
- [ ] Use variables for the number of sides and the size of a shape
- [ ] Change one variable to change the whole drawing
- [ ] Use Thonny's Variables panel to see what's in each box

## Lab notebook

Draw two labelled boxes, `sides` and `size`, with numbers in them. Copy
`any-shape.py`. Write a table of three shapes it can draw, and what
`sides` and `size` were. Add *variable*, *value* and *assign* to the
dictionary.

## Guide's background *(optional reading)*

A **variable** is a name for a value stored in the computer's memory. The
"labelled box" picture is close enough to be really useful at this stage.
(The full truth, that a Python name is more like a label tied to a value,
matters later, in Stage 3, when lists come in.)

The single biggest confusion for beginners is that `=` is not the `=` of
maths. In Python it's an action, called **assignment**, which happens at
one moment, and the box keeps its value until something else is put in.
Python uses `==` (two equals signs) for "are these equal?", which comes
in Lesson 2.12.

Variables are what make one program draw many different pictures. This
is the first step towards **abstraction**: writing something once, in a
general way, so it can be used for many cases.
