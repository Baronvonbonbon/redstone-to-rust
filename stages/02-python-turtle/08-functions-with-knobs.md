# Lesson 2.8: Functions with Knobs

**Time:** 45 min · **You need:** Thonny · **New words:** parameter,
argument

## Goal *(read this to the learner)*

> Your `square()` always draws the same size of square. What if you want
> a small one and a big one? Today you'll give functions **knobs** that
> you can turn each time you use them. By the end, one function will draw
> *every* shape there is.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"What's the difference between defining a function and calling it?
What does `t.forward(100)` do, and what does the 100 do?" *(The 100 says
how far.)* "So `forward` has a knob! Today we make our own."

## Activity

1. **A square with a knob.** New file, `knobs.py`:
   ```python
   import turtle

   t = turtle.Turtle()
   t.shape("turtle")

   def square(size):
       for i in range(4):
           t.forward(size)
           t.left(90)

   square(50)
   square(100)
   square(150)

   turtle.done()
   ```
   **They should see:** three squares of different sizes, sharing a
   corner.

   **Say:** "`size` in the brackets of the `def` is the knob. It's called
   a **parameter**. When we call `square(50)`, Python puts 50 in the
   `size` box, then runs the function. Next time, `square(100)` puts 100
   in the box. The number we give it is called an **argument**."

2. **Watch it happen.** In Thonny, use **View → Variables**. Then click
   the little bug button (**Debug current script**), and press **F7**
   (*step into*) again and again. Thonny highlights each step and shows
   `size` getting its value each time `square` is called. Stop with the
   red stop button when they've seen enough.

3. **Two knobs.** Replace `square` with a function for any shape:
   ```python
   def polygon(sides, size):
       for i in range(sides):
           t.forward(size)
           t.left(360 / sides)
   ```
   And call it:
   ```python
   polygon(3, 100)
   polygon(6, 60)
   polygon(10, 30)
   ```
   **Say:** "Two knobs, separated by a comma. The order matters: the first
   number goes in `sides`, the second in `size`. What would
   `polygon(100, 3)` do?" *(100 tiny sides: a little circle.)* Try it.

4. **Every shape from 3 to 10 sides.** Replace the calls with a loop:
   ```python
   t.speed(0)
   for sides in range(3, 11):
       polygon(sides, 60)
   ```
   **They should see:** a triangle, square, pentagon and so on up to a
   decagon, all sharing one corner, like a flower.

   **Say:** "`range(3, 11)` counts from 3 up to 10. It stops just
   *before* 11, the same way `range(4)` stops before 4. And look, the
   loop's counter is called `sides`, and we pass it straight into the
   knob."

5. **A colour knob.** Add a third parameter:
   ```python
   def polygon(sides, size, colour):
       t.pencolor(colour)
       for i in range(sides):
           t.forward(size)
           t.left(360 / sides)

   polygon(5, 100, "blue")
   polygon(8, 50, "red")
   ```
   Note that the old calls with two arguments now give an error (see the
   table). Update them or delete them.

6. **Upgrade the street.** Back in `street.py` (Lesson 2.7), give `house`
   a `size` parameter, so the street has small and big houses:
   `house(50)`, `house(100)`. Every `100` inside `house()` becomes `size`,
   and `square()` needs a `size` too.

   This is a good, real challenge. Let them work through it, using the
   error messages.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `TypeError: square() missing 1 required positional argument: 'size'` | Called `square()` without a number | Give it one: `square(100)`. |
| `TypeError: polygon() takes 2 positional arguments but 3 were given` | Too many arguments for the knobs | Count the knobs in the `def`, and give exactly that many. |
| `NameError: name 'size' is not defined` | Used `size` outside the function, or forgot to put it in the `def` brackets | Parameters only exist inside their function. Add it to the `def` line. |
| The shape is strangely huge or tiny | The arguments are in the wrong order | Check the `def`: which knob comes first? |
| `TypeError: 'float' object cannot be interpreted as an integer` | `range` got a decimal number, like `polygon(5.0, 100)` | Use a whole number for `sides`. |

## Talk about it

- What's a parameter? What's an argument?
  *(A parameter is the knob's name in the `def`; an argument is the value
  you turn it to when you call it.)*
- Why does `range(3, 11)` stop at 10?
- Why is `polygon(sides, size)` better than writing `triangle()`,
  `square()`, `hexagon()` and so on? *(One function does them all.)*

## Challenge *(if there's time, or for next time)*

- Draw 20 squares, each one 10 bigger than the last, in a loop:
  `square(i * 10)`. What does it look like?
- Write `star(size)`. Then draw stars of different sizes in a night sky.
- Write `polygon_flower(sides)` that draws the same polygon 12 times,
  turning 30 degrees between each.

## Checkpoint

The learner can, without help:
- [ ] Define a function with two or more parameters and call it with
      arguments
- [ ] Explain parameter and argument in their own words
- [ ] Use `range(start, stop)` and explain why it stops before `stop`
- [ ] Read a `TypeError` about missing or extra arguments and fix it

## Lab notebook

Copy `polygon(sides, size)`. Draw the 3-to-10 flower. Draw a picture of a
function as a machine with knobs on top: the knob names are parameters,
and the numbers you set them to are arguments. Add *parameter* and
*argument* to the dictionary.

## Guide's background *(optional reading)*

Parameters turn a function from "always does the same thing" into a
general tool. `polygon(sides, size)` captures the rule the learner
discovered in Lesson 2.3 in one place, and it works for every regular
polygon. Spotting the parts of a problem that change, and turning them
into parameters, is one of the main skills of programming.

Thonny's debugger (the bug button, then **F6** to step over a line and
**F7** to step into a function) is worth getting comfortable with now.
It shows the program running slowly, one step at a time, with every
variable visible. It's the best tool there is for understanding why a
program does what it does.
