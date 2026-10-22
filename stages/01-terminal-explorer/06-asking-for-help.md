# Lesson 1.6: Asking for Help

**Time:** 30–40 min · **New words:** manual, usage, option, argument

## Goal *(read this to the learner)*

> Nobody remembers every command and every option, not even experts. They
> know how to **ask the computer for help**. Today you'll learn to read
> the computer's own instruction books, and find superpowers no one
> taught you.

## Before the lesson *(guide, 5 min)*

- [ ] Try `man ls` yourself, scroll with the arrow keys, and quit with `q`.

## Warm-up (5 min)

"What does Ctrl+C do? What does Tab do?"

## Activity

1. **`--help`.** Most commands explain themselves:
   ```
   cowsay --help
   ```
   Read the **usage line** together. Something like
   `cowsay [-e eyes] [-f cowfile] ... [message]`. **Say:** "Things in
   `[square brackets]` are optional. `-e` is an option to change the eyes!"
   ```
   cowsay -e OO Whoa
   cowsay -e ^^ Happy
   ```

2. **When the help is long.** `ls --help` is LONG and zooms off the
   screen. Scroll up with the mouse wheel, or Shift+PageUp. Find the line
   about `-S` *(sort by file size)* and try it: `ls -S /usr/bin | head`.
   *(`| head` shows just the top of the list; pipes are coming in Lesson 1.10!)*

3. **The manual.**
   ```
   man figlet
   ```
   A whole manual page. **How to drive it:**
   - **↑ ↓** or **Space**: scroll
   - **/word** then **Enter**: search for a word; **n** finds the next one
   - **q**: quit

   Search for `/-c` to find the "center" option, then quit and try:
   ```
   figlet -c Middle
   ```

4. **The manual for the manual.** `man man`. Just look at the top
   section, then **q**.

5. **One-line summaries.**
   ```
   whatis ls
   whatis cowsay
   whatis cat
   ```

6. **Words to know.** In `cowsay -f dragon hello`:
   - `cowsay` is the **command**
   - `-f dragon` is an **option** (`-f`) with its value (`dragon`)
   - `hello` is an **argument**: the thing the command works on

7. **Help hunt.** Using only `--help` or `man`, find out how to:
   - make `ls` show sizes like `4.0K` instead of `4096` *(`ls -lh`)*
   - make `cat` number the lines *(`cat -n`)*
   - make `mkdir` print what it made *(`mkdir -v`)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Stuck in a manual page | | Press **q**. |
| `No manual entry for x` | That command has no manual | Try `x --help` instead. |
| Too many words, overwhelmed | Totally normal; manuals are written for adults | Read just the NAME, SYNOPSIS and the first lines of DESCRIPTION. Search for the word you care about with `/`. |

## Talk about it

- What are two ways to get help about a command?
- How do you get out of a manual? *(q)*
- What's an option? What's an argument?

## Challenge

Find three `cowsay` options that weren't in this lesson, and show off
each one. *(For example: `-t` thought bubble, `-d` dead, `-g` greedy, `-y` young,
`-w` wired.)*

## Checkpoint

The learner can, without help:
- [ ] Use `--help` to find an option they didn't know, and use it
- [ ] Open a `man` page, search it with `/`, and quit with `q`

## Lab notebook

Add `--help`, `man`, `whatis`, and the man-page keys (`/`, `n`, `q`) to the
command dictionary. Write down one option you discovered on your own.

## Guide's background *(optional reading)*

Being able to find answers on your own is one of the most valuable skills
in computing, and this course is offline on purpose to build exactly
that habit. Manual pages are terse and written for adults; the skill
isn't reading the whole thing, it's *searching* (with `/`) for the one
part you need.

A note on cowsay: the `-s` eyes option is named after a drug joke. If the
learner finds it, it's simply a chance for an honest, age-appropriate
word about it.
