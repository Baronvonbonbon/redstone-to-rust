# Lesson 5.10: Git, Part 2: Time Travel and Branches

**Time:** 2 sessions of 45 min · **You need:** a terminal; the notebook
repository from Lesson 5.9; the Catch the Diamonds game from Lesson 3.15
(`~/lab/python/catch/`) · **New words:** restore, branch, switch,
merge, `.gitignore`

## Goal *(read this to the learner)*

> Save points are only useful if you can go back to them. Today you'll
> undo a disaster with one command, look at any old version of a file,
> and then learn git's best trick: **branches**, parallel worlds where you
> can try a wild idea for your game without risking the version that
> works.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Check the game is there: `ls ~/lab/python/catch` should show
      `catch.py` and the `images` folder. (Any of the learner's games will
      do; change the names in the steps to match.)

## Warm-up (5 min)

"What are the two steps to make a save point?" *(`git add`, then `git
commit -m "..."`.)* "How do you see the history?" *(`git log`.)*

## Activity

### Session 1: going back

1. **The disaster.** In the notebook repo:
   ```
   cd ~/lab/notebook
   echo "OOPS" > stage5.md
   cat stage5.md
   ```
   **They should see:** just `OOPS`. The whole notebook page is gone!
   **Say:** "`>` replaces the whole file. Without git, that would be the
   end of it."

2. **Undo it.**
   ```
   git status
   git diff
   git restore stage5.md
   cat stage5.md
   ```
   **They should see:** `modified: stage5.md`, then a diff with all the
   old lines in red (`-`) and `+OOPS` in green, then, after `restore`, the
   whole page back. **Say:** "`git restore` puts a file back the way it was
   at the last commit. It's the undo button for changes you haven't
   committed."

3. **Look at an old version.**
   ```
   git log --oneline
   ```
   Pick the ID of the very first commit (the bottom line). Then:
   ```
   git show 3f2a9c1:stage5.md
   ```
   (With their ID.) **They should see:** the notebook page exactly as it
   was at that save point, with only the first entry. **Say:** "Git can show
   any file from any moment in history. Nothing is ever really lost once
   it's committed."

4. **Every change, ever.**
   ```
   git log -p
   ```
   **They should see:** each commit, followed by its diff. Press space to
   go down, `q` to quit. **Say:** "That `-p` will be very useful in the
   Mineshaft..."

### Session 2: branches

5. **Put the game in git.**
   ```
   cd ~/lab/python/catch
   git init
   git status
   ```
   **They should see:** `catch.py`, `images/`, maybe `best.txt` and other
   files, all untracked.

6. **Tell git what to ignore.** `best.txt` is the high score: it changes
   every game, so it shouldn't be in the history. Make a file called
   `.gitignore`:
   ```
   nano .gitignore
   ```
   with these lines:
   ```
   best.txt
   __pycache__/
   ```
   Then `git status` again. **They should see:** `best.txt` has
   disappeared from the list. Commit everything else:
   ```
   git add .
   git commit -m "Catch the Diamonds, as finished in Stage 3"
   ```
   **Say:** "`git add .` means 'add everything in this folder', except what
   `.gitignore` says."

7. **A parallel world.** **Say:** "Let's try a crazy idea: what if the
   background were bright pink? We don't want to break the working game,
   so we'll make a **branch**."
   ```
   git branch
   git switch -c pink-world
   git branch
   ```
   **They should see:** `* main` first; then `Switched to a new branch
   'pink-world'`, and two branches listed, with a `*` next to
   `pink-world`.

   In `catch.py`, change `screen.fill("midnightblue")` to
   `screen.fill("hotpink")`. Play it (`python3 catch.py`). Then commit on
   the branch:
   ```
   git commit -am "Try a pink background"
   ```

8. **Jump between worlds.**
   ```
   git switch main
   grep fill catch.py
   git switch pink-world
   grep fill catch.py
   ```
   **They should see:** `midnightblue` on `main` and `hotpink` on
   `pink-world`. The file really changes when you switch! **Say:** "Each
   branch is its own line of save points. `main` still has the safe
   version, untouched."

9. **Keep it, or throw it away?** Decide together. If they like pink,
   bring it into `main`:
   ```
   git switch main
   git merge pink-world
   ```
   **They should see:** `Fast-forward` and `1 file changed`. **Say:** "A
   **merge** brings a branch's changes into the branch you're on."

   If they don't like it, delete the branch instead:
   `git switch main` then `git branch -D pink-world`. **Say:** "Gone, and
   `main` never knew it existed. That's why programmers try every big idea
   on a branch."

10. **(Optional) Git games.** If the guide downloaded **Oh My Git!** (see
    the stage README), play its first few levels: it shows commits and
    branches as cards and pictures. **(Online, optional, no account):**
    *learngitbranching.js.org* draws the branches as you type commands.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error: pathspec 'stage5.md' did not match any file(s) known to git` | The file name is wrong, or it was never committed | `git status` to check the name. Only committed files can be restored. |
| `fatal: invalid object name '3f2a9c1'` | That commit ID doesn't exist here | Copy the ID from your own `git log --oneline`. |
| `error: Your local changes to the following files would be overwritten by checkout` | There are uncommitted changes, and switching would lose them | Commit them first (`git commit -am "..."`), or `git restore` the file. |
| `fatal: a branch named 'pink-world' already exists` | It was made before | `git switch pink-world` (without `-c`). |
| `best.txt` still shows in `git status` | The `.gitignore` file has a typo, or isn't in the game's folder | Check `cat .gitignore`, and that it's next to `catch.py`. |
| `error: the branch 'pink-world' is not fully merged.` | Using `-d` on a branch with unmerged work | `-D` (capital) deletes it anyway. |

## Talk about it

- What's the difference between `git restore` and going back to an old
  commit with `git show`?
- What's a branch for?
- What does `.gitignore` do, and why shouldn't the high score be in git?

## Challenge *(if there's time, or for next time)*

- Make two branches with different ideas (faster diamonds, and a new
  sprite). Merge the one you like best.
- `git log --oneline --graph --all` draws the branches.
- Bring back an old version of a file for real:
  `git restore --source=3f2a9c1 stage5.md` (then `git restore stage5.md`
  to come back).

## Checkpoint

The learner can, without help:
- [ ] Undo uncommitted changes with `git restore`
- [ ] Show an old version of a file with `git show ID:file`
- [ ] Make a branch, commit on it, switch between branches, and merge
- [ ] Use a `.gitignore` file

## Lab notebook

Write a notebook entry about branches, and commit it. Draw two branches
as two lines of dots in the entry (or on paper). Add *restore*,
*branch*, *switch*, *merge* and *.gitignore* to `dictionary.md`.

## Guide's background *(optional reading)*

A commit is a snapshot of the whole folder plus a link to its parent
commit, so history is a chain (and, with branches, a tree). A **branch**
is just a movable name pointing at one commit; `git switch` changes
which branch you're on and updates the files to match. When `main` hasn't
moved since the branch was made, merging just moves the `main` name
forward: that's a **fast-forward**.

`git restore` and `git switch` are the modern, clearer replacements for
the old all-purpose `git checkout`, which the learner will see in older
tutorials. They do the same jobs.

**Oh My Git!** is an open-source game that teaches git with cards and
live pictures of the repository. It isn't in the offline library
automatically: download the Linux version by hand from its itch.io page
(linked from ohmygit.org). itch.io lets you skip paying and making an
account ("No thanks, just take me to the downloads"). The course's
checks didn't test it.
