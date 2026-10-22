# Lesson 2.14: Project: My Art Gallery (Stage 2 Checkpoint)

**Time:** 3–4 sessions of 45 min, plus the checkpoint on a separate day ·
**You need:** Thonny; paper and coloured pencils; an audience for the
opening (family, friends, a video call with grandparents) · **New words:**
project, plan, menu

## Goal *(read this to the learner)*

> You're going to open your own art gallery! Your program will show a
> menu of at least three pictures, and draw whichever one the visitor
> chooses. You'll plan it, build it, test it, and then hold a grand
> opening. When it's finished, you'll be an official **Turtle Tamer**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Make the folder: `mkdir -p ~/lab/python/gallery`
- [ ] Print or copy out the requirements list below.
- [ ] Agree a date for the grand opening, so there's a goal.

## The requirements

The gallery program must:
1. Have **at least three pictures**, each one in its own **function**.
2. Have at least one function with **two or more parameters**.
3. Use **loops** (at least one).
4. Use **randomness** somewhere, so it's a little different each time.
5. Show a **menu** and ask the visitor which picture they want, using
   `input` and `if`/`elif`/`else`.
6. Do something sensible if the visitor types something that isn't on
   the menu.
7. Be saved as `~/lab/python/gallery/gallery.py`, and run from the
   terminal with `python3 gallery.py`.

## Activity

### Session 1: plan

1. **Ideas.** **Say:** "Look back through your lab notebook and your
   `~/lab/python` folder. Which drawings were your favourites? What would
   you like to draw that you haven't yet?" Ideas: a street at night, a
   Numberblocks family, a Minecraft scene (blocks, a creeper, a sword), a
   rocket launch, a firework display, a spiral galaxy, a fish tank, a
   pixel portrait.

2. **Plan each picture on paper.** For each one:
   - draw it, with the turtle's starting spot and coordinates marked;
   - name its function (like `night_street`);
   - write down which earlier functions it will use (like `house`,
     `polygon` or `block`);
   - write what's random about it.

   **Say:** "Big programs are built from small pieces. Which pieces do
   you already have?"

### Sessions 2 and 3: build

3. **Start from this skeleton.** Copy in any functions they need from
   earlier programs (`polygon`, `block`, `house`...).
   ```python
   import turtle
   import random

   turtle.setup(800, 600)
   t = turtle.Turtle()
   t.speed(0)

   # --- tools ---

   def polygon(sides, size):
       for i in range(sides):
           t.forward(size)
           t.left(360 / sides)

   # --- pictures ---

   def picture_one():
       polygon(6, 100)

   def picture_two():
       polygon(3, 100)

   def picture_three():
       polygon(8, 60)

   # --- the gallery ---

   print("Welcome to my gallery!")
   print("1: My first picture")
   print("2: My second picture")
   print("3: My third picture")

   choice = input("Which picture would you like to see? ")

   if choice == "1":
       picture_one()
   elif choice == "2":
       picture_two()
   elif choice == "3":
       picture_three()
   else:
       print("Sorry, that picture isn't in the gallery.")

   turtle.done()
   ```
   Run it once before changing anything, to check it works.

   **Say:** "Notice we compare the choice with `"1"`, in quote marks, not
   `1`. `input` gives us words, so we compare with words. That way, if a
   visitor types `banana`, there's no error: it just isn't on the menu."

4. **Build one picture at a time.** Replace `picture_one` with their first
   real picture, run it, fix it, and only then move on to the next. Change
   the menu names to match.

   **Say:** "Build a little, test a little. If you write everything and
   then run it, and there are ten mistakes, it's much harder to find them."

   Your job as guide is mostly to ask questions: "What should happen
   next? What does the error's last line say? Which line is it about?"
   Use the stuck ladder from the [Guide's Handbook](../../docs/GUIDE.md).

5. **Test it like a visitor.** When all three work: run it and choose
   each picture. Then try `4`, `banana`, and just pressing Enter. Does the
   program cope with all of them?

### Session 4: polish and open

6. **Polish.** Ideas, if there's time:
   - a title written on each picture with `t.write`;
   - `t.hideturtle()` when each picture is finished;
   - a fourth picture, maybe a "surprise" one that picks one of the others
     at random: `random.choice([picture_one, picture_two, picture_three])()`;
   - run it from the terminal: `cd ~/lab/python/gallery` then
     `python3 gallery.py`.

7. **The grand opening.** The learner runs the gallery for an audience,
   explains how one of the pictures works (showing the code), and takes
   requests. Visitors can sign a "guest book" page in the lab notebook.

## The Stage 2 checkpoint

On a separate day, with no help (the learner may look at their own old
programs and notebook, but not copy whole programs):

1. Write a program that asks "How many sides?" and draws that regular
   polygon, with a `for` loop and the turn worked out with 360 ÷ sides.
2. If the answer is less than 3, it prints a message instead of drawing.
3. Write a function `flower(petals, size)` that draws `petals` circles
   (or squares) rotated round a point, and call it twice with different
   arguments.
4. Make something in the program random (a colour, a size, a position).
5. Explain, in their own words: a variable, a loop, and a function.
6. The guide puts a mistake into one of their programs (a missing `:`, a
   misspelled name, or a missing bracket). The learner runs it, reads the
   error, finds the line, and fixes it.

All done means **Turtle Tamer!** Sign and stamp the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Choosing `1` prints "Sorry, that picture isn't in the gallery." | Comparing with the number `1` instead of the string `"1"` | Use quote marks: `if choice == "1":`. |
| Pictures draw on top of each other | Two pictures called, or one picture doesn't clean up | Each choice should call only one picture. Use `t.clear()` to start fresh. |
| A picture is half off the screen | The coordinates are bigger than the window | Keep x between -400 and 400, and y between -300 and 300. |
| `NameError` for a function | The function is defined lower down than where it's called, or spelled differently | Put all `def`s above the menu, and check spelling. |
| The learner is frustrated after a long stuck patch | Normal for a first project | Take a break. Then shrink the problem: get one simple version working first, then add to it. |
| The learner wants ten pictures | Brilliant, but a big project | Finish three, open the gallery, and then add more as "new exhibitions". |

## Talk about it

- Which picture was hardest to make? What was the hardest bug?
- Which earlier functions did you reuse? How much time did that save?
- If you made a gallery 2.0, what would you add?

## Checkpoint

The learner can, without help:
- [ ] Plan a program on paper before writing it
- [ ] Build a program one piece at a time, testing as they go
- [ ] Use functions, parameters, loops, randomness, input and decisions
      together in one program
- [ ] Pass the Stage 2 checkpoint above

## Lab notebook

Glue in the paper plans. Write "What I'm proud of" and "What I'd do
differently next time". Keep the guest book page.

## Guide's background *(optional reading)*

This is the learner's first **project**: a program they designed, rather
than one they followed. The habits matter more than the result: plan on
paper, build a small piece, test it, then add the next piece. Professional
programmers work exactly like this (they call it *incremental
development*), because finding one fresh bug is easy and finding ten old
ones at once is hard.

Comparing `choice` with strings (`"1"`) rather than converting it with
`int()` is a deliberate design choice: it means bad input can't crash
the program. This is the learner's first taste of **defensive
programming**: assuming users will type unexpected things, because they
always do.

After this stage, the learner moves on to Stage 3: Python Games &
Puzzles, which brings in lists, text adventures, and Pygame Zero.
