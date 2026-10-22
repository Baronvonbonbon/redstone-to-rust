# Lesson 1.14: Into the Mineshaft

**Time:** 45–60 min · **You need:** the Mineshaft running
([SETUP.md](../../docs/SETUP.md), step 5), the printed
[Hacker's Pledge](../../docs/HACKER-PLEDGE.md), and the
[passport](../../PASSPORT.md) · **New words:** server, SSH, remote,
wargame, host

## Goal *(read this to the learner)*

> There's a secret computer hidden inside this one: the **Mineshaft**.
> It has 20 levels, each one deeper underground. On every level, a
> password for the next one is hidden somewhere, and you'll need all your
> terminal skills to dig it out. Real hackers practise on games exactly
> like this, called **wargames**. But first: the Hacker's Pledge.

## Before the lesson *(guide, 10 min)*

- [ ] From **your** account, in `labs/mineshaft/`:
      `./mineshaft.sh status` should say "Up". If it doesn't:
      `./mineshaft.sh start`.
- [ ] Read [labs/mineshaft/README.md](../../labs/mineshaft/README.md) (the
      guide's handbook, with hints and solutions for every level).
- [ ] `./mineshaft.sh answers` shows all the passwords, in case you need
      to rescue a level. Keep them private.

## Warm-up: the Hacker's Pledge (10 min)

Read [the Pledge](../../docs/HACKER-PLEDGE.md) together, one rule at a
time. Ask "Why do you think that rule matters?" for each one. Sign it,
and put it up on the wall.

**Say:** "The Mineshaft is *yours*. It's made for breaking into. That's
what makes it okay. The same tricks on someone else's computer would be
wrong, and against the law."

## Activity

1. **What is SSH?** **Say:** "SSH lets you type commands on a *different*
   computer, as if you were sitting at it. Its name means **S**ecure
   **SH**ell. The Mineshaft is a little computer running inside this one,
   and you'll SSH into it."

2. **Two terminals.** Open **two** terminal windows side by side.
   - **Left: HOME.** Your own computer, for notes.
   - **Right: MINESHAFT.** For digging.

3. **The first connection** (right terminal):
   ```
   ssh miner0@localhost -p 2220
   ```
   - `miner0`: the account name on the Mineshaft
   - `localhost`: "this same computer"
   - `-p 2220`: the door number (called a **port**) the Mineshaft listens on

   The first time, it asks:
   `Are you sure you want to continue connecting (yes/no/[fingerprint])?`
   They type `yes` and press Enter. ("SSH is checking it's the real
   Mineshaft, not an impostor.")

   Then it asks for the password: `miner0`. **Nothing shows up while
   typing**, not even dots! "That's on purpose, so nobody can count the
   letters. Just type it and press Enter."

4. **Look at the prompt.** It now says `miner0@mineshaft:~$`. **Say:**
   "Look at the name! You're inside the Mineshaft now. Commands you type
   here run on *that* computer."

5. **Level 0.**
   ```
   cat GOAL.txt
   ```
   Every level has a `GOAL.txt`. Read it, then do it: `cat readme`.
   The password for miner1 appears!

6. **Save the password** in the **left (HOME)** terminal:
   ```
   echo "miner1 the-password-here" >> ~/lab/mineshaft.txt
   ```
   (Use copy and paste: select it, Ctrl+Shift+C, then Ctrl+Shift+V.)
   **Say:** "Game passwords are fine to save in a file. Real passwords
   *never* go in files like this."

7. **Next level.** In the right terminal: `exit` (you're back on your own
   computer; look at the prompt!), then:
   ```
   ssh miner1@localhost -p 2220
   ```
   Paste miner1's password. `cat GOAL.txt`. Dig!

8. **Levels 1 to 4.** The learner plays; you ask questions. Each one uses
   a skill from this stage:

   | Level | The skill it needs | From lesson |
   |---|---|---|
   | 1 | `cd` into a folder, then `cat` | 1.2 |
   | 2 | A file name with a space (quotes, or Tab) | 1.7 |
   | 3 | A hidden file (`ls -a`) | 1.7 |
   | 4 | `file`, a new command: the goal explains it | (new!) |

   After each level: save the password, shade it in on the passport, and
   celebrate.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Connection refused` | The Mineshaft isn't running | From your account: `labs/mineshaft/mineshaft.sh start` |
| `Permission denied, please try again.` | Wrong password | Copy and paste it instead of typing. Check the level number in the `ssh` command. |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | You ran `mineshaft.sh reset`, so it's a "new" Mineshaft | In the learner's terminal: `ssh-keygen -R "[localhost]:2220"`, then connect again. |
| `touch: cannot touch 'x': Permission denied` | Mineshaft home folders are read-only on purpose | Nothing needs saving there. Notes go in the HOME terminal. |
| Typed a command in the wrong terminal | | Check the prompt: `miner3@mineshaft` or `sam@pop-os`? |

## Talk about it

- What does SSH do?
- How can you tell which computer you're typing on? *(The prompt.)*
- Why do the Pledge rules matter even more now?

## Challenge

Run `ls /home` inside the Mineshaft. You can *see* the other levels'
folders. Try `ls /home/miner5`. *(Permission denied! Each level is locked
to its own miner.)* Why do you think it's built like that?

## Checkpoint

The learner can, without help:
- [ ] Log into the Mineshaft with `ssh`, and log out with `exit`
- [ ] Tell from the prompt which computer they're on
- [ ] Pass levels 0 to 4

## Lab notebook

Draw two computers with an SSH "tunnel" between them. For each level,
write: the level number, the command that cracked it, and one word about
how it felt.

## Guide's background *(optional reading)*

The Mineshaft is this course's own version of **OverTheWire's Bandit**,
the most famous beginner wargame, but it runs entirely on your computer
(in a Docker container), and needs no internet and no accounts. Every
level is a separate user on a tiny Linux system, with permissions set up
so you can only read your own level's files. SSH is how real servers are
managed all over the world, and the learner just used it.

Levels 0 to 9 belong to Stage 1. Levels 10 to 19 need Stage 5 skills (and
level 19 needs Python!), so they come later. Don't push past level 9 yet.
