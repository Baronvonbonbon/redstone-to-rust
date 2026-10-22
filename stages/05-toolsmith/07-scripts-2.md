# Lesson 5.7: Shell Scripts, Part 2: Decisions, Loops and Backups

**Time:** 2 sessions of 45 min · **You need:** a terminal on the family
computer; the `~/bin` folder from Lesson 5.6 · **New words:** exit code,
condition, loop, backup, restore

## Goal *(read this to the learner)*

> Your commands can talk and roll dice. Now they'll make decisions, repeat
> things, and do a real job: a **backup** command that saves a copy of all
> your work, with the date in its name. Then you'll do a fire drill:
> pretend your work is lost, and get it back.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Optional: a USB stick, to keep a copy of the backups somewhere
      else (step 9).

## Warm-up (5 min)

"How do you write `if` in Python? A loop that repeats for each thing in a
list?" *(`if ...:` and `for x in list:`.)* "Bash can do both, with
different punctuation."

## Activity

### Session 1: did it work?

1. **Every command answers a secret question.** In the terminal:
   ```
   ls ~
   echo $?
   ls ~/no-such-thing
   echo $?
   ```
   **They should see:** `0` after the `ls` that worked, then an error and
   `2`.

   **Say:** "When a command finishes, it gives back a number called its
   **exit code**. `$?` shows the last one. **0 means success**, and
   anything else means something went wrong. Scripts use this to decide
   what to do next."

2. **And, or.**
   ```
   mkdir -p ~/lab/test && echo "Made it!"
   cat ~/nope.txt || echo "No such file, but that's OK."
   ```
   **Say:** "`&&` means 'and then, *only if that worked*'. `||` means 'or
   else, *only if that failed*'. It's AND and OR again, from Stage 4!"

3. **`if` in a script.** Make `~/bin/whatsthat`:
   ```bash
   #!/bin/bash
   # whatsthat: says whether something is a file, a folder, or missing.
   if [ -f "$1" ]; then
       echo "$1 is a file."
   elif [ -d "$1" ]; then
       echo "$1 is a folder."
   else
       echo "There's no $1 here."
   fi
   ```
   `chmod +x ~/bin/whatsthat`, then try `whatsthat ~/lab`,
   `whatsthat ~/lab/facts.txt` and `whatsthat dragon-egg`.

   **Say:** "`[ -f "$1" ]` is a test: 'is `$1` a file?'. `-d` asks 'is it a
   folder?'. `[` is actually a command, and its answer is an exit code,
   which is what `if` checks."

4. **Comparing numbers.** Make `~/bin/bigger`:
   ```bash
   #!/bin/bash
   # bigger: which of two numbers is bigger?
   if [ "$1" -gt "$2" ]; then
       echo "$1 is bigger."
   elif [ "$1" -lt "$2" ]; then
       echo "$2 is bigger."
   else
       echo "They're the same."
   fi
   ```
   Try `bigger 64 16`, `bigger 3 7` and `bigger 5 5`. **Say:** "For numbers,
   bash uses words: `-gt` is greater than, `-lt` less than, `-eq` equal.
   That's because `>` already means 'send output to a file'!"

### Session 2: loops and backups

5. **`for` loops.** In the terminal:
   ```
   for mob in creeper zombie skeleton; do echo "Watch out for the $mob!"; done
   for n in $(seq 1 5); do echo "Level $n"; done
   ```
   **They should see:** three warnings, then Level 1 to Level 5.

   And over files:
   ```
   for f in ~/lab/python/*/*.py; do echo "$(wc -l < "$f") lines in $f"; done
   ```
   **They should see:** a line for each Python program from Stages 2 to 4,
   with its length. **Say:** "That's a loop over every file that matches
   the wildcard."

6. **A `while` loop.** Make `~/bin/countdown`:
   ```bash
   #!/bin/bash
   # countdown: counts down from a number (10 if you don't give one).
   n=${1:-10}
   while [ "$n" -gt 0 ]; do
       echo "$n"
       sleep 1
       n=$((n - 1))
   done
   echo "Liftoff!"
   ```
   Try `countdown 3`. **Say:** "Same as Python's `while`: keep going while
   the test is true."

