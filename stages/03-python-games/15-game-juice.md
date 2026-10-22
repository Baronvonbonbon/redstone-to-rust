# Lesson 3.15: Game Juice

**Time:** 2–3 sessions of 45 min · **You need:** Thonny; `catch.py` from
Lesson 3.14; speakers or headphones · **New words:** game state, game
over, difficulty, juice

## Goal *(read this to the learner)*

> Your game works, but it never ends, and it's a bit quiet. Today you'll
> add the things that make a game exciting: creepers to dodge, lives, a
> GAME OVER screen, sounds, diamonds that fall faster as you get better,
> and a high score that's saved forever. Game designers call this
> **juice**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Back up the working game:
      `cp ~/lab/python/catch/catch.py ~/lab/python/catch/catch-v1.py`
- [ ] Check the sound is turned up.

## Warm-up (5 min)

"Think of a game you love. What happens when you collect something? When
you get hit? When you lose?" *(Sounds, flashes, a score going up, a game
over screen, the music speeding up...)* "None of those change the rules.
They make it *feel* good. That's juice."

## Activity

Add one feature at a time, and play the game after each one. The finished
program is in step 7.

1. **A creeper to dodge.** Add a creeper Actor, drop it like the diamond,
   and make it fall a little faster. Turn `drop_diamond()` into a function
   that drops *any* Actor:
   ```python
   def drop(thing):
       thing.x = random.randint(30, WIDTH - 30)
       thing.y = random.randint(-300, -20)
   ```
   **Say:** "The Actor to drop is now a parameter, so one function works
   for the diamond *and* the creeper. And they start at a random height
   *above* the screen, so they don't arrive at the same moment."

2. **Lives.** Start with `lives = 3`. When the creeper hits the miner,
   take a life away and drop the creeper again. Show `Lives: 3` under the
   score.

3. **Game over.** A box called `game_over`, which starts as `False`. When
   lives reach 0, it becomes `True`. Then:
   - at the very top of `update()`: `if game_over: return`, so everything
     freezes;
   - in `draw()`, if `game_over`, show `GAME OVER` in big letters.

   **Say:** "`game_over` is part of the game's **state**: the box that says
   which mode the game is in. Lots of games have a state for the title
   screen, playing, paused, and game over."

4. **Play again.** A function `new_game()` that sets everything back to
   the start. Pygame Zero calls `on_key_down(key)` when a key is pressed:
   ```python
   def on_key_down(key):
       if key == keys.SPACE and game_over:
           new_game()
   ```

5. **Sounds.** Pygame Zero can play musical notes, made by the computer, so
   no sound files are needed:
   ```python
   tone.play("E5", 0.1)
   ```
   That plays the note E, in octave 5, for a tenth of a second. Use a high,
   short note for catching a diamond, and a low, longer one (`"C3", 0.4`)
   for getting hit. Try other notes, from `A` to `G`, and octaves 2 to 6.

6. **Faster and faster, and a high score.**
   - Keep the falling speed in a box, `fall_speed`. Every 5 diamonds
     (`score % 5 == 0`, the remainder trick again!), make it 1 faster.
   - Save the best score to `best.txt`, like the guessing game in Lesson
     3.10, and show it in the top right corner.

7. **The finished game.** Check the learner's game against this. Theirs
   doesn't have to match exactly, as long as it works:
   ```python
   import pgzrun
   import random

   WIDTH = 800
   HEIGHT = 600
   TITLE = "Catch the Diamonds"

   miner = Actor("miner")
   diamond = Actor("diamond")
   creeper = Actor("creeper")

   def drop(thing):
       thing.x = random.randint(30, WIDTH - 30)
       thing.y = random.randint(-300, -20)

   def load_best():
       try:
           with open("best.txt") as f:
               return int(f.read())
       except FileNotFoundError:
           return 0

   def new_game():
       global score, lives, fall_speed, game_over
       score = 0
       lives = 3
       fall_speed = 3
       game_over = False
       miner.pos = (WIDTH // 2, HEIGHT - 50)
       drop(diamond)
       drop(creeper)

   best = load_best()
   new_game()

   def draw():
       screen.fill("midnightblue")
       miner.draw()
       diamond.draw()
       creeper.draw()
       screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")
       screen.draw.text(f"Lives: {lives}", (10, 50), fontsize=40, color="pink")
       screen.draw.text(f"Best: {best}", topright=(WIDTH - 10, 10), fontsize=40, color="gold")
       if game_over:
           screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="red")
           screen.draw.text("Press SPACE to play again", center=(WIDTH // 2, HEIGHT // 2 + 70),
                            fontsize=40, color="white")

   def update():
       global score, lives, fall_speed, game_over, best
       if game_over:
           return

       if keyboard.left and miner.left > 0:
           miner.x -= 7
       if keyboard.right and miner.right < WIDTH:
           miner.x += 7

       diamond.y += fall_speed
       creeper.y += fall_speed + 1

       if diamond.colliderect(miner):
           score += 1
           tone.play("E5", 0.1)
           if score % 5 == 0:
               fall_speed += 1
           drop(diamond)
       elif diamond.top > HEIGHT:
           drop(diamond)

       if creeper.colliderect(miner):
           lives -= 1
           tone.play("C3", 0.4)
           drop(creeper)
           if lives == 0:
               game_over = True
               if score > best:
                   best = score
                   with open("best.txt", "w") as f:
                       f.write(str(best))
       elif creeper.top > HEIGHT:
           drop(creeper)

   def on_key_down(key):
       if key == keys.SPACE and game_over:
           new_game()

   pgzrun.go()
   ```
   **Say:** "`topright=` and `center=` say which part of the words to put at
   that spot, so the best score lines up with the right edge, and GAME
   OVER sits in the middle."

