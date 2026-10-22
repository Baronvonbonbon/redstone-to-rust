# Lesson 3.10: Saving Things

**Time:** 2 sessions of 45 min · **You need:** Thonny; the learner's
`~/lab/jokes.txt` from Stage 1; `mobbook.py` from Lesson 3.8 · **New
words:** file, read, write, append, JSON, exception

## Goal *(read this to the learner)*

> Every program you've written forgets everything the moment it stops.
> The Mob Book forgets the new mobs you taught it, and the guessing game
> forgets your best score. Today your programs learn to **save things in
> files** and read them back, so they remember, even after you turn the
> computer off.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check `~/lab/jokes.txt` exists, with a few jokes, one per line.

## Warm-up (5 min)

"In the terminal, how do you make a file with something in it?"
*(`echo "hi" > file.txt`.)* "And add a line to the end?" *(`>>`.)* "How do
you read it?" *(`cat`.)* Python can do all three.

## Activity

### Session 1: reading and writing

1. **Write a file.** New file, `~/lab/python/stage3/diary.py`:
   ```python
   entry = input("What happened today? ")

   with open("diary.txt", "a") as f:
       f.write(entry + "\n")

   print("Saved! Here's the whole diary:")
   with open("diary.txt") as f:
       print(f.read())
   ```
   Run it two or three times, with different entries.

   **Say:** "`open` opens a file. The `"a"` means **append**: add to the
   end, like `>>` in the terminal. `"\n"` is the special character for
   'new line', like pressing Enter. With no letter, `open` is for reading.
   And `with` closes the file again automatically at the end of the
   indented block."

2. **Find it in the terminal.**
   ```
   cd ~/lab/python/stage3
   ls
   cat diary.txt
   ```
   **Say:** "It's a real file, the same kind you made in Stage 1. Python
   saves it in the folder it's running in. Here, that's the same folder as
   the program."

3. **Write, not append.** The letters for `open`:

   | Letter | Means | Like |
   |---|---|---|
   | (none) or `"r"` | read | `cat` |
   | `"w"` | write: **wipes the file first** | `>` |
   | `"a"` | append: add to the end | `>>` |

   **Say:** "Be careful with `"w"`: it empties the file before writing,
   with no 'are you sure?'."

4. **The joke machine, in Python.** New file, `jokes.py`:
   ```python
   import random
   from pathlib import Path

   jokes_file = Path.home() / "lab" / "jokes.txt"

   with open(jokes_file) as f:
       jokes = [line.strip() for line in f if line.strip()]

   print(f"I know {len(jokes)} jokes. Here's one:")
   print(random.choice(jokes))
   ```
   **Say:** "`Path.home()` is your home folder, wherever you run the program
   from, and `/` joins folder names into a path, just like in the terminal.
   The line in the middle is a shortcut for building a list: 'for every
   line in the file, if it isn't blank, keep it with the spaces and the
   new line trimmed off'." This is the same job as `shuf -n 1 jokes.txt`
   from Lesson 1.10.

### Session 2: remembering

5. **A high score.** Change `guess.py` from Lesson 3.2 to remember the best
   (lowest) number of guesses. Add near the top:
   ```python
   try:
       with open("best.txt") as f:
           best = int(f.read())
   except FileNotFoundError:
       best = None
   ```
   And at the end, after the `print` that says how many guesses it took:
   ```python
   if best is None or guesses < best:
       print("NEW BEST SCORE!")
       with open("best.txt", "w") as f:
           f.write(str(guesses))
   else:
       print(f"The best is still {best}.")
   ```
   **Say:** "The first time, there's no `best.txt` yet, and opening it would
   be an error. `try` means 'try this', and `except FileNotFoundError` means
   'if the file isn't there, do this instead'. An error like that is called
   an **exception**. And `None` means 'no best score yet'."

6. **The Mob Book remembers.** Python has a module called `json` that saves
   a whole dictionary to a file in one go. In `mobbook.py`, replace the
   `mobs = { ... }` dictionary with:
   ```python
   import json

   try:
       with open("mobs.json") as f:
           mobs = json.load(f)
   except FileNotFoundError:
       mobs = {
           "creeper": "sneaks up and explodes",
           "zombie": "groans, and burns in daylight",
       }
   ```
   And after the line `mobs[name] = info`, add:
   ```python
           with open("mobs.json", "w") as f:
               json.dump(mobs, f, indent=2)
   ```
   Run it, teach it a new mob, quit, and run it again. It remembers!

   Then in the terminal: `cat mobs.json`. **Say:** "Look, it's almost
   exactly what a Python dictionary looks like. This format is called
   **JSON**, and it's how lots of programs, games and websites save and
   send information. Minecraft uses it too."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `FileNotFoundError: [Errno 2] No such file or directory: 'diary.txt'` | Reading a file that doesn't exist yet, or running from a different folder | Write it first. In the terminal, `cd` to the program's folder before running it. Or use `try`/`except`. |
| The file is empty after running | Opened with `"w"` and then nothing was written, or the program crashed first | Use `"a"` to add. Check for errors. |
| Everything is on one line | The `"\n"` is missing | `f.write(entry + "\n")`. |
| `TypeError: write() argument must be str, not int` | Writing a number | Use `str(guesses)`. |
| `json.decoder.JSONDecodeError` | `mobs.json` was edited by hand and has a mistake, or is empty | Delete `mobs.json` and the program starts fresh. |
| `IndentationError` after adding `json.dump` | The new lines need to be indented inside the `else` part | Line them up with `mobs[name] = info`. |

## Talk about it

- Why do programs forget things when they stop? *(Variables live in the
  computer's memory, which is cleared when the program ends. Files are
  saved on the disk.)*
- What's the difference between `"w"` and `"a"`?
- What's an exception? What does `try`/`except` do?

## Challenge *(if there's time, or for next time)*

- **Safe number input:** a function `ask_number(question)` that keeps
  asking until the player types a real number, using `try` and
  `except ValueError`. Use it in your games from now on.
- Count the words in your jokes file, and find the longest joke.
- Add a "delete" command to the Mob Book (`del mobs[name]`), and save.
- Keep a list of the top 5 scores in a JSON file.

## Checkpoint

The learner can, without help:
- [ ] Write to a file and read it back
- [ ] Explain read, write and append, and what `"w"` does to an old file
- [ ] Use `try`/`except FileNotFoundError` for a file that might not exist
- [ ] Save a dictionary with `json` and load it again

## Lab notebook

Copy the table of `open` letters next to the matching terminal symbols
(`cat`, `>`, `>>`). Add *file*, *append*, *JSON* and *exception* to the
dictionary.

## Guide's background *(optional reading)*

A program's variables live in **memory** (RAM), which is fast but
forgotten when the program ends. **Files** live on the disk, which is
slower but permanent. Saving and loading is how every program bridges the
two: your documents, game saves and settings are all files.

**Exceptions** are Python's way of reporting that something went wrong
in a way the program might be able to handle: a missing file, bad input,
a lost network connection. `try`/`except` lets the program recover instead
of crashing. Catching the *specific* exception (like `FileNotFoundError`)
rather than every possible error is good practice, because it doesn't hide
real bugs.

**JSON** (JavaScript Object Notation) is the most common format for
saving and sending structured data. Its shapes (dictionaries, lists,
strings, numbers) match Python's almost exactly. Rust has the same idea in
its `serde_json` library, in Stage 9.

The list-building line in `jokes.py` is a **list comprehension**. It's
introduced here only as a recipe; the learner doesn't need to master it
yet.
