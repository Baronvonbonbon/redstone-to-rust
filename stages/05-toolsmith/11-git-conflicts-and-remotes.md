# Lesson 5.11: Git, Part 3: Conflicts and Remotes

**Time:** 2 sessions of 45 min · **You need:** a terminal; the game
repository from Lesson 5.10; the Sandbox, for the challenge · **New
words:** conflict, remote, clone, push, pull

## Goal *(read this to the learner)*

> What happens when two branches change the *same line* in different
> ways? Git can't guess which one you want, so it asks you: that's a
> **conflict**, and every programmer meets them. Then you'll learn how
> git copies a repository to another place, a **remote**, and keeps them
> in step. That's how teams of programmers, all over the world, work on
> the same project.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Try steps 1 to 4 yourself on a copy of the game, if you'd like to
      see a conflict before the learner does. They're less scary than they
      look.

## Warm-up (5 min)

"How do you make a branch and switch to it?" *(`git switch -c NAME`.)*
"What does `git merge` do?" *(Brings another branch's changes into this
one.)*

## Activity

### Session 1: conflicts

1. **Two ideas for the same line.** In the game repository:
   ```
   cd ~/lab/python/catch
   git switch main
   git switch -c title-rocks
   ```
   Change the `TITLE = "Catch the Diamonds"` line to
   `TITLE = "Catch the Rocks"`, and commit:
   `git commit -am "Rename the game to Catch the Rocks"`.

   Now go back to `main` and change the *same* line differently:
   ```
   git switch main
   ```
   Change it to `TITLE = "Diamond Dash"`, and commit:
   `git commit -am "Rename the game to Diamond Dash"`.

2. **The merge.**
   ```
   git merge title-rocks
   ```
   **They should see:**
   ```
   Auto-merging catch.py
   CONFLICT (content): Merge conflict in catch.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```
   **Say:** "Don't panic! Nothing's broken. Git is asking: you changed this
   line in two different ways, which one do you want?"

3. **Read the conflict.** `git status` shows `both modified: catch.py`.
   Open `catch.py` and find the strange lines:
   ```
   <<<<<<< HEAD
   TITLE = "Diamond Dash"
   =======
   TITLE = "Catch the Rocks"
   >>>>>>> title-rocks
   ```
   **Say:** "Between `<<<<<<< HEAD` and `=======` is the version on the
   branch you're on (`main`). Between `=======` and `>>>>>>>` is the other
   branch's. Your job: make it the way you want, and delete the three
   marker lines."

4. **Fix it, and finish the merge.** Edit those five lines into one,
   choosing either title or inventing a new one, like
   `TITLE = "Diamond Dash: Rock Edition"`. Make sure all the `<<<<<<<`,
   `=======` and `>>>>>>>` lines are gone. Play the game to check it
   works. Then:
   ```
   git add catch.py
   git commit -m "Merge title-rocks, and choose a new title"
   git log --oneline --graph
   ```
   **They should see:** the history drawn with lines, showing two branches
   joining.

### Session 2: remotes

5. **A pretend server.** **Say:** "Teams keep the main copy of a project
   on a server that everyone can reach. Websites like GitHub do that. We
   don't need an account: a remote can be just another folder." Make an
   empty "server" repository for the notebook:
   ```
   mkdir -p ~/remotes
   git init --bare ~/remotes/notebook.git
   ```
   **They should see:** `Initialized empty Git repository in
   /home/sam/remotes/notebook.git/`. **Say:** "**Bare** means it has no
   working files, just the history: it's only for sharing."

6. **Push.** Connect the notebook to it and send the history:
   ```
   cd ~/lab/notebook
   git remote add origin ~/remotes/notebook.git
   git push -u origin main
   ```
   **They should see:** lines ending with `* [new branch]      main ->
   main` and `branch 'main' set up to track 'origin/main'.` **Say:**
   "`origin` is the usual nickname for the main remote. **Push** sends your
   commits to it."

