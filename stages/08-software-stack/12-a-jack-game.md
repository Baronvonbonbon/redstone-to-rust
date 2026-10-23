# Lesson 8.12: A Jack Game (Project 9)

**Time:** 4–6 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card; squared paper · **New words:** constructor,
method, field, `this`, game loop

## Goal *(read this to the learner)*

> Time to make a game for your own computer. First you'll play and read
> **Diamond Dash**, a little game written in Jack for this course: you
> collect diamonds while a creeper chases you. You'll learn how Jack's
> classes and objects work, change the game, and then design and build a
> game of your own. In Lesson 8.18, your game will run on a computer
> where *every* layer, from the compiler down, is your own work.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once, and play Diamond Dash yourself
      (step 1).
- [ ] The game is in `~/lab/n2t/stack/diamond-dash/` (from `give-lab.sh
      LEARNER stack`).

## Warm-up (5 min)

"In Lesson 7.11, what was a class?" *(A design for objects: each object
has its own values.)* "What's a method?" *(A function that belongs to
an object, and works on its values.)*

## Activity

### Session 1: play, then read

1. **Play.**
   ```
   cp -r ~/lab/n2t/stack/diamond-dash ~/lab/n2t/projects/9/DiamondDash
   cd ~/lab/n2t/projects/9
   jackc DiamondDash
   ```
   Open `vme`, load the folder `DiamondDash`, click **Yes** for the
   built-in OS, set **No animation**, and Run. Click the keyboard bar
   under the screen, and press any key. **They should see:** a grid
   world with a black square (you), a creeper with a face, and a diamond
   outline. The arrow keys move you one square at a time. Each diamond
   adds to the score at the bottom, and makes the creeper faster. If it
   catches you: `BOOM!`

2. **The three files.** Open them in Thonny. **Say:**
   - "`Main.jack` makes a game object and runs it. That's all.
   - `Random.jack` makes numbers that look random. Jack has no random
     numbers, so each one is worked out from the one before. It's the
     same trick Python uses, only simpler.
   - `DashGame.jack` is the game."

3. **Fields and the constructor.** In `DashGame.jack`, look at the top:
   ```
   field int playerX, playerY, creeperX, creeperY, diamondX, diamondY;
   field int score, ticks, speed;
   ```
   **Say:** "**Fields** are the object's own variables: every `DashGame`
   object has its own player position, score and so on. They're like
   `self.score` in Python." Then the **constructor**, `DashGame.new()`:
   "It sets the fields, then `return this;` gives back the new object.
   `this` means 'the object we're working on', like `self`."

4. **Methods and functions.** **Say:** "A **method** works on one
   object, and can use its fields: `movePlayer` changes `playerX`. A
   **function** belongs to the class and has no object, like `clear`,
   which only needs a column and a row." **Ask:** "In `run`, why does
   `do drawPlayer(true);` have no object in front?" *(It's a method of
   this same object: `this` is implied.)*

### Session 2: the game loop

5. **Read `run`.** **Say:** "Nearly every game has a **game loop**: over
   and over, read the keys, move things, check what's touching, draw, and
   wait a moment." Find each part in `run`:
   - `Keyboard.keyPressed()` gives the key being held down, or 0. The
     arrow keys are 130 to 133 (Jack card). `lastKey` makes one press
     move one square, however long the key is held.
   - The diamond check: are the player and the diamond in the same
     square?
   - `ticks` counts loops. When it passes `speed`, the creeper moves one
     square closer.
   - `Sys.wait(10)` waits 10 milliseconds, so the game runs at the same
     speed on fast and slow computers.

6. **How the creeper chases.** Read `moveCreeper`. **Ask:** "What path
   does the creeper take?" *(Across first, until it's in the player's
   column, then up or down.)* "Is that the shortest path?" *(On an open
   grid, yes. With walls, it would need breadth-first search, Lesson
   7.14!)*

7. **Change it.** One at a time, compiling and playing after each:
   - Make the creeper start slower (`speed` in the constructor) or speed
     up less with each diamond.
   - Give the player a face, like the creeper's.
   - Show `BOOM!` in the middle of the screen, with the final score
     under it.
   - Add a **gold block**, worth 5 points, that appears now and then.

   Commit after each change that works.

