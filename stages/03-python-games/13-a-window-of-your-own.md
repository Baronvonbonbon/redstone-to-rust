# Lesson 3.13: A Window of Your Own

**Time:** 2 sessions of 45 min · **You need:** Thonny; the Sprite Maker
(see below); squared paper and coloured pencils · **New words:** Pygame
Zero, sprite, actor, frame

## Goal *(read this to the learner)*

> Time to make games with real pictures that move! Today you'll open your
> own game window, paint on it, and design your own characters, pixel by
> pixel, like the pixel pictures from Stage 0. By the end, your miner will
> jump to wherever you click.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] From **your own** account, in the course folder, give the learner
      the Sprite Maker:
      ```
      ./scripts/give-lab.sh LEARNER sprites
      ```
      (Use the learner's account name.) It puts `make_sprite.py` and three
      example pictures in `~/lab/sprite-maker/` in their account.
- [ ] As the learner, make the game's folders:
      `mkdir -p ~/lab/python/catch/images`

## Warm-up (5 min)

"Remember the pixel pictures in Stage 0, where each square was a number
or a colour? Every picture on a screen is made like that. A game shows a
new picture about 60 times every second, and each one is a little
different. That's what makes things look like they move." Make a quick
flip-book on the corner of a notebook if you have time.

## Activity

### Session 1: a window and paint

1. **The smallest game.** New file, saved as
   `~/lab/python/catch/hello_window.py`:
   ```python
   import pgzrun

   WIDTH = 800
   HEIGHT = 600
   TITLE = "My First Window"

   def draw():
       screen.fill("skyblue")

   pgzrun.go()
   ```
   Run it (F5). **They should see:** a sky-blue window. Close it with the
   window's ✕.

   **Say:** "This uses **Pygame Zero**, a toolbox for making games. Every
   Pygame Zero game starts with `import pgzrun` and ends with
   `pgzrun.go()`, which starts the game running. `WIDTH`, `HEIGHT` and
   `TITLE` set up the window. And you write a function called `draw`, but
   you never call it yourself: Pygame Zero calls it, every time it needs to
   paint the screen."

   Thonny may underline `screen` as unknown. That's fine: Pygame Zero
   provides it when the game runs.

2. **Shapes and words.** Add to `draw()`:
   ```python
       screen.draw.filled_rect(Rect((0, 500), (800, 100)), "forestgreen")
       screen.draw.filled_circle((700, 90), 50, "yellow")
       screen.draw.text("Hello!", (20, 20), fontsize=60, color="white")
   ```
   **They should see:** grass along the bottom, a sun top right, and
   "Hello!" top left.

3. **Upside-down y!** **Say:** "Here's something strange. In Stage 2, the
   middle of the turtle's screen was (0, 0), and y went *up*. In Pygame
   Zero, (0, 0) is the **top left corner**, and y goes *down*. The grass
   starts at y = 500, near the *bottom*. Most game toolkits work this way,
   because screens are drawn from the top, line by line, like reading a
   book."

   On squared paper, draw the window with (0, 0) top left, (800, 0) top
   right, (0, 600) bottom left. Then add a cloud: a few overlapping white
   `filled_circle`s near the top. Work out the numbers on paper first.

   `Rect((x, y), (width, height))` is a rectangle: where its top-left
   corner is, then how big it is.

### Session 2: sprites

4. **Design a sprite.** A **sprite** is a small picture that moves around
   in a game. Look at the examples:
   ```
   cat ~/lab/sprite-maker/miner.txt
   ```
   **They should see:** the miner drawn in letters. **Say:** "Each letter
   is one pixel's colour: `n` is brown, `t` is tan, `k` is black, `c` is
   cyan, `b` is blue, and `.` is see-through. The full list is at the top
   of `make_sprite.py`."

   Copy the examples into the game's `images` folder and turn them into
   pictures:
   ```
   cp ~/lab/sprite-maker/*.txt ~/lab/python/catch/images/
   cd ~/lab/python/catch/images
   python3 ~/lab/sprite-maker/make_sprite.py miner.txt
   python3 ~/lab/sprite-maker/make_sprite.py diamond.txt
   python3 ~/lab/sprite-maker/make_sprite.py creeper.txt
   ls
   ```
   **They should see:** `Made miner.png (40 x 40 pixels)` and so on, and
   the `.png` files in the list.

5. **Make your own.** On squared paper, the learner designs their own
   miner (or a different hero), 8 or 10 squares wide. Then they type it as
   letters in Thonny (**File → New**, then save it in the `images` folder
   as, for example, `hero.txt`, choosing "all files" if Thonny asks), and
   run the maker on it. Every line must be the same width, and names
   should be lower case with no spaces.

   Use `--size 8` for a bigger sprite.

6. **An actor on the stage.** In Pygame Zero, a sprite that moves is called
   an **Actor**. Change `hello_window.py`:
   ```python
   import pgzrun

   WIDTH = 800
   HEIGHT = 600
   TITLE = "My First Window"

   miner = Actor("miner")
   miner.pos = (400, 450)

   def draw():
       screen.fill("skyblue")
       screen.draw.filled_rect(Rect((0, 500), (800, 100)), "forestgreen")
       miner.draw()

   def on_mouse_down(pos):
       miner.pos = pos

   pgzrun.go()
   ```
   **They should see:** the miner standing on the grass. Click anywhere,
   and the miner jumps there.

   **Say:** "`Actor("miner")` finds `miner.png` in the `images` folder by
   itself. `miner.pos` is where its middle is. And `on_mouse_down` is
   another function that Pygame Zero calls for you, every time the mouse is
   clicked, and tells you where. Functions like this, called when something
   happens, are called **event handlers**."

7. **Run it from the terminal too.**
   ```
   cd ~/lab/python/catch
   python3 hello_window.py
   ```

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'pgzrun'` | Pygame Zero isn't installed | The guide runs `sudo apt install python3-pgzero`. |
| `KeyError: "No image found like 'miner'. Are you sure the image exists?"` | There's no `miner.png` in an `images` folder next to the program | Check: `ls ~/lab/python/catch/images`. Run the Sprite Maker on the `.txt` file. The program must be saved in the `catch` folder. |
| `You must use lower case filenames.` | Pygame Zero wants lower-case image names | Rename the file in lower case, like `hero.png`, and use `Actor("hero")`. |
| `make_sprite: line 3 is 7 letters wide, but the first line is 8` | The picture's lines aren't all the same width | Add or remove letters so every line matches. Use `.` for empty pixels. |
| `make_sprite: line 2: I don't know the colour 'x'` | A letter that isn't in the colour list | Use a letter from the list, or add `x = #FF8800` above the picture. |
| `ValueError: invalid color name` | A colour name pygame doesn't know | Try a simpler name: `red`, `skyblue`, `forestgreen`, `gold`, `white`, `black`, `pink`, `purple`. |
| The window opens and closes straight away | `pgzrun.go()` is missing at the end | Add it as the last line. |
| `TypeError: draw() must not take any arguments.` | `def draw(something):` | It's just `def draw():`. |

## Talk about it

- Where is (0, 0) in Pygame Zero, and which way does y go? How is that
  different from the turtle?
- Who calls `draw()` and `on_mouse_down()`? *(Pygame Zero does, not us.)*
- What's a sprite? What's an Actor?

## Challenge *(if there's time, or for next time)*

- Make a second actor (the creeper), and put it somewhere else.
- `def on_mouse_move(pos):` makes the miner follow the mouse everywhere.
- Draw a whole scene in `draw()`: trees from rectangles and circles, a
  house, stars.
- Design a sprite with your own colour, using a line like `x = #FF8800`
  (the same colour codes as Lesson 2.6's challenge).

## Checkpoint

The learner can, without help:
- [ ] Make a Pygame Zero window with a background colour, shapes and text
- [ ] Explain that y goes down from the top-left corner
- [ ] Turn their own text pixel art into a sprite with the Sprite Maker
- [ ] Show an Actor and move it with an event handler

## Lab notebook

Glue in the sprite design on squared paper, with its letters next to it.
Draw the window with its corner coordinates. Add *sprite*, *Actor*,
*frame* and *event handler* to the dictionary.

## Guide's background *(optional reading)*

Pygame Zero is a beginner-friendly layer on top of **Pygame**, a widely
used Python games library. It handles the boring parts (opening a window,
running the game loop, loading pictures) so the learner writes only the
interesting parts: what to draw, what happens each moment, and what to do
when a key is pressed or the mouse is clicked.

That's a different style from everything so far. Before, the program ran
from top to bottom and asked for input when *it* wanted. Now the program
mostly sets things up, then waits: Pygame Zero runs the loop and calls the
learner's functions when it's time to draw, or when something happens.
This is **event-driven programming**, and it's how almost all apps,
websites and games work.

The y-down coordinate system comes from how screens were drawn by
electron beams in old TVs: top line first, left to right. Almost every
graphics system except maths-style ones (like turtle) uses it.

The Sprite Maker is a small tool in this repository
(`labs/sprite-maker/`). It writes PNG files using only Python's standard
library, so no extra software or downloads are needed. Any PNG works as a
sprite, though, so a learner who likes drawing can use a paint program
instead.
