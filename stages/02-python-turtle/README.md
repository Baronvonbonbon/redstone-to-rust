# Stage 2: Python Turtle

**Badge:** Turtle Tamer · **Needs first:** Stage 1; adding and subtracting
within 1000 · **Lessons:** 14

The learner writes real programs for the first time, in Python, using the
**turtle**: a little robot that draws as it moves. It's the Stage 0 floor
robot (forward, left, right) brought back as code. Along the way they
meet the core ideas of every programming language: instructions,
**loops**, **variables**, **functions**, **parameters**, randomness and
decisions. The math thread is strong here: angles, polygons, coordinates,
negative numbers, and multiplication as rectangles.

> **Status:** lesson list and plan below; full lesson scripts are coming.
> Until then, each lesson names its source and what to do. Write every
> program in **Thonny**, which is beginner-friendly, shows variables as
> they change, and has a step-by-step debugger.

## Tools

- **Thonny** (installed by setup): Super key, then type `thonny`. Use
  **View → Variables** to watch boxes change.
- Python's built-in `turtle` module. It's offline; `help("turtle")` or
  `python3 -m pydoc turtle` shows its manual.
- Reference: OpenStax *Introduction to Python Programming*, Chapters 1–5
  (the guide's reference; the learner reads selected parts).

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 2.1 | Hello, Python | Thonny tour; `print("hi")`; Python as a calculator (`7 * 8`, `2 ** 10`, `17 // 5`, `17 % 5`); the shell vs the editor; save `hello.py` in `~/lab/python` | program, print, operators |
| 2.2 | Meet the Turtle | `import turtle`, `t = turtle.Turtle()`, `forward`, `left`, `right`; draw a square, then a house | instructions in order |
| 2.3 | Angles Are Turns | Why a square turns 90°; triangle (120°), hexagon (60°); discover "360 ÷ number of sides" | angles, the 360 rule |
| 2.4 | Do It Again | `for i in range(4):`; indentation; shorten 2.3's shapes; a 36-sided "circle" | loops, indentation |
| 2.5 | Labelled Boxes | Variables: `size = 100`, `sides = 6`; change one number and the whole drawing changes | variables, `=` means "put in the box" |
| 2.6 | Colours and Pens | `pencolor`, `fillcolor`, `begin_fill`/`end_fill`, `pensize`, `speed`, `penup`/`pendown` | the turtle's state |
| 2.7 | Teach Python a New Word | `def square():` ... and call it; build a street of houses | functions |
| 2.8 | Functions with Knobs | `def polygon(sides, size):`; draw every shape from 3 to 10 sides in a loop | parameters, arguments |
| 2.9 | Numberblocks Builder | Draw numbers as stacks of blocks; draw `3 × 4` as a rectangle of 12 blocks; a times-table poster | nested loops, multiplication |
| 2.10 | The Map of the Screen | `goto(x, y)`, x and y, the centre is (0, 0); negative numbers; plot points | coordinates |
| 2.11 | Random Art | `import random`, `random.randint`, `random.choice` of colours; confetti and random walks | randomness, modules |
| 2.12 | Ask and Decide | `input()`, `int()`, `if`/`elif`/`else`; "how many sides?"; a polygon quiz | input, conditions, types |
| 2.13 | Spirals and Patterns | A loop where the size grows each time; spirographs; flowers from rotated squares | changing variables in loops |
| 2.14 | Project: My Art Gallery | Plan, build and present a gallery of 3 drawings using functions, loops and randomness; save it in `~/lab/python/gallery/` | putting it together |

## Free play for this stage

- Turtle drawing, any time. Keep a "best drawings" folder.
- Typing games and Stage 1 terminal games.
- Bashcrawl, if it's not finished.

## Habits to build now

- Save programs in `~/lab/python/`, with good names (`spiral.py`, not
  `untitled1.py`).
- Run programs from the terminal too: `cd ~/lab/python` then
  `python3 spiral.py`. This connects Stage 1 and Stage 2.
- When there's an error, **read the last line of the red text first**.
  The line number tells you where to look.

## Checkpoint

The learner can, without help, write a program that:
- [ ] Uses a `for` loop to draw a regular polygon, with the turn worked
      out from the number of sides
- [ ] Defines a function with at least two parameters, and calls it
      several times
- [ ] Asks the user a question and does something different depending
      on the answer
- [ ] Uses `random` to change something each time it runs

They can also:
- [ ] Explain a variable, a loop and a function in their own words
- [ ] Read a Python error message and find the line it's about
