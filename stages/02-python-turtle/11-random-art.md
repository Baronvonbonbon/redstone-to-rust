# Lesson 2.11: Random Art

**Time:** 45 min · **You need:** Thonny; a dice · **New words:** random,
module, list (sneak peek)

## Goal *(read this to the learner)*

> So far, your programs draw the same picture every time. Today you'll
> give them a dice to roll. Every time you run them, they'll do something
> different: confetti, a wandering mob, a night sky. Even you won't know
> exactly what's coming!

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] **Never let the learner name a file `random.py`.** Like `turtle.py`,
      it hides the real module.

## Warm-up (5 min)

Roll the dice a few times. "Can you guess the next number? Can a program
roll a dice? A computer does *exactly* what it's told, so how can it ever
be random?" Leave the question hanging; there's an answer in the guide's
background.

## Activity

1. **A dice in Python.** In the Shell:
   ```python
   import random
   random.randint(1, 6)
   random.randint(1, 6)
   random.randint(1, 6)
   ```
   **They should see:** numbers between 1 and 6, different (usually) each
   time. Press the up arrow to bring the line back, then Enter.

   **Say:** "`random` is another module, a toolbox for chance. `randint`
   means 'random whole number' (an **int**eger). Careful: `randint(1, 6)`
   includes 6, but `range(1, 6)` stops before 6. Different tools have
   different rules, so it's worth checking."

   Try `random.randint(1, 100)` and `random.randint(-10, 10)`.

2. **Pick one from a list.**
   ```python
   random.choice(["rock", "paper", "scissors"])
   random.choice(["red", "orange", "yellow", "green", "blue", "purple"])
   ```
   **Say:** "Things in square brackets, separated by commas, are a
   **list**. `choice` picks one, like pulling a name out of a hat. We'll
   do much more with lists in Stage 3."

3. **Confetti.** New file, `confetti.py`:
   ```python
   import turtle
   import random

   turtle.setup(800, 600)
   t = turtle.Turtle()
   t.speed(0)
   t.hideturtle()
   t.penup()

   colours = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

   for i in range(200):
       x = random.randint(-380, 380)
       y = random.randint(-280, 280)
       t.goto(x, y)
       t.dot(random.randint(5, 30), random.choice(colours))

   turtle.done()
   ```
   **They should see:** 200 dots of random sizes and colours. Run it again:
   a different picture!

   **Say:** "Every dot needs four random things: where across, where up,
   how big, and what colour. The loop does it 200 times."

4. **Night sky.** Change it: black background (`turtle.bgcolor("black")`),
   small white and yellow dots, and maybe 500 of them. Then add a moon
   with one big dot that isn't random.

5. **A wandering mob.** New file, `wander.py`. Mobs in Minecraft wander
   around at random, and so can the turtle:
   ```python
   import turtle
   import random

   t = turtle.Turtle()
   t.shape("turtle")
   t.color("green")
   t.pensize(3)

   for i in range(100):
       t.forward(20)
       t.left(random.choice([0, 90, 180, 270]))

   turtle.done()
   ```
   **They should see:** a random, blocky path, different every time.

   **Say:** "Each step, the turtle picks a direction at random: straight
   on, left, back, or right. This is called a **random walk**. Scientists
   use them to study how smells spread, and how tiny specks of dust
   jiggle around in water."

   Try `t.left(random.randint(0, 360))` instead, for a wobbly path.

6. **Free play.** Combine randomness with earlier lessons: random
   polygons with `polygon(random.randint(3, 8), ...)` from Lesson 2.8, a
   street where every house is a random colour, or a garden of random
   flowers.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `AttributeError: module 'random' has no attribute 'randint'` | There's a file called `random.py` in the folder | Rename it, and delete the `__pycache__` folder next to it. |
| `NameError: name 'random' is not defined` | `import random` is missing | Add it near the top. |
| `ValueError: empty range in randrange(10, 2)` | The smaller number must come first | `random.randint(1, 10)`, not `(10, 1)`. |
| `SyntaxError` in a list | A comma or quote mark missing between items | `["red", "blue"]`: each word in quotes, commas between. |
| The wandering turtle disappears off the screen | That's what random walks do sometimes! | Run it again, or see the Challenge. |

## Talk about it

- What's the difference between `randint(1, 6)` and `range(1, 6)`?
  *(`randint` can give 6; `range` stops before 6.)*
- Why is randomness useful in games? *(So the game is different every
  time: dice, card shuffles, where monsters appear, Minecraft's worlds.)*
- Can the computer really roll a dice? *(See the guide's background.)*

## Challenge *(if there's time, or for next time)*

- Roll two dice and add them, 100 times, and print the totals. Which total
  comes up most? Why? *(7: there are more ways to make it.)*
- In `confetti.py`, make each dot's size depend on how far it is from the
  middle.
- Bring the wanderer home: after it wanders, `t.goto(0, 0)` and draw a
  house there.
- **Seeds:** add `random.seed(42)` after `import random`. Run it twice.
  What happens? Try a different number. *(The same "random" picture each
  time for the same seed: Minecraft world seeds work like this!)*

## Checkpoint

The learner can, without help:
- [ ] Use `random.randint` to get a random number in a range
- [ ] Use `random.choice` to pick from a list
- [ ] Write a program that draws something different every time it runs
- [ ] Explain that `randint` includes both ends

## Lab notebook

Draw (or describe) the best random picture. Write the difference between
`randint(1, 6)` and `range(1, 6)`. Add *random*, *list* and *random walk*
to the dictionary.

## Guide's background *(optional reading)*

Computers can't really be random, because they follow instructions
exactly. Python's `random` module uses a **pseudo-random number
generator**: a formula that produces a long sequence of numbers that
*look* random, starting from a **seed** number. Python picks the seed
from the computer's clock and other unpredictable things, so each run is
different. If you set the seed yourself with `random.seed(42)`, you get
the same sequence every time. That's exactly how Minecraft world seeds
work: the same seed always generates the same world.

(For real secrets, like passwords, programmers use the `secrets` module,
which gets its randomness from the operating system and can't be
predicted from a seed.)

The two-dice challenge introduces probability: 7 is the most common total
because there are six ways to make it (1+6, 2+5, 3+4, 4+3, 5+2, 6+1) but
only one way to make 2 or 12.