### Sessions 3 to 6: your own game

8. **Design on paper first.** **Say:** "Every good game starts as a
   drawing." On squared paper, draw the screen (512 × 256, or 32 × 16
   squares of 16). Write down:
   - What does the player control, and with which keys?
   - What moves by itself?
   - How do you win, or score? How do you lose?
   - Which classes will there be, and which fields does each need?

   Ideas: Snake (a growing tail, kept in an `Array`); a Breakout game
   (Lesson 6.13's Pong was written in Jack); a maze game, with mazes from
   Lesson 7.16 typed in as strings; a Numberblocks counting game; a
   falling-blocks game.

9. **Build it in small steps.** One step per session, testing each:
   1. Draw the world, with nothing moving.
   2. Move the player with the keys.
   3. Add the thing that moves by itself.
   4. Add scoring, winning and losing.
   5. Polish: a title screen, sounds of `BOOM!`, faster levels.

   **Keep it small.** In Lesson 8.18, the whole game, plus the OS, has to
   fit into the Hack computer's 32K of ROM after going through *your*
   translator. Diamond Dash is under 200 lines of Jack, and that fits.
   About that size is a good target.

10. **Demo day.** Show the game to someone. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The keys do nothing | The keyboard bar isn't active | Click the bar under the screen. |
| The game is too fast or too slow | Animation is on, or the waits need changing | Set **No animation**, then change `Sys.wait` or `speed`. |
| `... is not defined as a field, parameter or local or static variable` | A typo; a variable from a different subroutine; or a `field` used in a `function`, which has no object | Check the `var` and `field` lines. Make it a method, or pass the value in. |
| Pieces of old drawings stay on the screen | Something was drawn in its new place without being cleared from the old one | Draw it in white (`Screen.setColor(false)`) first, then move it. |
| `Program Halted: Illegal rectangle coordinates`, and `ERR9` on the screen | Something was drawn off the edge of the screen | Keep x from 0 to 511 and y from 0 to 255. |

## Talk about it

- What's the difference between a field, a local variable and a static
  variable?
- What's the difference between a method and a function? What's `this`?
- What happens in a game loop?
- How does Diamond Dash make "random" numbers without any randomness?

## Challenge *(if there's time, or for next time)*

- Give Diamond Dash a second creeper. *(Hint: make a `Creeper` class with
  its own fields and a `move` method, so there can be as many as you
  like.)*
- Add a high score that stays while the program runs, using a `static`.
- Put walls in Diamond Dash, and make the creeper find its way round them
  with breadth-first search.

## Checkpoint

The learner can, without help:
- [ ] Explain fields, constructors, methods, functions and `this`
- [ ] Explain the parts of a game loop
- [ ] Change Diamond Dash, and explain what they changed
- [ ] Design a game on paper, and build it in Jack

## Lab notebook

Stick in the paper design of their game, with its classes and fields.
Commit. Add *constructor*, *method*, *field*, *this* and *game loop* to
`dictionary.md`. Tick Project 9 on the passport.

## Guide's background *(optional reading)*

This completes Nand to Tetris Project 9, whose task is simply "write an
interactive program in Jack". Diamond Dash is the course's own example
(MIT licence); the learner's game is theirs. Jack's objects work like
those in Python or Java, but there is no inheritance, and objects must
be freed by hand: `dispose` calls `Memory.deAlloc`, which Lesson 8.17
writes.

The `Random` class is a **linear congruential generator**: each number
is `(seed × 7 + 11) mod 509`. Starting it from how long the player takes
to press a key (counted in `waitToStart`) is a classic trick for games
on machines with no clock. The game reads `Keyboard.keyPressed()` (the
`KBD` register) directly instead of `readInt`, so it never waits.

The size limit is real: in Lesson 8.18, the learner's translator turns
the game and the whole OS (written in Jack, as VM code) into Hack, and
Hack's ROM holds 32,768 instructions. With the translator from Lesson
8.10, Diamond Dash and the OS come to about 50,000, and Lesson 8.18
shows how to shrink that to fit. A game much bigger than Diamond Dash
may not fit at all, which is fine: it still runs in `vme`.
