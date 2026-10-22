# Lesson 1.1: The Magic Talking Box

**Time:** 30–40 min · **You need:** the learner logged into their account ·
**New words:** terminal, command, prompt, shell

## Goal *(read this to the learner)*

> Real hackers don't click. They **type commands**, and the computer obeys
> instantly. Today you'll open the **terminal**, the magic talking box,
> and make the computer talk, draw giant letters, and drive a steam train
> across your screen.

## Before the lesson *(guide, 5 min)*

- [ ] Log in as the learner, open the terminal (Super key, type
      `terminal`, press Enter) and type `cowsay hi`. If you see a cow, you're
      ready. If you see "command not found", run `./scripts/install-packages.sh`
      from your own account.
- [ ] Make the text big: in the terminal, press **Ctrl** and **+** a few
      times. Bigger text means fewer typos.

## Warm-up (5 min)

"Remember the sandwich robot? The terminal is a robot that only
understands typed instructions, called **commands**. Spell them
*exactly*, or it won't understand."

## Activity

1. **Open the terminal.** Super key, type `terminal`, press Enter. Point
   at the line that looks something like this:

   ```
   sam@pop-os:~$
   ```

   **Say:** "This is the **prompt**. The computer is asking 'What do you
   want?' It shows your name, the computer's name, and where you are.
   The `$` means 'your turn'."

2. **The first command.** **Learner types** (then presses Enter):
   ```
   echo hello
   ```
   **They should see:** `hello`. "`echo` makes the computer repeat you,
   like an echo in a cave." Try `echo I like pizza`.

3. **The talking cow.**
   ```
   cowsay Moo! I am a computer cow.
   ```
   A cow says it! Now try other animals:
   ```
   cowsay -f dragon I breathe fire
   cowsay -f tux Hello from the Linux penguin
   cowsay -l
   ```
   `cowsay -l` lists every animal. Let them try a few.
   **Say:** "That `-f` part is called an **option**. It changes how the
   command works."

4. **Giant letters.**
   ```
   figlet SAM
   ```
   (Use their name.) Try `figlet -f slant ROCKET` too.

5. **The train.**
   ```
   sl
   ```
   A steam train drives across the screen! (It's a joke: `sl` is what
   happens when you mistype `ls`, which they'll learn next lesson. This
   train can't be stopped, so just wait.)

6. **Make a mistake on purpose.**
   ```
   cowsya hello
   ```
   **They should see:** `Command 'cowsya' not found, did you mean: command
   'cowsay'...`. **Say:** "The computer doesn't know 'cowsya'. Not a
   disaster! It even guessed what you meant. Errors are the computer
   *helping* you."

7. **Tidy up and leave.**
   ```
   clear
   ```
   That wipes the screen. Then:
   ```
   exit
   ```
   That closes the terminal. Open it again, so they practise finding it.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `command not found` | A typo, or the program isn't installed | Read the command out loud, letter by letter. Spaces matter too. |
| Nothing happens after typing | They didn't press Enter | Press Enter. Commands run when you press Enter. |
| A `>` prompt appears instead of `$` | They typed a quote mark `"` or `'` and didn't close it | Press **Ctrl+C** to escape, and try again. |
| Text is too small | | Ctrl and + makes it bigger; Ctrl and − makes it smaller. |

## Talk about it

- What's the prompt? What does `$` mean? *(It's your turn to type.)*
- What does `echo` do?
- What's an option? *(Something like `-f dragon` that changes how a
  command works.)*
- What happened when you spelled a command wrong? Did anything break?
  *(No! It just said it didn't understand.)*

## Challenge

- Make a dragon say your name in giant letters (try `figlet` alone first).
  You can't quite combine them yet; you'll learn how in Lesson 1.10!
- Try `toilet -f mono12 HI` (yes, that's really a program's name: it's a
  fancier figlet). And `sl -F`.

## Checkpoint

The learner can, without help:
- [ ] Open the terminal, and run `echo`, `cowsay` and `figlet`
- [ ] Explain what the prompt is
- [ ] Read a "command not found" error and fix their typo

## Lab notebook

Start a **command dictionary** at the back of the notebook: one line per
command, with what it does in their own words.
- `echo`: says back what I type
- `cowsay`: makes an animal say something
- `figlet`: GIANT letters
- `clear`: wipes the screen
- `exit`: closes the terminal

## Guide's background *(optional reading)*

The **terminal** is the window, and inside it runs a program called the
**shell** (here it's **bash**), which reads what you type and runs it.
Typing commands seems old-fashioned, but most programmers and almost
every server on the internet are driven this way. It's precise,
repeatable, and can be automated. Everything from here to the end of the
course uses the terminal.

`cowsay`, `figlet` and `sl` are classic joke programs. They're here so
the very first experience of the terminal is *fun*.
