# Lesson 13.3: How Open Source Works

**Time:** 2 sessions of 45 min · **You need:** a terminal; `~/lab/quest`
(Lesson 13.1); this course's own folder (the guide's copy); paper ·
**New words:** open source, licence, copyright, maintainer, contributor,
patch, review

## Goal *(read this to the learner)*

> Almost every program you've used in this course was given away free,
> with its code, by people you'll never meet: Linux, Python, Rust, Git,
> Luanti, even this course. Today you'll find out how that works: the
> rules (licences), the people (maintainers and contributors), and the
> way changes travel between them (patches). And you'll be the
> maintainer who decides whether to accept one.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] The learner has `~/lab/quest` with `QUEST.md` committed (Lesson
      13.1).
- [ ] In step 6 you'll make a small patch to the learner's quest, as
      "Guide". Find a real typo or a small improvement in their
      `QUEST.md` to fix. If there's none, add a missing full stop. You
      do it in a copy, so their files aren't touched until they decide.

## Warm-up (5 min)

"Who wrote Python? Who wrote Rust? Did you pay for them?" *(Lots of
people; no.)* "Why would anyone give away years of work?" Collect
guesses, and come back to them at the end.

## Activity

### Session 1: the rules

1. **Copyright.** **Say:** "When someone writes a story or a program, the
   law says they own it, automatically. That's **copyright**: nobody else
   may copy it without permission. A **licence** is the permission: a
   note saying what you're allowed to do."

2. **This course's licences.** In the course folder:
   ```
   ls
   head -3 LICENSE-CODE.txt
   head -1 LICENSE-CONTENT.txt
   ```
   **They should see** `MIT License` and `Attribution-ShareAlike 4.0
   International`. **Say:** "The code uses the MIT licence: do anything
   you like, but keep the note saying who wrote it. The lessons use
   Creative Commons BY-SA: share and change them, but say where they came
   from (that's 'BY'), and share your changes the same way ('SA',
   share-alike)."

3. **Three families of licence.** Draw three boxes, and read:
   - **Permissive** (MIT, BSD, Apache): "Take it, use it, even sell it.
     Just keep my name on it." *(Rust, clox, this course's code.)*
   - **Copyleft** (GPL): "Take it and change it, but if you give your
     version to anyone, you must give them the code too, under the same
     rules." *(Linux, Git, Luanti.)*
   - **Creative Commons** (CC BY, CC BY-SA, CC BY-NC...): for writing and
     pictures, not code. *(OpenStax books, this course's lessons, the
     Linux From Scratch book.)*

   **Ask:** "Which one stops a company from taking Linux, improving it,
   and keeping the improvement secret?" *(The GPL.)* Then read a real
   author's reasons:
   ```
   less /srv/redstone-library/repos/crafting-interpreters/LICENSE
   ```
   **They should see** `Copyright (c) 2015 Robert Nystrom`, then his
   "Commentary". Read the bullet points together. **Ask:** "Which part
   does he let you change freely, and which part does he want to keep
   his own? Why?" *(The code is MIT; the words and pictures are his
   voice and his handwriting.)* **Say:** "Code with no licence at all
   isn't open source, even if you can see it. The owner hasn't given
   permission."

4. **The people.** **Say:** "Every open-source project has
   **maintainers**: the people who look after it and decide what goes
   in. Anyone who sends a change is a **contributor**. Most contributors
   start with something tiny: a typo, a clearer sentence, a better error
   message." Read the course's own rules together: `less CONTRIBUTING.md`.
   **Ask:** "What does this project ask contributors to do? Which rule
   would be easiest to break by accident?"

### Session 2: you are the maintainer

5. **How changes travel.** **Say:** "Before websites with buttons, and
   still today for Linux and Git themselves, changes travelled by email,
   as a **patch**: a file saying 'change these lines like this'. Git can
   make a patch from a commit, and turn a patch back into a commit." Draw
   it: contributor's commit → `git format-patch` → a `.patch` file →
   `git am` → maintainer's commit.

6. **A patch arrives.** The guide types this, in the learner's terminal,
   while the learner watches (it makes a copy, fixes it as "Guide", and
   writes a patch file to `/tmp`):
   ```
   git clone -q ~/lab/quest /tmp/guide-quest
   cd /tmp/guide-quest
   nano QUEST.md
   git -c user.name=Guide -c user.email=guide@localhost commit -qam "QUEST: fix the spelling of controller"
   git format-patch -1 -o /tmp
   ```
   *(Use your own fix and message.)* **They should see** the new file's
   name, like `/tmp/0001-QUEST-fix-the-spelling-of-controller.patch`.
   **Say:** "A contributor has sent you a patch. You're the maintainer.
   It's your project: you decide."

