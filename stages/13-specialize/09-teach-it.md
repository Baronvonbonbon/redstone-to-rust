# Lesson 13.9: Teach It

**Time:** 3 sessions of 45 min (writing, a trial, and fixing) · **You
need:** `docs/LESSON-TEMPLATE.md`; the learner's copy of the course from
Lesson 13.4; a willing "student" (a sibling, a friend, a grandparent, or
the guide pretending) · **New words:** audience, trial run, feedback,
iterate

## Goal *(read this to the learner)*

> There's a saying: you don't really understand something until you
> can teach it. Every lesson in this course was written so that someone
> who'd never done it before could lead it. Now you'll write one: a
> lesson about something you know well, in the same format, for someone
> younger or newer than you. Then you'll try it out on a real person,
> fix what didn't work, and send it to the course as a patch.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once, and `docs/LESSON-TEMPLATE.md`.
- [ ] Find a "student" for Session 2: someone who doesn't already know
      the topic. A younger child is ideal; an adult who doesn't program
      is also good. Book 30 minutes with them.
- [ ] The learner has `~/lab/quest/course` from Lesson 13.4. If not,
      do that lesson's steps 2 and 3 first.

## Warm-up (5 min)

"Which lesson in this course was the best one? What made it good?"
*(Collect answers: a game, a surprise, something to hold, an
explanation that clicked.)* "And which one was confusing? Why?"

## Activity

### Session 1: writing it

1. **Choose a topic.** **Say:** "Teach one small thing, for one person,
   in about 30 minutes. Small is the hardest part." Good choices:
   - something from an early stage, for a younger child: binary on
     fingers, a turtle spiral, a `grep` treasure hunt;
   - something you invented: a Pickaxe feature, a Pico trick, a
     Redstone circuit;
   - something from your quest.

   **Ask:** "Who is your **audience**? What do they already know? What
   will they be able to do at the end?" Write the answers down: that's
   the Goal.

2. **Read the template.** In the course copy:
   ```
   cd ~/lab/quest/course
   less docs/LESSON-TEMPLATE.md
   ```
   **Say:** "Every lesson you've ever done has these parts. Each one has
   a job." Go through them together: *Goal* (why), *Before the lesson*
   (so the guide is ready), *Warm-up* (remember what you know),
   *Activity* (doing it), *If something goes wrong* (the mistakes you
   know people make), *Talk about it* (checking it stuck), *Checkpoint*
   (how to know it's learned).

3. **Write it.** A new branch, and a new file in the right stage's
   folder (or in `docs/` for a lesson that doesn't fit a stage):
   ```
   git switch main
   git switch -c lesson-binary-fingers
   cp docs/LESSON-TEMPLATE.md stages/00-hello-computer/extra-binary-fingers.md
   ```
   (Use your own topic's name.) Fill in every part. The two hardest
   rules, from `CONTRIBUTING.md`:
   - **Every "They should see" is something you really saw.** Do every
     step yourself first, and copy what really happened.
   - **"Say:" lines are in kid words.** Read them aloud: do they sound
     like a person talking?

   Commit when the first draft is done, even if it isn't perfect:
   `git add` and `git commit -m "Extra lesson: binary on your fingers
   (draft)"`.

### Session 2: the trial run

4. **Try it out.** The learner leads the lesson, reading from their own
   file, with the real student. The guide watches, says nothing, and
   writes down:
   - where the student got stuck, or bored;
   - where the learner had to say something that isn't in the file;
   - what the student said or asked that surprised everyone.

   **Say** (to the learner, beforehand): "If something goes wrong,
   that's not failure: it's the most useful thing that can happen
   today. It's exactly what this trial is for."

5. **Feedback.** Afterwards, ask the student (kindly) three questions:
   "What was the best bit? What was confusing? What would you change?"
   Write down their answers exactly. Then the guide shares their notes.
   **Say:** "Engineers call this **feedback**. Good feedback is about
   the lesson, not the person."

### Session 3: fixing it, and sending it

6. **Iterate.** Go through the notes. For each:
   - Something the learner had to say that wasn't in the file? Add it.
   - A place the student got stuck? Add a row to "If something goes
     wrong", or make the step smaller.
   - Too long? Move the extra parts to the Challenge.

   **Say:** "Changing something because of what you learned, and
   trying again, is called **iterating**. Every lesson in this course
   was changed after it was tried." `git diff` to see the changes, then
   commit: `git commit -am "Extra lesson: binary on your fingers, after
   a trial run"`.

7. **Send it.** As in Lesson 13.4: `git format-patch main` (two commits
   give two files, `0001-` and `0002-`: that's fine), the guide reviews
   it, there may be a v2, and the guide applies it with `git am`. Add a
   line to the lesson's *Guide's background*: "Written by Sam, and first
   tried with ...". (First names only.)

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The lesson is 3 hours long | The topic is too big | Cut it in half. The second half is another lesson. |
| The student finished in 5 minutes | Too small, or too easy for them | Add a Challenge; next time, ask more about what they already know. |
| `fatal: A branch named 'lesson-...' already exists` | The branch was made before | `git switch lesson-...` to go back to it. |
| `git format-patch main` makes patches from Lesson 13.4 too | The new branch was made from the old one, not from `main` | `git switch main` first, then make the branch again and `git cherry-pick` your commits onto it (with the guide). |
| The learner is upset by the feedback | Feedback feels personal at first | Start with what went well. Remind them that every lesson in the course had a v2. |

## Talk about it

- What did you understand better after writing it down?
- What did the student do that you didn't expect?
- Which part of the template was hardest to write? Why does it matter?
- What's the difference between feedback on a lesson and criticism of a
  person?

## Challenge *(if there's time, or for next time)*

- Write a second lesson that follows on from the first.
- Swap: be the student for someone else's lesson, and give kind,
  useful feedback.
- Make a one-page cheat sheet for a stage (all its commands, with one
  line each), as a patch.

## Checkpoint

The learner can, without help:
- [ ] Choose a small topic and an audience, and write a Goal
- [ ] Write a complete lesson with every part of the template
- [ ] Lead the lesson with a real student
- [ ] Collect feedback, and make at least three changes from it
- [ ] Send the lesson as a patch

## Lab notebook

Copy the student's three answers and the guide's notes, and list the
changes you made. Add *audience*, *trial run*, *feedback* and
*iterate* to `dictionary.md`.

## Guide's background *(optional reading)*

The "learning by teaching" effect (sometimes called the protégé effect)
is well studied: preparing to teach makes people organise knowledge
more carefully than preparing for a test. The trial-and-revise cycle
here is how this course itself was made, and how good documentation
is made everywhere: write, watch a real user try it, fix what tripped
them up. Watching silently in Session 2 is hard but important: every
time you help, you hide a problem in the lesson.

If the lesson is good enough to share, the course welcomes it (see
`CONTRIBUTING.md`); the privacy notes in Lesson 13.4 apply to the
"Written by" line and to the commit's author.
