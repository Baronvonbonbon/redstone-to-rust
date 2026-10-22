# Lesson 5.13: The Mineshaft, Levels 16–18

**Time:** 1–2 sessions of 45 min · **You need:** the Mineshaft running;
`~/lab/mineshaft.txt`; the [guide's handbook](../../labs/mineshaft/README.md)
· **New words:** gatekeeper, command line (of a process), commit history

## Goal *(read this to the learner)*

> Three levels, three of your new tools. A gatekeeper waiting behind a
> port. A careless miner who typed a password where everyone can see it.
> And a journal where someone deleted their password, not realising git
> remembers everything.

## Before the lesson *(guide, 5 min)*

- [ ] Re-read levels 16 to 18 in the [guide's handbook](../../labs/mineshaft/README.md).
- [ ] Check the Mineshaft is up: `./mineshaft.sh status`.

## Warm-up (5 min)

"How do you talk to a program behind a port?" *(`nc localhost PORT`.)*
"How do you see every process on a computer?" *(`ps aux`.)* "How do you
see every change ever made in a git repository?" *(`git log -p`.)*

## Activity

1. **Level 16: the gatekeeper.** Log in as miner16 and read the goal.
   ```
   nc localhost 30016
   ```
   **They should see:** `GATEKEEPER: Who goes there? Type the password for
   miner16.` Paste in the password for **this** level (the one used to log
   in as miner16, from `~/lab/mineshaft.txt`) and press Enter. **They
   should see:** `GATEKEEPER: Welcome, friend. The password for miner17
   is: ...`. Press **Ctrl+C** to hang up, and save the password.

   **Say:** "The gatekeeper is a server program inside the Mineshaft,
   waiting behind port 30016. `nc` was the client, like your chat line."

2. **Level 17: the careless miner.** Log in as miner17 and read the goal.
   **Say:** "`ps aux` shows the whole command each process was started
   with, for everyone to see. If someone types a secret into a command,
   it's not secret any more." Find it with a pipe:
   ```
   ps aux | grep gem
   ```
   **They should see:** a line for a process called `gem-keeper` with a
   `--secret=` part, and also a line for the `grep` itself (it contains
   the word "gem" too!). The password is the part after `--secret=`.

   **Say:** "Real programmers make this mistake! That's why programs ask
   for passwords by prompting (with nothing showing on screen), instead of
   taking them on the command line."

3. **Level 18: git never forgets.** Log in as miner18 and read the goal.
   ```
   cd journal
   git log
   ```
   **They should see:** two commits, the newest one called `Remove the
   password (nobody will ever know)`. `cat journal.txt` shows no password.
   But:
   ```
   git log -p
   ```
   **They should see:** the second commit's diff, with a red `-` line
   containing the password that was removed. (Or look at the first commit
   with `git show` and its ID.)

   **Say:** "Deleting something in a new commit doesn't delete it from the
   history. Real companies have accidentally published secrets this way,
   because someone thought deleting the line was enough. Once a secret is
   committed, you have to treat it as known, and change it."

4. **One level left.** Save the miner19 password. Level 19, the final
   vault, gets its own lesson (5.15), because it needs a program.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `GATEKEEPER: That is not the password for miner16. Go away!` | The miner17 password (or a typo) was typed | The gatekeeper wants miner16's password: the one used to log in to this level. |
| `nc` ends with nothing printed | Wrong port number | It's `nc localhost 30016`. |
| Level 17: only the `grep` line shows | The pattern doesn't match `gem-keeper` | `ps aux | grep gem`. Look for the line that isn't `grep gem`. |
| Level 18: `fatal: not a git repository` | Not inside the `journal` folder | `cd journal` first. |
| Level 18: `git log -p` fills the screen | It's in the pager | Space for more, `q` to quit. |

## Talk about it

- Why is a password on a command line a bad idea?
- Why didn't deleting the password in a new commit hide it?
- Which of this stage's tools did these three levels need?

## Challenge *(if there's time, or for next time)*

- On the family computer, start a program with a pretend password on its
  command line: `python3 -c 'import time; time.sleep(300)' --password=hunter2 &`.
  Find it with `ps aux | grep hunter2`, then stop it with `kill %1`.
- In your notebook repository, commit a "secret" line, then delete it in
  a second commit, and find it with `git log -p`, like level 18.

## Checkpoint

The learner can, without help:
- [ ] Talk to a server with `nc`
- [ ] Find a process and its command line with `ps aux | grep`
- [ ] Find removed lines in git history with `git log -p`
- [ ] Reach Mineshaft level 19

## Lab notebook

Add levels 16 to 18 to the level log, and commit the notebook. Write one
sentence for each level about the real-life lesson it teaches. Add
*gatekeeper* to `dictionary.md`.

## Guide's background *(optional reading)*

These levels are about real, common security mistakes. Any user can see
any process's command line with `ps`, so secrets passed as arguments
leak. And git history is permanent: removing a secret needs history
rewriting tools, and even then copies may exist elsewhere, so the only
real fix is to change the secret. Both mistakes appear regularly in
real security incidents.

Level 16's gatekeeper is a small Python server in `services.py` (in
`labs/mineshaft`). The learner will write servers themselves in
Stage 11.
