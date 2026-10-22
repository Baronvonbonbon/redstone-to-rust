# Lesson 1.2: Where Am I?

**Time:** 40 min · **You need:** the learner's account, with the `lab` folder
and the folders from Lesson 0.5 inside it · **New words:** directory,
current directory, path, home

## Goal *(read this to the learner)*

> In Lesson 0.5 you clicked through folders. Now you'll walk through them
> by typing, like exploring a dark cave with just three magic spells:
> **where am I?**, **what's here?** and **go there**.

## Before the lesson *(guide, 5 min)*

- [ ] Check that the learner's `lab` folder has `art` and `stories` in it
      (from Lesson 0.5). If not, make them in the Files app.
- [ ] Have paper ready to draw a map.

## Warm-up (5 min)

"In Lesson 0.5, what was a path? *(Directions through the folder boxes.)*
Today we'll walk those paths by typing."

## Activity

1. **Where am I?** Open the terminal.
   ```
   pwd
   ```
   **They should see:** `/home/sam` (with their own name).
   **Say:** "`pwd` means **P**rint **W**orking **D**irectory. 'Directory' is
   the grown-up word for folder. You're standing in your home folder."

2. **What's here?**
   ```
   ls
   ```
   **They should see:** a list including `lab`, `Documents`, `Pictures`...
   "`ls` is short for **l**i**s**t. It's like switching on a torch in the cave."

3. **Go there.**
   ```
   cd lab
   pwd
   ls
   ```
   **They should see:** `/home/sam/lab`, then `art  stories` (and anything
   else they made). "`cd` means **c**hange **d**irectory. You walked
   into `lab`!" Point out that the prompt changed too: `~/lab$`.

4. **Go deeper, then back up.**
   ```
   cd stories
   ls
   cd ..
   pwd
   ```
   **Say:** "`..` means 'the folder I'm inside of', one step back up
   towards the top. Like climbing back up a ladder."

5. **The magic way home.**
   ```
   cd ~
   pwd
   ```
   `~` (called **tilde**, the squiggle) always means "my home folder". And
   plain `cd` on its own goes home too.

6. **Long jumps.** Instead of one step at a time:
   ```
   cd ~/lab/stories
   pwd
   ```
   One command, straight there.

7. **Climb to the very top.**
   ```
   cd /
   ls
   ```
   "This is the **root**, the very top of the whole computer's folder tree.
   Every file on the computer is somewhere down here." Peek in a couple:
   `ls /home` (everyone's home folders), `ls /usr/games` (where cowsay lives!).
   Then go home with `cd`.

8. **Draw the map.**
   ```
   cd ~/lab
   tree
   ```
   `tree` draws the folders as a tree. They copy it onto paper.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `cd: lab: No such file or directory` | There's no `lab` folder *where they're standing* | Run `pwd` and `ls`. Are you where you think? `cd ~` to go home first. |
| `cd: Lab: No such file or directory` | Capital letters matter! `Lab` and `lab` are different | Type exactly what `ls` shows. |
| `cd: too many arguments` | A space in the folder name | Use folder names without spaces (Lesson 1.7 shows how to handle them). |
| `cd ..` didn't seem to work | It did! You moved up one level | Run `pwd` to check. |

## Talk about it

- Which three commands are your torch, your feet and your map? *(`ls`, `cd`, `pwd`.)*
- What does `..` mean? What does `~` mean? What does `/` at the very start mean?
- If you're lost, what's the fastest way home? *(`cd`)*

## Challenge

**Cave tour.** You call out a destination; they get there using as few
commands as possible:
- "Go to `stories`." *(`cd ~/lab/stories`)*
- "Now go to `art`, in one command." *(`cd ../art`)*
- "Now go to the root, then back to `art`." *(`cd /`, then `cd ~/lab/art`)*

## Checkpoint

The learner can, without help:
- [ ] Use `pwd` to say where they are
- [ ] Use `cd` with a folder name, with `..` and with `~`
- [ ] Get home from anywhere

## Lab notebook

Add `pwd`, `ls`, `cd`, `cd ..`, `cd ~` and `tree` to the command dictionary.
Copy the `tree` map of `lab`.

## Guide's background *(optional reading)*

The shell always has a **current directory**, the folder you're "standing
in". `ls` lists it, and commands that use file names look there first.
Paths that start with `/` are **absolute** (they start from the very top);
paths without one are **relative** (they start from where you are now).
`..` means "the parent folder". Getting used to "where am I?" is half
the battle in the terminal. When anything seems strange, `pwd` and `ls`
are always the first move.