8. **Play, and tune.** Is it too hard? Too easy? Adjust `fall_speed`, the
   creeper's extra speed, and the number of lives until it's fun. Let other
   people play and watch their faces.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `UnboundLocalError` for `lives`, `game_over` or `fall_speed` | Changed inside a function without `global` | Add it to the `global` line of that function. |
| `NameError: name 'score' is not defined` when the game starts | `new_game()` is never called, so the boxes are never filled | Call `new_game()` once, near the top, before `draw` and `update` need it. |
| No sound | Sound turned down, or no speakers | Check the volume. The game works without sound. |
| `InvalidNote: H4 is not a valid note` | Notes go from A to G (the message says A-F, but G works too) | Use `A` to `G`, with an octave number from 0 to 8. |
| Pressing space does nothing after game over | `keys.SPACE` spelled differently, or `on_key_down` misspelled | It's exactly `on_key_down(key)` and `keys.SPACE`. |
| Lose all three lives at once | The creeper isn't moved away after a hit | Call `drop(creeper)` right after `lives -= 1`. |
| `Segmentation fault` in the terminal right after closing the game | The window was closed while a sound was still being made | Harmless: the game was closing anyway. It's a quirk of Pygame Zero's `tone`. |
| `best.txt` appears in a strange folder | The game was run from the terminal in a different folder | `cd ~/lab/python/catch` before `python3 catch.py`. |

## Talk about it

- Which piece of juice made the biggest difference to how the game feels?
- What's in the game's state now? *(score, lives, fall_speed, game_over,
  best, and where everything is.)*
- Why does the game get faster? What would happen if it never did?

## Challenge *(if there's time, or for next time)*

- A title screen: a third state, before the game starts. ("Press SPACE to
  start".)
- A short tune on game over: several `tone.play` notes, using
  `clock.schedule(function, 0.3)` to play them one after another.
- Shake the screen when you're hit: draw everything slightly off-centre
  for a few frames.
- A heart Actor that falls rarely and gives an extra life.

## Checkpoint

The learner can, without help:
- [ ] Add a second falling Actor with a different effect
- [ ] Use a `game_over` state to freeze the game and show a message
- [ ] Restart with a key, using `on_key_down`
- [ ] Save and load a high score

## Lab notebook

List the juice you added, and rate each one: how much better did it make
the game? Write the best score ever. Add *game state*, *game over*,
*difficulty* and *juice* to the dictionary.

## Guide's background *(optional reading)*

"Juice" is a real game-design term for feedback that makes actions feel
satisfying: sounds, flashes, shakes, particles. A famous talk, *Juice it
or lose it*, showed the same simple game with and without juice: the rules
are identical, but one feels dead and the other feels alive.

`new_game()` is an important pattern: put *all* the starting state in one
function, and call it both at the start and to restart. If the starting
state were spread around the program, restarting would be full of bugs.

The `game_over` flag is a simple **state machine**: the game is in one of
a few modes, and each mode handles input and drawing differently. State
machines come back in Stage 6 (the CPU's control logic) and are everywhere
in industrial controls: a machine sequence (idle, running, faulted) is the
same idea.

`tone` generates sound waves mathematically (sine waves at each note's
frequency), which is why no sound files are needed.
