# Lesson 1.15: Deeper in the Mineshaft (Stage 1 Checkpoint)

**Time:** 2–3 sessions of 45 min · **You need:** the Mineshaft running; the
learner's saved passwords in `~/lab/mineshaft.txt` · **New words:**
encoding, base64

## Goal *(read this to the learner)*

> Levels 5 to 9 are where the Mineshaft gets serious. You'll need `find`,
> `grep`, pipes, `sort`, `uniq`, `head`, `tail`, and one brand-new
> command. Reach level 10 and you'll be an official **Terminal
> Detective**!

## Before the lesson *(guide, 5 min)*

- [ ] Re-read levels 5 to 9 in the [guide's handbook](../../labs/mineshaft/README.md).
- [ ] Check the Mineshaft is up (`./mineshaft.sh status`).

## Warm-up (5 min)

"How do you log into level 4? Where are your passwords saved? What does
`uniq -u` do?"

## Activity

1. **Log in to level 5** (two terminals, like last time).

2. **Levels 5 to 9.** The learner plays; you use the stuck ladder from the
   [Guide's Handbook](../../docs/GUIDE.md). Which skill each level needs:

   | Level | Skill | From lesson |
   |---|---|---|
   | 5 | `find -name` in a huge folder tree | 1.11 |
   | 6 | `grep` in a 2000-line file | 1.12 |
   | 7 | `sort` then `uniq -u` | 1.10 |
   | 8 | `head -n` then `tail -n` (the line in the middle) | 1.10 |
   | 9 | `base64 -d` (new; the goal explains it) | (new!) |

3. **Level 9's new idea.** After they solve it, **say:** "Base64 *looks*
   secret, but it isn't. It's an **encoding**: a way of writing data so it
   travels safely, not a way of hiding it. Anyone can decode it. Remember
   the Caesar cipher? That needed a key. Base64 doesn't have one."

4. **Stop at level 10.** When they have the miner10 password: "Levels 10
   and deeper need new skills you'll learn in Stage 5. Save that password!"

## The Stage 1 checkpoint

On a separate day, with no help (it's fine to use `--help` and `man`):

1. In `~/lab`, make a folder `checkpoint1`, with a file `about-me.txt` in
   it containing three lines about themselves, written with `echo` and `>>`.
2. Copy it to `about-me-backup.txt`, rename the backup to `old.txt`, then
   delete `old.txt`.
3. Show hidden files in their home folder.
4. Find `QUEST.txt` starting from home, using `find`.
5. Count how many lines in `/etc/passwd` contain `bash`. *(`grep -c bash /etc/passwd`)*
6. Pipe a random joke into cowsay.
7. Find out what `ls -t` does, using only the manual.
8. Log into Mineshaft level 10 with the saved password.
9. Explain the Hacker's Pledge in their own words.

All 9 done means **Terminal Detective!** Sign and stamp the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Level 7 shows lots of lines | `uniq -u` without `sort` first | `sort ores.txt \| uniq -u` |
| Level 8 shows 7777 lines | Just `head`, without `tail` | Pipe it: `head -n 7777 long-tunnel.txt \| tail -n 1` |
| Level 9: `base64: invalid input` | Tried to decode the *password* instead of the file | `base64 -d creeper-code.txt` |
| A checkpoint task fails | Not ready yet, and that's fine | Re-do that lesson, and try again another day. |

## Talk about it

- Which level was hardest? Why?
- What's the difference between encoding (base64) and encryption (Caesar)?
- Which command do you think you'll use most for the rest of your life?

## Lab notebook

Finish the level log for levels 5 to 9. Write: "I am a Terminal Detective
because I can..." and list five things.

## Guide's background *(optional reading)*

These levels deliberately need *combinations* of commands, especially
pipes, which is the real skill of the terminal. The learner will come
back to the Mineshaft in Stage 5 for levels 10 to 19, which cover
compression, permissions, environment variables, networking, processes
and git history, and finish with a level that needs a Python program.
