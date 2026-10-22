# Lesson 5.9: Git, Part 1: Save Points

**Time:** 2 sessions of 40 min · **You need:** a terminal on the family
computer; nano or vim · **New words:** git, repository, commit, stage,
history, version control

## Goal *(read this to the learner)*

> In Stage 3 you saved copies of your games before big changes:
> `catch-v1.py`, `catch-v2.py`... It works, but it's messy. Real
> programmers use **git**, a tool that keeps **save points** for a whole
> folder, like the save points in a game. You can always see what changed,
> when, and why, and go back to any save point. From today, your lab
> notebook lives in git too.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Decide what name the learner will use in git (a first name or a
      nickname). Git also wants an email-shaped label; a made-up local one
      like `sam@localhost` is fine. **Nothing is sent anywhere**: this all
      stays on your computer.

## Warm-up (5 min)

"In a video game, what's a save point for?" *(So you can go back if
something goes wrong.)* "Remember Mineshaft level 18's goal? 'Git
remembers.'" *(They'll solve that in Lesson 5.13.)*

## Activity

### Session 1: your first repository

1. **Tell git who you are** (once per computer):
   ```
   git config --global user.name "Sam"
   git config --global user.email "sam@localhost"
   git config --global init.defaultBranch main
   git config --global core.editor nano
   ```
   (Use the learner's name. If they liked vim, `core.editor vim`.)
   **Say:** "Every save point is labelled with who made it. This is the
   label."

2. **Make a repository.**
   ```
   mkdir -p ~/lab/notebook
   cd ~/lab/notebook
   git init
   ```
   **They should see:** `Initialized empty Git repository in
   /home/sam/lab/notebook/.git/`.

   **Say:** "A **repository** (or **repo**) is a folder that git looks
   after. Git keeps all its save points in a hidden folder called `.git`."
   Check: `ls -a`.

3. **Write the first page.** `nano stage5.md`, and write a first entry,
   in the lab notebook style:
   ```
   # Stage 5 lab notebook

   ## Today's date
   - I learned: what git is for.
   - Command to remember: git init
   ```
   Save it. Then:
   ```
   git status
   ```
   **They should see:** `Untracked files:` and `stage5.md` in red. **Say:**
   "Git has noticed the file, but it isn't looking after it yet."

4. **Stage it, then commit it.**
   ```
   git add stage5.md
   git status
   git commit -m "Start my Stage 5 notebook"
   ```
   **They should see:** after `add`, `Changes to be committed:` with the
   file in green. After `commit`, something like:
   ```
   [main (root-commit) 3f2a9c1] Start my Stage 5 notebook
    1 file changed, 5 insertions(+)
    create mode 100644 stage5.md
   ```

   **Say:** "Saving in git is two steps. `git add` puts changes on the
   **stage**, like getting ready for a photo. `git commit` takes the photo:
   a save point, called a **commit**, with a message saying what changed.
   `3f2a9c1` is the commit's ID. Yours will be different."

5. **Change, look, commit.** Add a second entry to `stage5.md` (a new
   date, and another thing learned). Then:
   ```
   git status
   git diff
   ```
   **They should see:** `modified: stage5.md`, then the new lines with a
   `+` in front, in green. **Say:** "`git diff` shows exactly what changed
   since the last commit. It's the `diff` from the Mineshaft!"
   ```
   git add stage5.md
   git commit -m "Add a second entry"
   ```

### Session 2: history

6. **The history.**
   ```
   git log
   git log --oneline
   ```
   **They should see:** both commits, newest first, with the name, date
   and message; then a short version, one line each.

   **Say:** "That's the **history**. Every commit forever, with who, when
   and why. That's why the messages matter: write them for the person who
   reads them in a year (probably you!)."

7. **Good messages.** Look at some messages together and decide if
   they're good:

   | Message | Good? |
   |---|---|
   | `stuff` | No: what stuff? |
   | `Add the creeper sprite` | Yes |
   | `fix` | No: fix what? |
   | `Fix diamonds falling through the floor` | Yes |

   **Say:** "A good message finishes the sentence 'This commit will...':
   '...Add the creeper sprite'."

8. **The dictionary moves in.** Make `dictionary.md` in the notebook repo,
   and copy in the words from the paper dictionary that the learner likes
   most, with their meanings. Commit it:
   ```
   git add dictionary.md
   git commit -m "Start my computer dictionary"
   ```
   From now on, the end of every session is: write the notebook entry, add
   new words to the dictionary, and commit.

9. **Shortcut.** For files git already knows about, `git commit -am
   "message"` adds and commits in one go. (New files still need `git add`
   first.)

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `fatal: not a git repository (or any of the parent directories): .git` | You're not inside the repository's folder | `cd ~/lab/notebook` |
| `Author identity unknown` and `Please tell me who you are.` | Step 1 was skipped | Run the two `git config --global user...` lines. |
| `nothing to commit, working tree clean` | No changes since the last commit, or the file wasn't saved | Save the file in the editor first, then `git status`. |
| `nothing added to commit but untracked files present` | The new file wasn't added | `git add FILENAME`, then commit. |
| An editor opens after `git commit` | The `-m "message"` was left off | Type a message on the first line, save and quit (nano: Ctrl+O, Enter, Ctrl+X). Or quit without saving to cancel. |
| `git log` fills the screen and won't go away | It's in a pager, like `less` | Press `q`. |

## Talk about it

- What's the difference between `git add` and `git commit`?
- Why do commit messages matter?
- How is git better than `catch-v1.py`, `catch-v2.py`...?

## Challenge *(if there's time, or for next time)*

- Make `~/bin` (the commands from Lessons 5.6 and 5.7) a repository too,
  and commit all the scripts.
- `git log --stat` shows which files each commit changed. `git show`
  shows the newest commit in full.
- Count your commits: `git log --oneline | wc -l`.

## Checkpoint

The learner can, without help:
- [ ] Make a repository with `git init`
- [ ] Use `git status`, `git add`, `git commit -m` and `git diff`
- [ ] Read the history with `git log`
- [ ] Write a good commit message

## Lab notebook

From now on, the lab notebook is `~/lab/notebook/stage5.md`, committed
at the end of every session. Add *git*, *repository*, *commit*, *stage*,
*history* and *version control* to `dictionary.md`.

## Guide's background *(optional reading)*

**Version control** records every version of a set of files. Git (2005)
is by far the most used version control system; nearly every software
project in the world uses it. It works completely offline: a repository
is just a folder, and its history lives inside `.git`. GitHub and
similar websites are places to *share* repositories, which needs an
account; this course doesn't need one, and Lesson 5.11 shows how to
share between folders and computers without it.

The two-step add-then-commit (the "staging area") lets you choose
exactly which changes go into each save point. Beginners often find it
odd; it pays off later when a commit should contain only some changes.

The made-up email is fine: git records it in each commit but never
sends it anywhere. If the learner ever publishes repositories, they can
choose a public-safe address then.

The paper notebook from Stages 0 to 4 stays precious. Moving to a git
notebook now matches the [Guide's Handbook](../../docs/GUIDE.md).