7. **A second computer (pretend).** Make a copy somewhere else, as if it
   were a friend's computer:
   ```
   cd "$(mktemp -d)"
   git clone ~/remotes/notebook.git
   cd notebook
   ls
   git log --oneline
   ```
   **They should see:** `Cloning into 'notebook'...`, the notebook files,
   and the whole history. **Say:** "**Clone** copies a repository, history
   and all."

   In this copy, add a line to `dictionary.md`, commit, and push:
   ```
   git commit -am "Add a word from the other computer"
   git push
   ```

8. **Pull.** Back in the original:
   ```
   cd ~/lab/notebook
   git pull
   git log --oneline
   ```
   **They should see:** `Fast-forward`, and the new commit at the top of
   the log. **Say:** "**Pull** fetches new commits from the remote and
   merges them in. Push sends, pull receives. With these, two people (or
   two computers) can work on the same project."

9. **The habit.** From now on: at the end of a session, commit the
   notebook and `git push`. The remote in `~/remotes` is one more copy of
   the history (and the `backup` command from Lesson 5.7 saves `~/lab`,
   which includes everything).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error: Committing is not possible because you have unmerged files.` | The conflicted file wasn't added after fixing | `git add catch.py`, then commit. |
| The game crashes with `SyntaxError` after a merge | A `<<<<<<<`, `=======` or `>>>>>>>` line was left in | Search the file for `<<<<` and remove the markers. |
| Scared of the conflict | Totally normal | `git merge --abort` puts everything back as it was before the merge. |
| `fatal: 'origin' does not appear to be a git repository` | The remote wasn't added, or its path is wrong | `git remote -v` shows it. Fix with `git remote set-url origin ~/remotes/notebook.git`. |
| `error: failed to push some refs` and `Updates were rejected because the remote contains work that you do not have locally` | Someone else pushed first | `git pull` first, then `git push`. |
| `fatal: destination path 'notebook' already exists` | Cloning into a folder that already has one | Clone in a fresh `mktemp -d` folder. |

## Talk about it

- What causes a conflict? How do you fix one?
- What's the difference between push, pull and clone?
- Why might a team want one shared remote?

## Challenge *(if there's time, or for next time)*

- **A real server: the Sandbox.** Make a bare repository *in the
  Sandbox* and push to it over SSH:
  ```
  ssh LEARNER@localhost -p 2222 "git init --bare game.git"
  cd ~/lab/python/catch
  git remote add sandbox ssh://LEARNER@localhost:2222/home/LEARNER/game.git
  git push sandbox main
  ```
  (With the learner's name; it asks for the Sandbox password.) Then log in
  to the Sandbox and `git clone game.git` there. It's a different
  computer, reached over the network, just like GitHub. (Remember: a
  Sandbox reset deletes it!)
- Make a conflict in the notebook between the two clones, and fix it.

## Checkpoint

The learner can, without help:
- [ ] Explain what a merge conflict is, and fix one
- [ ] Make a bare remote, push to it, clone it, and pull from it
- [ ] Explain push, pull and clone in their own words

## Lab notebook

Write a notebook entry about remotes, commit it, and push it. Add
*conflict*, *remote*, *clone*, *push* and *pull* to `dictionary.md`.

## Guide's background *(optional reading)*

Git merges changes line by line. When both sides changed the same lines,
it can't choose, so it writes both versions into the file between
markers and stops. Resolving a conflict is just editing the file into
the right shape and committing. `git merge --abort` is the escape hatch.

A **remote** is any other copy of the repository git can reach: a
folder, another computer over SSH, or a hosting site like GitHub,
GitLab or Codeberg. This course doesn't need an online account; the
`~/remotes` folder and the Sandbox show the same mechanics. If the
learner later wants to publish work online, it's the same `git push`,
to a remote that needs an account, and a family conversation first.

Git's "distributed" design means every clone is a full copy of the
history. Pushing to a remote on the same disk doesn't protect against
the disk failing; that's what the backup habit (and a USB stick) are
for.
