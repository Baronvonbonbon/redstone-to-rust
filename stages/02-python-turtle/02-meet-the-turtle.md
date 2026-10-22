# Lesson 2.2: Meet the Turtle

**Time:** 45 min · **You need:** Thonny · **New words:** module, import,
turtle, method

## Goal *(read this to the learner)*

> Remember being the robot, back in Stage 0, walking across the floor
> with "forward", "turn left" and "turn right"? Python has a robot like
> that, called the **turtle**. It carries a pen, so it draws as it walks.
> Today you'll make it draw a square, and then a house.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Have paper and a pencil ready for planning the house.
- [ ] **Important:** never let the learner name a file `turtle.py`. It
      breaks every turtle program in that folder (see the table below).

## Warm-up (5 min)

"In the Shell, what's `17 % 5`? What does `%` mean? How do you run a
program in Thonny?" *(2; the remainder; F5 or the green button.)*

## Activity

1. **Wake the turtle up, in the Shell.** Type each line and press Enter:
   ```python
   import turtle
   t = turtle.Turtle()
   ```
   **They should see:** a new window open, with a little arrow in the
   middle. That's the turtle, facing right.

   **Say:** "`import turtle` fetches the turtle toolbox. Python comes
   with lots of toolboxes, called **modules**, and you only unpack the
   ones you need. The second line makes a turtle and calls it `t`, so
   we can give it orders."

   Move the turtle window and Thonny so they can see both at once.

2. **Make it move.**
   ```python
   t.forward(100)
   ```
   **They should see:** the arrow move right, drawing a line.

   **Say:** "100 is how many steps. Each step is one tiny dot on the
   screen, called a **pixel**. Remember those from the pixel pictures?"

   Then:
   ```python
   t.left(90)
   t.forward(100)
   ```
   **Say:** "`left(90)` turns the turtle on the spot. It doesn't move or
   draw. 90 is how far it turns, in **degrees**. A quarter turn is 90."

3. **Finish the square.** Let the learner work out the rest themselves.
   They need two more `left(90)` and `forward(100)` pairs, and one last
   `left(90)` to face the start direction again.

   If they're stuck, act it out: the learner stands up and walks a square
   on the floor, counting the turns.

4. **Make the turtle look like a turtle.**
   ```python
   t.shape("turtle")
   ```
   Much better. Now some others:
   ```python
   t.right(45)
   t.backward(50)
   ```

5. **Start again.** Close the turtle window. In the Shell:
   ```python
   t = turtle.Turtle()
   ```
   If this gives an error (`Terminator`), just type it a second time.
   **Say:** "Closing the window ends that turtle. Making a new one opens
   a fresh window."

6. **Now as a program.** Click in the editor and type:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   t.forward(100)
   t.left(90)
   t.forward(100)
   t.left(90)
   t.forward(100)
   t.left(90)
   t.forward(100)
   t.left(90)

   turtle.done()
   ```
   Save it as `~/lab/python/square.py` and press F5.

   **Say:** "The last line, `turtle.done()`, means 'keep the window open
   until I close it'. Every turtle program ends with it. Without it,
   when you run the program from the terminal, the window disappears as
   soon as the drawing is finished."

7. **Plan a house on paper.** A house is a square with a triangle on top.
   **Say:** "Draw it on paper first, and mark where the turtle starts and
   which way it faces. Then write the turtle's instructions next to the
   picture, in order."

   A simple plan (starting at the bottom left corner, facing right):
   - the square: 4 × (forward 100, left 90)
   - move up to the top left corner: left 90, forward 100, right 90
   - the roof: forward 100, left 120, forward 100, left 120, forward 100

   Don't worry if they don't know why 120 yet. That's the next lesson!
   Let them try their own angles first, and be pleased with roofs that
   don't quite close.

8. **Build `house.py`.** A new file (Ctrl+N), the same three start lines
   (`import turtle`, `t = turtle.Turtle()`, `t.shape("turtle")`), their
   plan, and `turtle.done()` at the end. Save it in `~/lab/python/` and
   run it. Fix it, run it again, and keep going until the house looks
   right.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `AttributeError: module 'turtle' has no attribute 'Turtle'` (or `partially initialized module 'turtle'`) | There's a file called `turtle.py` in the folder, and Python opened it instead of the real turtle | Rename that file (for example to `my-turtle.py`) and delete any `__pycache__` folder next to it. Never call a file `turtle.py`. |
| `turtle.Terminator` (or `TclError: invalid command name`) | The turtle window was closed while the turtle was still drawing, or before making a new turtle | Run the program again (or type the line again in the Shell). |
| `NameError: name 't' is not defined` | The line `t = turtle.Turtle()` is missing or comes too late | Put it near the top, after `import turtle`. |
| `NameError: name 'turtle' is not defined` | `import turtle` is missing | Add it as the first line. |
| `AttributeError: 'Turtle' object has no attribute 'foward'` | A spelling mistake | Check the spelling: `forward`. |
| `ModuleNotFoundError: No module named 'tkinter'` | The turtle's drawing window isn't installed | The guide runs `sudo apt install python3-tk` (setup normally does this). |
| The window opens and vanishes straight away | `turtle.done()` is missing | Add it as the last line. |

## Talk about it

- What does `import` do? *(Fetches a module, a toolbox of extra commands.)*
- The turtle does *exactly* what you say. Where else have you seen that?
  *(The robot sandwich, and the terminal.)*
- Why plan on paper first? *(It's much easier to fix a drawing than a
  program, and you can see where the turtle should be.)*

## Challenge *(if there's time, or for next time)*

- Add a door and a window to the house.
- Draw the first letter of your name.
- Draw a staircase: forward, left, forward, right, again and again.

## Checkpoint

The learner can, without help:
- [ ] Start a turtle program with `import turtle` and `t = turtle.Turtle()`
- [ ] Draw a square using `forward` and `left`
- [ ] End a program with `turtle.done()`, and explain why
- [ ] Plan a drawing on paper before writing it

## Lab notebook

Draw the house, with the turtle's starting arrow and the instructions
next to each line. Add *module*, *import*, *pixel* and *degree* to the
dictionary.

## Guide's background *(optional reading)*

Turtle graphics come from a language called Logo, made in the 1960s by
Seymour Papert and others to help children learn maths by programming.
The early turtles were real robots that crawled on paper with a pen.

`t.forward(100)` is a **method call**: `t` is the turtle, and `forward`
is something a turtle knows how to do. The dot means "the thing on the
left does the action on the right". `turtle.Turtle()` (capital T) is a
recipe for making turtles; you could make two, called `t` and `u`, and
they'd draw separately.

The "`turtle.py`" trap catches almost every beginner. When Python runs
`import turtle`, it looks in the program's own folder first, so a file
with the same name hides the real module.
