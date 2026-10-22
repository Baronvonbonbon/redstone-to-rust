# Lesson 3.14: Catch the Diamonds

**Time:** 2 sessions of 45 min · **You need:** Thonny; the sprites from
Lesson 3.13 in `~/lab/python/catch/images/` · **New words:** update, game
loop, collision, global

## Goal *(read this to the learner)*

> Today you'll make a real arcade game. Diamonds fall from the sky, and
> you steer your miner left and right with the arrow keys to catch them.
> Every diamond scores a point. You'll learn how games make things move,
> and how they know when two things touch.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check the sprites are there: `ls ~/lab/python/catch/images` should
      show `miner.png`, `diamond.png` and `creeper.png`.

## Warm-up (5 min)

"In Pygame Zero, who calls `draw()`? When does `on_mouse_down` happen?"
*(Pygame Zero calls them: `draw` when the screen needs painting,
`on_mouse_down` when you click.)* "Today we meet a third one, `update`,
which happens 60 times every second."

## Activity

### Session 1: moving things

1. **A falling diamond.** New file, saved as `~/lab/python/catch/catch.py`:
   ```python
   import pgzrun
   import random

   WIDTH = 800
   HEIGHT = 600
   TITLE = "Catch the Diamonds"

   diamond = Actor("diamond")
   diamond.pos = (400, 0)

   def draw():
       screen.fill("midnightblue")
       diamond.draw()

   def update():
       diamond.y += 4

   pgzrun.go()
   ```
   **They should see:** a diamond falling down the screen, and off the
   bottom.

   **Say:** "Pygame Zero calls `update()` about 60 times a second, and then
   `draw()`. Each time, the diamond's y gets 4 bigger, so it moves down
   4 pixels. 60 times a second, that's 240 pixels a second. Each picture is
   called a **frame**, so this game runs at 60 frames per second. This is
   the **game loop** again, like in the text adventure, but much faster:
   update everything, draw everything, repeat."

2. **Drop it again.** Add a function (above `draw`) that puts the diamond
   back at the top, somewhere random:
   ```python
   def drop_diamond():
       diamond.x = random.randint(20, WIDTH - 20)
       diamond.y = 0
   ```
   And in `update`, after moving it:
   ```python
       if diamond.top > HEIGHT:
           drop_diamond()
   ```
   **Say:** "`diamond.top` is the y of the top edge of the picture. When
   even the top has gone past the bottom of the window, it's completely off
   the screen, so we drop a new one." Actors also have `bottom`, `left` and
   `right`.

3. **The miner, with arrow keys.** Add near the top:
   ```python
   miner = Actor("miner")
   miner.pos = (WIDTH // 2, HEIGHT - 50)
   ```
   Add `miner.draw()` to `draw()`, and to `update()`:
   ```python
       if keyboard.left:
           miner.x -= 6
       if keyboard.right:
           miner.x += 6
   ```
   **They should see:** the miner moving while an arrow key is held down.

   **Say:** "`keyboard.left` is `True` while the left arrow key is held
   down. Every frame, if it's down, the miner moves 6 pixels."

4. **Don't fall off the edge.** Drive the miner off the side. Oops. Change
   the two `if` lines:
   ```python
       if keyboard.left and miner.left > 0:
           miner.x -= 6
       if keyboard.right and miner.right < WIDTH:
           miner.x += 6
   ```
   **Say:** "Only move left if there's room on the left. That's `and` from
   rock, paper, scissors!"

### Session 2: catching and scoring

5. **Collisions.** Add `score = 0` near the top. Then in `update()`:
   ```python
       if diamond.colliderect(miner):
           score += 1
           drop_diamond()
   ```
   Run it, and catch a diamond. **They should see:** an error,
   `UnboundLocalError: cannot access local variable 'score'`.

   **Say:** "Python thinks `score` inside `update` is a brand-new box that
   belongs only to the function, because we're changing it. We have to tell
   it: 'I mean the `score` from outside'." Add this as the *first* line
   inside `update`:
   ```python
       global score
   ```
   **Say:** "`global` means 'use the box from the main program'. You only
   need it when a function *changes* an outside variable, not when it just
   reads it."

   **Say:** "`colliderect` checks whether two pictures' rectangles overlap.
   When they touch, that's a **collision**. Games check for collisions every
   single frame."