7. **Review it.** **Say:** "A maintainer never accepts a change without
   reading it. That's a **review**." In the learner's own repository:
   ```
   cd ~/lab/quest
   cat /tmp/0001-*.patch
   ```
   **They should see** an email-like header (`From: Guide
   <guide@localhost>`, `Subject: [PATCH] QUEST: fix the spelling of
   controller`), then a diff, like Lesson 5.10's, with `-` and `+` lines:
   ```
   -What I want to make or understand: a fan controler
   +What I want to make or understand: a fan controller
   ```
   Go through the review questions, out loud:
   - Does the message say clearly what it does?
   - Is the change right? Does it do only what the message says?
   - Does it break any of the project's rules?
   - Would I rather it were done differently?

8. **Check, then accept (or not).**
   ```
   git apply --check /tmp/0001-*.patch
   git am /tmp/0001-*.patch
   git log --format='%h %an | %cn | %s'
   ```
   `--check` prints nothing if the patch fits. **They should see**
   `Applying: QUEST: fix the spelling of controller`, and the log:
   ```
   d095e04 Guide | Sam | QUEST: fix the spelling of controller
   898e20d Sam | Sam | Start my quest
   ```
   **Say:** "Look at the two names. The **author** is Guide, who wrote the
   change; the **committer** is you, who accepted it. Git remembers both,
   forever. That's how open source gives credit." If the learner decided
   to *refuse* the patch, that's allowed too: they write the reason in
   `JOURNAL.md`, and explain it, kindly, to the guide. **Say:** "A good
   maintainer says thank you, even when the answer is no."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error: patch failed: QUEST.md:1` and `Patch failed at 0001` | The patch was already applied, or the file changed since the copy was made | `git am --abort`. Check `git log`: is it already there? |
| `fatal: not a git repository` | `git am` was typed outside `~/lab/quest` | `cd ~/lab/quest` first. |
| `fatal: destination path '/tmp/guide-quest' already exists` | Step 6 was done before | Use another name, like `/tmp/guide-quest2`. |
| `head: cannot open '/srv/redstone-library/...'` | The offline library isn't there | The guide runs `./scripts/mirror-library.sh`. |
| The guide's name shows as `Sam` | The `-c user.name=Guide` part was missed | Make the copy again; it doesn't matter much, but the credit is the point. |

## Talk about it

- What's the difference between copyright and a licence?
- Name a permissive licence, a copyleft licence and a Creative Commons
  licence, with a project for each.
- Who is the author and who is the committer of an accepted patch?
- Why do maintainers review every change, even from friends?
- Back to the warm-up: why do people give their work away?

## Challenge *(if there's time, or for next time)*

- Find the licence of three more programs on the computer: look in
  `/usr/share/doc/python3/copyright` and `/usr/share/doc/git/copyright`.
- Make a patch for the guide's own copy of something (switch roles:
  the learner is the contributor). That's next lesson's main job.
- Read the "Contributing" section of the Rust Cookbook's README in the
  library. How is it like this course's?

## Checkpoint

The learner can, without help:
- [ ] Explain copyright and licence in their own words
- [ ] Sort MIT, GPL and CC BY-SA into their families
- [ ] Read a patch and say what it changes
- [ ] Review, check and apply a patch with `git am`
- [ ] Find the author and the committer in `git log`

## Lab notebook

Draw the patch's journey from contributor to maintainer. Write the four
review questions on a card. Add *licence*, *copyright*, *maintainer*,
*contributor*, *patch* and *review* to `dictionary.md`.

## Guide's background *(optional reading)*

The Free Software Foundation's "four freedoms" and the Open Source
Definition are the two formal definitions; in practice the licences on
the OSI's list are the ones that count. Copyleft's "share your changes"
rule applies only when a program is *distributed*, which is why the
GPL's reach surprises people in both directions. Creative Commons
licences with NC (non-commercial) or ND (no derivatives) are not "open"
by the OSI's definition, but are common for books; the Linux From
Scratch book is CC BY-NC-SA, for example, while its code fragments are
MIT.

`git format-patch` and `git am` are how the Linux kernel and Git itself
still take contributions (by email, with `git send-email`). Forges like
Codeberg, GitLab and GitHub wrap the same idea in a web page (a "pull
request" or "merge request"), but need an account, so this course
keeps patches as files. Lesson 13.4 covers how a learner's patch can
reach a real project through the guide.
