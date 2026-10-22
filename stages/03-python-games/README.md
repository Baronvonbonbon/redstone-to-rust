# Stage 3: Python Games & Puzzles

**Badge:** Game Maker · **Needs first:** Stage 2; multiplication and
division facts, and remainders · **Lessons:** 16

The learner goes from drawing pictures to making things people can
**play**. Python gets three new powers: `while` loops that keep going
until something happens, **lists** and **dictionaries** for keeping lots
of things, and **files** for remembering things after the program stops.
With those, they build a rock-paper-scissors game, prime-number and
hailstone-number explorers, a secret code machine, a text adventure set in
Fuzzlewood Elementary (the school from the Underpants Heist), and finally
real arcade games with moving sprites in **Pygame Zero**.

Every lesson is fully scripted. Programs are still written in **Thonny**
and saved in `~/lab/python/`.

## Tools

- **Thonny**, as in Stage 2. **View → Variables** is even more useful now,
  because it shows what's inside lists and dictionaries.
- **Pygame Zero** (installed by setup as `python3-pgzero`), for Lessons
  3.13–3.16. Every game starts with `import pgzrun` and ends with
  `pgzrun.go()`, so it runs from Thonny's F5 *and* from the terminal.
- **Sprite Maker** ([labs/sprite-maker](../../labs/sprite-maker/)): turns
  text pixel art into pictures for the games. The guide gives it to the
  learner before Lesson 3.13 with `./scripts/give-lab.sh LEARNER sprites`.
- **bsdgames** (installed by setup): `adventure`, the very first text
  adventure, from the 1970s, for Lesson 3.11; and `primes`, `caesar`,
  `rot13` and `arithmetic`, which Lessons 3.6 and 3.9 compare with the
  learner's own programs.
- References for the guide: OpenStax *Introduction to Python Programming*
  (Chapters 5–10 cover loops, lists, dictionaries and files), and *Think
  Python 2e* in the offline library (`/srv/redstone-library/books/`).
  For extra game ideas, Al Sweigart's *Invent Your Own Computer Games with
  Python* and *The Big Book of Small Python Projects* are free to read on
  his website **(online, optional)**.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 3.1 | [Silly Sentences](01-silly-sentences.md) | Strings in depth: joining, f-strings, `.upper()`, `len`, letters by number; a silly story machine | strings, f-strings, methods |
| 3.2 | [Keep Going!](02-keep-going.md) | `while` loops: countdowns, guess-my-number until you get it, `break`, a menu that repeats | `while`, `break`, counters |
| 3.3 | [The Inventory](03-the-inventory.md) | Lists as a Minecraft inventory: add, remove, check, count, loop through, sort | lists |
| 3.4 | [Rock, Paper, Scissors](04-rock-paper-scissors.md) | A complete game: best of 5 against the computer, with `and`/`or` | combining everything, Boolean logic |
| 3.5 | [Functions That Answer Back](05-functions-that-answer-back.md) | `return`; checking functions with `assert`; FizzBuzz | return values, testing |
| 3.6 | [Prime Hunters](06-prime-hunters.md) | `is_prime(n)`; all the primes to 1000; check against the `primes` command | primes, algorithms |
| 3.7 | [Hailstone Numbers](07-hailstone-numbers.md) | The Collatz puzzle: a `while` loop nobody can prove always stops; a turtle graph | open problems, graphs |
| 3.8 | [The Mob Book](08-the-mob-book.md) | Dictionaries: a Minecraft mob encyclopedia, and counting things | dictionaries, key and value |
| 3.9 | [Secret Code Machine](09-secret-code-machine.md) | A Caesar cipher program with `%`, then cracking it by trying every key | algorithms, brute force |
| 3.10 | [Saving Things](10-saving-things.md) | Files: write a diary, read the Stage 1 jokes file, keep a high score | files, `with` |
| 3.11 | [Text Adventure, Part 1: Rooms](11-text-adventure-rooms.md) | Play `adventure`; build Fuzzlewood Elementary as a dictionary of rooms you can walk around | data structures, game loop |
| 3.12 | [Text Adventure, Part 2: Things](12-text-adventure-things.md) | Items, an inventory, a locked door and a way to win; add your own rooms | state, design |
| 3.13 | [A Window of Your Own](13-a-window-of-your-own.md) | Pygame Zero: `draw()`, shapes, text, y going *down*; make sprites with the Sprite Maker | game window, sprites |
| 3.14 | [Catch the Diamonds](14-catch-the-diamonds.md) | `update()`, keyboard movement, falling diamonds, collisions, a score | the game loop, collision |
| 3.15 | [Game Juice](15-game-juice.md) | Creepers to dodge, lives, game over, restart, sounds with `tone`, speeding up, a saved high score | game state, polish |
| 3.16 | [Project: My Own Game](16-my-own-game.md) | Plan, build, playtest and publish (to the family) a game of their own; Stage 3 checkpoint | putting it together |

## Free play for this stage

- `adventure`, `wump` (Hunt the Wumpus) and `hangman` in the terminal.
- `arithmetic` for quick maths-facts practice (`arithmetic -o +-x/`).
- Turtle art from Stage 2, any time.
- Improving old games: every game in this stage can grow new features.

## Habits to build now

- **One folder per game**, in `~/lab/python/`: `rps/`, `adventure/`,
  `catch/`. Pygame Zero games *must* have their own folder, because their
  pictures go in an `images/` folder next to them.
- **Test as you go.** Run the program after every few lines.
- **Save a working copy** before a big change (`cp game.py game-v1.py`
  in the terminal). Git, a much better way of doing this, arrives in Stage 5.
- **Let other people play.** Watching someone else play your game is the
  best way to find bugs.

## Checkpoint

The learner can, without help:
- [ ] Write a `while` loop that keeps going until the player wins or quits
- [ ] Use a list: add to it, remove from it, check if something is in it,
      and loop through it
- [ ] Use a dictionary to look things up by name
- [ ] Write a function that **returns** a value, and check it with `assert`
- [ ] Save something to a file and read it back the next time the program runs
- [ ] Make a Pygame Zero game where a sprite moves with the keyboard,
      something collides with it, and a score is shown

They can also:
- [ ] Explain the difference between a list and a dictionary
- [ ] Read a traceback with several lines, and find the line in *their*
      program that caused it
