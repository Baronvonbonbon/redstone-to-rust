# Lesson 1.3: Making Things

**Time:** 40 min · **New words:** create, redirect, text editor

## Goal *(read this to the learner)*

> You can explore. Now you'll **build**: make folders, make files, write
> words into them, and read them back, all without touching the mouse.

## Before the lesson *(guide, 2 min)*

- [ ] Nothing special. The learner starts in their home folder.

## Warm-up (5 min)

"Show me how to get into `lab`. How do you check where you are?"

## Activity

1. **Make a folder.**
   ```
   cd ~/lab
   mkdir terminal-fun
   ls
   cd terminal-fun
   ```
   "`mkdir` = **m**a**k**e **dir**ectory."

2. **Make an empty file.**
   ```
   touch empty.txt
   ls
   ```
   "`touch` makes a new, empty file. (It's called touch because if the file
   already exists, it just 'touches' it to update its time.)"

3. **Write into a file with `>`.**
   ```
   echo Dragons are the best > dragons.txt
   ls
   cat dragons.txt
   ```
   **They should see:** `Dragons are the best`.
   **Say:** "The `>` arrow means 'don't show it on the screen, pour it into
   this file instead'. And `cat` shows what's inside a file." (`cat` is
   short for con**cat**enate, which means joining things together.)

4. **Careful! `>` replaces.**
   ```
   echo Unicorns are better > dragons.txt
   cat dragons.txt
   ```
   The dragons line is GONE. "One `>` throws away what was in the file."

5. **Add to a file with `>>`.**
   ```
   echo Dragons are the best > dragons.txt
   echo Dragons can fly >> dragons.txt
   echo Dragons like tacos >> dragons.txt
   cat dragons.txt
   ```
   Three lines! "`>>` (two arrows) **adds** to the end."

6. **The `nano` editor.** For writing lots of text:
   ```
   nano story.txt
   ```
   They type a short story (use the arrow keys to move around; no mouse).
   The help at the bottom: `^` means the **Ctrl** key.
   - **Ctrl+O**, then **Enter**: save ("**O**utput the file")
   - **Ctrl+X**: exit

   Then check:
   ```
   cat story.txt
   ```

7. **A jokes file** (they'll need this in Lesson 1.10!).
   ```
   nano ~/lab/jokes.txt
   ```
   Write 5 or more jokes, **one per line**. Save and exit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `mkdir: cannot create directory 'x': File exists` | It's already there | `ls` to see it. That's fine! |
| `cat: x: No such file or directory` | Wrong name, or the wrong folder | `ls` to check the spelling, and `pwd` to check where you are. |
| `cat: x: Is a directory` | You tried to `cat` a folder | Use `ls` for folders and `cat` for files. |
| Stuck in nano | | **Ctrl+X**. If it asks "Save modified buffer?", press **Y** then **Enter** to save, or **N** to throw away the changes. |
| Stuck at a blank screen after typing `cat` with no file | `cat` is waiting for typing | Press **Ctrl+C**. |

## Talk about it

- What's the difference between `>` and `>>`?
- What does `cat` do? What does `touch` do?
- When would you use `nano` instead of `echo`?

## Challenge

Make this whole tree using only commands, then check it with `tree`:
```
pets/
├── dogs/
│   └── names.txt   (3 dog names, one per line)
└── cats/
    └── names.txt   (3 cat names, one per line)
```
*(Hint: `mkdir -p pets/dogs` makes both folders at once.)*

## Checkpoint

The learner can, without help:
- [ ] Make a folder, and a file inside it, with some words written in
- [ ] Explain the difference between `>` and `>>`
- [ ] Open, edit, save and exit a file in `nano`

## Lab notebook

Add `mkdir`, `touch`, `cat`, `>`, `>>` and `nano` (plus Ctrl+O and Ctrl+X)
to the command dictionary.

## Guide's background *(optional reading)*

`>` is called **redirection**. Normally a command's output goes to the
screen; `>` sends it to a file instead. It's one of the shell's
building blocks, and pipes (Lesson 1.10) are its cousin. `nano` is a
simple text editor that runs inside the terminal. In Stage 5 the learner
will learn `vim`, a powerful editor that's harder to learn; `nano` is
perfect for now.
