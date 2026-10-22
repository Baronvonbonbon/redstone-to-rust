# Lesson 3.16: Project: My Own Game (Stage 3 Checkpoint)

**Time:** 4–6 sessions of 45 min, plus the checkpoint on a separate day ·
**You need:** Thonny; the Sprite Maker; squared paper; playtesters
(family, friends) · **New words:** design, prototype, feature, release

## Goal *(read this to the learner)*

> You've made a guessing game, rock-paper-scissors, a text adventure, and
> an arcade game. Now you'll design and build a game that's **all yours**:
> your idea, your characters, your rules. At the end, you'll release it
> to the family, with instructions, so anyone can play it. Finish, and you
> become a **Game Maker**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Agree a "release day" with the learner, about two weeks away, and
      invite the playtesters.

## The rules for the project

The game must:
1. Be the learner's own idea (it can be inspired by a game they love).
2. Be a Pygame Zero game **or** a text game. If it's a text game, it must
   be at least as big as Fuzzlewood.
3. Use a list or a dictionary.
4. Have at least one function that returns a value.
5. Have a way to win or a score, and a way to lose or end.
6. Save something to a file (a high score, a save game, settings).
7. Live in its own folder, `~/lab/python/mygame/` (or a better name),
   with a `HOW-TO-PLAY.txt` file explaining the controls and the goal.

## Activity

### Session 1: design

1. **Ideas.** Brainstorm at least five ideas on paper, quickly, without
   judging them. Some starters:
   - **Dodge:** survive as long as possible while things fly at you.
   - **Clicker:** click things before they disappear (`on_mouse_down` and
     `collidepoint`).
   - **Maze:** steer through a maze made of blocks, to a treasure.
   - **Number game:** Numberblocks fall, and you catch only the ones that
     add up to 10.
   - **Quiz show:** a times-table or prime-number quiz with lives, a
     timer and sounds.
   - **A bigger adventure:** a new story with your own world.

2. **Pick one, and write the one-sentence pitch.** For example: "You're a
   bee collecting flowers while avoiding wasps, and every flower makes you
   faster."

3. **The design page.** On one sheet of paper:
   - a sketch of the screen;
   - the player: what do they control, and how?
   - the goal: how do you score or win?
   - the danger: how do you lose?
   - the sprites needed (designed on squared paper later);
   - the state: which boxes will the program need? (`score`, `lives`...)

4. **Three lists of features.**
   - **Must have:** the smallest version that's playable. (This is the
     first thing to build.)
   - **Nice to have:** what makes it good.
   - **Dream:** what you'd add with endless time.

   **Say:** "Professional game makers build the *must have* list first, as
   quickly as they can. That first rough version is called a
   **prototype**. Only when it's fun do they add more."

### Sessions 2 to 4: build

5. **Build the prototype.** Start from the closest earlier game (copy
   `catch.py` or `fuzzlewood.py` into the new folder) and change it, or
   start fresh. Use plain rectangles or circles for sprites at first; the
   real pictures can come later.

   The guide's job: ask questions, use the stuck ladder, and keep the
   learner on the "must have" list until it works.

6. **Play it, then add features.** One feature at a time, from the "nice
   to have" list. After each one: run it, play it, and save a copy that
   works (`cp game.py game-v2.py`).

7. **Sprites and juice.** Make the real sprites with the Sprite Maker, and
   add sounds and messages.

### Sessions 5 and 6: playtest and release

8. **Playtest.** At least two people play it, while the learner watches
   silently and takes notes. Then fix the biggest problems.

9. **Write `HOW-TO-PLAY.txt`.** The name of the game, the goal, the
   controls, and how to run it:
   ```
   cd ~/lab/python/mygame
   python3 game.py
   ```

10. **Release day.** The learner presents the game: the pitch, a live
    demo, one piece of code they're proud of, and one bug they found and
    fixed. Then everyone plays. Keep a "high score table" on paper.

## The Stage 3 checkpoint

On a separate day, without help (they may look at their own old programs
and lab notebook, and use `help()`):

1. **A loop that waits.** Write a times-table quiz that keeps asking
   random questions (two numbers from 2 to 12) until the player gets 5
   right. It counts how many tries it took.
2. **A list.** Make a list of 10 random numbers from 1 to 100, then print
   the biggest, the smallest, and how many are even.
3. **A dictionary.** Make a dictionary of 5 friends' or family members'
   favourite foods. Ask for a name, and print their food, or "I don't
   know" if the name isn't there.
4. **A function with tests.** Write `is_square(n)`, which returns `True`
   if `n` is a square number (1, 4, 9, 16...). Test it with at least four
   `assert`s.
5. **A file.** Make the quiz from task 1 save its best (fewest) number of
   tries in a file, and show the best when it starts.
6. **The game.** Their Pygame Zero game from Lesson 3.15 (or their project,
   if it's a Pygame Zero game) shows a sprite moving with the keyboard,
   a collision, and a score. They explain how `update` and `draw` work.
7. **A bug hunt.** The guide puts a bug inside a *function* in one of their
   programs (a wrong variable name, or a missing `return`). They run it,
   read the whole traceback, find the line in *their* code, and fix it.
8. **Explain:** the difference between a list and a dictionary, in their
   own words.

All done means **Game Maker!** Sign and stamp the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The project is too big to finish | The "must have" list is too long | Cut it down to the smallest playable game. Everything else can be version 2. |
| The learner wants to start a new idea halfway through | Normal! Finishing is the hardest part | Write the new idea on the "next game" list, and finish this one first. |
| A bug nobody can find | | Add `print` lines to show what's in the variables, or use Thonny's debugger, one step at a time. Explain the code out loud, line by line, to someone (or a toy). |
| The traceback has many lines | Each line is one function calling the next | Read from the **bottom** for the error, then look up the list for the last line that's in *your* file. |
| The game works in Thonny but not the terminal | The terminal is in a different folder | `cd` into the game's folder first. |

## Talk about it

- What was the hardest bug? How did you find it?
- What did your playtesters do that surprised you?
- What's on your "dream" list? Will you build it?

## Checkpoint

The learner can, without help:
- [ ] Design a game on paper, with a must-have list
- [ ] Build a prototype, then add features one at a time
- [ ] Run a playtest and act on what they learned
- [ ] Pass the Stage 3 checkpoint above

## Lab notebook

Glue in the design page and the playtest notes. Write the release-day high
score table. Write: "The thing I'm proudest of is..." and "Next time I
would...". Add *prototype*, *feature* and *release* to the dictionary.

## Guide's background *(optional reading)*

This is the first project where the learner owns the design, and the
biggest lesson is **scope**: a small game that's finished beats a big one
that isn't. The "must have / nice to have / dream" lists are a simple
version of how real software teams decide what to build first (often
called an MVP, a *minimum viable product*).

A traceback lists the chain of function calls that led to an error, from
the outside in. The bottom line is the error itself; the lines above it
show where each call came from. When the error happens inside Pygame
Zero's own code, the useful line is the last one in the learner's file.

After this stage, the course goes *down* the stack: Stage 4 turns numbers
into bits and bits into logic gates, with redstone-style circuits in
Luanti. The learner will see that every `if`, `and` and `or` they've
written is, deep down, made of switches.