6. **Show the score.** In `draw()`, after everything else:
   ```python
       screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")
   ```
   Things drawn last appear on top, so the score is never hidden.

7. **The whole game so far.** Check it against this:
   ```python
   import pgzrun
   import random

   WIDTH = 800
   HEIGHT = 600
   TITLE = "Catch the Diamonds"

   miner = Actor("miner")
   miner.pos = (WIDTH // 2, HEIGHT - 50)
   diamond = Actor("diamond")
   score = 0

   def drop_diamond():
       diamond.x = random.randint(20, WIDTH - 20)
       diamond.y = 0

   drop_diamond()

   def draw():
       screen.fill("midnightblue")
       miner.draw()
       diamond.draw()
       screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")

   def update():
       global score
       if keyboard.left and miner.left > 0:
           miner.x -= 6
       if keyboard.right and miner.right < WIDTH:
           miner.x += 6
       diamond.y += 4
       if diamond.colliderect(miner):
           score += 1
           drop_diamond()
       elif diamond.top > HEIGHT:
           drop_diamond()

   pgzrun.go()
   ```
   Play it! How high can you score in one minute? (Use a timer.)

8. **Tune it.** The speeds are just numbers. Try changing the miner's 6 and
   the diamond's 4. Which feels best? **Say:** "Game designers spend ages
   changing numbers like these until a game feels just right. It's called
   **tuning**."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `UnboundLocalError: cannot access local variable 'score' where it is not associated with a value` | Changing `score` inside a function without `global` | Add `global score` as the first line of `update`. |
| `SyntaxError: name 'score' is assigned to before global declaration` (or `is used prior to`) | `global score` isn't the first thing in the function | Move it to the very top of `update`. |
| The miner doesn't move (maybe with `DeprecationWarning: Uppercase keyboard attributes`) | `keyboard.left` written as `keyboard.Left`, or the window doesn't have focus | Lower case `left`. Click on the game window first. |
| Diamonds are counted many times, or the score races up | The diamond isn't moved away after a catch | Call `drop_diamond()` right after `score += 1`. |
| Nothing falls | `update` is spelled differently, like `def updat():` | It must be exactly `update`. Pygame Zero only calls functions with the right names. |
| `NameError: name 'drop_diamond' is not defined` | `drop_diamond()` is called before the `def` | Put the `def` above the line that calls it. |

## Talk about it

- What does `update()` do, and how often? What does `draw()` do?
- What's a collision? How does the game check for one?
- Why do we need `global score`, but not `global miner`? *(We change what's
  in the `score` box. We don't put a new miner in the `miner` box; we only
  change the miner's position.)*

## Challenge *(if there's time, or for next time)*

- Make the diamond fall at a random speed each time.
- Two diamonds at once.
- A golden diamond worth 5 points that only falls sometimes
  (`random.randint(1, 10) == 1`).
- Let the miner move up and down too, with `keyboard.up` and
  `keyboard.down`.

## Checkpoint

The learner can, without help:
- [ ] Move an Actor every frame in `update()`
- [ ] Move an Actor with the arrow keys, without letting it leave the screen
- [ ] Detect a collision with `colliderect` and add to a score
- [ ] Explain when `global` is needed

## Lab notebook

Draw the game loop as a circle: update → draw → update → draw... Write
"60 frames a second". Write the best one-minute score. Add *update*,
*frame*, *collision*, *global* and *tuning* to the dictionary.

## Guide's background *(optional reading)*

Every real-time game, from Pong to Minecraft, runs a loop like this many
times a second: read the input, update the world, check for collisions,
draw the frame. Minecraft calls each update a "tick" (20 per second).
If you work with PLCs, this is the same idea as the **scan cycle**: read
inputs, run the logic, write outputs, repeat.

`colliderect` checks whether two Actors' bounding rectangles overlap. It's
the simplest kind of collision detection; it can count a "hit" when two
see-through corners touch. Most 2D games start with rectangles and only
use more exact methods when they need to.

`global` is often considered a bit messy in bigger programs, but for a
small game with a few pieces of state, it's the clearest way. The learner
will see tidier ways (classes in Python, structs in Rust) later. Python's
error message for this case changed between versions: Pop!_OS 22.04
(Python 3.10) says `local variable 'score' referenced before assignment`,
which means the same thing.
