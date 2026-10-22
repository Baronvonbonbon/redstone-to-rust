# Lesson 5.4: Back to the Mineshaft (Levels 10–12)

**Time:** 2 sessions of 45 min · **You need:** the Mineshaft running;
the learner's saved passwords in `~/lab/mineshaft.txt`; the
[guide's handbook](../../labs/mineshaft/README.md) · **New words:**
translate, archive, compress, temporary folder

## Goal *(read this to the learner)*

> At the end of Stage 1 you stopped at level 10 of the Mineshaft, because
> the deeper levels needed tools you didn't have yet. Now you're a
> Toolsmith, so back down you go! These three levels need a letter
> scrambler, a bundle of squashed files, and a search for one exact file
> among hundreds.

## Before the lesson *(guide, 10 min)*

- [ ] Re-read levels 10 to 12 in the [guide's handbook](../../labs/mineshaft/README.md).
- [ ] From your account, in `labs/mineshaft`: `./mineshaft.sh status`
      should say "Up". If you've reset the Mineshaft since Stage 1, the
      passwords changed: `./mineshaft.sh answers` shows the miner10
      password, so the learner can carry on.
- [ ] Check the learner can find their miner10 password:
      `grep miner10 ~/lab/mineshaft.txt`.

## Warm-up (5 min)

"What was ROT13 in Stage 1?" *(Moving every letter 13 places.)* "What
was the Caesar cipher program in Stage 3?" *(The same idea, with any
key.)* "What do you get if you ROT13 something twice?" *(The original!)*

## Activity

1. **Log in to level 10.** Two terminals, as in Stage 1: HOME on the left,
   MINESHAFT on the right.
   ```
   ssh miner10@localhost -p 2220
   cat GOAL.txt
   ```

2. **Level 10: `tr`, the letter swapper.** The goal gives the whole
   command. Before running it, take it apart:
   ```
   tr 'A-Za-z' 'N-ZA-Mn-za-m' < scrambled.txt
   ```
   **Say:** "`tr` means **translate**: it swaps characters. The first list
   is `A` to `Z` and `a` to `z`. The second list starts at `N`, goes to
   `Z`, then wraps round to `A` to `M`, and the same for small letters. So
   A becomes N, B becomes O... that's your cipher wheel, as a command!
   The `<` feeds the file in."

   Try it on something simple first: `echo hello | tr 'a-z' 'A-Z'`. *(HELLO.)*
   Then solve the level, and save the password in the HOME terminal like
   before: `echo "miner11 the-password" >> ~/lab/mineshaft.txt`.

3. **Level 11: bundles of files.** Log in as miner11 and read the goal.
   **Say:** "`buried.tar.gz` is two things at once. `tar` bundles lots of
   files into one, called an **archive**. `.gz` means it's also been
   **compressed** (squashed smaller) with `gzip`. Like a chest, wrapped
   up tight."

   The goal says the home folder is read-only. Try `tar -xzf buried.tar.gz`
   right there. **They should see:** errors like `tar: treasure: Cannot
   mkdir: Permission denied`. **Say:** "Unpacking makes new files, and
   we're not allowed to make files here. We need somewhere we *can*
   write."

   ```
   cd "$(mktemp -d)"
   pwd
   ```
   **They should see:** a path like `/tmp/tmp.Ab3dE9xQ2k`. **Say:**
   "`mktemp -d` makes a brand-new empty folder in `/tmp`, with a random
   name, and `$( )` puts its name into the `cd` command. Your own private
   scratch space."

   Then unpack, look around and read:
   ```
   tar -xzf ~/buried.tar.gz
   ls -R
   ```
   `-x` extracts, `-z` un-gzips, `-f` names the file. They'll find a
   `.gz` file inside. `zcat` reads gzipped files without unpacking them.
   *(The solution is in the handbook.)*

4. **Level 12: the exact file.** Read the goal. **Say:** "Hundreds of
   files, and only one is exactly 1234 bytes and *not* executable.
   Remember executable from Lesson 5.2? The `x` permission!"

   Look first: `ls storage` *(ten boxes)* and
   `find storage -type f | wc -l` *(hundreds of files inside them)*. Then
   read `find --help` and look for `-size` and `-executable`. Build the command
   a bit at a time:
   ```
   find storage -size 1234c
   ```
   **They should see:** lots of files, all exactly 1234 bytes. *(The `c`
   means bytes. Without it, `find` counts in blocks of 512 bytes, which
   nobody wants.)* Then add
   "not executable". `!` means NOT, just like a NOT gate:
   ```
   find storage -size 1234c ! -executable
   ```
   *(One file. `cat` it.)*

   **Say:** "`find` can combine tests with AND (just put them next to each
   other), NOT (`!`) and even OR (`-o`). It's Stage 4's logic gates, used
   to search!"

5. **Stop at level 13.** Save the miner13 password. Levels 13 to 15 come
   in Lesson 5.8.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Level 10: the output is still scrambled | The two lists in `tr` are swapped or mistyped | Copy the command from GOAL.txt exactly, quotes and all. |
| Level 11: `tar: treasure: Cannot mkdir: Permission denied` | Unpacking in the read-only home folder | `cd "$(mktemp -d)"` first, then `tar -xzf ~/buried.tar.gz`. |
| Level 11: `tar (child): buried.tar.gz: Cannot open: No such file or directory` | In the scratch folder, the file is back in the home folder | Use `~/buried.tar.gz`. |
| Level 11: `zcat` shows file names mixed with strange symbols | `zcat` was used on the `.tar.gz` itself | First `tar -xzf`, then `zcat` the `.gz` file inside. |
| Level 12: no files found | `-size 1234` without the `c` | It's `-size 1234c`. |
| Level 12: several files found | `! -executable` is missing | Add `! -executable`. |
| Forgot the password for this level | It's in `~/lab/mineshaft.txt` (HOME terminal) | `grep miner12 ~/lab/mineshaft.txt` |

## Talk about it

- What does `tr` do? How is it like the cipher wheel?
- What's the difference between an archive and compression?
- Why did level 11 need `mktemp`?
- How is `find ... ! -executable` like a NOT gate?

## Challenge *(if there's time, or for next time)*

- On the family computer, make your own buried treasure: a folder with a
  secret file inside, bundled with `tar -czf treasure.tar.gz folder`.
  Swap with the guide, and unbury each other's.
- `ls -lh` the `.tar.gz`, then unpack it and use `du -sh` on the folder.
  How much smaller was the compressed version?
- Write a `tr` command that does ROT1 (A becomes B). *(`tr 'A-Za-z'
  'B-ZAb-za'`.)*

## Checkpoint

The learner can, without help:
- [ ] Use `tr` to translate letters
- [ ] Make a scratch folder with `mktemp -d`, and unpack a `.tar.gz` there
- [ ] Use `find` with `-size` and `!`
- [ ] Reach Mineshaft level 13

## Lab notebook

Add levels 10 to 12 to the level log: the level, the command that solved
it, and one sentence about why it works. Add *translate*, *archive*,
*compress* and *temporary folder* to the dictionary.

## Guide's background *(optional reading)*

`tr` with ranges is the classic Unix way to do ROT13. `tar` ("tape
archive") dates from the days of tape drives; `tar -czf` makes an
archive and `tar -xzf` extracts one, and nearly all source code on the
internet is shipped this way. The learner will use `tar` again for
backups in Lesson 5.7.

The Mineshaft's home folders are read-only so learners can't leave
notes for each other or break a level. `mktemp -d` is the safe way to get
a private scratch folder in a shared `/tmp`: the Mineshaft lets you make
folders there but not list other people's.
