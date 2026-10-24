# Lesson 13.4: Your First Patch

**Time:** 2 sessions of 45 min · **You need:** a terminal; the guide's
copy of this course (a Git repository); `~/lab/quest` · **New words:**
upstream, bundle, version (v2), credit

## Goal *(read this to the learner)*

> You've been using this course for years. You know where it's
> confusing, where an error message wasn't in the table, and where
> there's a typo. Today you'll fix one of them, the way open-source
> contributors do: in your own copy, on a branch, sent as a patch to the
> maintainer. If it's accepted, your name goes into the course's history
> for good.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, and Lesson 13.3.
- [ ] Find the folder where you keep this course (the one you ran
      `give-lab.sh` from). It's a Git repository. Make a **bundle** of
      it, a single file holding the whole history, where the learner can
      read it:
      ```
      cd ~/redstone-to-rust          # or wherever your copy is
      git bundle create /tmp/course.bundle --all
      ```
      **You should see** something like `Enumerating objects...` and
      `done`.
- [ ] Think of one or two things that could be improved, in case the
      learner has no ideas: an error they hit that's missing from a
      lesson's table, a sentence that confused them, a challenge they
      invented.
- [ ] Decide about **privacy** now (see Guide's background). The patch
      carries the learner's Git name and email, which since Lesson 5.9
      have been a first name and `@localhost`. Keep it that way.

## Warm-up (5 min)

"In Lesson 13.3, who was the author and who was the committer?" *(Guide
wrote it; the learner accepted it.)* "Today, swap."

## Activity

### Session 1: making the change

1. **What to fix.** Make a list, together, of things in the course the
   learner would change. Look at old lab notebooks: where did they get
   stuck? Good first patches:
   - a typo, or a sentence that confused them;
   - a row for an "If something goes wrong" table: an error they really
     saw, what it meant, and what fixed it;
   - a new challenge for a lesson they loved.

   **Say:** "Small is good. Maintainers love small patches, because
   they're easy to review. Your first one should be a few lines."

2. **Your own copy.** The course you're improving is the **upstream**:
   the original, which other copies come from. Clone the bundle:
   ```
   cd ~/lab/quest
   git clone /tmp/course.bundle course
   cd course
   git log --oneline | head -5
   ```
   **They should see** `Cloning into 'course'...` and the newest few
   commits of the course. **Say:** "That's the whole history, every
   change since the first lesson was written."

3. **A branch.** Never change `main` directly (Lesson 5.10):
   ```
   git switch -c fix-thanks
   ```
   (Name the branch after your change.) **They should see** `Switched to
   a new branch 'fix-thanks'`.

4. **Make the change.** Find the file with `grep -rn` (Lesson 1.12),
   open it in `nano` or `vim`, and change it. Follow the course's rules:
   every lesson follows `docs/LESSON-TEMPLATE.md`; error rows have three
   columns; every output must be something that really happened. Check
   it:
   ```
   git diff
   ```
   **Ask:** "Does the diff show only what you meant to change?"

5. **Commit it.** A good message says what and where, in less than a
   line:
   ```
   git commit -am "CONTRIBUTING: a more excited thank-you"
   ```
   (Use your own message, like `Lesson 9.4: add the E0382 error row`.)

### Session 2: sending it

6. **Make the patch.**
   ```
   git format-patch main
   ```
   **They should see** a file name made from the message, like
   `0001-CONTRIBUTING-a-more-excited-thank-you.patch`. `head -5` it:
   ```
   From 687e2b340f77480d462efd02be0a21c56d1a749d Mon Sep 17 00:00:00 2001
   From: Sam <sam@localhost>
   Date: Sat, 24 Oct 2026 17:53:34 +0000
   Subject: [PATCH] CONTRIBUTING: a more excited thank-you
   ```
   **Say:** "`main` means 'every commit on my branch that isn't on main'.
   That's your change, and only your change." Copy it where the guide
   can read it: `cp 0001-*.patch /tmp/`.

7. **The review.** Now the guide is the maintainer. The guide reads the
   patch, with the learner, using Lesson 13.3's four questions, and
   gives real feedback: something good, and (if there is one) something
   to change. **Say:** "Nearly every patch gets changes asked for, even
   from experts. It's how projects stay good, not a telling-off."

8. **Version 2.** If changes are asked for, fix the file, then fold the
   fix into the same commit and make the patch again, numbered:
   ```
   git commit -a --amend --no-edit
   git format-patch -v2 main
   ```
   **They should see** `v2-0001-CONTRIBUTING-a-more-excited-thank-you.patch`.
   **Say:** "v2 means 'the second try'. Real projects see v5 and v10."

9. **Accepted!** In the guide's own copy of the course:
   ```
   git am /tmp/v2-0001-*.patch          # or 0001-* if there was no v2
   git log -1 --format='%an <%ae> | %cn | %s'
   ```
   **They should see** `Applying: ...`, and the learner's name as author
   with the guide's as committer, like `Sam <sam@localhost> | Guide |
   CONTRIBUTING: a more excited thank-you`. **Say:** "That's your name in
   the course, for as long as it exists. You're an open-source
   contributor." Write it in the journal, with the date.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `fatal: repository '/tmp/course.bundle' does not exist` | The guide hasn't made the bundle yet, or it's somewhere else | The guide does "Before the lesson". |
| `fatal: Need a repository to create a bundle.` | The guide ran `git bundle` outside the course folder | `cd` into the course folder first. |
| `git format-patch main` makes no file | The change isn't committed, or you're on `main` | `git status`, then `git switch -c ...` and commit. |
| Several `0001-`, `0002-`... files | More than one commit on the branch | That's fine: a patch series. Send them all, or squash them (Challenge). |
| `error: patch failed` in the guide's copy | The guide's copy has changed since the bundle was made | Make a new bundle, `git pull` it into the learner's copy (Lesson 5.11), and `git rebase main` on the branch. |
| The patch shows `From: Sam <sam@...>` with a real email | `git config` was set to a real address | `git config --global user.email sam@localhost`, then `git commit --amend --reset-author --no-edit`. |

## Talk about it

- What makes a patch easy to review?
- Why work on a branch, not on `main`?
- What's a v2? Why is asking for changes a good thing?
- How does Git make sure you get the credit?

## Challenge *(if there's time, or for next time)*

- Make a second patch, on a new branch from `main`. Two commits? Try
  `git rebase -i main` with the guide, to squash them into one.
- Find a typo in a book in the offline library, and write the patch for
  it (in a copy). The guide can send it upstream (see below).
- Review a patch the guide makes to the course, as in Lesson 13.3.

## Checkpoint

The learner can, without help:
- [ ] Clone a bundle and make a branch for a change
- [ ] Make a small change that follows the project's rules
- [ ] Write a clear commit message, and make a patch with
      `git format-patch`
- [ ] Respond to review with a v2
- [ ] Say who is the author and who the committer of their accepted patch

## Lab notebook

Copy your patch's commit message and its `git diff`. Write what the
reviewer said and what you changed. Update the passport. Add *upstream*,
*bundle* and *credit* to `dictionary.md`.

## Guide's background *(optional reading)*

**Sending patches upstream, for real.** Most projects (including this
course, if you're working from a public copy) take contributions as
pull requests on a forge like Codeberg or GitHub, which need an account
and an email address. By the course's rules the learner doesn't have
those, so the guide does that part from their own account: apply the
learner's patch with `git am` (which keeps the learner as author), push
to a fork, and open the pull request, saying in the description that
it's the learner's work. Projects that take patches by email (the Linux
kernel, Git itself) use `git send-email` from the guide's address in
the same way.

**Privacy.** A public commit is public forever, and Git records the
author's name and email in every one. Use a first name or a handle and
a non-address like `sam@localhost` (or the forge's "noreply" address on
the guide's account); never a child's full name, school or real email.
Some families prefer the guide to be the author, with "Co-authored-by:
Sam" or a thank-you in the description: that's a fine choice.

`git bundle` makes a single file that `git clone`, `git fetch` and
`git pull` understand, which is handy for offline machines and for
moving a repository on a USB stick. `git format-patch main` is shorthand
for `main..HEAD`; for a branch with many commits, `--cover-letter` adds a
`0000-` file for a summary of the series.
