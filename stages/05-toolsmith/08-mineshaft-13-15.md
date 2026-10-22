# Lesson 5.8: The Mineshaft, Levels 13–15

**Time:** 1–2 sessions of 45 min · **You need:** the Mineshaft running;
`~/lab/mineshaft.txt`; the [guide's handbook](../../labs/mineshaft/README.md)
· **New words:** setuid, environment variable, `export`, `diff`

## Goal *(read this to the learner)*

> Three more levels, and each one uses something you learned this stage.
> A fussy door that's really a program with special permissions. A
> password hidden in the invisible notes every program carries. And two
> almost identical maps, where one line has changed.

## Before the lesson *(guide, 5 min)*

- [ ] Re-read levels 13 to 15 in the [guide's handbook](../../labs/mineshaft/README.md).
- [ ] Check the Mineshaft is up: `./mineshaft.sh status`.

## Warm-up (5 min)

"What does `echo $PATH` show?" *(The folders where the shell looks for
commands.)* "What's the `s` in `ls -l /usr/bin/passwd`?" *(A special
permission that lets the program do things with its owner's powers.)*
"How did you compare two folders in the fire drill?" *(`diff -r`.)*

## Activity

1. **Level 13: the door.** Log in as miner13 and read the goal. Then:
   ```
   ls -l door
   ./door
   ```
   **They should see:** `-rwsr-x--- 1 miner14 miner13 ... door` and
   `The door is locked. It has a sign: 'Try ./door --help'`.

   **Say:** "Look who owns the door: **miner14**, not you. And see the `s`
   where the owner's `x` would be? That's **setuid**: when anyone runs
   this program, it runs with its *owner's* powers. So the door can read
   miner14's password, even though you can't." Check:
   `cat /etc/mineshaft/pass/miner14` *(Permission denied)*.

   Now read the sign: `./door --help`. Experiment with the options until
   the door opens. (The door's replies are hints.)

   **Say:** "Setuid programs are powerful and dangerous: if one has a bug,
   anyone can borrow its owner's powers. `passwd` is setuid root, so
   ordinary users can change their own password. In Stage 8 you'll read the
   door's source code to see exactly how it works."

2. **Level 14: environment variables.** Log in as miner14 and read the
   goal. **Say:** "You've used some of these: `$USER`, `$HOME`, `$PATH`.
   They're **environment variables**: little labelled notes that every
   program is given when it starts." List them all:
   ```
   env
   ```
   Find the secret one by reading, then do it the Toolsmith way with a
   pipe: `env | grep` and a good word to search for. Or, if you know its
   name: `echo $NAME_OF_IT`.

   **Say:** "Where did it come from? Look at the end of `.bashrc`:
   `tail -3 ~/.bashrc`. An `export` line puts a variable into the
   environment, so every program started from this shell gets it. It's
   just like the `export PATH=...` line you added in Lesson 5.6!"

3. **Level 15: spot the difference.** Log in as miner15 and read the goal.
   Two maps, each 500 lines long (`wc -l *.txt`). Reading them both would
   take forever.
   ```
   diff old-map.txt new-map.txt
   ```
   **They should see:** something like:
   ```
   377c377
   < some-old-line
   ---
   > some-new-line
   ```
   **Say:** "`377c377` means 'line 377 was **c**hanged'. Lines starting with
   `<` are from the first file, `>` from the second. The password is the
   new line." Save it.

   **Say:** "Remember `diff`. In the next lesson, git uses exactly this
   way of showing changes, for every save you make."

4. **Stop at level 16.** Levels 16 to 18 come in Lesson 5.13, after the
   lessons on git and on processes and ports.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `bash: door: command not found` | The current folder isn't on the `PATH` | Run it as `./door`. |
| `...the door wants a different number of knocks.` | The number after `--knock` is wrong | Read `./door --help` again: it says how many. |
| `The door says: 'What's the magic word?'` | `--say` is missing | Give both options in the same command. |
| `env` shows nothing secret | Logged in as the wrong miner | `whoami` should say `miner14`. |
| `diff` shows nothing | The two names are the same file | `diff old-map.txt new-map.txt`, two different files. |

## Talk about it

- What does setuid let a program do? Why is it risky?
- What's an environment variable? Name three.
- How do you read the output of `diff`?

## Challenge *(if there's time, or for next time)*

- On the family computer: `export FAVOURITE_MOB=axolotl`, then
  `echo $FAVOURITE_MOB`. Open a *new* terminal and try again. Where did it
  go? *(Exported variables only last until the terminal closes, unless
  they're in `~/.bashrc`.)*
- `find /usr/bin -perm -4000` lists every setuid program on the family
  computer. How many are there? What do you think each one is for?
- Make two copies of a file, change one line, and `diff` them. Then try
  `diff -u`, the style git uses.

## Checkpoint

The learner can, without help:
- [ ] Explain setuid, and spot it in `ls -l`
- [ ] Find an environment variable with `env` and `grep`
- [ ] Read `diff` output and find what changed
- [ ] Reach Mineshaft level 16

## Lab notebook

Add levels 13 to 15 to the level log. Add *setuid*, *environment
variable*, *export* and *diff* to the dictionary.

## Guide's background *(optional reading)*

**Setuid** ("set user ID") is a permission bit that makes a program run
as its owner instead of as the person running it. It's how ordinary
users can do a few carefully controlled privileged things (`passwd`,
`sudo` itself). Because a bug in a setuid program hands out its owner's
powers, they're a favourite target in real security work; that's
exactly what the learner will study in Stage 8 by reading `door.c`.

The **environment** is a set of name=value strings that every process
inherits from the one that started it. That's how `PATH`, `HOME` and
`USER` reach every program. Secrets are often (unwisely) passed this
way too, which is the point of level 14.

`diff` output: `377c377` means line 377 of the first file changed into
line 377 of the second; `a` and `d` mean added and deleted. `diff -u`
("unified" format, with `-` and `+` lines) is what git shows.
