# Lesson 5.5: Vim, the Editor That Never Dies

**Time:** 2 sessions of 40 min · **You need:** a terminal; `vim` (installed
by setup) · **New words:** editor, mode, normal mode, insert mode, command

## Goal *(read this to the learner)*

> Programmers have a famous joke: "How do you get out of vim?" Vim is a
> text editor from 1991 (and its grandparent, vi, is from 1976), and it's
> on almost every Linux computer in the world, including tiny ones with no
> screen. It's strange at first, because the keys do different things in
> different **modes**. But once you know it, your hands never leave the
> keyboard. Today you'll learn enough vim to edit any file, anywhere, and,
> most importantly, how to get out!

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Run `vimtutor` yourself for 10 minutes (lessons 1.1 to 1.6), so
      you've felt the modes.

## Warm-up (5 min)

"What editors have you used in the terminal?" *(nano.)* "How do you save
and quit in nano?" *(Ctrl+O, Enter, Ctrl+X.)* **Say:** "Nano shows its keys
at the bottom. Vim doesn't show you anything. That's why we need a map."

## Activity

### Session 1: modes, and escaping

1. **The escape plan first.** On a card, write and keep next to the
   keyboard:

   ```
   ESCAPE FROM VIM
   Esc   then   :q!   then Enter     quit and throw away changes
   Esc   then   :wq   then Enter     save (write) and quit
   ```

   **Say:** "Whatever happens, pressing **Esc** and typing `:q!` gets you
   out. You're never trapped."

2. **Open vim.** In the terminal:
   ```
   mkdir -p ~/lab/vim
   cd ~/lab/vim
   vim hello.txt
   ```
   **They should see:** an empty screen with `~` down the left side (those
   mean "no line here"), and the file name at the bottom.

3. **Modes.** Type `hello`. **They should see:** probably nothing sensible:
   vim takes `h` as "move left", `e` as "jump to the end of a word", and
   so on. **Say:** "Vim starts in **normal mode**, where keys are
   *commands*, not letters. To type words, you go into **insert mode** by
   pressing `i`."

   Press `i`. **They should see:** `-- INSERT --` at the bottom. Now type
   `Hello from vim!` and a few more lines. Press **Esc**. The `-- INSERT
   --` goes away: back in normal mode.

4. **Save and quit.** Type `:wq` and press Enter. **They should see:** the
   terminal again. Check: `cat hello.txt`.

   **Say:** "`:` starts a **command**. `w` means write (save) and `q` means
   quit. `:w` saves and stays; `:q!` quits without saving: the `!` means
   'yes, I'm sure'."

5. **The vim tutor.** Vim comes with its own lessons:
   ```
   vimtutor
   ```
   Do **Lesson 1** (sections 1.1 to 1.6) together. It teaches moving with
   `h j k l`, deleting with `x`, inserting with `i` and `A`, and saving.
   The tutor is just a text file, so it's safe to change anything.

### Session 2: getting quick

6. **Finish vimtutor Lessons 2 and 3.** Take turns: one reads the
   instructions, the other does them. The big ones to remember:

   | Keys (in normal mode) | What they do |
   |---|---|
   | `h` `j` `k` `l` | left, down, up, right |
   | `w` `b` | next word, back a word |
   | `0` `$` | start of the line, end of the line |
   | `x` | delete one character |
   | `dw` `dd` | delete a word, delete a whole line |
   | `u` | undo (press it again to undo more) |
   | `Ctrl+R` | redo |
   | `p` | paste what was last deleted |
   | `o` | make a new line below, and go into insert mode |
   | `/word` then Enter | search for "word"; `n` finds the next one |

   **Say:** "Look how commands combine: `d` means delete, `w` means word,
   so `dw` is 'delete word'. `3dd` deletes three lines. Vim is like a
   language: verbs and nouns."

7. **The vim race.** Make a practice file:
   ```
   seq 1 20 > numbers.txt
   vim numbers.txt
   ```
   Race the guide (who uses the arrow keys and mouse in nano, if they
   like) to: delete line 5, move line 10 to the end (`dd`, then `G` to go
   to the last line, then `p`), and change `20` to `twenty`
   (`/20`, Enter, `cw`, type `twenty`, Esc). Save and quit.

8. **Choose your editor.** **Say:** "From now on you can use nano *or*
   vim. Many programmers use vim forever; many use something else. What
   matters is that if you're ever on a strange computer with no other
   editor, you won't be stuck." If the learner likes vim, set it for git
   (Lesson 5.9) later with `git config --global core.editor vim`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Letters do strange things, lines vanish | You're in normal mode, typing commands | Press `u` a few times to undo, then `i` to type. |
| `E37: No write since last change (add ! to override)` | `:q` won't quit because there are unsaved changes | `:wq` to save, or `:q!` to throw them away. |
| `E212: Can't open file for writing` | You can't save in that folder (permissions!) | `:q!`, then open a file in your own folder. |
| `-- INSERT --` won't go away | Esc wasn't pressed, or the window lost focus | Click on the terminal, then press Esc. |
| A strange line at the bottom starting with `q:` or a split screen | `q:` opens the command history window | Press `:q` and Enter to close that window. |
| `Found a swap file by the name ".hello.txt.swp"` | Vim was closed suddenly last time | Press `d` to delete the swap file (if offered), or `q` to quit, then delete it: `rm .hello.txt.swp`. |

## Talk about it

- What are vim's two main modes, and how do you switch?
- How do you always get out of vim?
- Why might someone choose vim, even though it's harder at first?

## Challenge *(if there's time, or for next time)*

- In normal mode, `.` repeats the last change. Delete a word with `dw`,
  then press `.` five times.
- `:set number` shows line numbers. `:help` opens vim's own manual (`:q`
  to close it).
- Make vim show line numbers every time: put `set number` in a file
  called `~/.vimrc`.

## Checkpoint

The learner can, without help:
- [ ] Open a file in vim, add text, save and quit
- [ ] Quit without saving, from any mode
- [ ] Move with `h j k l`, delete with `x` and `dd`, and undo with `u`
- [ ] Explain normal mode and insert mode

## Lab notebook

Copy the "escape from vim" card. Write the five vim keys they like
best. Add *editor*, *mode*, *normal mode* and *insert mode* to the
dictionary.

## Guide's background *(optional reading)*

Vim ("vi improved") descends from `vi`, written by Bill Joy in 1976 for
terminals so slow that every keystroke counted. Its "modal" design means
letters can be commands, which makes editing fast once learned. Some form
of vi is on nearly every Unix-like system, including routers, servers
and the Raspberry Pi, which is why it's worth knowing the basics even for
people who prefer other editors.

`vimtutor` is about 30 minutes of hands-on lessons in a temporary copy of
a text file, and it's the best way to learn. Spreading it over two
sessions works well.

The Sandbox (Lesson 5.1) has `vim` and `nano` too, so the learner can
practise there.
