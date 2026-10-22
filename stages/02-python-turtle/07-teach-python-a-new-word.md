# Lesson 2.7: Teach Python a New Word

**Time:** 45 min · **You need:** Thonny; the house plan from Lesson 2.2 ·
**New words:** function, define, call

## Goal *(read this to the learner)*

> Python knows `forward` and `left`, but it doesn't know `house`. Today
> you'll **teach** it. Once Python knows a new word, you can use it as
> often as you like. You'll build a whole street of houses, and it'll
> take you less time than building one did before.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Open the learner's `house.py` from Lesson 2.2 to show them.

## Warm-up (5 min)

"In Stage 0, the robot sandwich: if I said 'make a sandwich', the robot
didn't understand. We had to explain every step. But once the robot knows
how, could we just say 'make a sandwich' next time?" Today, Python learns
new words the same way.

## Activity

1. **Define a new word.** New file, `street.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   def square():
       for i in range(4):
           t.forward(100)
           t.left(90)

   turtle.done()
   ```
   Run it. **They should see:** nothing drawn!

   **Say:** "`def` is short for **define**. We've taught Python what
   `square` means, but we haven't asked it to *do* a square yet.
   Teaching a word isn't the same as using it."

2. **Use the new word.** Add this line just above `turtle.done()` (not
   indented):
   ```python
   square()
   ```
   Run it. A square! **Say:** "Using the word is called **calling** the
   function. The brackets `()` mean 'do it now'."

   Add three more lines to call it again with a turn in between:
   ```python
   t.left(90)
   square()
   t.left(90)
   square()
   ```

3. **Leave the turtle as you found it.** **Say:** "A function is easiest
   to use if the turtle finishes in the **same spot, facing the same
   way**, as when it started. Our `square` does that: it turns four times,
   back to where it began. Let's keep that rule for every function."

4. **A house function.** Replace the square calls with a `house` function,
   based on the plan from Lesson 2.2. Here's one way (bottom left corner,
   facing right):
   ```python
   def house():
       # the walls
       square()
       # climb to the top left corner
       t.left(90)
       t.forward(100)
       t.right(90)
       # the roof
       for i in range(3):
           t.forward(100)
           t.left(120)
       # back down to the start
       t.right(90)
       t.forward(100)
       t.left(90)
   ```
   **Say:** "A function can use another function! `house` uses `square`.
   And the lines starting with `#` are **comments**: notes for humans.
   Python skips them."

   Check: after `house()`, is the turtle back where it started, facing
   right? (Put a `house()` call at the bottom and see.)

5. **A street.** The function's real power:
   ```python
   t.speed(0)
   t.penup()
   t.backward(300)
   t.pendown()

   for i in range(4):
       house()
       t.penup()
       t.forward(150)
       t.pendown()
   ```
   **They should see:** four houses in a row.

   **Say:** "Four houses, and the loop is only four lines long. Because the
   turtle comes back to the start of each house, moving it along for the
   next one is easy."

6. **Make it theirs.** Add a door to `house()` (it then appears on every
   house at once!), or colours with `begin_fill` and `end_fill`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Nothing is drawn | The function is defined but never called | Add `house()` (with brackets) at the bottom, not indented. |
| `NameError: name 'house' is not defined` | The call comes before the `def` | Python reads from top to bottom. Put all the `def`s at the top. |
| `house` with no brackets, and nothing happens | Without `()`, Python only looks at the function, it doesn't run it | Write `house()`. |
| The houses get drawn on top of each other, or crooked | The function doesn't leave the turtle where it found it | Check the last few lines of the function: does the turtle get back to the start, facing right? |
| `IndentationError` | The lines inside the `def` aren't all indented the same | Every line in the function needs one indent; lines in a loop inside it need two. |
| The call is indented, and nothing happens | The call became part of the function | Un-indent the call with Shift+Tab. |

## Talk about it

- What's the difference between defining and calling a function?
  *(Defining teaches Python the word; calling makes it happen.)*
- Why is it useful that `house` leaves the turtle where it started?
  *(You can use it anywhere without working out where the turtle ended up.)*
- If you change the door in `house()`, what happens to the street?
  *(Every house changes.)*

## Challenge *(if there's time, or for next time)*

- Write a function `tree()`: a brown trunk and a green triangle on top.
  Put trees between the houses.
- Write a function `star()` and draw a night sky above the street.
- A function `creeper_face()`.

## Checkpoint

The learner can, without help:
- [ ] Define a function with `def` and call it with `()`
- [ ] Explain why a function that does nothing until it's called is useful
- [ ] Write a function that leaves the turtle where it started
- [ ] Use a function inside a loop

## Lab notebook

Draw the street. Copy the `house()` function, and next to it write in
words what each part does. Add *function*, *define*, *call* and *comment*
to the dictionary.

## Guide's background *(optional reading)*

A **function** is a named list of instructions. It's the most important
tool for managing big programs: you break a hard problem into smaller
named pieces, solve each once, then use them as building blocks. Real
programs are made of thousands of functions calling each other.

The rule "leave the turtle where you found it" is what Logo programmers
call a **state-transparent** procedure. It's a nice, gentle introduction
to a habit that matters in all programming: a function should do what its
name says and avoid surprising side effects.

Comments (`#`) help the reader understand *why* code is written the way
it is. Encourage a few of them; the main reader of a comment is usually
the same person, a week later.