7. **The backup command.** **Say:** "Here's a tool you'll actually use.
   What if the computer broke tomorrow? All your programs and notes would
   be gone. A **backup** is a copy kept somewhere safe." Make `~/bin/backup`:
   ```bash
   #!/bin/bash
   # backup: saves a copy of ~/lab, with today's date in the name.
   mkdir -p ~/backups
   name=~/backups/lab-$(date +%Y-%m-%d).tar.gz
   tar -czf "$name" -C ~ lab
   echo "Saved $name ($(du -h "$name" | cut -f1))"
   ```
   `chmod +x ~/bin/backup`, then `backup`. **They should see:** something
   like `Saved /home/sam/backups/lab-2026-10-29.tar.gz (64K)`.

   **Say:** "It's the `tar -czf` from Mineshaft level 11, the other way
   round: making a buried treasure instead of digging one up. `-C ~ lab`
   means 'go to the home folder, and pack up `lab`'. `date +%Y-%m-%d` makes
   the date with the year first, so the backups sort in order."

   Look inside: `tar -tzf ~/backups/lab-*.tar.gz | head`.

8. **The fire drill.** **Say:** "A backup you've never tested isn't a
   backup. Let's pretend everything was lost, and get it back." Restore it
   into a scratch folder (*not* over the real one):
   ```
   cd "$(mktemp -d)"
   tar -xzf ~/backups/lab-*.tar.gz
   ls lab
   diff -r ~/lab lab && echo "The backup matches perfectly!"
   ```
   **They should see:** the folders from `~/lab`, then `The backup matches
   perfectly!`. **Say:** "`diff -r` compares two folders, every file inside.
   No differences, so the backup is good."

   (If `diff` shows differences, something changed since the backup, which
   is fine. Make a new backup and try again.)

9. **Keep it safe.** **Say:** "A backup on the same computer is lost if
   the computer is lost." If there's a USB stick, copy `~/backups` onto it
   together (the guide may need to help, as the stick appears under
   `/media`). Make it a habit: `backup` at the end of every week.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `[: : integer expression expected` | `bigger` was run without numbers | Give it two numbers: `bigger 3 7`. |
| `[: abc: integer expression expected` | A word was given where a number was needed | Use whole numbers with `-gt` and `-lt`. |
| ``syntax error near unexpected token `echo'`` | `do` is missing from the loop | It's `for x in a b c; do ...; done`. |
| The countdown never ends | `n=$((n - 1))` is missing | Every loop needs something that changes, like in Python. |
| `tar: lab: Cannot stat: No such file or directory` | The `-C ~` part is missing or mistyped | It's `tar -czf "$name" -C ~ lab`. |
| `ls: cannot access 'lab': No such file or directory` in the fire drill | `tar -xzf` wasn't run in the scratch folder | `cd "$(mktemp -d)"` first, then `tar -xzf`. |
| Two backups with the same name | Both made on the same day | The second one replaces the first. That's fine. |

## Talk about it

- What does an exit code of 0 mean?
- What's the difference between `&&` and `||`?
- Why do we test backups?
- Why should a backup live somewhere else too?

## Challenge *(if there's time, or for next time)*

- Make `backup` keep only the newest five backups. *(Hint: `ls -t
  ~/backups` lists newest first; `tail -n +6` gives everything after the
  fifth.)*
- A bash guessing game: `$RANDOM`, `read`, and a `while` loop until it's
  right. Compare it with your Python one from Lesson 3.2. Which is easier
  to read?
- `whatsthat` for several things at once: loop over `"$@"`, which means
  "all the arguments".

## Checkpoint

The learner can, without help:
- [ ] Check an exit code with `$?`, and use `&&` and `||`
- [ ] Write a script with `if`, `elif` and `else`, using `-f`, `-d`, `-gt`
- [ ] Write `for` and `while` loops in bash
- [ ] Make a backup, and prove it works by restoring it somewhere else

## Lab notebook

Copy the backup script and explain each line. Write the date of the
first fire drill. Add *exit code*, *condition*, *loop*, *backup* and
*restore* to the dictionary.

## Guide's background *(optional reading)*

Exit codes are how Unix programs report success or failure, and they're
the basis of every `if`, `&&` and `||` in the shell. `[` is a real
program (also called `test`), which is why it needs spaces around it.

The backup script is deliberately simple: a dated, compressed copy of
`~/lab`. The fire drill (restore, then compare with `diff -r`) is the
habit that matters most. Professional system administrators say "you
don't have a backup until you've restored it", and many have learned it
the hard way.

From Lesson 5.9, the learner's work also lives in git, which is a
different kind of safety: git remembers every version, but if the whole
folder is lost, so is its history. Backups and version control together
cover both cases.
